import sys
import os


def main():
    """ An example program that has two functionalities:
        R1/ Ask for user's name and print it out
        R2/ Write 'hello 327' to the file specified by app
            argument if the user's name is 327.
    """
    print('hello world!')

    # R1:
    name = input('what is your name please?:' + os.linesep)
    print('hello', name)

    # R2:
    if name == '327':
        with open(sys.argv[1], 'w') as of1:
            of1.write('hello 327')
        print('file written!')
