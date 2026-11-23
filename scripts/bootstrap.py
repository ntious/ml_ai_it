"""Install a documented course profile; no hidden provider authentication."""
import argparse
from pathlib import Path
import platform
import subprocess
import sys
import venv

ROOT=Path(__file__).resolve().parents[1]
FRAMEWORK_PYTHON=(3, 12)
CORE_MINIMUM=(3, 11)


def check_python(profile):
    """Stop before any download when this interpreter cannot build the requested profile."""
    found=sys.version_info[:2]; shown=".".join(map(str,found))
    if profile == "frameworks" and found != FRAMEWORK_PYTHON:
        sys.exit(f"The frameworks profile needs Python 3.12, but this command is running Python {shown}.\n"
                 "Python 3.12 is the verified course framework environment. Check with: python3.12 --version\n"
                 "Then run: python3.12 scripts/bootstrap.py --profile frameworks\n"
                 "No Python 3.12? See docs/setup/frameworks.md (Install Python 3.12) or use Codespaces.")
    if found < CORE_MINIMUM:
        sys.exit(f"The course needs Python 3.11 or newer, but this command is running Python {shown}.\n"
                 "Install Python 3.12 and run this command with it. See QUICKSTART.md.")


def main():
    parser=argparse.ArgumentParser();parser.add_argument("--profile",choices=["core","frameworks"],default="core")
    parser.add_argument("--current",action="store_true",help="Install into the current kernel environment (e.g. Colab); restart after package changes.")
    args=parser.parse_args()
    if args.profile == "frameworks" and platform.system() != "Linux":
        parser.error("Use the verified Linux CPU route for frameworks.")
    check_python(args.profile)
    if args.current:
        executable=Path(sys.executable)
    else:
        directory=ROOT/(".venv-ml" if args.profile == "frameworks" else ".venv")
        try:
            venv.EnvBuilder(with_pip=True,symlinks=platform.system()!="Windows").create(directory)
        except (OSError, subprocess.CalledProcessError) as error:
            sys.exit(f"Could not create the course environment at {directory}: {error}\n"
                     "Check free disk space and folder permissions. On Ubuntu, install the venv package for your Python "
                     "(for Python 3.12: sudo apt install python3.12-venv). Then retry the same command.\n"
                     "More help: docs/setup/troubleshooting.md")
        executable=directory/("Scripts/python.exe" if platform.system()=="Windows" else "bin/python")
    def run(*arguments):
        try: subprocess.run([str(executable),*arguments],cwd=ROOT,check=True)
        except subprocess.CalledProcessError as error:
            step=" ".join(str(argument) for argument in arguments[:4])
            sys.exit(f"\nSetup stopped during: {step} (exit code {error.returncode}).\n"
                     "Read the last error lines above. A download or network message means the computer could not reach the package site.\n"
                     "Fix that, then run the same bootstrap command again. More help: docs/setup/troubleshooting.md")
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
