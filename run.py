from project import app
from sys import argv

if __name__ == '__main__':
    if len(argv) == 2 and argv[1] == "-noreload":
        app.run(use_reloader=False)
    else:
        app.run()
