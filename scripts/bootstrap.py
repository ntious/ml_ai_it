"""Install a documented course profile; no hidden provider authentication."""
import argparse
from pathlib import Path
import platform
import subprocess
import sys
import venv

ROOT=Path(__file__).resolve().parents[1]


def main():
    parser=argparse.ArgumentParser();parser.add_argument("--profile",choices=["core","frameworks"],default="core")
    parser.add_argument("--current",action="store_true",help="Install into the current kernel environment (e.g. Colab); restart after package changes.")
    args=parser.parse_args()
    if args.profile == "frameworks" and platform.system() != "Linux":
        parser.error("Use the verified Linux CPU route for frameworks.")
    if args.current:
        executable=Path(sys.executable)
    else:
        directory=ROOT/(".venv-ml" if args.profile == "frameworks" else ".venv")
        venv.EnvBuilder(with_pip=True).create(directory)
        executable=directory/("Scripts/python.exe" if platform.system()=="Windows" else "bin/python")
    def run(*arguments): subprocess.run([str(executable),*arguments],cwd=ROOT,check=True)
    if args.profile == "frameworks": run("-m","pip","install","torch==2.6.0","--index-url","https://download.pytorch.org/whl/cpu")
    extras="regression,visualization,verification"+(",neural,language,deployment" if args.profile == "frameworks" else "")
    constraint="constraints-neural.txt" if args.profile == "frameworks" else "constraints-tested.txt"
    run("-m","pip","install","-e",f".[{extras}]","-c",str(ROOT/"environments"/constraint))
    kernel="ml-ai-frameworks" if args.profile == "frameworks" else "ml-ai-core"
    label="Python (course frameworks)" if args.profile == "frameworks" else "Python (course core)"
    run("-m","ipykernel","install","--user","--name",kernel,"--display-name",label)
    run(str(ROOT/"scripts/preflight.py"),"--profile",args.profile)
    print(f"Select the kernel {label!r} ({kernel}) and save work before an ephemeral session ends.")

if __name__ == "__main__": main()
