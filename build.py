#!/usr/bin/env python
from __future__ import print_function, division
import os
import sys
from base64 import b64decode

import requests
from tqdm import tqdm
from github import Github
import yaml

g = Github(os.getenv("GITHUB_API_TOKEN"))
repos = list(g.get_organization("OpenWorm").get_repos())


def repo2content(repo):
    """
    @return {"filename": "content"} where `filename` starts with `.openworm.`
    """
    tree = repo.get_git_tree("master", recursive=False).tree
    files = [i for i in tree if i.path.lower().startswith('.openworm.')]
    if not files:
        return {}
    reqs = [requests.get(i.url) for i in files]
    data = [b64decode(i.json()['content']) for i in reqs]
    return dict(zip((i.path.lower() for i in files), data))


def repo2meta(repo):
    content = repo2content(repo)
    if not content:
        return {}
    meta = {}
    for file, data in content.items():
        if file.endswith('.yml') or file.endswith('.yaml'):
            meta.update(yaml.safe_load(data))
        elif file.endswith('.rst'):
            raise NotImplementedError
        elif file.endswith('.md'):
            raise NotImplementedError
        else:
            raise KeyError("Unknown file extension: {}".format(file))
    return meta


def main():
    meta = {}

    for repo in tqdm(repos, unit="repo"):
        files = repo2meta(repo)
        if files:
            meta[repo.name] = files
    print(meta)


if __name__ == "__main__":
    sys.exit(main() or 0)
