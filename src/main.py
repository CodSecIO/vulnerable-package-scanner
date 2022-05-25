import os
import sys
import json
import shutil
import subprocess

from git import Repo
from tabulate import tabulate


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
generic = subprocess.run([
    'semgrep --config=../../rules/generic.yaml --json $(find . -name "*.txt")'
], cwd=repo_path, shell=True, capture_output=True, encoding='utf8')
python = subprocess.run([
    'semgrep --config=../../rules/python.yaml --json .'
], cwd=repo_path, shell=True, capture_output=True, encoding='utf8')

results = []
results += [[r['path'], r['start']['line'], r['extra']['lines'], r['extra']['message']] for r in json.loads(generic.stdout)['results']]
results += [[r['path'], r['start']['line'], r['extra']['lines'], r['extra']['message']] for r in json.loads(python.stdout)['results']]

print(tabulate(results, headers=['file', 'line', 'pattern', 'description']) if len(results) > 0 else '[*] No results found!')

shutil.rmtree('.tmp')
