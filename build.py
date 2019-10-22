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

GH = Github(os.getenv("GITHUB_API_TOKEN"))
REPOS = list(GH.get_organization("OpenWorm").get_repos())
TEMPLATE = open("docs/gsod19/repos.md.template").read()


def repo2content(repo):
    """
    @return {"filename": (File, "content")}
    where `filename` starts with `.openworm.`
    """
    tree = repo.get_git_tree("master", recursive=False).tree
    files = [i for i in tree if i.path.lower().startswith(".openworm.")]
    if not files:
        return {}

    reqs = [requests.get(i.url) for i in files]
    try:
        data = [b64decode(i.json()["content"]) for i in reqs]
    except KeyError:
        raise ValueError(reqs)  # likely 403
    return dict(zip((i.path.lower() for i in files), zip(files, data)))


def repo2meta(repo):
    content = repo2content(repo)
    if not content:
        return {}
    meta = {}
    for name, (fObj, data) in content.items():
        if name.endswith(".yml") or name.endswith(".yaml"):
            meta.update(
                {
                    k.lower().replace("-", "_"): v
                    for k, v in yaml.safe_load(data).items()
                }
            )
            meta["ymlObj"] = fObj
        elif name.endswith(".rst"):
            raise NotImplementedError
        elif name.endswith(".md"):
            meta["markdown"] = data
            meta["mdObj"] = fObj
        else:
            raise KeyError("Unknown file extension: {}".format(name))
        lastMod = fObj.last_modified_at
        meta.setdefault("latest_generated_date", lastMod)
        meta["latest_generated_date"] = max(
            meta["latest_generated_date"], lastMod
        )
    return meta


def main():
    logging.basicConfig(level=logging.INFO)
    log = logging.getLogger(__name__)

    meta = {}
    for repo in tqdm(REPOS, unit="repo"):
        fmt = repo2meta(repo)
        if fmt:
            fmt["repoObj"] = repo
            meta[repo.name] = fmt
    log.info(meta)

    defaults = {
        # TODO: build graph based on the following, and use it to determine
        # 1. order of printing
        # 2. heading levels
        "children": [],
        "parent": "",
        "inputs": [],
        "outputs": [],
        # TODO: use the following
        # 'earnable_badges': '',
        # 'members': '',
        # 'tests': ''
        "contributor_guide": "",
        "coordinator": "",
        "documentation": "",
        "gitter": "",
        "keywords": [],
        "languages": [],
        "latest_release": "",
        "repo": "",
        "shortdescription": "",
        "latest_release_date": "",
        "latest_generated_date": "",
    }

    for name, fmt in meta.items():
        if "markdown" in fmt:
            print(fmt["markdown"])
            continue

        repo = fmt["repoObj"]
        fmt = merge(defaults, dict(name=name), fmt)

        fmt.setdefault("shortdescription", repo.description)
        # TODO: maybe use repo.updated_at or repo.pushed_at ?

        # TODO: auto determine from repo
        fmt["keywords"] = ", ".join(fmt["keywords"])
        # TODO: auto determine from repo
        fmt["languages"] = ", ".join(fmt["languages"])

        try:
            rel = repo.get_latest_release()
        except:  # NOQA
            pass
        else:
            fmt["latest_release_date"] = fmt[
                "latest_release_date"
            ] or "{rel.published_at:%Y-%m-%d}".format(rel=rel)
            fmt["latest_release"] = fmt[
                "latest_release"
            ] or "{rel.title} ({rel.tag_name})".format(rel=rel)

        print(
            TEMPLATE.format(**fmt)
            .replace(" | [docs]()", "")
            .replace(" | [gitter]()", "")
            .replace(" | [contributor guide]()", "")
            .replace("- lang(s): \n", "")
            .replace("- keyword(s): \n", "")
            .replace("- current version:  \n", "")
            .replace("- contact: <>\n", "")
            .replace("\n\n\n", "\n")
        )


if __name__ == "__main__":
    sys.exit(main() or 0)
