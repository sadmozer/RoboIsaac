import subprocess, sys

def StartGame():
    p = subprocess.Popen(["powershell.exe",
    "-ExecutionPolicy",
    "Unrestricted",
    ".\\Set-Window.ps1"], 
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE)
    out, err = p.communicate()
    try:
        print(f"[SETUP-STDOUT]: {out.decode('utf-8').strip()}")
        print(f"[SETUP-STDERR]: {err.decode('utf-8').strip()}")
    except Exception as e:
        print(e)
    