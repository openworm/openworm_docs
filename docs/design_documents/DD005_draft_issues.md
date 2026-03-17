# DD005 Draft GitHub Issues

**Epic:** DD005 — Cell-Type Differentiation Strategy

**Generated from:** [DD005: Cell-Type Differentiation Strategy](DD005_Cell_Type_Differentiation_Strategy.md)

**Methodology:** [DD015 §2.2 — DD Issue Generator](DD015_AI_Contributor_Model.md#22-the-dd-issue-generator-automated-issue-creation)

**Totals:** 6 issues (ai-workable: 3 / human-expert: 3 | L1: 2, L2: 3, L3: 1)

**Roadmap Context:** DD005 is a **Phase 1** DD (proposed). These ion channel library issues were originally part of DD001 Draft Issues (Group 3) and have been relocated here because the extended channel library is a prerequisite for DD005's expression→conductance mapping. DD005 drives cell-type specialization; these channels provide the molecular basis.

| Group | Phase | Rationale |
|-------|-------|-----------|
| 1. Ion Channel Library (Issues 1-6) | **Phase 1** | Extended channels feed DD005 cell-type specialization |

---

## Group 1: Extended Ion Channel Library (Phase 1)

Target: Expand from 4 generic channels to 14+ neuron-class-specific channels, leveraging existing NeuroML2 models from Nicoletti et al. and NMODL files from BAAIWorm.

---

### Issue 1: Survey existing ion channel implementations across all OpenWorm repos

- **Title:** `[DD005] Survey existing NeuroML2 and NMODL ion channel implementations across all OpenWorm and related repos`
- **Labels:** `DD005`, `ai-workable`, `L1`
- **Roadmap Phase:** Phase 1
- **Target Repo:** `openworm/c302`
- **Required Capabilities:** python, neuroml
- **DD Section to Read:** [DD001 — Extended Ion Channel Library](DD001_Neural_Circuit_Architecture.md#extended-ion-channel-library-phase-1-2) (code reuse plan) and [DD005 — Ion Channel Sources](DD005_Cell_Type_Differentiation_Strategy.md)
- **Depends On:** None
- **Existing Code to Reuse (THIS IS THE CODE TO SURVEY):**
    - [`openworm/NicolettiEtAl2019_NeuronModels/NeuroML2/`](https://github.com/openworm/NicolettiEtAl2019_NeuronModels) — **31 ion channels already in NeuroML2**: AWCon (16 channels: shal, kvs1, shak, kqt3, egl2, kir, unc2, egl19, cca, bk, slo1, bk2, slo2, sk, nca, leak) and RMD (15 channels: bk, bk2, cca, egl19, egl36, kir, leak, nca, shak, shal, sk, slo1, slo2, unc2). Includes `GenerateNeuroML.py` and Ca dynamics model. **Validated against original XPP models.**
    - [`openworm/NicolettiEtAl2024_MN_IN/`](https://github.com/openworm/NicolettiEtAl2024_MN_IN) — **22 NMODL files** for motor neurons (VA5, VB6, VD5) and interneurons (AVAL, AVAR, AIY, RIM). Includes voltage-clamp and current-clamp simulation scripts. **6 channels partially converted to NeuroML2** (AIY subset: egl19, egl2, shk1, shl1, unc2, leak).
    - [`Jessie940611/BAAIWorm/eworm/components/mechanism/modfile/`](https://github.com/Jessie940611/BAAIWorm) — **17+ NMODL files** covering all DD001 target channels. Also contains per-neuron conductance parameters (`eworm/components/param/cell/*.json` — one JSON per neuron with max conductance for each channel), ion channel validation scripts (`eworm/ion_channel_tune/`), and calcium correlation data (`eworm/components/cb2022_data/`). All channels cite Nicoletti et al. 2019 as source.
    - [`openworm/ChannelWorm2/NML2_models/`](https://github.com/openworm/ChannelWorm2) — **4 NeuroML2 channels** (EGL-19, SHK-1, SHL-1, SLO-2) with annotated PDFs of equations. Uses Boyle & Cohen 2008 parameters (different from Nicoletti). Also has **200+ raw electrophysiology JSON files** with digitized I-V curves for C. elegans channels, and a parameter fitting pipeline (`parameter_fitting/`).
    - [`openworm/CElegansNeuroML/CElegans/generatedNeuroML2/`](https://github.com/openworm/CElegansNeuroML) — Generic `LeakConductance.channel.nml` only, but has 11 synapse types (Acetylcholine, GABA, Glutamate, etc.) and all 302 neuron morphologies as multicompartmental NeuroML2.
- **Approach:** **Survey, catalog, and produce a reconciliation matrix** — not just BAAIWorm, but ALL existing channel implementations. The key output is: which channels already exist in NeuroML2 (and can be adopted immediately), which exist only as NMODL (and need conversion), and where parameter discrepancies exist between sources.
- **Files to Modify:**
    - None (research issue — output is a summary comment on the issue)
- **Test Commands:**
    - N/A (research task)
- **Acceptance Criteria:**
    - [ ] Catalog all existing NeuroML2 channel files across: NicolettiEtAl2019, NicolettiEtAl2024, ChannelWorm2, CElegansNeuroML
    - [ ] Catalog all existing NMODL channel files across: BAAIWorm, NicolettiEtAl2024
    - [ ] For each of the 14 channels in DD001's target library table: identify ALL existing implementations (NeuroML2 and/or NMODL), note repository, file path, and parameter source
    - [ ] Produce a reconciliation matrix: where parameters differ between sources (e.g., ChannelWorm2 EGL-19 uses Boyle & Cohen 2008 parameters vs. Nicoletti 2019 parameters), flag for expert review
    - [ ] Assess: do the existing NicolettiEtAl2019 NeuroML2 channels pass `jnml -validate`? Test all 31
    - [ ] Document: license compatibility across repos (Apache 2.0 / MIT)
    - [ ] Recommend: for each channel, which existing implementation to adopt as canonical
    - [ ] Post findings as issue comment
- **Sponsor Summary Hint:** Before converting anything, let's catalog what already exists. Multiple OpenWorm and related repos already contain ion channel models — 31 channels in NeuroML2 from Nicoletti 2019 alone. This survey maps every existing implementation, flags parameter discrepancies between sources, and recommends which to adopt. It could save weeks of conversion work.

---

### Issue 2: Validate and adopt EGL-19 (Cav1 L-type) NeuroML2 channel into c302

- **Title:** `[DD005] Validate and adopt existing EGL-19 (Cav1 L-type Ca²⁺) NeuroML2 channel into c302 channel library`
- **Labels:** `DD005`, `human-expert`, `L2`
- **Roadmap Phase:** Phase 1
- **Target Repo:** `openworm/c302`
- **Required Capabilities:** python, neuroml, electrophysiology
- **DD Section to Read:** [DD001 — Extended Ion Channel Library](DD001_Neural_Circuit_Architecture.md#extended-ion-channel-library-phase-1-2) (EGL-19 row, HIGH priority) and [DD005 — Conductance Calibration](DD005_Cell_Type_Differentiation_Strategy.md)
- **Depends On:** Issue 1 (survey)
- **Existing Code to Reuse:**
    - [`NicolettiEtAl2019_NeuronModels/NeuroML2/AWCon_egl19.channel.nml`](https://github.com/openworm/NicolettiEtAl2019_NeuronModels) — **EGL-19 already exists in validated NeuroML2.** Part of the AWCon 16-channel model. Validated against XPP original.
    - [`NicolettiEtAl2024_MN_IN/NeuroML/egl19.channel.nml`](https://github.com/openworm/NicolettiEtAl2024_MN_IN) — Another NeuroML2 version (AIY subset conversion)
    - [`NicolettiEtAl2024_MN_IN/egl19.mod`](https://github.com/openworm/NicolettiEtAl2024_MN_IN) — NMODL reference
    - [`ChannelWorm2/NML2_models/EGL-19.channel.nml`](https://github.com/openworm/ChannelWorm2) — Older NeuroML2 version using Boyle & Cohen 2008 parameters (different from Nicoletti)
    - `ChannelWorm2/raw_data/JSON/` — Digitized experimental I-V curves for validation
- **Approach:** **Validate and adopt** the existing NicolettiEtAl2019 NeuroML2 channel. Reconcile parameters against the NicolettiEtAl2024 and ChannelWorm2 versions. Validate against experimental I-V data from ChannelWorm2. Do NOT convert from NMODL — the NeuroML2 already exists.
- **Files to Modify:**
    - `channel_models/egl19_cav1.channel.nml` (adopted from NicolettiEtAl2019, possibly reconciled)
    - `tests/test_egl19_channel.py` (new)
- **Test Commands:**
    - `jnml -validate channel_models/egl19_cav1.channel.nml`
    - `pytest tests/test_egl19_channel.py`
- **Acceptance Criteria:**
    - [ ] EGL-19 channel adopted from existing NicolettiEtAl2019 NeuroML2 — not reimplemented
    - [ ] Parameters reconciled against NicolettiEtAl2024 and ChannelWorm2 versions; discrepancies documented
    - [ ] Passes `jnml -validate`
    - [ ] I-V curve matches NMODL reference within ±5% (test with voltage clamp protocol)
    - [ ] Validated against ChannelWorm2 experimental I-V data where available
    - [ ] Activation and inactivation kinetics (V_half, slope, tau) documented with literature source
    - [ ] Can be inserted into a GenericCell definition alongside existing channels
    - [ ] Unit test compares NeuroML channel output against NMODL reference
- **Sponsor Summary Hint:** EGL-19 is the primary L-type calcium channel in *C. elegans* — and it already exists in NeuroML2 format from Nicoletti et al. 2019. This issue validates that existing model against experimental data and integrates it into c302's channel library. Adoption, not reinvention.

---

### Issue 3: Validate and adopt SLO-1 (BK Ca²⁺-activated K⁺) NeuroML2 channel into c302

- **Title:** `[DD005] Validate and adopt existing SLO-1 (BK Ca²⁺-activated K⁺) NeuroML2 channel into c302 channel library`
- **Labels:** `DD005`, `human-expert`, `L2`
- **Roadmap Phase:** Phase 1
- **Target Repo:** `openworm/c302`
- **Required Capabilities:** python, neuroml, electrophysiology
- **DD Section to Read:** [DD001 — Extended Ion Channel Library](DD001_Neural_Circuit_Architecture.md#extended-ion-channel-library-phase-1-2) (SLO-1 row, HIGH priority) and [DD005 — Conductance Calibration](DD005_Cell_Type_Differentiation_Strategy.md)
- **Depends On:** Issue 1 (survey)
- **Existing Code to Reuse:**
    - [`NicolettiEtAl2019_NeuronModels/NeuroML2/AWCon_slo1.channel.nml`](https://github.com/openworm/NicolettiEtAl2019_NeuronModels) — **SLO-1 already exists in validated NeuroML2.** Calcium-dependent gating modeled. Part of AWCon model.
    - [`NicolettiEtAl2024_MN_IN/slo1egl19.mod`, `slo1unc2.mod`, `slo1iso.mod`](https://github.com/openworm/NicolettiEtAl2024_MN_IN) — Three SLO-1 variants coupled to different calcium sources (EGL-19, UNC-2, isolated)
    - [`BAAIWorm/eworm/components/mechanism/modfile/slo1_egl19.mod`, `slo1_unc2.mod`](https://github.com/Jessie940611/BAAIWorm) — BAAIWorm NMODL versions
- **Approach:** **Validate and adopt** the existing NicolettiEtAl2019 NeuroML2 channel. Note that BAAIWorm and NicolettiEtAl2024 have calcium-source-specific variants (SLO-1 coupled to EGL-19 vs UNC-2) — determine if the c302 library needs separate variants or a unified model.
- **Files to Modify:**
    - `channel_models/slo1_bk.channel.nml` (adopted from NicolettiEtAl2019)
    - `tests/test_slo1_channel.py` (new)
- **Test Commands:**
    - `jnml -validate channel_models/slo1_bk.channel.nml`
    - `pytest tests/test_slo1_channel.py`
- **Acceptance Criteria:**
    - [ ] SLO-1 BK channel adopted from existing NicolettiEtAl2019 NeuroML2 — not reimplemented
    - [ ] Calcium-dependent gating correctly modeled (conductance depends on both V and [Ca²⁺]ᵢ)
    - [ ] Decision documented: single unified SLO-1 or separate EGL-19/UNC-2/iso variants per NicolettiEtAl2024
    - [ ] I-V curve matches NMODL reference within ±5%
    - [ ] Activation kinetics documented with literature source
    - [ ] Unit test compares NeuroML channel output against NMODL reference
- **Sponsor Summary Hint:** SLO-1 is a "big potassium" (BK) channel that opens when it senses both voltage AND calcium inside the cell. It already exists in NeuroML2 from Nicoletti et al. 2019. This issue validates and adopts it, with a decision on whether to carry the calcium-source-specific variants from the newer Nicoletti 2024 models.

---

### Issue 4: Validate and adopt KVS-1 and EGL-36 NeuroML2 channels into c302

- **Title:** `[DD005] Validate and adopt existing KVS-1 (Kv Shaker) and EGL-36 (ERG) NeuroML2 channels into c302 library`
- **Labels:** `DD005`, `human-expert`, `L2`
- **Roadmap Phase:** Phase 1
- **Target Repo:** `openworm/c302`
- **Required Capabilities:** python, neuroml, electrophysiology
- **DD Section to Read:** [DD001 — Extended Ion Channel Library](DD001_Neural_Circuit_Architecture.md#extended-ion-channel-library-phase-1-2) (KVS-1 and EGL-36 rows, HIGH priority) and [DD005 — Conductance Calibration](DD005_Cell_Type_Differentiation_Strategy.md)
- **Depends On:** Issue 1 (survey)
- **Existing Code to Reuse:**
    - [`NicolettiEtAl2019_NeuronModels/NeuroML2/AWCon_kvs1.channel.nml`](https://github.com/openworm/NicolettiEtAl2019_NeuronModels) — **KVS-1 already exists in validated NeuroML2** (AWCon model)
    - [`NicolettiEtAl2019_NeuronModels/NeuroML2/RMD_egl36.channel.nml`](https://github.com/openworm/NicolettiEtAl2019_NeuronModels) — **EGL-36 already exists in validated NeuroML2** (RMD model)
    - [`NicolettiEtAl2024_MN_IN/kvs1.mod`, `egl36.mod`](https://github.com/openworm/NicolettiEtAl2024_MN_IN) — NMODL references
    - `ChannelWorm2/raw_data/JSON/` — Experimental I-V data for KVS-1 and EGL-36
- **Approach:** **Validate and adopt** the existing NeuroML2 channels from NicolettiEtAl2019. Both channels already exist — reconcile and integrate.
- **Files to Modify:**
    - `channel_models/kvs1_shaker.channel.nml` (adopted)
    - `channel_models/egl36_erg.channel.nml` (adopted)
    - `tests/test_kvs1_channel.py` (new)
    - `tests/test_egl36_channel.py` (new)
- **Test Commands:**
    - `jnml -validate channel_models/kvs1_shaker.channel.nml`
    - `jnml -validate channel_models/egl36_erg.channel.nml`
    - `pytest tests/test_kvs1_channel.py tests/test_egl36_channel.py`
- **Acceptance Criteria:**
    - [ ] Both channels adopted from existing NicolettiEtAl2019 NeuroML2 — not reimplemented
    - [ ] KVS-1: Shaker-type voltage-gated K⁺ channel with fast activation kinetics
    - [ ] EGL-36: ERG-type K⁺ channel with characteristic slow inactivation recovery
    - [ ] I-V curves match NMODL references within ±5%
    - [ ] All kinetics documented with literature sources
    - [ ] Unit tests compare NeuroML outputs against NMODL references
- **Sponsor Summary Hint:** Both KVS-1 and EGL-36 already exist as validated NeuroML2 files from Nicoletti et al. 2019. This issue adopts them into c302's channel library with validation against experimental data and NMODL references.

---

### Issue 5: Adopt or convert remaining MEDIUM-priority channels into c302

- **Title:** `[DD005] Adopt existing NeuroML2 or convert NMODL for MEDIUM-priority channels (CCA-1, EGL-2, KQT-3, SLO-2, KCNL, IRK, NCA)`
- **Labels:** `DD005`, `ai-workable`, `L3`
- **Roadmap Phase:** Phase 1
- **Target Repo:** `openworm/c302`
- **Required Capabilities:** python, neuroml, electrophysiology
- **DD Section to Read:** [DD001 — Extended Ion Channel Library](DD001_Neural_Circuit_Architecture.md#extended-ion-channel-library-phase-1-2) (MEDIUM priority rows) and [DD005 — Conductance Calibration](DD005_Cell_Type_Differentiation_Strategy.md)
- **Depends On:** Issues 3-4 (HIGH priority channels establish the adoption/validation workflow)
- **Existing Code to Reuse:**
    - **Already in NeuroML2 (NicolettiEtAl2019):** CCA-1 (`AWCon_cca.channel.nml`), EGL-2 (`AWCon_egl2.channel.nml`), KQT-3 (`AWCon_kqt3.channel.nml`), SLO-2 (`AWCon_slo2.channel.nml`), SK/KCNL (`AWCon_sk.channel.nml`), IRK/KIR (`AWCon_kir.channel.nml`), NCA (`AWCon_nca.channel.nml`) — **ALL 7 channels already exist in validated NeuroML2**
    - **NMODL references (NicolettiEtAl2024):** `cca1.mod`, `egl2.mod`, `kqt3.mod`, `slo2egl19.mod`/`slo2unc2.mod`/`slo2iso.mod`, `kcnl.mod`, `irk.mod`, `nca.mod`
    - **ChannelWorm2:** `SLO-2.channel.nml` (older NeuroML2 with Boyle & Cohen parameters)
    - **BAAIWorm per-neuron conductances:** `eworm/components/param/cell/*.json` — max conductance values for every channel in every neuron (302 neurons × ~15 channels)
- **Approach:** **Adopt all 7 from NicolettiEtAl2019 NeuroML2** — they already exist and are validated. Reconcile with NicolettiEtAl2024 variants where parameters differ. This should be primarily validation and integration work, not conversion.
- **Files to Modify:**
    - `channel_models/cca1_cav3.channel.nml` (adopted)
    - `channel_models/egl2_eag.channel.nml` (adopted)
    - `channel_models/kqt3_kcnq.channel.nml` (adopted)
    - `channel_models/slo2_sk.channel.nml` (adopted)
    - `channel_models/kcnl2_sk.channel.nml` (adopted)
    - `channel_models/irk_kir.channel.nml` (adopted)
    - `channel_models/nca_na.channel.nml` (adopted)
    - `tests/test_medium_channels.py` (new)
- **Test Commands:**
    - `for f in channel_models/*.nml; do jnml -validate $f; done`
    - `pytest tests/test_medium_channels.py`
- **Acceptance Criteria:**
    - [ ] All 7 channels adopted from existing NicolettiEtAl2019 NeuroML2 — conversion from NMODL only if no NeuroML2 version exists after Issue 1 survey
    - [ ] Each passes `jnml -validate`
    - [ ] I-V curves match NMODL references within ±5%
    - [ ] Parameters reconciled against NicolettiEtAl2024 and ChannelWorm2 where applicable; discrepancies documented
    - [ ] All kinetics documented with literature sources
    - [ ] Total channel library: 4 existing + 4 HIGH + 7 MEDIUM = 15 channels
- **Sponsor Summary Hint:** Here's the plot twist: all 7 MEDIUM-priority channels already exist in NeuroML2 from Nicoletti et al. 2019's AWCon model. This issue validates and adopts them into c302's channel library — turning what looked like weeks of conversion work into a validation and integration task.

---

### Issue 6: Create channel library test suite with voltage-clamp protocols

- **Title:** `[DD005] Create comprehensive channel library test suite with standard voltage-clamp protocols`
- **Labels:** `DD005`, `ai-workable`, `L2`
- **Roadmap Phase:** Phase 1
- **Target Repo:** `openworm/c302`
- **Required Capabilities:** python, neuroml
- **DD Section to Read:** [DD001 — Extended Ion Channel Library](DD001_Neural_Circuit_Architecture.md#extended-ion-channel-library-phase-1-2) and [DD001 — Quality Criteria](DD001_Neural_Circuit_Architecture.md#quality-criteria) (criterion 3: biophysical units)
- **Depends On:** Issues 2-5 (channel adoptions)
- **Existing Code to Reuse:**
    - [`NicolettiEtAl2024_MN_IN/*_vclamp.py`](https://github.com/openworm/NicolettiEtAl2024_MN_IN) — Voltage-clamp simulation scripts already exist for VA5, VB6, VD5 neurons. Includes conductance unit conversion utilities (`g_to_Scm2.py`, `g_to_nS.py`).
    - [`BAAIWorm/eworm/ion_channel_tune/`](https://github.com/Jessie940611/BAAIWorm) — Channel validation scripts with result PNG plots for each channel against published I-V curves
    - [`ChannelWorm2/raw_data/JSON/`](https://github.com/openworm/ChannelWorm2) — **200+ digitized experimental I-V curves** across species — use C. elegans-specific data for validation targets
    - `c302/examples/parametersweep/` — Parameter sweep infrastructure with firing rate analysis and heatmap generation
- **Approach:** **Adapt existing voltage-clamp protocols** from NicolettiEtAl2024 and BAAIWorm validation scripts. Use ChannelWorm2's experimental I-V data as validation targets.
- **Files to Modify:**
    - `tests/test_channel_library.py` (new — adapted from existing vclamp scripts)
    - `tests/protocols/` (new — voltage clamp protocol files)
- **Test Commands:**
    - `pytest tests/test_channel_library.py -v`
- **Acceptance Criteria:**
    - [ ] Standard voltage-clamp protocol: step from -80mV to -60,-40,-20,0,+20,+40 mV
    - [ ] For each channel: measure peak current, steady-state current, activation time constant
    - [ ] Compare against published electrophysiology data where available (use ChannelWorm2 JSON data)
    - [ ] Generate I-V curve plots for each channel (saved as PNG test artifacts)
    - [ ] Verify units are correct (conductance in nS, voltage in mV, time in ms)
    - [ ] Detect common errors: reversed polarity, wrong magnitude, unrealistic kinetics
    - [ ] All 15 channels pass the test suite
- **Sponsor Summary Hint:** A voltage-clamp test suite built on existing validation scripts from Nicoletti et al. and BAAIWorm, plus 200+ digitized experimental I-V curves from ChannelWorm2 as ground truth. Calibrating 15 ion channels against their published spec sheets.

---

## Summary Statistics

| Category | Count |
|----------|-------|
| **Total Issues** | 6 |
| **ai-workable** | 3 |
| **human-expert** | 3 |
| **L1** | 2 |
| **L2** | 3 |
| **L3** | 1 |

| Group | Issues | Target |
|-------|--------|--------|
| **1: Ion Channel Library** | 1–6 | Survey + adopt/validate 14 channels from existing NeuroML2 and NMODL |

### Cross-References

| Related DD | Relationship |
|------------|-------------|
| **[DD001](DD001_draft_issues.md) (Neural Circuit)** | **Original source** — these issues were extracted from DD001 Draft Issues Group 3 |
| DD010 (Validation Framework) | Channel validation criteria |
| DD025 (Foundation Models) | Alternative kinetics prediction pathway |
| [DD027](DD027_draft_issues.md) (Multicompartmental) | Issues 1-2 depend on this channel library |

### Dependency Graph

```
Issue 1 (channel survey across ALL repos — reconciliation matrix)
  ├→ Issue 2 (adopt EGL-19 from NicolettiEtAl2019)   ─┐
  ├→ Issue 3 (adopt SLO-1 from NicolettiEtAl2019)     ├→ Issue 5 (adopt MEDIUM channels)
  └→ Issue 4 (adopt KVS-1, EGL-36)                    ─┘    └→ Issue 6 (channel test suite)
```
