# DD028: Project Metrics Dashboard

- **Status:** Proposed
- **Author:** OpenWorm Core Team
- **Date:** 2026-02-27
- **Related:** [DD010](DD010_Validation_Framework.md), [DD011](DD011_Contributor_Progression_Model.md), [DD013](DD013_Simulation_Stack_Architecture.md), [DD014](DD014_Dynamic_Visualization_Architecture.md)

> **Phase:** [Phase A1: Core Infrastructure](DD_PHASE_ROADMAP.md#phase-a1-core-infrastructure-weeks-1-2) | **Layer:** Infrastructure

---

## TL;DR

DD028 defines a real-time project metrics dashboard aggregating validation scores, contributor activity, CI pipeline health, and phase progress into a single status page. The dashboard transforms the static Phase Roadmap into a live instrument panel, closing the feedback loop that lets maintainers and contributors see the project's pulse without reading issue trackers. Success metric: all four dashboard panels update automatically on every CI run.

---

## Goal & Success Criteria

| Criterion | Target |
|-----------|--------|
| DD010 tier improvement | Tier 1 (structural) — dashboard verifies validation infrastructure is running |
| Validation panel | Displays current Tier 2 and Tier 3 scores with trend over last 30 runs |
| Contributor panel | Shows PRs merged, issues closed, and badge counts per contributor level (L0–L4) |
| CI health panel | Aggregates GitHub Actions results across all active repos into pass/fail/pending |
| Phase progress panel | Parses DD status fields and displays completion percentages per phase |
| Update latency | Dashboard refreshes within 10 minutes of any CI run completing |
| Zero-install access | Deployed as a static site via GitHub Pages — no login, no server |

---

## Deliverables

| File | Format | Description |
|------|--------|-------------|
| `dashboard/index.html` | HTML + JS | Single-page dashboard with four panels |
| `dashboard/data/validation.json` | JSON | Time-series validation scores (Tier 2/3 metrics per run) |
| `dashboard/data/contributors.json` | JSON | Contributor activity: PRs, issues, badge counts from BadgeList API |
| `dashboard/data/ci-status.json` | JSON | GitHub Actions workflow run results across repos |
| `dashboard/data/phase-progress.json` | JSON | Phase completion derived from DD status fields |
| `.github/workflows/dashboard-update.yml` | YAML | Scheduled + event-triggered workflow that collects data and deploys |
| `scripts/collect_metrics.py` | Python | Data collection script: GitHub API + BadgeList API → JSON |

---

## Repository & Issues

- **Repository:** `openworm/openworm` (or a dedicated `openworm/dashboard` repo if preferred)
- **Issue label:** `dd028-dashboard`
- **Milestone:** Phase 1 — Project Metrics Dashboard

---

## How to Build & Test

### Prerequisites

- Python 3.10+
- GitHub Personal Access Token (read-only, for API queries)
- BadgeList API token (from hello@badgelist.com)

### Getting Started

**Path A: Local preview**

```bash
git clone https://github.com/openworm/openworm.git
cd openworm/dashboard
python ../scripts/collect_metrics.py --local   # generates data/*.json from GitHub API
python -m http.server 8080                      # preview at localhost:8080
```

**Path B: GitHub Actions (production)**

The `dashboard-update.yml` workflow runs:

1. On schedule (every 6 hours)
2. On `workflow_run` completion (any CI pipeline across tracked repos)
3. On manual dispatch

It calls `collect_metrics.py`, commits updated JSON to the `gh-pages` branch, and GitHub Pages serves the result.

### Green Light Criteria

- [ ] `python scripts/collect_metrics.py --local` produces 4 JSON files without error
- [ ] `dashboard/index.html` opens in browser and renders all 4 panels
- [ ] Validation panel shows at least one data point with Tier 2 score
- [ ] Contributor panel shows badge counts matching BadgeList totals
- [ ] CI panel shows pass/fail for at least 3 repos
- [ ] Phase progress panel shows non-zero completion for Phase 0

### Scripts That Don't Exist Yet

- `scripts/collect_metrics.py` `[TO BE CREATED]` — [Issue: Implement metrics collector](#)
- `.github/workflows/dashboard-update.yml` `[TO BE CREATED]` — [Issue: Create dashboard CI workflow](#)

---

## How to Visualize

DD028 **is** the visualization. The dashboard itself is the deliverable. It does not depend on DD014's simulation viewer — it is a separate static site focused on project health rather than simulation output.

Dashboard URL (target): `https://openworm.github.io/openworm/dashboard/` or `status.openworm.org`

---

## Technical Approach

### Architecture

```
GitHub Actions (repos) ──→ collect_metrics.py ──→ JSON files ──→ Static dashboard
BadgeList API ─────────────┘                                      (GitHub Pages)
```

### Panel 1: Validation Scores

- **Source:** GitHub Actions artifacts from DD013's `validate` workflow
- **Data:** Tier 2 functional connectivity score (% of known connections reproduced), Tier 3 behavioral kinematics score (body wave frequency, amplitude, speed within empirical bounds)
- **Display:** Line chart (last 30 runs), current score with pass/fail indicator, regression alerts (score drops > 5% from rolling average)
- **Library:** Chart.js (lightweight, no build step, CDN-loadable)

### Panel 2: Contributor Activity

- **Source:** GitHub API (`/repos/{owner}/{repo}/stats/contributors`) across tracked repos + BadgeList API (`/groups/openworm/users`, `/portfolios`)
- **Data:** PRs merged (last 30/90/365 days), issues opened/closed, active contributors by level (L0–L4 from DD011 badge counts)
- **Display:** Bar chart of monthly activity, contributor count by level (stacked), badge leaderboard (top 10 by badges earned)
- **Privacy:** Display GitHub usernames only (already public); no email addresses

### Panel 3: CI Pipeline Health

- **Source:** GitHub API (`/repos/{owner}/{repo}/actions/runs`) across all active repos
- **Data:** Latest workflow run status per repo (success/failure/pending/skipped), failure rate over last 30 days
- **Display:** Traffic-light grid (green/yellow/red per repo), aggregate health score, link to failing run

### Panel 4: Phase Progress

- **Source:** DD status fields parsed from markdown files in the `docs/design_documents/` directory + Phase Roadmap milestone definitions
- **Data:** Per-phase count of Accepted vs. Proposed vs. Superseded DDs, key milestone status (manual annotation in `phase-progress.json`)
- **Display:** Horizontal progress bars per phase, DD status breakdown, link to Phase Roadmap for details

### Technology Choices

| Choice | Rationale |
|--------|-----------|
| Static HTML + vanilla JS | Zero server cost, trivial to maintain, no build toolchain |
| Chart.js | 70KB CDN, no dependencies, sufficient for line/bar/doughnut charts |
| GitHub Pages | Free hosting, automatic deployment from `gh-pages` branch |
| JSON data files | Human-readable, git-diffable, trivially consumed by JS |
| Python collector script | Consistent with project's Python toolchain (c302, cect, validation) |

---

## Alternatives Considered

| Alternative | Why Rejected |
|------------|--------------|
| **Grafana + InfluxDB** | Requires a running server, operational burden for a volunteer project. Overkill for 4 panels updated every few hours. |
| **GitHub Actions badges only** | Per-repo badges don't aggregate across 40+ repos. No trend data, no contributor view. |
| **Notion / Google Sheets** | Not programmatically updatable from CI. Manual maintenance defeats the purpose. |
| **Embed in MkDocs site** | MkDocs builds are slow and the docs site serves a different audience (contributors reading specs). Dashboard is for at-a-glance health. |
| **Streamlit dashboard** | Requires a running server (Streamlit Cloud or self-hosted). Static is simpler and free. |

---

## Quality Criteria

- Dashboard loads in < 3 seconds on a standard connection
- All 4 panels render without JavaScript errors
- Data files are valid JSON (validated by CI)
- Validation scores match the values in the latest CI run artifacts
- Contributor counts match BadgeList API totals (± 1 day lag acceptable)
- Mobile-responsive layout (panels stack vertically on narrow screens)

---

## Boundaries (Explicitly Out of Scope)

- **Simulation visualization** — that is DD014's domain
- **Real-time streaming** — the dashboard updates periodically (every CI run + every 6 hours), not via WebSocket
- **User authentication** — the dashboard is fully public
- **Historical data beyond 1 year** — older data can be archived; the dashboard shows rolling windows
- **Alerting / notifications** — the dashboard displays status; alerting (Slack/email on regression) is a future extension

---

## Context & Background

The ExO (Exponential Organizations) framework identifies **Dashboards** as one of five internal attributes for managing abundance: real-time metrics with short feedback loops. OpenWorm currently has no dynamic dashboard — the Phase Roadmap is a static markdown document, validation results are buried in CI logs, contributor activity requires manual GitHub queries, and badge progress is visible only on individual BadgeList profiles.

As the project scales from 5 active contributors toward dozens (human + AI), the absence of a shared status view creates information asymmetry. Maintainers cannot identify regressions without reading CI logs. New contributors cannot see where help is needed. The board cannot assess project health without asking the core team.

DD028 closes this gap with the simplest possible implementation: a static page fed by a Python script on a cron schedule.

---

## References

1. DD010 — Validation Framework (defines Tier 2/3 metrics this dashboard tracks)
2. DD011 — Contributor Progression Model (defines badge categories and level thresholds)
3. DD013 — Simulation Stack Architecture (defines CI pipeline whose results this dashboard aggregates)
4. Chart.js — https://www.chartjs.org/ (visualization library)
5. GitHub REST API — https://docs.github.com/en/rest (data source for CI and contributor activity)
6. BadgeList API v1 — https://badgelist.com/api/v1 (data source for badge counts)
7. Ismail, Diamandis & Malone — *Exponential Organizations 2.0* (2023), Chapter on Dashboards

---

## Integration Contract

### Inputs

| Source | Data | Format | Frequency |
|--------|------|--------|-----------|
| DD013 CI pipeline | Validation scores, build status | GitHub Actions artifacts (JSON) | Every CI run |
| DD011 BadgeList | Badge counts, user counts per level | BadgeList API v1 (JSON) | Every 6 hours |
| GitHub API | PR/issue counts, contributor stats | REST API (JSON) | Every 6 hours |
| DD status fields | Phase completion | Parsed from markdown files | Every 6 hours |

### Outputs

| Consumer | Data | Format |
|----------|------|--------|
| Project website | Embeddable status badge (overall health) | SVG badge |
| Contributors | At-a-glance project health | Static HTML dashboard |
| Board | Phase progress and contributor trends | Same dashboard, Phase Progress panel |
| DD010 | Historical validation score trends | `dashboard/data/validation.json` |

### Repository & Packaging

- Dashboard files live in `dashboard/` directory of the integration repo
- Deployed to GitHub Pages on the `gh-pages` branch
- No package dependencies beyond Python standard library + `requests`

### Configuration (`openworm.yml` section)

```yaml
dashboard:
  enabled: true
  repos_tracked:
    - openworm/openworm
    - openworm/c302
    - openworm/sibernetic
    - openworm/open-worm-analysis-toolbox
    - openworm/ConnectomeToolbox
  update_schedule: "0 */6 * * *"   # every 6 hours
  badgelist_group: "openworm"
  github_pages_branch: "gh-pages"
```

### How to Test (Contributor Workflow)

```bash
# 1. Run collector locally
python scripts/collect_metrics.py --local --output dashboard/data/

# 2. Preview dashboard
cd dashboard && python -m http.server 8080
# Open http://localhost:8080 — all 4 panels should render

# 3. Validate JSON schema
python -c "import json; [json.load(open(f'dashboard/data/{f}.json')) for f in ['validation','contributors','ci-status','phase-progress']]"
```

### Coupling Dependencies

- **Upstream:** DD013 (CI artifacts), DD011/BadgeList (badge data), DD010 (validation metric definitions)
- **Downstream:** None (dashboard is a read-only consumer)
- **Coupling strength:** Loose — dashboard reads public APIs and CI artifacts; no subsystem needs to know the dashboard exists
