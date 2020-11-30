![purpose](https://img.shields.io/badge/purpose-education-green)   ![license](https://img.shields.io/badge/license-GPL-blue) 

# PASSWORD CRACKER

The password cracker uses by default, first, dictionary attack and second, brute force attack.
To work this one requires a hash to crack and the type of hash used

(Possibility of using multiple processors)

## REQUIRED

Python 3.6 minimum

## USAGE

**For crack a password with dictionary attack AND brute force attack:**

`$ python cracker.py -p hash -t typeOfHash`

or:

`$ python cracker.py -p hash -t typeOfHash -f [pathToDictionary] -b`



**For generate a hash from a password:**

`$ python cracker.py -g -p password -t typeOfHash`

## CONFIGURATION

### GENERAL CONFIGURATION
| Argument | Definition | DEFAULT VALUE | REQUIRED |
| ------ | ------ | ------ | ------ |
| -h / --help | Show the help message and exit | - | - |
| -p / --password | Hash to find OR password to generate | - | + |
| -t / --type | Type of hash desired (Hash available = md5, sha224,sha256, sha384 and sha512) | - | + |
| -c / --process | Number of processes to use for cracking | 2 | - |
| --time | Displays the execution time | - | - |

### DICTIONARY ATTACK CONFIGURATION
| Argument | Definition | DEFAULT VALUE | REQUIRED |
| ------ | ------ | ------ | ------ |
| -f / --file | Launches the dictionary attack. Can take as argument the path of a file containing a list of words | lstWord.txt (word list provided with the project) | - |

### BRUTE FORCE ATTACK CONFIGURATION
| Argument | Definition | DEFAULT VALUE | REQUIRED |
| ------ | ------ | ------ | ------ |
| -b / --brute | Launches brute force attack | - | - |
| -m / --maximum | Maximum number of characters of the password  | 10 | - |

### GENERATE HASH CONFIGURATION
| Argument | Definition | DEFAULT VALUE | REQUIRED |
| ------ | ------ | ------ | ------ |
| -g / --generate | Starts hash generation | - | - |

## EXAMPLE USAGE

Launch of a brute force attack with a password of a maximum length of 5 characters, hashed in SHA224, with the help of 6 processors and display of the cracking time:

`$ python cracker.py -b -m 5 -c 6 -p bdd03d560993e675516ba5a50638b6531ac2ac3d5847c61916cfced6 -t sha224 --time`

launch of a dictionary attack (with dictionary by default), with a password hashed in md5, with the help of 8 processors and display of the cracking time:

`$ python cracker.py -f -c 10 -p bdd03d560993e675516ba5a50638b6531ac2ac3d5847c61916cfced6 -t md5 --time`

## ALGORITHM EXPLANATION 

**Dictionary attack (single processor):**

The program browses the list of word of the file from the first to the last word and compares the hash of the password provided in parameter with the hash of the words contained in the file

**Dictionary attack (multiprocessor):**

The number of words contained in the file is divided by the number of processors. Each processor browses a unique portion of the file.

**Brute Force attack (single processor):**

The program incrementally generates a word to try. Starting with a length of 1 up to the maximum length requested by the user (default value: 10)

**Brute Force attack (multiprocessor):**

Each character of the first four characters of the word to be tested is managed by a processor.
For the following characters, the available character lists are divided by the number of processors requested by the user. Each processor will try to find the password in its available character portion. (example: processor 1 will try from 'aaaaa' to 'faaaa', processor 2 will try to: 'faaaaa' to 'maaaaa', etc...)

## DEMO
![](https://gitlab.com/krotarox/python-password-breaker/-/raw/master/gif/demo.gif)

## Warning

**The program is specially designed to test only YOUR own passwords / hashs, for the legitimate purpose of knowing the strength of your passwords.**

**You will therefore be fully responsible for any unauthorized use of this program.**


