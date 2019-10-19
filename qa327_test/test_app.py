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

    # compare terminal outputs from the the last time backward`
    for i in range(1, len(expected_terminal_tails)+1):
        index = i * -1
        assert expected_terminal_tails[index] == out_lines[index]

    # compare expected file output:
    if expected_output_file is not None:
        with open(temp_file, 'r') as temp_file_of:
            content = temp_file_of.read()
            with open(expected_output_file, 'r') as exp_file_of:
                exp_content = exp_file_of.read()
                assert content == exp_content

    # clean up
    os.close(temp_fd)
    os.remove(temp_file)
