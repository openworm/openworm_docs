'''
Script to show what happens after checking out the gh-pages branch in recent GH Actions
runs. Useful for seeing which jobs caused an unnecessary deploy.
'''
from os.path import expanduser
import io
import zipfile
import requests

token = open(expanduser('~/.gh-token'), 'rt').read().strip()
headers = {"Accept": "application/vnd.github.v3+json",
           "Authorization": f"token {token}"}
runs_resp = requests.get('https://api.github.com/repos/openworm/openworm_docs/actions/runs',
        headers=headers).json()
runs = runs_resp['workflow_runs']
for run in runs:
    run_id = run['id']
    run_number = run['run_number']
    logs_url = run['logs_url']
    logs_resp = requests.get(logs_url, headers=headers)
    logs_zip = io.BytesIO(logs_resp.content)
    print(f"Run number: {run_number}")
    with zipfile.ZipFile(logs_zip) as logs_zf:
        with logs_zf.open('1_build.txt') as logs_txt:
            do_print = False
            for ln in logs_txt:
                ln = ln.decode().strip()
                if "Switched to branch 'gh-pages'" in ln:
                    do_print = True
                if "Post job cleanup" in ln:
                    do_print = False
                if do_print:
                    print(ln)
