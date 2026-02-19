How We Know It's Working: The Validation Framework
===================================================

## The Challenge

Building a digital organism is hard. How do we know we're getting it right?

**Answer:** We validate at 3 levels, specified in **[DD010: Validation Framework](design_documents/DD010_Validation_Framework.md)**.

---

## Tier 1: Single-Cell Validation

**What:** Do individual neurons and muscles behave correctly in isolation?

**Test:** Compare simulated voltage/calcium traces to patch clamp recordings

**Data Sources:**

- Goodman lab (touch neurons)
- Lockery lab (interneurons)
- Liu lab (motor neurons)

**Status:** Non-blocking (warning if fails). A Tier 1 failure means a cell model needs tuning but doesn't prevent the overall simulation from running.

---

## Tier 2: Circuit-Level Validation

**What:** Do neurons interact correctly as a network?

**Test:** Compute pairwise calcium correlations (302x302 matrix), compare to Randi et al. 2023 whole-brain imaging data.

**Acceptance Criteria:** Correlation-of-correlations r > 0.5

**Why r > 0.5?** This threshold means the simulated network captures more than 25% of the variance in real neural activity patterns. It's a stringent bar — random connectivity produces r ~ 0.

**Status:** **BLOCKING** — a PR cannot merge if it degrades Tier 2 below threshold.

---

## Tier 3: Behavioral Validation

**What:** Does the organism produce correct emergent behavior?

**Test:** 5 kinematic metrics compared to Schafer lab behavioral database:

| Metric | What It Measures | Real Worm Value | Acceptable Range |
|--------|-----------------|-----------------|-----------------|
| **Speed** | Forward crawling velocity | ~0.2 mm/s | +/-15% |
| **Wavelength** | Body wave spatial period | ~1.5 mm | +/-15% |
| **Frequency** | Body wave temporal frequency | ~0.5 Hz | +/-15% |
| **Amplitude** | Body bend depth | ~0.15 mm | +/-15% |
| **Gait** | Overall movement pattern | Sinusoidal | Qualitative |

**Acceptance Criteria:** All 5 metrics within +/-15% of experimental mean.

**Status:** **BLOCKING** — a PR cannot merge if it causes Tier 3 regression.

**Tool:** [open-worm-analysis-toolbox](https://github.com/openworm/open-worm-analysis-toolbox) — being revived per [DD021](design_documents/DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md).

---

## Why 3 Tiers?

A model can produce correct movement for the wrong reasons (parameter compensation, overfitting). Multi-tier validation ensures:

- **Mechanistic correctness** (Tier 1: cells work right)
- **Circuit correctness** (Tier 2: connections work right)
- **Behavioral correctness** (Tier 3: organism works right)

**All three must pass** for the model to be considered validated.

Think of it like building a car: you test individual engine components (Tier 1), test the engine as a system (Tier 2), then test the car driving on a road (Tier 3). If the car drives fine but the engine is wrong, you got lucky — and the next change will break everything.

---

## Organ-Specific Validation (Phase 3)

Beyond the 3-tier framework for locomotion, organ systems have their own validation targets:

| Organ | DD | Validation Metric | Target |
|-------|----|-------------------|--------|
| **Pharynx** | DD007 | Pumping frequency | 3-4 Hz |
| **Intestine** | DD009 | Defecation cycle period | 50 +/- 10 seconds |
| **Egg-laying** | DD018 | Active/inactive pattern | ~20 min inactive, ~2 min active |

---

## How Validation Runs in Practice

1. **Per-PR (quick-test):** Runs Tier 1 + subset of Tier 3 (<5 min)
2. **Pre-merge (validate):** Runs all 3 tiers (~30 min)
3. **Nightly (full):** Extended runs with statistical analysis

The [DD013 Simulation Stack](design_documents/DD013_Simulation_Stack_Architecture.md) specifies the Docker commands:

```bash
docker compose run quick-test    # Per-PR validation
docker compose run validate      # Full 3-tier validation
```

---

## Current Status

| Tier | Implementation | Automated? |
|------|---------------|------------|
| **Tier 1** | Scripts exist but not integrated into CI | No |
| **Tier 2** | Randi 2023 data identified, needs ingestion pipeline | No |
| **Tier 3** | **BLOCKED** — analysis toolbox needs revival ([DD021](design_documents/DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md)) | No |

**Infrastructure priority:** Get all 3 tiers automated in CI so every PR is validated automatically.

---

[Read the complete specification](design_documents/DD010_Validation_Framework.md)
