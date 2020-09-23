import pytest
import subprocess
import os
import signal
import time
import tempfile
from qa327.__main__ import FLASK_PORT

base_url = 'http://localhost:{}'.format(FLASK_PORT)


@pytest.fixture(scope="module", autouse=True)
def server():
    onWin = os.name == 'nt'
    with tempfile.TemporaryDirectory() as tmp:
        # create a live server for testing
        # with a temporary file as database
        db = os.path.join(tmp, 'db.sqlite')
        p = subprocess.Popen(
            ['python', '-m', 'qa327', db],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            # add process group id
            # so it is easier to kill
            preexec_fn=None if onWin else os.setsid
        )
        time.sleep(5)
        yield
        # triple kill!
        # [for robust killing across different platforms]
        if not onWin:
            os.killpg(os.getpgid(p.pid), signal.SIGTERM)
        p.terminate()
        p.kill()
        p.communicate()
