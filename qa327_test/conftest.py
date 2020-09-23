import pytest
import requests
import subprocess
import os
import signal
import time
from qa327.__main__ import FLASK_PORT

base_url = 'http://localhost:{}'.format(FLASK_PORT)


@pytest.fixture(scope="module", autouse=True)
def server():
    # create a live server for testing
    p = subprocess.Popen(
        ' '.join(['python', '-m', 'qa327']),
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        # add process group id
        # so it is easier to kill
        preexec_fn=os.setsid
    )
    time.sleep(5)
    yield
    # triple kill!
    # [for robust killing across differnt platforms]
    os.killpg(os.getpgid(p.pid), signal.SIGTERM)
    p.terminate()
    p.kill()
    p.communicate()
