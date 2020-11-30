from utils import *
import hashlib
import multiprocessing
import string
import sys


class Cracker:

    def __init__(self, password, type_hash, file, max_char, processes):
        self._password = password
        self._type_hash = type_hash
        if not max_char:
            self._max_char = 10
        else:
            self._max_char = max_char
        self._processes = processes
        if file:
            try:
                with open(file, 'r') as my_file:
                    print(f"[*] Keyword file : {file}")
                    print("[*] PREPARE DICTIONARY ")
                    lst = my_file.read().split('\n')
                    lst = map(str.strip, lst)
                    self._file = list(lst)
                    self.line = len(list(self._file))
            except Exception as err:
                print(Color.RED + "[-] ERROR : " + str(err) + Color.END)
                exit()

    def prepare_dictionary_crack_multi(self):
        """
        Multiprocessor launch function for dictionary attack
        :return: Booleen to find out if the password has been cracked
        """
        processes = []
        done_queue = multiprocessing.Queue()
        processes = [multiprocessing.Process(target=self.dictionary_crack,
                                             args=(done_queue, nb_process, True))
                     for nb_process in range(0, self._processes)]
        for process in processes:
            process.daemon = True
            process.start()

        count = self._processes
        while True:
            response = done_queue.get()
            if response[1]:
                for process in processes:
                    process.terminate()
                return response
            else:
                count -= 1
                if not count:
                    return response

    def dictionary_crack(self, done_queue=None, nb_process=None, multi=False):
        """
        Function to read each word from a dictionary and compare them with the password provided
        :param done_queue: Multiprocessing queue to return the response
        :param nb_process: Number of processor allocated to the task
        :param multi: Boolean allowing to know if the multiprocessor is started
        :return:Booleen to find out if the password has been cracked
        """
        find = False
        begin = int(0)
        end = None
        if multi:
            nb_line_process = self.line / self._processes
            begin = round(nb_process * nb_line_process)
            if self.line % self._processes == 0 or \
                    (self.line % self._processes > 0 and nb_process < self._processes - 1):
                end = round((nb_process * nb_line_process) + nb_line_process)
        for line in self._file[begin:end]:
            func = getattr(hashlib, self._type_hash)
            line_hash = func(line.encode('utf8'))
            if line_hash.hexdigest() == self._password:
                find = True
                response = (True, line, line_hash.hexdigest())
                if multi:
                    done_queue.put(response)
                    break
                else:
                    return response
        if not find:
            response = (False, None, None)
            if multi:
                done_queue.put(response)
            else:
                return response
        return True

    def prepare_bruteforce_multi(self):
        """
        Multiprocessor launch function
        :return:
        """
        processes = []
        done_queue = multiprocessing.Queue()

        # USEFUL VARIABLE FOR THE FIRST 4 CHARTS
        nb = self._max_char // self._processes
        if nb == 0:
            nb = 1
        length = 1

        # USEFUL VARIABLE FOR CHARS GREATER THAN 4
        interval_letter = (len(string.printable) / self._processes)  # maximum call process by char
        min_char = 0
        max_char = interval_letter
        call_nb = 0
        count_process_running = 0

        # PREPARE PROCESS
        for _ in range(0, self._processes):
            if length <= self._max_char:
                if length < 4:
                    processes.append(multiprocessing.Process(target=self.run_bruteforce_attack,
                                                             args=(done_queue, length, nb, True)))
                    length += 1
                else:
                    if call_nb > self._processes:  # TRY WITH ONE MORE CHAR
                        length += 1
                        min_char = 0
                        max_char = interval_letter
                        call_nb = 0

                    begin_letter = string.printable[int(min_char)]
                    end_letter = string.printable[int(max_char)]
                    processes.append(multiprocessing.Process(target=self.bruteforce_attack_opti,
                                                             args=(begin_letter, done_queue, length,
                                                                   0, end_letter)))
                    call_nb += 1
                    min_char += interval_letter
                    max_char += interval_letter
                    if max_char >= len(string.printable):
                        max_char = len(string.printable) - 1

        # START PROCESS
        for process in processes:
            process.daemon = True
            process.start()
            count_process_running += 1

        while True:
            response = done_queue.get()

            # IF PASSWORD IS CRACKED
            if response[0]:
                for process in processes:
                    process.terminate()
                return response
            # IF PROCESS FINISH AND PASSWORD IS NOT CRACKED
            else:
                count_process_running -= 1
                if not count_process_running:
                    response = (False, None, None)
                    return response
                if length <= self._max_char:
                    if length < 4:
                        processes.append(multiprocessing.Process(target=self.run_bruteforce_attack,
                                                                 args=(done_queue, length, nb, True)))
                        length += 1
                    else:
                        count_process_running += 1
                        if call_nb > self._processes:  # TRY WITH ONE MORE CHAR
                            length += 1
                            min_char = 0
                            max_char = interval_letter
                            call_nb = 0

                        begin_letter = string.printable[int(min_char)]
                        end_letter = string.printable[int(max_char)]
                        processes.append(multiprocessing.Process(target=self.bruteforce_attack_opti,
                                                                 args=(begin_letter, done_queue, length,
                                                                       0, end_letter)))
                        processes[-1].daemon = True
                        processes[-1].start()
                        call_nb += 1
                        min_char += interval_letter
                        max_char += interval_letter
                        if max_char >= len(string.printable):
                            max_char = len(string.printable) - 1

    def run_bruteforce_attack(self, done_queue=None, begin_length=None, nb=None, multi=False):
        """
        Function launching the attack by bruteForce
        :param done_queue: Multiprocessing queue to return the response
        :param begin_length: position at which the attack should start
        :param nb: number of characters each processor should use
        :param multi: Boolean allowing to know if the multiprocessor is started
        :return:
        """
        response = (False, None, None)
        if not multi:
            for length in range(1, self._max_char + 1):
                self.bruteforce_attack('', length, 0, multi)
            return response
        else:
            for length in range(begin_length, begin_length + nb):
                self.bruteforce_attack('', length, 0, multi, done_queue)
            done_queue.put(response)

    def bruteforce_attack(self, trying, target_length, current_length, multi, done_queue=None):
        """
        Recursive function allowing to test each character of 'string.printable' (brute force attack)
        :param trying: password tested
        :param target_length: length of the word being tested
        :param current_length: current length of the tested password
        :param multi: Boolean allowing to know if multiprocessing is used
        :param done_queue: Multiprocessing queue to return the response
        :return:
        """
        if current_length == target_length:
            func = getattr(hashlib, self._type_hash)
            line_hash = func(trying.encode("utf8"))
            if line_hash.hexdigest() == self._password:
                if not multi:
                    print(f"{Color.GREEN}[+] SUCCESS: Password : {Color.END}"
                          f"{Color.BLUE}{trying} ({line_hash.hexdigest()}){Color.END}")
                    sys.exit()
                else:
                    response = (True, trying, line_hash.hexdigest())
                    done_queue.put(response)
        else:
            for c in string.printable:
                self.bruteforce_attack(trying + c, target_length, current_length + 1, multi, done_queue)

    def bruteforce_attack_opti(self, trying, done_queue, target, length, end_letter):
        """
        Recursive function allowing to test each character of 'string.printable' with the help of multiple processor
        which divides the tasks (attack by brute force) (call by prepare_bruteforce_multi())
        :param trying: password tried
        :param done_queue: Multiprocessing queue to return the response
        :param target: length of the word being tested
        :param length: current length of the tested password
        :param end_letter: test limit letter
        :return:
        """
        if trying != end_letter:
            if length == target:
                func = getattr(hashlib, self._type_hash)
                line_hash = func(trying.encode("utf8"))
                if line_hash.hexdigest() == self._password:
                    response = (True, trying, line_hash.hexdigest())
                    done_queue.put(response)
            else:
                check_letter = False
                for c in string.printable:
                    if length == 0:
                        if c == trying[0]:
                            check_letter = True
                        if check_letter:
                            self.bruteforce_attack_opti(trying + c, done_queue, target, length + 1, end_letter)
                    else:
                        self.bruteforce_attack_opti(trying + c, done_queue, target, length + 1, end_letter)

        else:
            response = (False, None, None)
            done_queue.put(response)
