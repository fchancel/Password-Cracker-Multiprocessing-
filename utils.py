import hashlib
import time
import sys

class Color:
    RED = '\033[91m'
    GREEN = '\033[92m'
    BLUE = '\033[96m'
    END = '\033[0m'


def generate_hash(password, type_hash):
    """
    Generate a hash from the param password with the hash type from the type_hash param
    :param password: hash password
    :param type_hash: type of hash
    :return:
    """
    func = getattr(hashlib, type_hash)
    pwd_hash = func(password.encode('utf8'))
    print(f'{Color.GREEN}[+] SUCCESS: hash : {Color.END}{Color.BLUE}{pwd_hash.hexdigest()}{Color.END}')


def display_time(begin_time):
    """
    Displays the execution time of the cracking
    :param begin_time: time at which the cracker started
    :return:
    """
    end_time = time.time()
    exec_time = end_time - begin_time
    print(f"[*] CRACKING TIME : {str(exec_time)}")
