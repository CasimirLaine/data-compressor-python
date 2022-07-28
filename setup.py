import os


def install_requirements():
    req_file = 'requirements.txt'
    del_req_file = '.del_requirements.txt'
    commands = [
        f'python -m venv env',
        f'source env/bin/active',
        f'python -m pip install --upgrade pip',
        f'python -m pip freeze > {del_req_file}',
        f'python -m pip uninstall -y -r {del_req_file}',
        f'python -m pip install -r {req_file}',
    ]

    def del_frozen_requirements():
        if os.path.isfile(del_req_file):
            os.remove(del_req_file)

    del_frozen_requirements()
    for command in commands:
        stream = os.popen(command)
        output = stream.read()
        print(output)
    del_frozen_requirements()


if __name__ == '__main__':
    install_requirements()
