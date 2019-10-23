#!/usr/bin/env python
from __future__ import print_function, division
import os
import sys
from base64 import b64decode
import logging

import requests
from tqdm import tqdm
from github import Github
import yaml
from funcy import merge
from six import string_types
import igraph

GH = Github(os.getenv("GITHUB_API_TOKEN"))
REPOS = list(GH.get_organization("OpenWorm").get_repos())
TEMPLATE = open("docs/gsod19/repos.md.template").read()


class RepoTree(igraph.Graph):
    def __init__(self, directed=True, **k):
        super(RepoTree, self).__init__(directed=directed, **k)

    def add_edge(self, src, dst):
        try:
            for v in {src, dst}.difference(self.vs['name']):
                self.add_vertex(v)
        except KeyError:
            self.add_vertex(src)
            self.add_vertex(dst)
        try:
            self.get_eid(src, dst)
        except igraph.InternalError:
            super(RepoTree, self).add_edge(src, dst)


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
    outfile = open("docs/gsod19/repos.md", "w")

    def tee(*a):
        print(*a)
        print(*a, file=outfile)

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
        "parent": [],
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

    tee("![Repos](repos.png)")
    graph = RepoTree()
    for name, fmt in meta.items():
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

        if isinstance(fmt['parent'], string_types):
            fmt['parent'] = [fmt['parent']]
        #for i in filter(None, fmt['children']):
        for i in fmt['children']:
            graph.add_edge(fmt['repo'], i)
        #for i in filter(None, fmt['parent']):
        for i in fmt['parent']:
            graph.add_edge(i, fmt['repo'])
        continue

        if "markdown" in fmt:
            tee(fmt["markdown"])
            continue
        tee(
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

    outfile.close()

    igraph.plot(
        graph,
        "docs/gsod19/repos.png",
        layout=graph.layout('large'),
        bbox=(860, 860),
        margin=80,
        vertex_label=[
            i[len('openworm/'):] if i.lower().startswith('openworm/') else i
            for i in graph.vs['name']
        ]
    )


if __name__ == "__main__":
    sys.exit(main() or 0)
