#!/usr/bin/env python
from __future__ import print_function, division
import os
import sys
from base64 import b64decode
import logging
from textwrap import dedent

import requests
from tqdm import tqdm
from github import Github
import yaml
from funcy import merge

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
    try:
        data = [b64decode(i.json()['content']) for i in reqs]
    except KeyError:
        raise ValueError(reqs)  # likely 403
    return dict(zip((i.path.lower() for i in files), data))


def repo2meta(repo):
    content = repo2content(repo)
    if not content:
        return {}
    meta = {}
    for file, data in content.items():
        if file.endswith('.yml') or file.endswith('.yaml'):
            meta.update({
                k.lower().replace('-', '_'): v
                for k, v in yaml.safe_load(data).items()
            })
        elif file.endswith('.rst'):
            raise NotImplementedError
        elif file.endswith('.md'):
            meta['markdown'] = data
        else:
            raise KeyError("Unknown file extension: {}".format(file))
    return meta


def main():
    logging.basicConfig(level=logging.DEBUG)
    log = logging.getLogger(__name__)

    meta = {}

    for repo in tqdm(repos, unit="repo"):
        files = repo2meta(repo)
        if files:
            meta[repo.name] = files
    log.debug(meta)

    defaults = {
        # TODO: build graph based on the following, and use it to determine
        # 1. order of printing
        # 2. heading levels
        'children': [],
        'parent': '',
        'inputs': [],
        'outputs': [],
        # TODO: use the following
        #'earnable_badges': '',
        #'members': '',
        #'tests': ''
        'contributor_guide': '',
        'coordinator': '',
        'documentation': '',
        'gitter': '',
        'keywords': [],
        'languages': [],
        'latest_release': '',
        'repo': '',
        'shortdescription': '',
        'latest_release_date': '',
        'latest_generated_date': '',
    }

    for repo, fmt in meta.items():
        if 'markdown' in fmt:
            print(fmt['markdown'])
            continue
        # TODO: auto determine {latest_release}
        # TODO: auto determine {latest_release_date}
        # TODO: auto determine {latest_generated_date}
        fmt = merge(defaults, dict(name=repo), fmt)
        fmt['keywords'] = ", ".join(fmt['keywords'])
        fmt['languages'] = ", ".join(fmt['languages'])

        print(dedent("""
        # {name}

        [repo](https://github.com/{repo}) | [docs]({documentation}) | [gitter]({gitter}) | [contributor guide]({contributor_guide})

        - lang(s): {languages}
        - keyword(s): {keywords}
        - current version: {latest_release} {latest_release_date}

        {shortdescription}

        <{coordinator}>
        <small>Last generated {latest_generated_date}</small>

        TODO: autoremove undefined vars
        """).format(**fmt))


if __name__ == "__main__":
    sys.exit(main() or 0)
