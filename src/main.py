import os
import sys
import shutil
import subprocess

from git import Repo


try:
    repo_url = sys.argv[1]
except IndexError:
    print("[!] You must provide a valid git url as argument, e.g.: codesec/packscan <git-url>")
repo_path = os.path.join('.tmp', repo_url.split('/')[-1].split('.')[0])

try:
    os.mkdir('.tmp')
except FileExistsError:
    shutil.rmtree('.tmp')
    os.mkdir('.tmp')

Repo.clone_from(repo_url, repo_path)
subprocess.run([
    'semgrep',
    '--config=../../rules.yaml',
    '.'
], cwd=repo_path)

shutil.rmtree('.tmp')
