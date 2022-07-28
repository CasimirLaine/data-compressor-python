import os


def install_requirements():
    stream = os.popen('python -m pip install -r requirements.txt')
    output = stream.read()
    print(output)


if __name__ == '__main__':
    install_requirements()
