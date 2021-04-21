#!/usr/bin/env python
"""
Creates docs/gsod19/repos-graph.html
Requires env `$GITHUB_API_TOKEN`
"""
from __future__ import print_function, division
import os
import sys
from base64 import b64decode
import logging
import datetime
import math
from time import sleep, time

import requests
from tqdm import tqdm, trange
from github import Github
from github.GithubException import UnknownObjectException, RateLimitExceededException
import yaml
from jinja2 import Template
from funcy import merge
from six import string_types
import igraph

GH = Github(os.getenv("GITHUB_TOKEN"))
REPOS = list(GH.get_organization("OpenWorm").get_repos())
TEMPLATE = Template(open("resources/repos.md.template").read())
REPO_METADATA_SHAS = os.getenv("REPO_METADATA_SHAS")

LOGGER = logging.getLogger(__name__)


class RepoTree(igraph.Graph):
    def __init__(self, directed=True, **k):
        super(RepoTree, self).__init__(directed=directed, **k)

    def add_edge(self, src, dst):
        try:
            for v in {src, dst}.difference(self.vs["name"]):
                self.add_vertex(v)
        except KeyError:
            self.add_vertex(src)
            self.add_vertex(dst)
        try:
            self.get_eid(src, dst)
        except igraph.InternalError:
            super(RepoTree, self).add_edge(src, dst)

    def plot(self, outfile, layout="kk"):
        labels = [
            i[len("openworm/") :] if i.lower().startswith("openworm/") else i
            for i in self.vs["name"]
        ]
        layout = self.layout(layout)
        width, height = 680, 860

        if outfile.lower().endswith(".png"):
            igraph.plot(
                self,
                outfile,
                layout=layout,
                bbox=(width, height),
                margin=10,
                vertex_label=labels,
            )
            return

        assert outfile.lower().endswith(".html")
        from plotly import graph_objects as go

        edges = [e.tuple for e in self.es]
        Xn = [layout[i][0] for i in range(len(labels))]
        Yn = [layout[i][1] for i in range(len(labels))]
        Xe = sum([[layout[i][0], layout[j][0], None] for (i, j) in edges], [])
        Ye = sum([[layout[i][1], layout[j][1], None] for (i, j) in edges], [])

        traceLines = go.Scatter(
            x=Xe,
            y=Ye,
            mode="lines",
            line=dict(color="rgb(210,210,210)", width=1),
            hoverinfo="none",
        )
        traceNodes = go.Scatter(
            x=Xn,
            y=Yn,
            mode="markers",
            name="ntw",
            marker=dict(
                symbol="circle-dot",
                size=16,
                color="#6959CD",
                line=dict(color="rgb(50,50,50)", width=0.5),
            ),
            text=labels,
            hoverinfo="text",
        )
        ax = dict(
            showline=False,  # hide axis line, grid, ticklabels and  title
            zeroline=False,
            showgrid=False,
            showticklabels=False,
            title="",
        )

        layout_html = go.Layout(
            title="OpenWorm Repositories",
            font=dict(size=12),
            showlegend=False,
            autosize=False,
            width=width,
            height=height,
            xaxis=go.layout.XAxis(ax),
            yaxis=go.layout.YAxis(ax),
            margin=go.layout.Margin(l=80, r=80, b=80, t=80),  # NOQA: E741
            hovermode="closest",
            annotations=[
                dict(
                    showarrow=False,
                    text="All OpenWorm repositories",
                    xref="paper",
                    yref="paper",
                    x=0,
                    y=-0.1,
                    xanchor="left",
                    yanchor="bottom",
                    font=dict(size=14),
                )
            ],
        )

        fig = go.Figure(data=[traceLines, traceNodes], layout=layout_html)
        fig.write_html(outfile, auto_open=False)


def get_first_tree(repo, branches):
    """
    @return `tree` corresponding to the first existing branch in `branches`
    """
    for branch in branches:
        retry = None
        while retry is None or retry:
            retry = False
            try:
                return repo.get_git_tree(branch, recursive=False).tree
            except UnknownObjectException:
                LOGGER.debug(
                    "Did not find branch %s in %s", branch, repo, exc_info=True
                )
            except RateLimitExceededException as e:
                try:
                    print("all the headers", e.headers)
                    limit = e.headers["x-ratelimit-limit"]
                    reset = int(e.headers["x-ratelimit-reset"])
                    wait_time_seconds = reset - time()
                    LOGGER.warning(
                        "Rate limit of %s exceeded. Waiting %d seconds",
                        limit,
                        wait_time_seconds,
                        exc_info=True,
                    )
                    wait_for_limit_expiration(wait_time_seconds)
                    retry = True
                except Exception:
                    LOGGER.warning(
                        "Rate limit exceeded. Couldn't determine limit or reset time,"
                        " so just waiting for five minutes before retrying",
                        exc_info=True,
                    )
                    wait_for_limit_expiration(300)
                    retry = True
            except Exception:
                LOGGER.warning(
                    "Failed to recover branch %s in %s", branch, repo, exc_info=True
                )


def wait_for_limit_expiration(time):
    seconds = math.ceil(time / 5)
    for n in trange(seconds):
        sleep(5)


def repo2content(repo):
    """
    @return {"filename": (File, "content")}
    where `filename` starts with `.openworm.`
    """
    tree = get_first_tree(repo, ["master", "main", "develop"])
    if tree is None:
        LOGGER.info("Skipping %s because we cannot find a branch", repo)
        return {}
    files = [i for i in tree if i.path.lower().startswith(".openworm.")]
    if not files:
        LOGGER.info(
            "Skipping %s because we cannot find .openworm.* file among %s", repo, files
        )
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
        meta["sha"] = fObj.sha
        lastMod = datetime.datetime.strptime(
            fObj.last_modified, "%a, %d %b %Y %H:%M:%S %Z"
        )
        meta.setdefault("latest_generated_date", lastMod)
        meta["latest_generated_date"] = max(meta["latest_generated_date"], lastMod)
    meta["latest_generated_date"] = "{:%Y-%m-%d}".format(meta["latest_generated_date"])
    return meta


def main():
    logging.basicConfig(level=logging.INFO)

    meta = {}
    for repo in tqdm(REPOS, unit="repo"):
        fmt = repo2meta(repo)
        if fmt:
            fmt["repoObj"] = repo
            meta[repo.name] = fmt
    LOGGER.info(meta)

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

    graph = RepoTree()
    shas = []
    with open("docs/Community/repositories.md", "w") as outfile:

        def tee(*a):
            tqdm.write(" ".join(map(str, a)))
            print(*a, file=outfile)

        tee('<iframe src="../repos-graph.html" width="100%" height=880></iframe>\n')
        for name, fmt in tqdm(meta.items(), unit="repos"):
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

            if isinstance(fmt["parent"], string_types):
                fmt["parent"] = [fmt["parent"]]
            # for i in filter(None, fmt['children']):
            for i in fmt["children"]:
                graph.add_edge(fmt["repo"], i)
            # for i in filter(None, fmt['parent']):
            for i in fmt["parent"]:
                graph.add_edge(i, fmt["repo"])

            if "markdown" in fmt:
                tee(fmt["markdown"])
                continue
            tee(TEMPLATE.render(**fmt))
            shas.append((fmt["repo"], fmt["sha"]))
    with open(REPO_METADATA_SHAS, "w") as shasfile:
        for repo, sha in sorted(shas):
            print(f"{repo} {sha}", file=shasfile)

    graph.plot("docs/Community/repos-graph.html")


if __name__ == "__main__":
    sys.exit(main() or 0)
