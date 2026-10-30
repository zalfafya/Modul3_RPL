import sys
import os

if sys.stdin is None:
    sys.stdin = open(os.devnull, 'r')
if sys.stdout is None:
    sys.stdout = open(os.devnull, 'w')
if sys.stderr is None:
    sys.stderr = open(os.devnull, 'w')

from controllers.auth_controller import AuthController

if __name__ == "__main__":
    app = AuthController()
    app.run()