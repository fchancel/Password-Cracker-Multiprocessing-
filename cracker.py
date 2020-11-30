# coding: utf8

import utils
from ClassCracker import *
import argparse
import multiprocessing
import time
import atexit
import sys


def parse_mode(m_args):
    """
    Parse argument, allowing to know which mode launched and which values assigned
    :param m_args: Argparse.Namespace object
    :return:
    """
    if m_args.generate:
        utils.generate_hash(m_args.password, m_args.type)
    else:
        if not m_args.brute and not m_args.file:
            call_default = True
            m_args.file = "lstWord.txt"
        else:
            call_default = False
        cracker = Cracker(m_args.password, m_args.type, m_args.file, m_args.maximum, m_args.process)
        response = False
        if m_args.time:
            begin_time = time.time()
            atexit.register(utils.display_time, begin_time)
        # ATTACK DICTIONARY MODE
        if m_args.file or call_default:
            print("[*] Number of words in the file : " + str(cracker.line))
            print("[*] CRACKING DICTIONARY IN PROGRESS")
            if m_args.process > 1:
                response = cracker.prepare_dictionary_crack_multi()
                if response[0]:
                    print(f"{Color.GREEN}[+] SUCCESS: Password : {Color.END}"
                          f"{Color.BLUE}{response[1]} ({response[2]}){Color.END}")
                else:
                    print(f"{Color.RED}[-] ERROR : no match found in file {Color.END}")
            else:
                response = cracker.dictionary_crack()
                if response[0]:
                    print(f"{Color.GREEN}[+] SUCCESS: Password : {Color.END}"
                          f"{Color.BLUE}{response[1]} ({response[2]}){Color.END}")
                else:
                    print(f"{Color.RED}[-] ERROR : no match found in file {Color.END}")
        # ATTACK BRUTE FORCE
        if (m_args.brute or call_default) and not response:
            print("[*] CRACKING BRUTE FORCE IN PROGRESS")
            if m_args.process > 1:
                response = cracker.prepare_bruteforce_multi()
                if response[0]:
                    print(f"{Color.GREEN}[+] SUCCESS: Password : {Color.END}"
                          f"{Color.BLUE}{str(response[1])} ({str(response[2])}){Color.END}")
                else:
                    print(f"{Color.RED}[-] ERROR : no match found {Color.END}")
            else:
                response = cracker.run_bruteforce_attack()
                if not response[0]:
                    print(f"{Color.RED}[-] ERROR : no match found {Color.END}")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Try to break the password given as an argument (hash) "
                                                 "with a dictionary attack and a Brute Force attack."
                                                 " REQUIRED ARGUMENT = -p / --password (hashed password),"
                                                 " -t / - type (type of hash used on the password)")

    # PARSER GENERAL ARGUMENT
    parser.add_argument("-p", "--password", help="Hash to find OR password to generate", required=True)
    parser.add_argument("-t", "--type", help="type of hash desired (Hash available = md5, sha224, sha256, "
                        "sha384 and sha512) ", required=True)
    parser.add_argument("-c", "--process", help="choose the number of processes to use for cracking (default value : 2",
                        type=int, default=2, required=False)
    parser.add_argument("--time", help="displays the execution time", action="store_true", required=False)

    # PARSER BRUTE FORCE ARGUMENT
    group_brute = parser.add_argument_group('brute force', 'Brute force attack. Try all possible combinations')
    group_brute.add_argument("-b", "--brute", help="brute force attack mode",
                             action="store_true")
    group_brute.add_argument("-m", "--maximum", help="maximum number of characters of the password (default value : 10",
                             type=int)

    # PARSER DICTIONARY ATTACK ARGUMENT
    group_file = parser.add_argument_group('dictionary attack', 'dictionary attack. Try all the words in a file')
    group_file.add_argument("-f", "--file", nargs='?', const='lstWord.txt',
                            help="Takes as argument a file with a list of words "
                                 "(default value = lstWord.txt)")

    # PARSER GENERATE HASH ARGUMENT
    group_generate = parser.add_argument_group('generate hash', "generate a hash with the given password -p --password."
                                                                " Requires the use of -t --type (choice of hash)")
    group_generate.add_argument("-g", "--generate", help="Generate hash mode",
                                action="store_true")

    my_args = parser.parse_args()
    cont = True
    print(f"[*] Password : {my_args.password}\n[*] Type of hash : {my_args.type}")

    # CHECK IF THE TYPE HASH IS CORRECT
    try:
        getattr(hashlib, my_args.type)
    except Exception:
        print(f"{Color.RED}[-] ERROR: the type of hash requested is unknown{Color.END}")
        cont = False

    # CHECK IF THE NUMBER OF CHOSEN PROCESSES IS POSSIBLE
    if my_args.process > multiprocessing.cpu_count():
        print(f"{Color.RED}[-] ERROR: number of processes chosen greater than the number available. "
                          f"You have a maximum of : {str(multiprocessing.cpu_count())}{Color.END}")
        cont = False
    if my_args.process == 0:
        print(f"{Color.RED}[-] ERROR: you must choose at least one process. "
                          f"You have a maximum of : {str(multiprocessing.cpu_count())}{Color.END}")
        cont = False

    # PARSE THE MODE OF CRACK
    if cont:
        parse_mode(my_args)
