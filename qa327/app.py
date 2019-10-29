import sys
import os


def main():
    """ An example program of frontend that does
    R1 program only accepts 'login' as key
    R2 print valid_account_list_file's content
    R3 write 'hmm i am a transaction.' to the transaction_summary_file
    """
    print('Welcome the Queens ATM machine')

    # for simplicity
    # you can use argparse for sure
    valid_account_list_file = sys.argv[1]
    transaction_summary_file = sys.argv[2]

    # R1:
    user_input = input('what is the key?\n')
    if(user_input == 'login'):
        print('here is the content')
        with open(valid_account_list_file) as rf:
            print(rf.read())
        print('writing transactions...')
        with open(transaction_summary_file, 'w') as wf:
            wf.write('hmm i am a transaction.')
            # exit
    else:
        print('omg wrong key')
    
    
