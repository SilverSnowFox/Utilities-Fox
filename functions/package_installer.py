import subprocess
import sys

reqs = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
installed_packages = [r.decode().split('==')[0].lower() for r in reqs.split()]

with open("requirements.txt") as f:
    req_list = f.read().splitlines()


def install_req():
    """Installs the packages from requirements that are missing, if not installed."""
    for req in req_list:
        if req.split("~")[0] not in installed_packages:
            subprocess.check_call([sys.executable, "-m", "pip", "install", req])
        else:
            print(f"{req} already installed.")
