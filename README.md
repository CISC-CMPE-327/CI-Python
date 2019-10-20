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
│   │   app.py
│   │   __init__.py
│   └───__main__.py
│ 
│ 
└───qa327_test
    │   test_app.py
    │   __init__.py
    │
    └───r2
        └───file_output.txt
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

```



We created a helper function to test for different cases:

```python
import tempfile
import os
import io
import sys
import qa327.app as app

path = os.path.dirname(os.path.abspath(__file__))


def test_r1(capsys):
    run_app(
        capsys=capsys,
        terminal_input=['steven'],
        expected_terminal_tails=['hello steven']
    )


def test_r2(capsys):
    run_app(
        capsys=capsys,
        terminal_input=['327'],
        expected_terminal_tails=['hello 327', 'file written!'],
        expected_output_file=os.path.join(path, 'r2', 'file_output.txt')
    )


def run_app(
        capsys,
        terminal_input,
        expected_terminal_tails,
        expected_output_file=None):
    """ a helper function that test requirements for the example app

    Arguments:
        capsys -- object created by pytest to capture stdout and stderr
        terminal_input : list -- list of string as terminal input for
            stdin stream
        expected_terminal_tails : list -- list of string to be matched at
            the tail of the terminal output
        expected_output_file : str -- the path to the correct output file
            [optional]
    """

    # setup parameters
    temp_fd, temp_file = tempfile.mkstemp()
    sys.argv = ['app.py', temp_file]

    # set input
    sys.stdin = io.StringIO(
        os.linesep.join(terminal_input))

    # run the program
    app.main()

    # capture terminal output / errors
    # assuming that in this case we don't use stderr
    out, err = capsys.readouterr()

    # split terminal output in lines
    out_lines = out.splitlines()

    # compare terminal outputs 
    for i in range(1, len(expected_terminal_tails)+1):
        index = i * -1
        assert expected_terminal_tails[index] == out_lines[index]

    # compare output file to the expected output fuke:
    if expected_output_file is not None:
        with open(temp_file, 'r') as temp_file_of:
            content = temp_file_of.read()
            with open(expected_output_file, 'r') as exp_file_of:
                exp_content = exp_file_of.read()
                assert content == exp_content

    # clean up
    os.close(temp_fd)
    os.remove(temp_file)
```

