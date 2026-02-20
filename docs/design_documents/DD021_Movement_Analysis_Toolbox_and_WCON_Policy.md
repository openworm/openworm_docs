# DD021: Movement Analysis Toolbox and WCON Policy

**Status:** Proposed  
**Author:** OpenWorm Core Team  
**Date:** 2026-02-16  
**Supersedes:** None  
**Related:** [DD003](DD003_Body_Physics_Architecture.md) (Body Physics — WCON producer), [DD008](DD008_Data_Integration_Pipeline.md) (Data Integration Pipeline), [DD010](DD010_Validation_Framework.md) (Validation Framework — Tier 3 consumer), [DD013](DD013_Simulation_Stack_Architecture.md) (Simulation Stack — CI consumer), [DD020](DD020_Connectome_Data_Access_and_Dataset_Policy.md) (Connectome Data Access — structural model)

---

## Quick Action Reference

| Question | Answer |
|----------|--------|
| **What does this produce?** | Revived `open-worm-analysis-toolbox` package: installs on Python 3.12, extracts 5 kinematic features from WCON files, compares simulated vs. experimental worm movement, outputs pass/fail validation report |
| **Success metric** | Toolbox installs cleanly; `NormalizedWorm.from_schafer_file()` + `WormFeatures()` produces speed, wavelength, frequency, amplitude, gait classification for Schafer N2 baseline data; Sibernetic WCON output parses without error |
| **Repository** | [`openworm/open-worm-analysis-toolbox`](https://github.com/openworm/open-worm-analysis-toolbox) (primary) + [`openworm/tracker-commons`](https://github.com/openworm/tracker-commons) (WCON spec). Note: `openworm/movement_validation` is the **archived predecessor** — do not use. |
| **Config toggle** | `validation.tier3_behavioral: true` in `openworm.yml` (DD010/DD013) |
| **Build & test** | `pip install open-worm-analysis-toolbox` then `python -c "from open_worm_analysis_toolbox import NormalizedWorm; print('OK')"` |
| **Visualize** | Toolbox generates matplotlib comparison plots (simulated vs. experimental feature distributions); DD014 viewer shows validation overlay in `validation/overlay/` OME-Zarr group |
| **CI gate** | Toolbox import succeeds; feature extraction on sample WCON returns 5 non-NaN metrics; version matches `versions.lock` |

---

## TL;DR

The `open-worm-analysis-toolbox` is OpenWorm's canonical tool for **Tier 3 behavioral validation** (DD010). It compares simulated worm movement trajectories against Schafer lab experimental data by extracting kinematic features from WCON (Worm tracker Commons Object Notation) files. The toolbox is **dormant** (last commit: January 16, 2020 — 6 years ago) with 28 open issues and broken Python 3.12 compatibility. This DD specifies: (1) the toolbox's revival plan with owners and effort estimates, (2) WCON 1.0 format pinning from tracker-commons, (3) the canonical API contract for feature extraction and comparison, (4) version pinning policy, and (5) the relationship to Tierpsy Tracker (modern community successor). **Without a working analysis toolbox, Tier 3 validation is impossible — this is a blocking dependency for DD010 and DD013.**

---

## Goal & Success Criteria

| Criterion | Target | DD010 Tier |
|-----------|--------|------------|
| **Primary:** Toolbox installs on Python 3.12 | `pip install` succeeds in Docker image with no import errors | Tier 3 (blocking) |
| **Secondary:** 5 kinematic metrics computable | Speed, wavelength, frequency, amplitude, crawl/swim classification extracted from sample WCON | Tier 3 (blocking) |
| **Tertiary:** Sibernetic WCON output parseable | `NormalizedWorm.from_simulation()` successfully loads Sibernetic's WCON output file | Tier 3 (blocking) |
| **Quaternary:** Test suite passes | ≥80% of existing tests pass on Python 3.12 after dependency updates | Non-blocking (quality gate) |

**Before:** DD010 specifies Tier 3 behavioral validation but the tool to perform it is broken. The revival checklist (DD010 lines 260-270) is buried, unactionable, and has no owners or timeline. The WCON format is referenced but not pinned to a version. Tierpsy Tracker (the modern successor used by the broader community) is never mentioned. The archived predecessor repo (`movement_validation`) is not noted, risking contributor confusion.

**After:** A single DD (this one) specifies the toolbox revival, WCON format pinning, API contract, and landscape context. DD010 points here for "how to perform Tier 3 validation." DD013 points here for the Docker stage and `versions.lock` entry. Contributors know exactly what to build, test, and validate.

---

## Deliverables

| Artifact | Path / Location | Format | Example |
|----------|----------------|--------|---------|
| Revived `open-worm-analysis-toolbox` | GitHub: `openworm/open-worm-analysis-toolbox` / PyPI (future) | Python package | `from open_worm_analysis_toolbox import NormalizedWorm` |
| WCON format pin | This DD (Section: WCON Format Specification) | Markdown specification | "WCON 1.0 per tracker-commons" |
| `openworm.yml` validation config | `validation.tier3_behavioral` key (defined in DD010, consumed here) | YAML | `tier3_behavioral: true` |
| `versions.lock` entries | `open_worm_analysis_toolbox` + `tracker_commons` keys in `versions.lock` (DD013) | Lock file | `open_worm_analysis_toolbox: { commit: "abc123" }` |
| Feature extraction report | `output/validation_report.json` (Tier 3 section) | JSON | `{ "speed": { "simulated": 0.22, "experimental": 0.25, "pass": true } }` |
| Comparison plots | `output/validation_plots/` | PNG (matplotlib) | `speed_comparison.png`, `wavelength_histogram.png` |

---

## Repository & Issues

| Item | Value |
|------|-------|
| **Primary repository** | [`openworm/open-worm-analysis-toolbox`](https://github.com/openworm/open-worm-analysis-toolbox) |
| **WCON specification** | [`openworm/tracker-commons`](https://github.com/openworm/tracker-commons) |
| **Archived predecessor** | [`openworm/movement_validation`](https://github.com/openworm/movement_validation) — **archived, do not use** |
| **Issue label** | `dd021` |
| **Milestone** | Toolbox Revival (Phase A) |
| **Branch convention** | `dd021/description` (e.g., `dd021/python312-compat`) |
| **Example PR title** | `DD021: Update dependencies for Python 3.12 compatibility` |
| **De facto maintainer** | TBD — Validation L4 (currently unfilled) |
| **Stars / Issues** | 48 stars, 28 open issues (as of Feb 2026) |
| **Last commit** | January 16, 2020 |

### Repository Landscape

```
openworm/movement_validation        (ARCHIVED — original Schafer lab port, do not use)
        │
        └──→ openworm/open-worm-analysis-toolbox  (CURRENT — Python rewrite, dormant since Jan 2020)
                                                    This DD revives this repo.

openworm/tracker-commons            (WCON spec — last pushed Apr 2025, 32 issues)
        │                           Defines the data format consumed by the toolbox.
        └──→ WCON 1.0 specification
```

---

## How to Build & Test

### Prerequisites

- Python 3.12 (Docker image or local)
- pip
- NumPy, SciPy, matplotlib, h5py (dependencies)

### Step-by-step

```bash
# Step 1: Install the toolbox (after revival PR merged)
pip install -e git+https://github.com/openworm/open-worm-analysis-toolbox.git@dd021/python312-compat#egg=open_worm_analysis_toolbox

# Step 2: Verify import
python -c "
from open_worm_analysis_toolbox import NormalizedWorm, WormFeatures
print('Analysis toolbox loaded successfully')
"

# Step 3: Load sample experimental data (Schafer lab N2 baseline)
python -c "
from open_worm_analysis_toolbox import NormalizedWorm, WormFeatures
worm = NormalizedWorm.from_schafer_file('examples/example_contour_and_skeleton_info.mat')
features = WormFeatures(worm)
print(f'Speed: {features.locomotion.velocity.midbody.speed.mean():.3f} mm/s')
print(f'Feature extraction: OK')
"

# Step 4: Verify WCON parser loads Sibernetic output
python -c "
from open_worm_analysis_toolbox.wcon_parser import WCONParser
# After Sibernetic simulation produces a .wcon file:
# wcon = WCONParser.load('output/worm_trajectory.wcon')
# worm = NormalizedWorm.from_wcon(wcon)
print('WCON parser loaded successfully')
"

# Step 5: Run test suite
cd open-worm-analysis-toolbox/
python -m pytest tests/ -v --tb=short
# Target: ≥80% pass rate after dependency updates

# Step 6: Docker-based verification (DD013 stack)
docker compose run shell python -c "
from open_worm_analysis_toolbox import NormalizedWorm, WormFeatures
print('Toolbox in Docker: OK')
"
```

---

## Toolbox Architecture

### Package Structure

The `open-worm-analysis-toolbox` is organized around a feature extraction pipeline derived from Yemini et al. 2013:

```
open-worm-analysis-toolbox/
├── open_worm_analysis_toolbox/
│   ├── __init__.py
│   ├── features/                    # Feature computation modules
│   │   ├── locomotion_features.py   # Speed, velocity, motion events
│   │   ├── posture_features.py      # Bends, wavelength, amplitude, eccentricity
│   │   ├── morphology_features.py   # Length, width, area
│   │   └── path_features.py         # Range, curvature, dwelling
│   ├── prefeatures/                 # Preprocessing (skeleton → features)
│   │   ├── normalized_worm.py       # NormalizedWorm class (core data structure)
│   │   ├── basic_worm.py            # BasicWorm (raw data container)
│   │   └── worm_plotter.py          # Visualization utilities
│   ├── statistics/                  # Statistical comparison framework
│   │   ├── histogram.py             # Feature histograms
│   │   ├── histogram_manager.py     # Multi-feature histogram management
│   │   └── specs.py                 # Feature specification metadata
│   └── wcon/                        # WCON format parser (tracker-commons)
│       ├── wcon_parser.py           # WCON file I/O
│       └── measurement_unit.py      # Unit handling
├── tests/                           # Test suite
├── examples/                        # Example data files
│   ├── example_contour_and_skeleton_info.mat  # Schafer lab MAT format
│   └── example_worm.wcon            # Example WCON file
└── setup.py / pyproject.toml        # Package configuration
```

### Core Classes

**`NormalizedWorm`** — The central data structure. Represents a worm's posture as a time series of 49-point skeletons (dorsal/ventral contours normalized to a standard frame).

```python
from open_worm_analysis_toolbox import NormalizedWorm

# From Schafer lab .mat file (experimental data)
exp_worm = NormalizedWorm.from_schafer_file("schafer_N2_baseline.mat")

# From WCON file (simulation output or tracked data)
sim_worm = NormalizedWorm.from_wcon("simulation_output.wcon")

# From simulation output (convenience wrapper)
sim_worm = NormalizedWorm.from_simulation("c302_output.wcon")

# Properties:
# exp_worm.skeleton       — (n_frames, 49, 2) array of skeleton points
# exp_worm.ventral_contour — (n_frames, 49, 2)
# exp_worm.dorsal_contour  — (n_frames, 49, 2)
# exp_worm.angles          — (n_frames, 49) body bend angles
# exp_worm.length          — (n_frames,) worm length per frame
```

**`WormFeatures`** — Computes the full Yemini et al. 2013 feature set (~726 features in 6 categories).

```python
from open_worm_analysis_toolbox import WormFeatures

features = WormFeatures(exp_worm)

# Locomotion features:
features.locomotion.velocity.midbody.speed    # Forward/backward speed
features.locomotion.bends.midbody.frequency   # Undulation frequency

# Posture features:
features.posture.bends.midbody.amplitude      # Bend amplitude
features.posture.wavelength.primary            # Body wavelength

# Morphology features:
features.morphology.length                     # Body length

# Path features:
features.path.range                            # Distance traveled
```

**`WormFeatures.compare()`** — Compares two feature sets (simulated vs. experimental).

```python
# Compare simulated to experimental
comparison = sim_features.compare(exp_features)
print(comparison.summary())
# Output: Per-metric pass/fail with deviation percentages

# Specific metric check
speed_match = comparison.check_metric("speed", tolerance=0.15)
# Returns: True if within ±15%
```

### Five Core Validation Metrics (DD010 Tier 3)

| Metric | Feature Path | Units | Experimental Range (N2) | Tolerance |
|--------|-------------|-------|------------------------|-----------|
| **Speed** | `locomotion.velocity.midbody.speed` | mm/s | 0.20 - 0.30 | ±15% |
| **Wavelength** | `posture.wavelength.primary` | mm | 0.5 - 0.8 | ±15% |
| **Frequency** | `locomotion.bends.midbody.frequency` | Hz | 0.3 - 0.6 | ±15% |
| **Amplitude** | `posture.bends.midbody.amplitude` | degrees | 20 - 40 | ±15% |
| **Gait** | `locomotion.motion_events.crawl_vs_swim` | categorical | "crawl" on agar | exact match |

---

## WCON Format Specification

### What Is WCON?

WCON (Worm tracker Commons Object Notation) is a JSON-based file format for storing *C. elegans* tracking data. It was developed by the `tracker-commons` project to provide a universal interchange format across worm tracking software.

### Version Pin

**This DD pins WCON 1.0** as defined in `openworm/tracker-commons` (commit to be recorded in `versions.lock`).

WCON 1.0 specification: https://github.com/openworm/tracker-commons/blob/master/WCON_format.md

### Required Fields for OpenWorm Simulation Output

Sibernetic (DD003) must produce WCON files with at minimum these fields:

```json
{
    "units": {
        "t": "s",
        "x": "mm",
        "y": "mm"
    },
    "data": [
        {
            "id": "1",
            "t": [0.0, 0.001, 0.002],
            "x": [[0.1, 0.2, 0.3, "...49 skeleton points"]],
            "y": [[0.5, 0.6, 0.7, "...49 skeleton points"]]
        }
    ],
    "metadata": {
        "software": {
            "name": "Sibernetic",
            "version": "ow-0.10.0",
            "settings": {
                "backend": "opencl",
                "particle_count": 100000,
                "duration_ms": 15.0
            }
        },
        "lab": {
            "name": "OpenWorm Simulation"
        }
    }
}
```

### WCON Field Requirements

| Field | Required? | Description | Notes |
|-------|-----------|-------------|-------|
| `units.t` | **Yes** | Time unit | Must be `"s"` (seconds) |
| `units.x`, `units.y` | **Yes** | Spatial units | Must be `"mm"` (millimeters) |
| `data[].id` | **Yes** | Worm identifier | `"1"` for single-worm simulation |
| `data[].t` | **Yes** | Time points array | Monotonically increasing |
| `data[].x`, `data[].y` | **Yes** | Skeleton x/y coordinates | Array of arrays, 49 points per frame |
| `metadata.software` | Recommended | Producing software info | Sibernetic version, settings |
| `metadata.lab` | Optional | Lab/source info | "OpenWorm Simulation" |

### Parser Requirements

The analysis toolbox's WCON parser must:

1. **Load WCON 1.0 files** conforming to the `tracker-commons` specification
2. **Handle both compressed (`.wcon.zip`) and uncompressed (`.wcon`) formats**
3. **Convert to `NormalizedWorm`** — extract skeleton points, compute contours if absent, normalize frame count
4. **Validate units** — reject files with inconsistent or missing unit declarations
5. **Handle chunked files** — WCON supports splitting large datasets across multiple files via `"files"` array

### Sibernetic WCON Output (DD003 Coupling)

Sibernetic currently outputs body positions in a custom format (`position_buffer.txt`). A WCON exporter must be added:

```python
# In master_openworm.py (DD013 orchestrator), Step 4:
# Convert Sibernetic particle positions → 49-point skeleton → WCON

from open_worm_analysis_toolbox.wcon import WCONExporter

exporter = WCONExporter(
    software_name="Sibernetic",
    software_version=config["versions"]["sibernetic"],
    time_unit="s",
    spatial_unit="mm"
)

for frame in simulation_frames:
    skeleton = extract_skeleton_from_particles(frame.particles)  # 49 points
    exporter.add_frame(t=frame.time, skeleton=skeleton)

exporter.save("output/worm_trajectory.wcon")
```

**This WCON exporter is a deliverable of DD003/DD013, not DD021.** DD021 specifies what the toolbox expects to receive; DD003/DD013 specify how to produce it.

---

## Revival Plan

The analysis toolbox has been dormant for 6 years. The following 8-task plan brings it back to operational status.

| # | Task | Owner | Effort | Dependency | Status |
|---|------|-------|--------|------------|--------|
| 1 | Test on Python 3.12 | Validation L4 | 4h | None | Not started |
| 2 | Update NumPy/SciPy/matplotlib to current versions | Validation L4 | 8h | Task 1 |  Not started |
| 3 | Verify WCON parser vs. tracker-commons spec | Validation L4 | 4h | Task 2 | Not started |
| 4 | Fix test suite failures | Validation L4 | 8h | Task 2 | Not started |
| 5 | Pin in `versions.lock` (DD013) | Integration Maintainer | 1h | Task 4 (tests pass) | Not started |
| 6 | Add Docker `validation` stage | Integration Maintainer | 2h | Task 5 | Not started |
| 7 | Verify Sibernetic WCON output parses | Body Physics L4 | 2h | Task 6 | Not started |
| 8 | End-to-end `NormalizedWorm.from_simulation()` | Validation L4 | 4h | All above | Not started |

**Total effort: ~33 hours**

### Task Details

**Task 1: Test on Python 3.12**
```bash
# Create fresh virtualenv with Python 3.12
python3.12 -m venv test_env && source test_env/bin/activate
pip install -e .
python -c "from open_worm_analysis_toolbox import NormalizedWorm"
# Document all import errors and deprecation warnings
```

**Task 2: Update Dependencies**
- NumPy: likely needs `np.float` → `np.float64`, `np.int` → `np.int64` fixes (deprecated aliases removed in NumPy 1.24+)
- SciPy: check for removed functions (`scipy.misc.comb` → `scipy.special.comb`, etc.)
- matplotlib: update deprecated API calls
- h5py: verify MAT file reading compatibility

**Task 3: Verify WCON Parser**
- Load example WCON files from `tracker-commons/tests/`
- Verify parser handles all WCON 1.0 required fields
- Test with Sibernetic's actual output format (once available)

**Task 4: Fix Test Suite**
```bash
python -m pytest tests/ -v --tb=short 2>&1 | tee test_results.txt
# Categorize failures: dependency issues vs. logic bugs vs. data file issues
# Target: ≥80% pass rate
```

**Task 5: Pin in `versions.lock`**
```yaml
# versions.lock addition
open_worm_analysis_toolbox:
  repo: "https://github.com/openworm/open-worm-analysis-toolbox.git"
  commit: "<revival-commit-hash>"

tracker_commons:
  repo: "https://github.com/openworm/tracker-commons.git"
  commit: "<pinned-commit-hash>"
  wcon_version: "1.0"
```

**Task 6: Add Docker Stage**
```dockerfile
# In multi-stage Dockerfile (DD013)
FROM base AS validation
ARG OWAT_REF=dd021/python312-compat
RUN git clone --branch $OWAT_REF --depth 1 \
    https://github.com/openworm/open-worm-analysis-toolbox.git \
    /opt/openworm/validation
RUN pip install -e /opt/openworm/validation
# Include Schafer lab experimental data
COPY validation_data/kinematics/ /opt/openworm/validation/data/
```

**Task 7: Verify Sibernetic WCON Parses**
```python
# After a Sibernetic simulation:
from open_worm_analysis_toolbox import NormalizedWorm
worm = NormalizedWorm.from_wcon("output/worm_trajectory.wcon")
assert worm.skeleton.shape[1] == 49, "Expected 49 skeleton points"
assert not np.any(np.isnan(worm.skeleton)), "NaN values in skeleton"
print(f"Loaded {worm.skeleton.shape[0]} frames")
```

**Task 8: End-to-End Validation**
```python
from open_worm_analysis_toolbox import NormalizedWorm, WormFeatures

# Load simulated
sim_worm = NormalizedWorm.from_simulation("output/worm_trajectory.wcon")
sim_features = WormFeatures(sim_worm)

# Load experimental
exp_worm = NormalizedWorm.from_schafer_file("data/schafer_N2_baseline.mat")
exp_features = WormFeatures(exp_worm)

# Compare
comparison = exp_features.compare(sim_features)
report = comparison.summary()
print(report)
# Must produce: 5 metrics, each with simulated value, experimental value, pass/fail
```

### Revival Priority

**This is a Phase A (DD013 roadmap) task.** Without a working analysis toolbox:
- DD010 Tier 3 validation cannot run
- DD013 CI pipeline Steps 4-5 remain unimplemented
- Behavioral regression detection is impossible
- The simulation stack has no automated quality gate for movement

---

## Relationship to Tierpsy Tracker

### What Is Tierpsy?

**Tierpsy Tracker** (Javer et al. 2018) is the modern community-standard tool for *C. elegans* behavioral phenotyping. It is the spiritual successor to the Schafer lab's original Worm Tracker 2.0 software and provides:

- Multi-worm tracking from video
- 726-feature behavioral phenotyping (same feature set as the analysis toolbox, based on Yemini et al. 2013)
- Automated quality control
- Database of wild-type and mutant phenotypes
- Active development (last commit: 2024)
- Python 3.x compatible

**Repository:** [`ver228/tierpsy-tracker`](https://github.com/ver228/tierpsy-tracker)

### Why Not Use Tierpsy Directly?

| Consideration | Analysis Toolbox | Tierpsy Tracker |
|--------------|-----------------|-----------------|
| **Designed for** | Comparing simulated vs. experimental data | Analyzing video of real worms |
| **Input format** | WCON files, Schafer .mat files | Video files (.avi, .hdf5) |
| **Simulation coupling** | `NormalizedWorm.from_simulation()` convenience method | No simulation input pathway |
| **OpenWorm integration** | Referenced in DD010, DD013; Docker stage planned | Not integrated; would require adapter layer |
| **Feature set** | Same 726 features (Yemini 2013) | Same 726 features (extended) |
| **Maintenance** | Dormant (6 years) | Actively maintained |
| **Community** | OpenWorm-specific | Broader *C. elegans* community |

### CODE REUSE: OpenWorm Has a Tierpsy Fork!

**Repository:** `openworm/tierpsy-tracker` (pushed 2025-06-29, OpenWorm fork of ver228/tierpsy-tracker)

**Critical Finding:** OpenWorm already forked tierpsy-tracker (the modern successor to the analysis toolbox). This fork may already be customized for OpenWorm's needs.

**URGENT EVALUATION NEEDED:**

```bash
# Test OpenWorm's tierpsy fork
git clone https://github.com/openworm/tierpsy-tracker.git
cd tierpsy-tracker
pip install -e .

# Check: Does it support WCON input?
python -c "
from tierpsy import ...  # (inspect their API)
# Try loading a WCON file
# Try extracting the 5 core metrics (speed, wavelength, frequency, amplitude, gait)
"
```

**Decision Point:**
- **If OpenWorm's tierpsy fork works with WCON:** Skip the entire DD021 8-task revival (saves 33 hours!), use tierpsy directly
- **If it doesn't work but upstream tierpsy does:** Sync OpenWorm's fork with upstream
- **If neither works:** Proceed with DD021 analysis toolbox revival as planned

**This evaluation is Phase A Week 1 priority** (before committing to 33-hour toolbox revival).

### Decision

**Keep the analysis toolbox as the canonical Tier 3 validation tool for now** (pending tierpsy evaluation). Rationale:

1. The toolbox has an existing `from_simulation()` API designed for comparing simulated vs. real data
2. Tierpsy's input pathway assumes video, not simulation output
3. Reviving the toolbox (~33 hours) is less effort than building a Tierpsy adapter (~60+ hours)
4. The feature computation is identical (both implement Yemini 2013)

### Future Evaluation

**Evaluate Tierpsy as a replacement in Phase 3+ when:**
1. The toolbox revival is complete and Tier 3 validation is running
2. Tierpsy has a stable WCON/simulation input pathway
3. The broader community has standardized on Tierpsy for phenotyping
4. Maintaining two tools becomes burdensome

**If adopting Tierpsy:**
- Create `tierpsy_adapter.py` that wraps Tierpsy's feature extraction with OpenWorm's comparison API
- Maintain backward compatibility with existing validation scripts
- Update DD010 acceptance criteria if Tierpsy's feature definitions differ slightly
- File DD amendment via DD012 RFC process

---

## Alternatives Considered

### 1. Use Tierpsy Tracker Directly (Replace the Analysis Toolbox)

**Description:** Abandon the dormant analysis toolbox entirely and use Tierpsy Tracker for all behavioral validation.

**Deferred (not rejected) because:**
- Tierpsy is designed for video analysis, not simulation-to-experiment comparison
- No `from_simulation()` or WCON input pathway exists in Tierpsy
- Building an adapter layer is more effort than reviving the existing toolbox
- The analysis toolbox's comparison API (`WormFeatures.compare()`) is purpose-built for OpenWorm's use case

**When to reconsider:** Phase 3+, after Tier 3 validation is operational and if Tierpsy adds WCON input support.

### 2. Build Custom Validation Scripts (No Shared Library)

**Description:** Write one-off Python scripts for each kinematic metric (speed, wavelength, etc.) without using a shared feature extraction library.

**Rejected because:**
- Duplicates effort already done in the toolbox (6+ years of feature extraction code)
- Feature computation is non-trivial (skeleton normalization, bend detection, motion event classification)
- No standardization across metrics — each script would use different conventions
- The analysis toolbox already implements the full Yemini 2013 feature set

### 3. Statistical-Only Comparison (Skip Feature Extraction)

**Description:** Compare simulated and experimental WCON files using raw statistical measures (DTW distance, Frechet distance) on trajectories, without extracting biological features.

**Rejected because:**
- Loses biological interpretability — "speed is 20% too fast" is actionable; "DTW distance is 0.42" is not
- DD010 Tier 3 criteria are defined in terms of biological features (speed, wavelength, frequency, amplitude, gait)
- Cannot diagnose which aspect of movement is wrong without feature decomposition

### 4. Abandon WCON (Use Custom Binary Format)

**Description:** Replace WCON with a more efficient binary format (HDF5, NumPy .npz) for simulation output.

**Rejected because:**
- WCON is the community standard for worm tracking data (adopted by Tierpsy, WormBase, tracker-commons)
- WCON is human-readable (JSON), which aids debugging
- The overhead of JSON for ~1000 frames of 49-point skeletons is trivial (~1MB)
- Abandoning WCON would isolate OpenWorm from the broader *C. elegans* phenotyping community
- `tracker-commons` repo is still maintained (pushed Apr 2025) and defines the spec

---

## Quality Criteria

### What Defines a Working Analysis Toolbox?

1. **Installability:** `pip install` succeeds on Python 3.12 in a clean virtualenv with no manual intervention.

2. **Feature Extraction:** Given a valid WCON or Schafer .mat file, `WormFeatures()` produces non-NaN values for all 5 core metrics (speed, wavelength, frequency, amplitude, gait).

3. **WCON Parsing:** The WCON parser loads files conforming to WCON 1.0 (tracker-commons spec). Unit conversion is handled automatically.

4. **Comparison API:** `WormFeatures.compare()` produces a per-metric pass/fail report with deviation percentages.

5. **Test Suite:** ≥80% of existing tests pass after dependency updates. New tests added for WCON 1.0 parsing and Python 3.12 compatibility.

6. **Docker Integration:** The toolbox is installable in the DD013 Docker `validation` stage and accessible from `docker compose run validate`.

7. **Reproducibility:** Same input file + same toolbox version always produces identical feature values.

---

## Boundaries (Explicitly Out of Scope)

### What This Design Document Does NOT Cover:

1. **What to validate (acceptance criteria):** DD010 defines the three-tier validation framework and acceptance thresholds (±15% for Tier 3 metrics). This DD specifies the tool that performs the validation.

2. **CI/CD pipeline:** DD013 defines how validation runs in Docker and CI. This DD specifies the tool that DD013's pipeline invokes.

3. **Experimental data curation:** DD008 (OWMeta) and DD010 define how experimental data (Schafer lab, Raizen pumping, Thomas defecation) are ingested, versioned, and stored. This DD specifies how the toolbox consumes that data.

4. **WCON production (Sibernetic output):** DD003 defines how Sibernetic produces body positions. DD013's orchestrator converts particle positions to skeleton → WCON. This DD specifies what the toolbox expects to receive.

5. **Visualization:** DD014 defines the viewer. The toolbox produces matplotlib plots for validation reports; DD014's viewer shows validation overlays in the OME-Zarr output.

6. **Pharyngeal pumping / defecation validation:** DD007 and DD009 define pumping and defecation metrics. The analysis toolbox covers locomotion only. Pumping and defecation are validated by separate scripts (DD010).

7. **Video tracking:** The toolbox does not track worms from video. It analyzes pre-tracked data (skeleton time series). For video tracking, use Tierpsy Tracker.

---

## Integration Contract

### Inputs (What This Subsystem Consumes)

| Input | Source DD | Variable | Format | Units |
|-------|----------|----------|--------|-------|
| Simulated movement trajectory | DD003 (via DD013 orchestrator) | Body centroid + 49-point skeleton over time | WCON 1.0 file | mm, seconds |
| Experimental kinematic data | DD008 / DD010 / Schafer lab | N2 baseline and mutant recordings | Schafer .mat or WCON | mm, seconds |
| Validation config | DD010 / DD013 | Acceptance criteria (tolerance, metric selection) | `openworm.yml` YAML | config keys |

### Outputs (What This Subsystem Produces)

| Output | Consumer DD | Variable | Format | Units |
|--------|------------|----------|--------|-------|
| Kinematic feature values | DD010 (Tier 3 report) | Speed, wavelength, frequency, amplitude, gait per frame | JSON | mm/s, mm, Hz, degrees, categorical |
| Comparison report | DD010 (pass/fail), DD013 (CI gate) | Per-metric simulated vs. experimental, deviation %, pass/fail | JSON | mixed |
| Comparison plots | DD010 (validation report), DD014 (overlay) | Feature distribution histograms, time series overlays | PNG (matplotlib) | visual |
| CI exit code | DD013 (pipeline gate) | 0 if all blocking metrics pass, non-zero if any fail | Process exit code | integer |

### Repository & Packaging

| Item | Value |
|------|-------|
| **Repository** | `openworm/open-worm-analysis-toolbox` |
| **Docker stage** | `validation` in multi-stage Dockerfile (DD013) |
| **`versions.lock` keys** | `open_worm_analysis_toolbox`, `tracker_commons` |
| **Build dependencies** | numpy, scipy, matplotlib, h5py |
| **Data in image** | Schafer lab N2 baseline data (~10MB), example WCON files |

### Configuration (`openworm.yml` Section)

The toolbox is invoked via DD010's validation config (no separate config section):

```yaml
# openworm.yml (DD010 section, consumed by toolbox)
validation:
  tier3_behavioral: true              # Enable behavioral validation
  acceptance_criteria:
    tier3_max_deviation: 0.15         # ±15% tolerance for kinematic metrics
  experimental_data:
    kinematics: "data/schafer_N2_baseline"  # Path to experimental data
```

### How to Test (Contributor Workflow)

```bash
# Per-PR quick test (must pass before submission)
python -c "
from open_worm_analysis_toolbox import NormalizedWorm, WormFeatures
# Load example data (shipped with package)
worm = NormalizedWorm.from_schafer_file('examples/example_contour_and_skeleton_info.mat')
features = WormFeatures(worm)
speed = features.locomotion.velocity.midbody.speed
assert speed is not None, 'Speed computation failed'
assert not all(v is None for v in speed), 'All speed values are None'
print('DD021 quick test: PASS')
"

# Full validation (must pass before merge)
python -c "
from open_worm_analysis_toolbox import NormalizedWorm, WormFeatures
import numpy as np

# Load and extract features from example data
worm = NormalizedWorm.from_schafer_file('examples/example_contour_and_skeleton_info.mat')
features = WormFeatures(worm)

# Verify 5 core metrics are computable
assert features.locomotion.velocity.midbody.speed is not None, 'Speed failed'
assert features.posture.wavelength is not None, 'Wavelength failed'
assert features.locomotion.bends.midbody is not None, 'Frequency failed'
assert features.posture.bends.midbody is not None, 'Amplitude failed'

print('DD021 full validation: PASS')
"
```

### How to Visualize (DD014 Connection)

| Data Flow | Description |
|-----------|-------------|
| Toolbox → JSON report → DD010 | Feature comparison results flow into validation report |
| Toolbox → matplotlib PNGs → `output/validation_plots/` | Standalone comparison plots for human review |
| Toolbox → DD014 overlay | Validation pass/fail per metric exported to `validation/overlay/` in OME-Zarr for viewer overlay |

### Coupling Dependencies

| I Depend On | DD | What Breaks If They Change |
|-------------|----|-----------------------------|
| Movement output format (WCON) | DD003 | If Sibernetic changes skeleton format or WCON structure, parser breaks |
| Experimental data (Schafer lab) | DD008 / DD010 | If experimental data files are relocated or reformatted, loading fails |
| Docker validation stage | DD013 | If `validation` service configuration changes, toolbox environment breaks |
| `versions.lock` entry | DD013 | If toolbox version is bumped, must verify feature computation is unchanged |
| WCON specification | tracker-commons | If WCON spec changes, parser must be updated |

| Depends On Me | DD | What Breaks If I Change |
|---------------|----|-----------------------------|
| Tier 3 validation (acceptance criteria) | DD010 | If feature computation changes, Tier 3 pass/fail thresholds may need recalibration |
| CI pipeline (behavioral gate) | DD013 | If toolbox API changes, CI validation scripts must be updated |
| Validation report format | DD012 (PR review) | If report JSON schema changes, Mind-of-a-Worm can't parse Tier 3 results |
| Visualization overlay | DD014 | If validation output format changes, viewer overlay breaks |

### Integration Test

```bash
# Step 1: Verify toolbox installs in Docker
docker compose run shell python -c "
from open_worm_analysis_toolbox import NormalizedWorm, WormFeatures
print('Analysis toolbox loaded successfully')
"

# Step 2: Verify experimental data is present
docker compose run shell ls /opt/openworm/validation/data/
# Must show: schafer_N2_baseline files

# Step 3: Run feature extraction on example data
docker compose run shell python -c "
from open_worm_analysis_toolbox import NormalizedWorm, WormFeatures
worm = NormalizedWorm.from_schafer_file('/opt/openworm/validation/data/schafer_N2_baseline.mat')
features = WormFeatures(worm)
print(f'Speed: {features.locomotion.velocity.midbody.speed.mean():.3f}')
print('Feature extraction: OK')
"

# Step 4: Run full validation (after simulation)
docker compose run validate
# Verify: output/validation_report.json contains tier3 section
# Verify: tier3 section has speed, wavelength, frequency, amplitude, gait
# Verify: CI exit code = 0 if all metrics pass
```

---

## Context & Background

### History

The open-worm-analysis-toolbox has its origins in the Schafer lab's worm behavioral database (Yemini et al. 2013), which defined a standardized set of ~726 features for phenotyping *C. elegans* movement. The original MATLAB code was ported to Python as `movement_validation` (now archived), then refactored into `open-worm-analysis-toolbox`.

| Year | Event |
|------|-------|
| 2013 | Yemini et al. publish behavioral phenotyping feature set (726 features) |
| 2014 | `movement_validation` repository created (MATLAB → Python port) |
| 2015 | Renamed/refactored to `open-worm-analysis-toolbox` |
| 2015-2018 | Active development, WCON support added |
| 2018 | Javer et al. publish Tierpsy Tracker (modern reimplementation) |
| 2020 | Last commit to analysis toolbox (Jan 16, 2020) |
| 2025 | tracker-commons last pushed (Apr 2025) |
| 2026 | **This DD: revival plan** |

### Why This DD Is Needed Now

The analysis toolbox is referenced as a critical dependency in:
- **DD010** (lines 95, 229, 260-270, 326-346): Tier 3 behavioral validation tool
- **DD013** (lines 28, 54, 61): Validation pipeline Steps 4-5 (unimplemented)
- **DD001/DD003**: Success metrics reference kinematic validation

Yet no DD specifies:
- How to revive the dormant toolbox
- Which WCON version to target
- The API contract for simulation-to-experiment comparison
- The relationship to Tierpsy Tracker
- That `movement_validation` is archived and should not be used

This is the same "referenced everywhere, specified nowhere" pattern that ConnectomeToolbox had before DD020.

---

## Known Issues and Future Work

### Issue 1: NumPy Deprecation Breakage

NumPy 1.24+ removed `np.float`, `np.int`, `np.complex`, `np.bool` aliases. The toolbox likely uses these throughout. Fix: global find-and-replace to explicit types (`np.float64`, `np.int64`, etc.).

### Issue 2: Schafer Lab Data Format Evolution

The original Schafer lab data was in MATLAB `.mat` format (HDF5-backed). Newer data may be in WCON or NWB format. The toolbox should support multiple input formats.

**Future work:** Add NWB (Neurodata Without Borders) reader alongside existing MAT and WCON readers.

### Issue 3: 49-Point Skeleton Assumption

The toolbox assumes 49 skeleton points per frame (Schafer lab convention). Sibernetic's output may have a different number of points depending on particle resolution.

**Mitigation:** The WCON exporter (DD013) must interpolate/resample to exactly 49 points before writing WCON.

### Issue 4: Feature Definitions May Diverge from Tierpsy

While both tools implement Yemini 2013, minor implementation differences may cause feature values to differ slightly. If OpenWorm later switches to Tierpsy, acceptance thresholds may need recalibration.

**Future work:** Benchmark analysis toolbox vs. Tierpsy feature values on identical input data. Document any systematic offsets.

---

## References

1. **Yemini E, Jucikas T, Grundy LJ, Brown AEX, Schafer WR (2013).** "A database of *Caenorhabditis elegans* behavioral phenotypes." *Nature Methods* 10:877-879.
   *Defines the 726-feature behavioral phenotyping framework implemented by the analysis toolbox.*

2. **Javer A, Currie M, Lee CW, Hokanson J, Li K, Martineau CN, et al. (2018).** "An open-source platform for analyzing and sharing worm-behavior data." *Nature Methods* 15:645-646.
   *Tierpsy Tracker — modern reimplementation of Schafer lab phenotyping.*

3. **Schafer WR (2005).** "Deciphering the neural and molecular mechanisms of *C. elegans* behavior." *Current Biology* 15:R723-R729.
   *Context for behavioral analysis in C. elegans.*

4. **Brown AEX, Yemini EI, Grundy LJ, Jucikas T, Schafer WR (2013).** "A dictionary of behavioral motifs reveals clusters of genes affecting *Caenorhabditis elegans* locomotion." *PNAS* 110:791-796.
   *Behavioral motif analysis using the feature set.*

5. **WCON Format Specification.** https://github.com/openworm/tracker-commons/blob/master/WCON_format.md
   *Worm tracker Commons Object Notation format definition.*

6. **Sarma GP, Ghayoomie V, Jacobs T, et al. (2016).** "Unit testing, model validation, and biological simulation." *F1000Research* 5:1946.
   *Philosophical framework: validation as testing.*

---

**Approved by:** Pending (Validation Tools)
**Implementation Status:** Proposed
**Next Actions:**
1. Appoint or recruit Validation L4 maintainer (or assign revival to existing contributor)
2. Begin Task 1: Test toolbox on Python 3.12 in Docker
3. File `dd021` issues on `openworm/open-worm-analysis-toolbox` for each revival task
4. Coordinate with DD003/DD013 owners on WCON exporter timeline
5. Pin `tracker_commons` commit in `versions.lock`
