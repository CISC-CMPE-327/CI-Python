# CI-Python

[![](https://github.com/CISC-CMPE-327/CI-Python/workflows/Python%20application/badge.svg)](https://github.com/CISC-CMPE-327/CI-Python/actions)

Python CI template for GitHub Actions

Folder structure:
```
.
│   .gitignore
│   LICENSE
│   README.md
│   requirements.txt ========> python dependencies, a MUST
│
├───.github
│   └───workflows
│           pythonapp.yml =======> CI workflow for python
│
├───qa327
│   │   app.py ===============> where we actually store the main function
│   │   __init__.py
│   └───__main__.py ==========> trigger by 'python -m qa327'
│ 
│ 
└───qa327_test
    │   test_main_approach1.py
    │   __init__.py
    │   
    └───r2
            terminal_input.txt
            terminal_output_tail.txt
            transaction_summary_file.txt
            valid_account_list_file.txt
```

To run all the test code:

```
pytest
```


This example app has two simple requirements:

```python
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
    
    

```



We created a helper function to test for different cases:

Approach #1. We store all the input content (terminal & file) and all the output content (terminal & file) in a folder. The helper function looks up data from the folder.

```python
import tempfile
from importlib import reload
import os
import io
import sys
import qa327.app as app

path = os.path.dirname(os.path.abspath(__file__))


def test_r2(capsys):
    """Testing r2. All required information stored in folder r2. 

    Arguments:
        capsys -- object created by pytest to capture stdout and stderr
    """
    helper(
        capsys=capsys,
        test_id='r2'
    )


def helper(
        capsys,
        test_id):
    """ a helper function that test requirements for the example app

    Arguments:
        capsys -- object created by pytest to capture stdout and stderr
    """

    # cleanup package
    reload(app)

    # locate test case folder:
    case_folder = os.path.join(path, test_id)

    # read terminal input:
    with open(
        os.path.join(
            case_folder, 'terminal_input.txt')) as rf:
        terminal_input = rf.read().splitlines()

    # read expected tail portion of the terminal output:
    with open(
        os.path.join(
            case_folder, 'terminal_output_tail.txt')) as rf:
        terminal_output_tail = rf.read().splitlines()

    # create a temporary file in the system to store output transactions
    temp_fd, temp_file = tempfile.mkstemp()
    transaction_summary_file = temp_file

    # prepare program parameters
    sys.argv = [
        'app.py',
        os.path.join(case_folder, 'valid_account_list_file.txt'),
        transaction_summary_file]

    # set terminal input
    sys.stdin = io.StringIO(
        os.linesep.join(terminal_input))

    # run the program
    app.main()

    # capture terminal output / errors
    # assuming that in this case we don't use stderr
    out, err = capsys.readouterr()

    # split terminal output in lines
    out_lines = out.splitlines()

    # compare terminal outputs at the end.`
    for i in range(1, len(terminal_output_tail)+1):
        index = i * -1
        assert terminal_output_tail[index] == out_lines[index]

    # compare transactions:
    with open(transaction_summary_file, 'r') as of:
        content = of.read()
        with open(os.path.join(case_folder, 'transaction_summary_file.txt'), 'r') as exp_file_of:
            expected_content = exp_file_of.read()
            assert content == expected_content

    # clean up
    os.close(temp_fd)
    os.remove(temp_file)

```
Approach #2. We store all the input content (terminal & file) and all the output content (terminal & file) in the code. The helper function create temporary file on the system as needed for the program to run (e.g. valid_account_list_file).
```python
import tempfile
from importlib import reload
import os
import io
import sys
import qa327.app as app

path = os.path.dirname(os.path.abspath(__file__))


def test_r2(capsys):
    """Testing r2. Self-contained (i.e. everything in the code approach)
    [my favorite - all in one place with the code]

    Arguments:
        capsys -- object created by pytest to capture stdout and stderr
    """
    helper(
        capsys=capsys,
        terminal_input=[
            'login'
        ],
        intput_valid_accounts=[
            '123456'
        ],
        expected_tail_of_terminal_output=[
            'here is the content',
            '123456',
            'writing transactions...'],
        expected_output_transactions=[
            'hmm i am a transaction.'
        ]
    )


def helper(
        capsys,
        terminal_input,
        expected_tail_of_terminal_output,
        intput_valid_accounts,
        expected_output_transactions
):
    """Helper function for testing

    Arguments:
        capsys -- object created by pytest to capture stdout and stderr
        terminal_input -- list of string for terminal input
        expected_tail_of_terminal_output list of expected string at the tail of terminal
        intput_valid_accounts -- list of valid accounts in the valid_account_list_file
        expected_output_transactions -- list of expected output transactions
    """

    # cleanup package
    reload(app)

    # create a temporary file in the system to store output transactions
    temp_fd, temp_file = tempfile.mkstemp()
    transaction_summary_file = temp_file

    # create a temporary file in the system to store the valid accounts:
    temp_fd2, temp_file2 = tempfile.mkstemp()
    valid_account_list_file = temp_file2
    with open(valid_account_list_file, 'w') as wf:
        wf.write('\n'.join(intput_valid_accounts))

    # prepare program parameters
    sys.argv = [
        'app.py',
        valid_account_list_file,
        transaction_summary_file]

    # set terminal input
    sys.stdin = io.StringIO(
        os.linesep.join(terminal_input))

    # run the program
    app.main()

    # capture terminal output / errors
    # assuming that in this case we don't use stderr
    out, err = capsys.readouterr()

    # split terminal output in lines
    out_lines = out.splitlines()

    # compare terminal outputs at the end.`
    for i in range(1, len(expected_tail_of_terminal_output)+1):
        index = i * -1
        assert expected_tail_of_terminal_output[index] == out_lines[index]

    # compare transactions:
    with open(transaction_summary_file, 'r') as of:
        content = of.read().splitlines()
        for ind in range(len(content)):
            assert content[ind] == expected_output_transactions[ind]

    # clean up
    os.close(temp_fd)
    os.remove(temp_file)

```
