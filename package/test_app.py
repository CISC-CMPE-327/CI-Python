import pytest
from package.app import main

def test_file1_method1(capsys):
    main()
    out, err = capsys.readouterr()
    assert out == "hello word!\n"
    x=5
    y=6
    assert x+1 == y," test failed"