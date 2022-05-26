import os
import sys
import json
import shutil
import subprocess
import requests

from urllib.parse import urlparse
from git import Repo
from git.exc import GitCommandError
from tabulate import tabulate


args_no = len(sys.argv)
if args_no == 1:
    print("[!] You must provide a valid git url as argument, e.g.: codesec/packscan <git-url>")
    sys.exit(0)

url = sys.argv[1]
token = sys.argv[2] if args_no > 2 else None

repos = []
if url[-4:] == '.git':
    repos.append(url)
else:
    parsed_url = urlparse(url)
    headers = {'Authorization': f'token {token}'} if token else {}
    r = requests.get(
        f'{parsed_url.scheme}://api.{parsed_url.netloc}/orgs{parsed_url.path}/repos',
        headers=headers
    )

    if r.status_code != 200:
        print(r.reason)
        sys.exit(0)

    for repo in r.json():
        repos.append(repo['clone_url'])


try:
    os.mkdir('.tmp')
except FileExistsError:
    shutil.rmtree('.tmp')
    os.mkdir('.tmp')


for repo in repos:
    repo_name = repo.split('/')[-1].split('.')[0]
    repo_path = os.path.join('.tmp', repo_name)

    if token:
        parsed_url = urlparse(repo)
        repo = f'{parsed_url.scheme}://{token}@{parsed_url.netloc}{parsed_url.path}'

    try:    
        Repo.clone_from(repo, repo_path)
    except GitCommandError:
        print("[!] Authorization failed! Maybe you are trying to scan a private repository, check if token was provided or if the provided token have access to the repository you want to scan.")
        sys.exit(0)

    generic = subprocess.run([
        'semgrep --config=../../rules/generic.yaml --json --include *.txt .'
    ], cwd=repo_path, shell=True, capture_output=True, encoding='utf8')
    python = subprocess.run([
        'semgrep --config=../../rules/python.yaml --json .'
    ], cwd=repo_path, shell=True, capture_output=True, encoding='utf8')

    results = []
    results += [[r['path'], r['start']['line'], r['extra']['lines'], r['extra']['message']] for r in json.loads(generic.stdout)['results']]
    results += [[r['path'], r['start']['line'], r['extra']['lines'], r['extra']['message']] for r in json.loads(python.stdout)['results']]

    print(f'\nResults for: {repo_name}')
    print(f"\n{tabulate(results, headers=['file', 'line', 'pattern', 'description'])}" if len(results) > 0 else '[*] No results found!\n')

shutil.rmtree('.tmp')
