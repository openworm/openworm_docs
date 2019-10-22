#!/usr/bin/env python
from __future__ import print_function, division
import os
import sys
from base64 import b64decode
import logging
from textwrap import dedent
from time import strptime, strftime

import requests
from tqdm import tqdm
from github import Github
import yaml
from funcy import merge

g = Github(os.getenv("GITHUB_API_TOKEN"))
repos = list(g.get_organization("OpenWorm").get_repos())


def repo2content(repo):
    """
    @return {"filename": (File, "content")} where `filename` starts with `.openworm.`
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
    return dict(zip((i.path.lower() for i in files), zip(files, data)))


def repo2meta(repo):
    content = repo2content(repo)
    if not content:
        return {}
    meta = {}
    for name, (fname, data) in content.items():
        if name.endswith('.yml') or name.endswith('.yaml'):
            meta.update({
                k.lower().replace('-', '_'): v
                for k, v in yaml.safe_load(data).items()
            })
            meta['ymlObj'] = fname
        elif name.endswith('.rst'):
            raise NotImplementedError
        elif name.endswith('.md'):
            meta['markdown'] = data
            meta['mdObj'] = fname
        else:
            raise KeyError("Unknown file extension: {}".format(name))
        lastMod = strptime(fname.last_modified, "%a, %d %b %Y %H:%M:%S %Z")
        meta.setdefault('latest_generated_date', lastMod)
        meta['latest_generated_date'] = max(
            meta['latest_generated_date'], lastMod)
    return meta


def main():
    logging.basicConfig(level=logging.INFO)
    log = logging.getLogger(__name__)

    meta = {}

    for repo in tqdm(repos, unit="repo"):
        files = repo2meta(repo)
        if files:
            files['repoObj'] = repo
            meta[repo.name] = files
    log.info(meta)

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

    for name, fmt in meta.items():
        if 'markdown' in fmt:
            print(fmt['markdown'])
            continue

        repo = fmt['repoObj']
        fmt = merge(defaults, dict(name=name), fmt)

        fmt['latest_generated_date'] = strftime(
            "%Y-%m-%d", fmt['latest_generated_date'])
        # TODO: auto determine {shortdescription} from repo description

        # TODO: auto determine from repo
        fmt['keywords'] = ", ".join(fmt['keywords'])
        # TODO: auto determine from repo
        fmt['languages'] = ", ".join(fmt['languages'])

        try:
            rel = repo.get_latest_release()
        except:
            pass
        else:
            fmt['latest_release_date'] = fmt['latest_release_date'] or "{rel.last_modified}".format(rel=rel)
            fmt['latest_release'] = fmt['latest_release'] or "{rel.title} ({rel.tag_name})".format(rel=rel)

        print(dedent("""
        # {name}

        [repo](https://github.com/{repo}) | [docs]({documentation}) | [gitter]({gitter}) | [contributor guide]({contributor_guide})

        - lang(s): {languages}
        - keyword(s): {keywords}
        - current version: {latest_release_date} {latest_release}
        - contact: <{coordinator}>

        {shortdescription}

        <small>Last generated {latest_generated_date}</small>
        """)
        .format(**fmt)
        .replace(' | [docs]()', '')
        .replace(' | [gitter]()', '')
        .replace(' | [contributor guide]()', '')
        .replace('- lang(s): \n', '')
        .replace('- keyword(s): \n', '')
        .replace('- current version:  \n', '')
        .replace('- contact: <>\n', '')
        .replace('\n\n\n', '\n')
        )


if __name__ == "__main__":
    sys.exit(main() or 0)
