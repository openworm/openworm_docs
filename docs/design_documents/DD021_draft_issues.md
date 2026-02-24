# DD021 Draft GitHub Issues

**Epic:** DD021 — Movement Analysis Toolbox Revival and WCON Policy

**Generated from:** [DD021: Movement Analysis Toolbox and WCON Policy](DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md)

**Methodology:** [DD015 §2.2 — DD Issue Generator](DD015_AI_Contributor_Model.md#22-the-dd-issue-generator-automated-issue-creation)

**Totals:** 2 issues (ai-workable: 2 / human-expert: 0 | L1: 1, L2: 1)

**Note:** These are the first two issues for DD021. DD021's full issue set (toolbox revival, Python 3.12 compat, WCON parser, etc.) will be generated in a future pass. These two issues were originally in DD001 but belong here because they are **validation infrastructure** — thin wrappers around the analysis toolbox that serve as CI gates in the DD013 simulation pipeline. They are consumed by all DDs that need kinematic validation (DD001, DD002, DD003, DD010), not specific to any one DD. They are Phase A deliverables required for the milestone: "Containerized Stack with Automated Validation."

**Note on provenance:** These issues were moved from DD001 Draft Issues (originally Issues 3 and 4) because they wrap `open-worm-analysis-toolbox` functionality — which DD021 owns — and target `openworm/open-worm-analysis-toolbox`, not `openworm/c302`.

---

## Phase A: Validation Infrastructure

Target: Make the revived analysis toolbox usable as a CI gate — regression detection and baseline generation.

---

### Issue 1: Wrap OWAT's statistics engine as `scripts/check_regression.py`

- **Title:** `[DD021] Wrap open-worm-analysis-toolbox statistics engine into check_regression.py — validation regression detector`
- **Labels:** `DD021`, `ai-workable`, `L1`
- **Target Repo:** `openworm/open-worm-analysis-toolbox`
- **Required Capabilities:** python
- **DD Section to Read:** [DD001 — How to Build & Test](DD001_Neural_Circuit_Architecture.md#how-to-build-test) (Step 5-6) and [DD010 — Tier 3](DD010_Validation_Framework.md) (kinematic validation)
- **Existing Code to Reuse:**
    - [`open-worm-analysis-toolbox/statistics/statistics_manager.py`](https://github.com/openworm/open-worm-analysis-toolbox) — **Already computes** Wilcoxon rank-sum and Student's t-test across **726 kinematic features** with FDR correction (q-values). Includes `histogram_manager.py` for feature distribution comparison. (reuse strategy: **wrap**)
    - [`open-worm-analysis-toolbox/features/`](https://github.com/openworm/open-worm-analysis-toolbox) — Locomotion features including speed, wavelength, frequency, amplitude, crawling/swimming classification — all 5 key metrics needed for validation are already computed. (reuse strategy: **import directly**)
    - `c302/runAndPlot.py` — Generates comparison images across all parameter sets (visual regression checking) (reuse strategy: **reference**)
- **Approach:** **Wrap** OWAT's `StatisticsManager` with a pass/fail gate. Map the 5 key metrics to the corresponding OWAT feature names, add threshold comparison against baseline, return exit code.
- **DD013 Pipeline Role:** Validation gate. Runs as final pipeline stage in `master_openworm.py`. Non-zero exit code blocks the run as failed. Must be callable from `docker compose run validate`.
- **Depends On:** DD021 toolbox revival (OWAT must be installable on Python 3.12)
- **Files to Modify:**
    - `scripts/check_regression.py` (new — thin wrapper around OWAT)
    - `tests/test_check_regression.py` (new)
    - `baseline/validation_baseline.json` (new — baseline scores)
- **Test Commands:**
    - `python3 scripts/check_regression.py validation_report.json baseline/validation_baseline.json`
    - `pytest tests/test_check_regression.py`
- **Acceptance Criteria:**
    - [ ] Uses `open-worm-analysis-toolbox` `StatisticsManager` as the comparison engine — does NOT reimplement feature comparison
    - [ ] Reads a validation report JSON (output from OWAT) and a baseline JSON
    - [ ] Compares 5 key metrics: speed, wavelength, frequency, amplitude, crawling/swimming classification
    - [ ] Flags REGRESSION if any metric degrades >15% from baseline
    - [ ] Prints per-metric comparison table (current vs. baseline vs. threshold)
    - [ ] Returns exit code 0 if no regression, non-zero if regression detected
    - [ ] Unit tests with synthetic reports (passing, regressing, improving)
- **Sponsor Summary Hint:** A guard-rail script built on the existing Schafer lab analysis toolbox — which already compares 726 kinematic features using statistical tests. This wraps that engine with a simple pass/fail gate for CI: does the worm still move like a real worm? If not, the change is flagged. Used by DD001 (neural changes), DD002 (muscle changes), DD003 (body physics changes) — any change that could affect movement is checked here.

---

### Issue 2: Generate Schafer lab kinematic baseline using OWAT

- **Title:** `[DD021] Generate kinematic baseline metrics from Schafer lab N2 WCON data using open-worm-analysis-toolbox`
- **Labels:** `DD021`, `ai-workable`, `L2`
- **Target Repo:** `openworm/open-worm-analysis-toolbox`
- **Required Capabilities:** python, worm-biology
- **DD Section to Read:** [DD001 — Goal & Success Criteria](DD001_Neural_Circuit_Architecture.md#goal-success-criteria) (±15% of Schafer lab) and [DD010](DD010_Validation_Framework.md) (Tier 3)
- **Existing Code to Reuse:**
    - [`open-worm-analysis-toolbox`](https://github.com/openworm/open-worm-analysis-toolbox) — **IS the Python port of the Schafer lab's Worm Analysis Toolbox.** `WormFeatures` class computes all 726 Schafer features including the 5 key metrics needed. Has WCON loading (`examples/WCON demo.py`), `NormalizedWorm` class for 49-point skeleton, and validation against original MATLAB toolbox (`documentation/Schafer_validation/`). (reuse strategy: **import directly**)
    - [`open-worm-analysis-toolbox/examples/generate_stats.py`](https://github.com/openworm/open-worm-analysis-toolbox) — Example script for statistical comparison (reuse strategy: **adapt**)
- **Approach:** **Use the existing library** — load Schafer N2 WCON data through OWAT, extract the 5 key metrics from its 726-feature output, save as baseline JSON. The feature computation is already implemented; this issue is data extraction and formatting, not algorithm development.
- **DD013 Pipeline Role:** Produces the baseline artifact that `check_regression.py` (Issue 1) compares against. Run once to generate, then committed to repo.
- **Depends On:** DD021 toolbox revival (OWAT must be installable on Python 3.12)
- **Files to Modify:**
    - `baseline/schafer_baseline_metrics.json` (new)
    - `scripts/generate_baseline.py` (new — thin script calling OWAT)
- **Test Commands:**
    - `python3 scripts/generate_baseline.py --input schafer_n2_data/ --output baseline/schafer_baseline_metrics.json`
- **Acceptance Criteria:**
    - [ ] Uses `open-worm-analysis-toolbox` `WormFeatures` to compute kinematics — does NOT reimplement feature extraction
    - [ ] Downloads or locates Schafer lab N2 wild-type WCON data (from open-worm-analysis-toolbox or Zenodo)
    - [ ] Extracts 5 key metrics via OWAT: forward speed, body wavelength, undulation frequency, body amplitude, crawling/swimming gait classification
    - [ ] Saves metrics with mean ± std to JSON file
    - [ ] Documents data provenance (which dataset, which animals, which conditions)
    - [ ] ±15% thresholds computed and stored alongside baseline values
    - [ ] Baseline committed to repo as reference for `check_regression.py`
- **Sponsor Summary Hint:** The Schafer lab analysis toolbox — already ported to Python by OpenWorm — computes 726 movement features from real worm tracking data. This issue runs it on wild-type N2 recordings to extract the 5 key metrics our simulation must match. The toolbox does the heavy lifting; this issue extracts and formats the answer key.

---

## Summary Statistics

| Category | Count |
|----------|-------|
| **Total Issues** | 2 |
| **ai-workable** | 2 |
| **human-expert** | 0 |
| **L1** | 1 |
| **L2** | 1 |

| Phase | Issues | Target |
|-------|--------|--------|
| **Phase A: Validation Infrastructure** | 1–2 | CI regression gate (via OWAT) and Schafer lab baseline generation |

### Cross-References

| Related DD | Related Issues |
|------------|---------------|
| DD001 (Neural Circuit) | Consumer: neural circuit changes validated by Issue 1 regression gate |
| DD002 (Muscle Model) | Consumer: muscle changes validated by Issue 1 regression gate |
| DD003 (Body Physics) | Consumer: body physics changes validated by Issue 1 regression gate |
| DD010 (Validation Framework) | Issue 1 implements the Tier 3 kinematic validation gate that DD010 specifies |
| DD013 (Simulation Stack) | Issue 1 runs as `docker compose run validate` pipeline stage |

### Dependency Graph

```
DD021 toolbox revival (OWAT Python 3.12 compatible)
  └→ Issue 2 (generate Schafer baseline) → Issue 1 (check_regression.py wrapping OWAT)
```

### Future Issues (Not Yet Generated)

DD021's full issue set — covering toolbox revival (Python 3.12 compat, dependency cleanup), WCON parser fixes, feature extraction validation, and integration with DD010's validation framework — will be generated in a future pass. Issues 1-2 above are the "last mile" deliverables that depend on the toolbox being functional.
