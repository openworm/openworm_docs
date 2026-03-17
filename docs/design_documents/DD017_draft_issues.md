# DD017 Draft GitHub Issues

**Epic:** DD017 — Hybrid Mechanistic-ML Framework

**Generated from:** [DD017: Hybrid Mechanistic-ML Framework](DD017_Hybrid_Mechanistic_ML_Framework.md)

**Methodology:** [DD015 §2.2 — DD Issue Generator](DD015_AI_Contributor_Model.md#22-the-dd-issue-generator-automated-issue-creation)

**Totals:** 3 issues (ai-workable: 2 / human-expert: 1 | L1: 1, L2: 2, L3: 0)

**Roadmap Context:** DD017 is a **Phase 3** DD (proposed). These synaptic optimization issues were originally part of DD001 Draft Issues (Group 4) and have been relocated here because synaptic weight optimization requires DD017's differentiable simulation backend. DD017 Component 1 provides the gradient descent infrastructure; these issues prepare the biological constraints and validation targets.

| Group | Phase | Rationale |
|-------|-------|-----------|
| 1. Synaptic Optimization (Issues 1-3) | **Phase 2** | Weight optimization requires DD017 differentiable backend |

---

## Group 1: Synaptic Optimization (Phase 2)

Target: Per-synapse conductance optimization using differentiable simulation and neurotransmitter identity constraints.

---

### Issue 1: Consolidate existing neurotransmitter data into synapse polarity constraints

- **Title:** `[DD017] Consolidate existing neurotransmitter identity data from c302, wormneuroatlas, and Wang et al. 2024 into validated synapse polarity constraints`
- **Labels:** `DD017`, `human-expert`, `L2`
- **Roadmap Phase:** Phase 2
- **Target Repo:** `openworm/c302`
- **Required Capabilities:** python, neuroml, neuroscience
- **DD Section to Read:** [DD001 — Synaptic Weight and Polarity Optimization](DD001_Neural_Circuit_Architecture.md#synaptic-weight-and-polarity-optimization) (neurotransmitter identity constraints) and [DD017 — Component 1: Differentiable Backend](DD017_Hybrid_Mechanistic_ML_Framework.md)
- **Depends On:** None
- **Existing Code to Reuse:**
    - [`c302/data/GABA.py`](https://github.com/openworm/c302) — GABAergic neuron identity vector (binary, 279 neurons). Already used in c302 network generation.
    - [`c302/data/Bentley_et_al_2016_expression.csv`](https://github.com/openworm/c302) — Comprehensive CSV with neurotransmitter identities (Dopamine, Serotonin, GABA, etc.), neuropeptide expression, and receptor expression per neuron, with evidence citations.
    - [`c302/__init__.py` `generate()` function](https://github.com/openworm/c302) — Already uses `synclass` to set synapse polarity (excitatory vs inhibitory) during network generation.
    - [`wormneuroatlas/SynapseSign.py`](https://github.com/openworm/wormneuroatlas) — Synapse sign predictions from Fenyves et al. 2020, accessible via `NeuroAtlas.get_synapse_sign()`.
    - [`BAAIWorm/eworm/components/cb2022_data/`](https://github.com/Jessie940611/BAAIWorm) — Calcium correlation data used for model fitting
- **Approach:** **Consolidate and validate** existing data sources — c302 already has neurotransmitter data in multiple places (GABA.py, Bentley CSV, synclass in generate()). Merge these with wormneuroatlas SynapseSign data, update with Wang et al. 2024 where it supersedes older sources, and create a single validated constraint module.
- **Files to Modify:**
    - `c302/data/neurotransmitter_identities.csv` (new — consolidated from existing sources)
    - `c302/synapse_constraints.py` (new — wrapping existing polarity logic)
- **Test Commands:**
    - `python3 -c "from c302 import synapse_constraints; sc = synapse_constraints.load(); print(sc.get_polarity('AVAL', 'AVAR'))"`
    - `pytest tests/test_synapse_constraints.py`
- **Acceptance Criteria:**
    - [ ] Consolidates neurotransmitter data from: c302 GABA.py, Bentley et al. 2016 CSV, wormneuroatlas SynapseSign, and Wang et al. 2024
    - [ ] Documents where sources agree and disagree; flags conflicts for expert review
    - [ ] Map neurotransmitter type to synapse polarity: glutamatergic → excitatory, GABAergic → inhibitory, cholinergic → excitatory (with exceptions)
    - [ ] Provide a Python API: `get_polarity(pre, post)` returns +1 (excitatory) or -1 (inhibitory)
    - [ ] Flag synapses where polarity is ambiguous or unknown
    - [ ] Data stored in version-controlled CSV with provenance
    - [ ] Unit tests verify known polarity assignments (e.g., DD/VD GABAergic → inhibitory)
- **Sponsor Summary Hint:** c302 already has neurotransmitter data scattered across multiple files (GABA.py, Bentley CSV, synclass logic) and wormneuroatlas provides synapse sign predictions. This issue consolidates all of it — plus newer Wang et al. 2024 data — into a single validated constraint module, so the synapse optimizer can't violate known biology.

---

### Issue 2: Add `neural.synapse_optimization` config toggle

- **Title:** `[DD017] Add neural.synapse_optimization config toggle to openworm.yml`
- **Labels:** `DD017`, `ai-workable`, `L1`
- **Roadmap Phase:** Phase 2
- **Target Repo:** `openworm/c302` + `openworm/OpenWorm`
- **Required Capabilities:** python, yaml
- **DD Section to Read:** [DD001 — Synaptic Weight and Polarity Optimization](DD001_Neural_Circuit_Architecture.md#synaptic-weight-and-polarity-optimization) (Configuration section) and [DD017 — Configuration](DD017_Hybrid_Mechanistic_ML_Framework.md)
- **Depends On:** DD013 Issue 1 (openworm.yml schema)
- **Files to Modify:**
    - `openworm.yml` (add `neural.synapse_optimization: false`)
    - c302 network generation (read optimization flag)
- **Test Commands:**
    - `python3 -c "from c302 import generate; generate('C1', 'FW', synapse_optimization=False)"`
    - `python3 -c "from c302 import generate; generate('C1', 'FW', synapse_optimization=True)"`
- **Acceptance Criteria:**
    - [ ] `neural.synapse_optimization: false` → uses uniform g_syn = 0.09 nS (backward compatible)
    - [ ] `neural.synapse_optimization: true` → loads per-synapse fitted values from `data/optimized_weights.json`
    - [ ] Placeholder `optimized_weights.json` with uniform weights (actual optimization is a separate issue)
    - [ ] Config documented with DD cross-reference to DD017 (differentiable backend)
    - [ ] Both modes produce valid NeuroML
- **Sponsor Summary Hint:** Currently all synapses in the model have the same strength (0.09 nS) — like every connection in the brain being equally strong. In reality, some connections are powerful and some are whisper-quiet. This toggle switches between the simple uniform model and an optimized model where each synapse has its own fitted strength. The optimization itself is a separate task (requires DD017 differentiable backend).

---

### Issue 3: Create thin adapter for Randi 2023 functional connectivity via wormneuroatlas

- **Title:** `[DD017] Create adapter for Randi 2023 functional connectivity matrix using wormneuroatlas API`
- **Labels:** `DD017`, `ai-workable`, `L2`
- **Roadmap Phase:** Phase 2
- **Target Repo:** `openworm/c302`
- **Required Capabilities:** python, neuroscience
- **DD Section to Read:** [DD001 — Synaptic Weight and Polarity Optimization](DD001_Neural_Circuit_Architecture.md#synaptic-weight-and-polarity-optimization) (full 302-neuron optimization) and [DD017 — Validation Targets](DD017_Hybrid_Mechanistic_ML_Framework.md)
- **Depends On:** None
- **Existing Code to Reuse:**
    - [`wormneuroatlas`](https://github.com/openworm/wormneuroatlas) — **The Randi 2023 signal propagation atlas is already included** as `funatlas.h5` with a clean Python API: `NeuroAtlas.get_signal_propagation_atlas(strain="wt")`. Supports WT and unc-31 strains. Handles neuron ID conventions and bilateral/dorsoventral merging.
    - [`c302/examples/test/test_WNA.py`](https://github.com/openworm/c302) — Already tests wormneuroatlas integration including gap junctions, chemical synapses, and neurotransmitter sign
    - [`BAAIWorm/eworm/components/cb2022_data/Ca_corr_mat.txt`](https://github.com/Jessie940611/BAAIWorm) — Same underlying Randi data in matrix form, used for BAAIWorm model fitting
- **Approach:** **Thin adapter on wormneuroatlas** — the data loading is essentially a one-liner (`NeuroAtlas.get_signal_propagation_atlas()`). The real work is neuron name mapping to c302 conventions and the `compare_to_simulation()` utility.
- **Files to Modify:**
    - `c302/data/randi2023_functional_connectivity.py` (new — thin adapter)
    - `tests/test_randi_data.py` (new)
- **Test Commands:**
    - `python3 -c "from c302.data import randi2023_functional_connectivity as rfc; m = rfc.load_correlation_matrix(); print(m.shape)"`
    - `pytest tests/test_randi_data.py`
- **Acceptance Criteria:**
    - [ ] Loads Randi 2023 data via `wormneuroatlas.NeuroAtlas.get_signal_propagation_atlas()` — does NOT duplicate the dataset
    - [ ] Maps neuron IDs from wormneuroatlas convention to c302 neuron names
    - [ ] Handle missing neurons gracefully (not all 302 are in the imaging data)
    - [ ] Provide utility: `compare_to_simulation(sim_calcium_matrix)` → Pearson correlation
    - [ ] Unit tests verify matrix is symmetric, diagonal is 1.0, shape is correct
- **Sponsor Summary Hint:** Randi et al. (2023) recorded nearly every neuron in the worm's brain simultaneously — and the data is already in wormneuroatlas with a clean Python API. This issue writes a thin adapter that maps wormneuroatlas neuron names to c302's conventions, plus a comparison utility for optimization. The hard data work is already done.

---

## Summary Statistics

| Category | Count |
|----------|-------|
| **Total Issues** | 3 |
| **ai-workable** | 2 |
| **human-expert** | 1 |
| **L1** | 1 |
| **L2** | 2 |
| **L3** | 0 |

| Group | Issues | Target |
|-------|--------|--------|
| **1: Synaptic Optimization** | 1–3 | Consolidate neurotransmitter data, weight fitting prep |

### Cross-References

| Related DD | Relationship |
|------------|-------------|
| **[DD001](DD001_draft_issues.md) (Neural Circuit)** | **Original source** — these issues were extracted from DD001 Draft Issues Group 4 |
| DD005 (Cell-Type Specialization) | Channel library informs synapse models |
| DD010 (Validation Framework) | Functional connectivity validation targets |
| DD013 (Simulation Stack) | Issue 2 (config toggle depends on openworm.yml schema) |
| DD020 (Connectome Data Access) | Neurotransmitter data consolidation |

### Dependency Graph

```
Issue 1 (consolidate neurotransmitter constraints) — independent
Issue 2 (synapse_optimization config) — depends on DD013 Issue 1
Issue 3 (Randi 2023 adapter via wormneuroatlas) — independent
```
