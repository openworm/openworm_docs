# DD020 Draft GitHub Issues

**Epic:** DD020 — Connectome Data Access and Dataset Policy

**Generated from:** [DD020: Connectome Data Access and Dataset Policy](https://docs.openworm.org/design_documents/DD020_Connectome_Data_Access_and_Dataset_Policy/)

**Methodology:** [DD015 §2.2 — DD Issue Generator](https://docs.openworm.org/design_documents/DD015_AI_Contributor_Model/#22-the-dd-issue-generator-automated-issue-creation)

**Totals:** 23 issues (ai-workable: 18 / human-expert: 5 | L1: 10, L2: 10, L3: 3)

**Roadmap Context:** DD020 is a **Phase 0** DD (existing, working). Its draft issues span multiple roadmap phases:

| Group | Phase | Rationale |
|-------|-------|-----------|
| 1. Build Integration (Issues 1-5) | **Phase A** | Pin cect in DD013 Docker stack |
| 2. CI & Quality Gates (Issues 6-9) | **Phase A** | Automated regression detection |
| 3. Connectome Loaders (Issues 10-14) | **Phase 1+** | Built as consuming DDs are implemented |
| 4. API & Utilities (Issues 15-18) | **Phase 1+** | Bilateral symmetry, cell type classifier |
| 5. Documentation (Issues 19-21) | **Any** | Can be addressed independently |
| 6. Research (Issues 22-23) | **Phase 3+** | Developmental connectome, E/L classification |

---

## Group 1: Build Integration (Phase A)

Target: `cect` is pinned, configured, cached, and installable inside the DD013 Docker stack.

---

### Issue 1: Pin `cect==0.2.7` in `versions.lock`

- **Title:** `[DD020] Pin cect==0.2.7 in versions.lock`
- **Labels:** `DD020`, `ai-workable`, `L1`
- **Roadmap Phase:** Phase A
- **Target Repo:** `openworm/OpenWorm`
- **Required Capabilities:** yaml
- **DD Section to Read:** [DD020 — Version Pinning & Update Procedure](https://docs.openworm.org/design_documents/DD020_Connectome_Data_Access_and_Dataset_Policy/#version-pinning-update-procedure) and [DD013 §4 — Dependency Pinning](https://docs.openworm.org/design_documents/DD013_Simulation_Stack_Architecture/#4-dependency-pinning-versionslock)
- **Depends On:** DD013 Issue 7 (versions.lock file)
- **Files to Modify:**
    - `versions.lock` (add `cect` entry)
- **Test Commands:**
    - `python3 -c "import yaml; d = yaml.safe_load(open('versions.lock')); assert d['cect'] == '0.2.7'"`
- **Acceptance Criteria:**
    - [ ] `versions.lock` contains `cect: "0.2.7"` entry
    - [ ] Entry includes repo URL: `https://github.com/openworm/ConnectomeToolbox`
    - [ ] Entry includes current commit hash from ConnectomeToolbox main branch
    - [ ] Comment references DD020 as the policy owner
    - [ ] Valid YAML after edit
- **Sponsor Summary Hint:** Version pinning ensures every contributor gets the exact same connectome data. Without it, one person might install cect 0.2.5 (missing bilateral symmetry) while another gets 0.3.0 (potentially changed connection counts). Like pinning a reagent lot number in a lab protocol — reproducible science requires reproducible dependencies.

---

### Issue 2: Add `data.connectome` section to `openworm.yml`

- **Title:** `[DD020] Add data.connectome configuration section to openworm.yml`
- **Labels:** `DD020`, `ai-workable`, `L1`
- **Roadmap Phase:** Phase A
- **Target Repo:** `openworm/OpenWorm`
- **Required Capabilities:** yaml
- **DD Section to Read:** [DD020 — Configuration](https://docs.openworm.org/design_documents/DD020_Connectome_Data_Access_and_Dataset_Policy/#configuration) (openworm.yml section)
- **Depends On:** DD013 Issue 1 (openworm.yml config schema)
- **Files to Modify:**
    - `openworm.yml` (add `data.connectome` section)
    - `configs/validation_full.yml` (add connectome cross-validation settings)
- **Test Commands:**
    - `python3 -c "import yaml; d = yaml.safe_load(open('openworm.yml')); print(d['data']['connectome']['dataset'])"`
- **Acceptance Criteria:**
    - [ ] `data.connectome.dataset` defaults to `"Cook2019Herm"`
    - [ ] `data.connectome.cect_version` set to `"0.2.7"`
    - [ ] `data.connectome.use_cache` defaults to `true`
    - [ ] All 10 config keys from DD020 Configuration table present with correct defaults
    - [ ] `pharyngeal_dataset`, `functional_dataset`, `neuropeptide_dataset`, `neurotransmitter_dataset`, `cross_validation_dataset` keys included
    - [ ] Each key has an inline comment referencing the consuming DD
    - [ ] `validation_full.yml` enables cross-validation dataset
    - [ ] Valid YAML after edit
- **Sponsor Summary Hint:** This config section is the "dataset control panel" for the connectome. It specifies which wiring diagram the simulation uses (default: Cook 2019 adult hermaphrodite), which neuropeptide network to load (Ripoll-Sanchez), which functional data for validation (Randi 2023), and what version of cect to use. One place to control all connectome data access across 9 consuming Design Documents.

---

### Issue 3: Write connectome config validation logic

- **Title:** `[DD020] Add connectome config validation to validate_config.py`
- **Labels:** `DD020`, `ai-workable`, `L1`
- **Roadmap Phase:** Phase A
- **Target Repo:** `openworm/OpenWorm`
- **Required Capabilities:** python
- **DD Section to Read:** [DD020 — Configuration](https://docs.openworm.org/design_documents/DD020_Connectome_Data_Access_and_Dataset_Policy/#configuration) (config keys table) and [DD020 — Quality Criteria](https://docs.openworm.org/design_documents/DD020_Connectome_Data_Access_and_Dataset_Policy/#quality-criteria)
- **Depends On:** Issue 2, DD013 Issue 2 (validate_config.py)
- **Files to Modify:**
    - `scripts/validate_config.py` (add connectome validation rules)
    - `tests/test_config.py` (add connectome validation tests)
- **Test Commands:**
    - `python3 scripts/validate_config.py openworm.yml`
    - `pytest tests/test_config.py -k connectome`
- **Acceptance Criteria:**
    - [ ] Validates `data.connectome.dataset` is a known cect reader name
    - [ ] Validates `data.connectome.cect_version` matches `versions.lock` entry
    - [ ] Validates `use_cache` is boolean
    - [ ] Warns if `developmental_dataset` is set (non-standard usage)
    - [ ] Validates that reader names correspond to importable cect modules (e.g., `"Cook2019Herm"` → `cect.Cook2019HermReader`)
    - [ ] Cross-validates: if `neural.neuropeptides: true` (DD006), then `neuropeptide_dataset` must be set
    - [ ] Unit tests cover: valid config passes, unknown reader name fails, version mismatch warns
    - [ ] Returns exit code 0 on valid, non-zero on invalid
- **Sponsor Summary Hint:** A guardrail that catches connectome config mistakes before the simulation runs. Typo in the dataset name? Wrong cect version? Neuropeptide mode enabled but no neuropeptide dataset specified? This script catches all of that upfront instead of failing 10 minutes into a simulation.

---

### Issue 4: Add `cect` to Docker neural stage

- **Title:** `[DD020] Install cect at pinned version in Docker neural stage`
- **Labels:** `DD020`, `ai-workable`, `L1`
- **Roadmap Phase:** Phase A
- **Target Repo:** `openworm/OpenWorm`
- **Required Capabilities:** docker
- **DD Section to Read:** [DD020 — Repository & Packaging](https://docs.openworm.org/design_documents/DD020_Connectome_Data_Access_and_Dataset_Policy/#repository-packaging) (Docker stage, build dependencies)
- **Depends On:** Issue 1, DD013 Issue 3 (multi-stage Dockerfile)
- **Files to Modify:**
    - `Dockerfile` (neural stage — add `pip install cect==$CECT_VERSION`)
    - `build.sh` (pass `--build-arg CECT_VERSION` from versions.lock)
- **Test Commands:**
    - `docker build --target neural .`
    - `docker run openworm/neural python3 -c "import cect; print(cect.__version__)"`
- **Acceptance Criteria:**
    - [ ] `pip install cect==$CECT_VERSION` in neural Docker stage
    - [ ] `CECT_VERSION` build arg read from `versions.lock` by `build.sh`
    - [ ] `cect` and its dependencies (numpy, xlrd, openpyxl, networkx, wormneuroatlas) installed
    - [ ] `import cect` succeeds inside container
    - [ ] `cect.__version__` matches pinned version
    - [ ] Cached JSON data files present in container (~5MB)
- **Sponsor Summary Hint:** The neural Docker stage is where c302 generates the worm's nervous system from connectome data. Installing cect here means the wiring diagram is available at the moment the neural circuit is built — like putting the blueprint in the workshop before construction starts.

---

### Issue 5: Pre-cache cect dataset JSON in Docker image

- **Title:** `[DD020] Pre-generate and cache cect dataset JSON files in Docker image`
- **Labels:** `DD020`, `ai-workable`, `L2`
- **Roadmap Phase:** Phase A
- **Target Repo:** `openworm/OpenWorm`
- **Required Capabilities:** python, docker
- **DD Section to Read:** [DD020 — Dataset Selection Rules](https://docs.openworm.org/design_documents/DD020_Connectome_Data_Access_and_Dataset_Policy/#dataset-selection-rules) (rule 4: `from_cache=True` in CI) and [DD020 — Quality Criteria](https://docs.openworm.org/design_documents/DD020_Connectome_Data_Access_and_Dataset_Policy/#quality-criteria) (criterion 6)
- **Depends On:** Issue 4
- **Files to Modify:**
    - `Dockerfile` (neural stage — add cache generation step)
    - `scripts/precache_cect.py` (new — generates cached JSON files)
- **Test Commands:**
    - `docker build --target neural .`
    - `docker run openworm/neural python3 -c "from cect.Cook2019HermReader import get_instance; cds = get_instance(from_cache=True); print(len(cds.nodes))"`
- **Acceptance Criteria:**
    - [ ] `scripts/precache_cect.py` calls `get_instance()` (without cache) for the default dataset and stores JSON
    - [ ] Also caches: Cook2019Herm, Randi2023 (functional), RipollSanchezShortRange (neuropeptide), Witvliet8 (cross-validation)
    - [ ] Cached JSON files embedded in Docker image at build time
    - [ ] `from_cache=True` calls succeed inside container without network access
    - [ ] Cache adds <10MB to Docker image size
    - [ ] Cache files deterministic: same input → same JSON bytes
- **Sponsor Summary Hint:** The cect package can load datasets from cached JSON files instead of parsing Excel/CSV every time. Pre-caching in the Docker image means: (1) no network access needed during CI or simulation, (2) faster startup (~100ms vs ~3s), and (3) bit-identical data across all runs — critical for reproducible science. Like pre-loading reagents into a lab kit.

---

## Group 2: CI & Quality Gates (Phase A)

Target: Every PR is automatically checked for correct connectome data access.

---

### Issue 6: Create CI gate for cect version and dataset load

- **Title:** `[DD020] Create CI gate: verify cect version and default dataset load`
- **Labels:** `DD020`, `ai-workable`, `L1`
- **Roadmap Phase:** Phase A
- **Target Repo:** `openworm/OpenWorm`
- **Required Capabilities:** ci-cd, python
- **DD Section to Read:** [DD020 — How to Test](https://docs.openworm.org/design_documents/DD020_Connectome_Data_Access_and_Dataset_Policy/#how-to-test-contributor-workflow) (quick test and full validation scripts)
- **Depends On:** Issue 4, DD013 Issue 13 (CI Gate 1)
- **Files to Modify:**
    - `scripts/test_connectome.py` (new — DD020 CI test)
    - `.github/workflows/integration.yml` (add connectome test step)
- **Test Commands:**
    - `python3 scripts/test_connectome.py`
    - Push to branch and verify CI runs connectome test
- **Acceptance Criteria:**
    - [ ] Verifies `cect.__version__` matches `versions.lock`
    - [ ] Loads Cook2019Herm from cache, verifies ≥300 nodes
    - [ ] Verifies `original_connection_infos` is non-empty
    - [ ] Verifies cell classification: `get_SIM_class('AVAL') == 'Interneuron'`
    - [ ] Verifies bilateral symmetry function returns valid percentage
    - [ ] CI step added after Docker build, before smoke test
    - [ ] Script prints `[DD020] connectome test: PASS` on success
    - [ ] Script returns exit code 0 on pass, non-zero on fail
    - [ ] Total test time <30 seconds
- **Sponsor Summary Hint:** The automatic checkpoint that runs on every PR. Does the connectome package load? Is it the right version? Can it return the worm's wiring diagram? If any of these fail, the PR is blocked before a human even looks at it. Catches version drift and broken installs instantly.

---

### Issue 7: Audit consuming DDs for raw file parsing

- **Title:** `[DD020] Audit all 9 consuming DDs for raw connectome file parsing`
- **Labels:** `DD020`, `ai-workable`, `L1`
- **Roadmap Phase:** Phase A
- **Target Repo:** `openworm/OpenWorm`
- **Required Capabilities:** python, git
- **DD Section to Read:** [DD020 — Quality Criteria](https://docs.openworm.org/design_documents/DD020_Connectome_Data_Access_and_Dataset_Policy/#quality-criteria) (criterion 1: API-only access) and [DD020 — Goal & Success Criteria](https://docs.openworm.org/design_documents/DD020_Connectome_Data_Access_and_Dataset_Policy/#goal-success-criteria)
- **Depends On:** None
- **Files to Modify:**
    - None (research issue — output is a summary posted on the issue)
- **Test Commands:**
    - N/A (audit task)
- **Acceptance Criteria:**
    - [ ] Search `openworm/c302` for direct CSV/Excel connectome file parsing (grep for `pandas.read_csv`, `xlrd`, `openpyxl`, hardcoded neuron lists)
    - [ ] Search `openworm/Sibernetic` for any connectome data loading outside `cect`
    - [ ] Search `openworm/owmeta` for connectome ingestion that bypasses `cect`
    - [ ] Check all 9 consuming DD repos for compliance with DD020 API-only access rule
    - [ ] Document each finding: file path, line number, what it does, whether it should use `cect` instead
    - [ ] Categorize: already compliant / needs refactoring / n/a
    - [ ] File follow-up issues for repos that need refactoring
    - [ ] Post findings as issue comment with a compliance table
- **Sponsor Summary Hint:** DD020's primary goal is "all consuming DDs obtain connectome data via cect API, not raw file parsing." But does the code actually do this today? This audit checks all 9 repos to find any places where connectome data is loaded from raw CSV/Excel files instead of through cect. Like a lab safety audit — find the violations before they cause problems.

---

### Issue 8: Create connectome API compliance checker script

- **Title:** `[DD020] Create connectome API compliance checker for CI`
- **Labels:** `DD020`, `ai-workable`, `L2`
- **Roadmap Phase:** Phase A
- **Target Repo:** `openworm/OpenWorm`
- **Required Capabilities:** python
- **DD Section to Read:** [DD020 — Quality Criteria](https://docs.openworm.org/design_documents/DD020_Connectome_Data_Access_and_Dataset_Policy/#quality-criteria) (all 6 criteria) and [DD020 — API Contract for Consumers](https://docs.openworm.org/design_documents/DD020_Connectome_Data_Access_and_Dataset_Policy/#api-contract-for-consumers)
- **Depends On:** Issue 7 (audit findings)
- **Files to Modify:**
    - `scripts/check_connectome_compliance.py` (new)
    - `tests/test_connectome_compliance.py` (new)
- **Test Commands:**
    - `python3 scripts/check_connectome_compliance.py --repo openworm/c302`
    - `pytest tests/test_connectome_compliance.py`
- **Acceptance Criteria:**
    - [ ] Scans Python files for connectome data access patterns
    - [ ] Flags: raw CSV/Excel parsing of connectome data (criterion 1)
    - [ ] Flags: unnamed/implicit dataset usage — imports without explicit reader name (criterion 2)
    - [ ] Flags: hardcoded cect version not matching versions.lock (criterion 3)
    - [ ] Flags: custom cell name normalization (criterion 4)
    - [ ] Reports compliance percentage per repo
    - [ ] Prints PASS if all checks pass, FAIL with details if not
    - [ ] Unit tests with synthetic code samples (compliant and non-compliant)
    - [ ] Can be run as CI step on consuming repos
- **Sponsor Summary Hint:** An automated linter for connectome data access patterns. Scans Python code in any repo and flags violations of DD020's quality criteria — like using raw file parsing instead of cect, or importing unnamed datasets. Think of it as a spell-checker for connectome API usage. Prevents drift back to ad hoc data loading.

---

### Issue 9: Create cect version update procedure script

- **Title:** `[DD020] Create cect version update and regression test script`
- **Labels:** `DD020`, `ai-workable`, `L2`
- **Roadmap Phase:** Phase A
- **Target Repo:** `openworm/OpenWorm`
- **Required Capabilities:** python
- **DD Section to Read:** [DD020 — Update Procedure](https://docs.openworm.org/design_documents/DD020_Connectome_Data_Access_and_Dataset_Policy/#update-procedure) (6-step process)
- **Depends On:** Issue 6 (CI test)
- **Files to Modify:**
    - `scripts/update_cect_version.py` (new)
- **Test Commands:**
    - `python3 scripts/update_cect_version.py --new-version 0.2.8 --dry-run`
- **Acceptance Criteria:**
    - [ ] Accepts `--new-version X.Y.Z` argument
    - [ ] Installs new cect version in temporary virtualenv
    - [ ] Loads default dataset with new version and compares neuron count, connection count, and adjacency matrix against current version
    - [ ] Reports: any new/removed neurons, changed connection counts, new/removed readers
    - [ ] `--dry-run` mode prints comparison report without modifying any files
    - [ ] `--apply` mode updates `versions.lock` and `openworm.yml` cect_version
    - [ ] If neuron count or connection count changes, prints warning: "SIMULATION-AFFECTING CHANGE — requires full DD010 revalidation"
    - [ ] Regenerates cect cache files if `--apply` used
- **Sponsor Summary Hint:** When cect releases a new version, we need to check if anything changed that would affect the simulation. Did a connection count change? Did a new neuron appear? This script automates the 6-step update procedure from DD020, comparing old vs. new versions side-by-side and flagging any simulation-affecting changes. Like a diff tool for biological wiring diagrams.

---

## Group 3: Consumer DD Integration (Phase 1+)

Target: Canonical data loaders exist for each consuming DD's connectome access pattern.

---

### Issue 10: Create canonical connectome loader for c302 (DD001)

- **Title:** `[DD020] Create canonical connectome loader for c302 using DD020 API patterns`
- **Labels:** `DD020`, `DD001`, `ai-workable`, `L2`
- **Roadmap Phase:** Phase 1+
- **Target Repo:** `openworm/c302`
- **Required Capabilities:** python, neuroml
- **DD Section to Read:** [DD020 — Canonical Query Patterns](https://docs.openworm.org/design_documents/DD020_Connectome_Data_Access_and_Dataset_Policy/#canonical-query-patterns) (Patterns 1, 2, 5, 6) and [DD001 Integration Contract](https://docs.openworm.org/design_documents/DD001_Neural_Circuit_Architecture/)
- **Depends On:** Issue 4 (cect in Docker)
- **Files to Modify:**
    - `c302/connectome_loader.py` (new — canonical loader wrapping cect)
    - `c302/CElegans.py` (refactor to use connectome_loader)
    - `tests/test_connectome_loader.py` (new)
- **Test Commands:**
    - `python3 -c "from c302.connectome_loader import load_connectome; cds = load_connectome('Cook2019Herm'); print(len(cds.nodes))"`
    - `pytest tests/test_connectome_loader.py`
- **Acceptance Criteria:**
    - [ ] `connectome_loader.py` provides `load_connectome(dataset_name, from_cache=True)` function
    - [ ] Wraps cect reader import + `get_instance()` call
    - [ ] Used by `CElegans.py` for network generation (replaces any direct file parsing)
    - [ ] Logs which dataset and cect version are being used
    - [ ] Raises clear error if dataset name is invalid or cect not installed
    - [ ] Unit tests verify: loads Cook2019Herm, returns expected neuron count, works with cache
    - [ ] Existing c302 network generation produces identical results after refactor
- **Sponsor Summary Hint:** c302 is where the connectome becomes a neural circuit — it reads the wiring diagram and generates a runnable NeuroML network. This creates a clean, testable loader function that follows DD020's API patterns, replacing whatever ad hoc data loading currently exists. The single funnel through which all connectome data enters the neural circuit model.

---

### Issue 11: Create neuron-to-muscle loader for DD002

- **Title:** `[DD020] Create neuron-to-muscle connection loader for DD002 muscle model`
- **Labels:** `DD020`, `DD002`, `ai-workable`, `L2`
- **Roadmap Phase:** Phase 1+
- **Target Repo:** `openworm/c302`
- **Required Capabilities:** python
- **DD Section to Read:** [DD020 — Canonical Query Patterns](https://docs.openworm.org/design_documents/DD020_Connectome_Data_Access_and_Dataset_Policy/#canonical-query-patterns) (Pattern 3: neuron-to-muscle) and [DD002 Integration Contract](https://docs.openworm.org/design_documents/DD002_Muscle_Model_Architecture/)
- **Depends On:** Issue 10 (connectome loader)
- **Files to Modify:**
    - `c302/connectome_loader.py` (add `load_neuron_to_muscle_conns()` function)
    - `tests/test_connectome_loader.py` (add NMJ tests)
- **Test Commands:**
    - `python3 -c "from c302.connectome_loader import load_neuron_to_muscle_conns; conns = load_neuron_to_muscle_conns(); print(f'{len(conns)} NMJ connections')"`
    - `pytest tests/test_connectome_loader.py -k muscle`
- **Acceptance Criteria:**
    - [ ] `load_neuron_to_muscle_conns(dataset_name)` returns list of `ConnectionInfo` for neuron→muscle connections
    - [ ] Uses `cds.get_neuron_to_muscle_conns()` from cect
    - [ ] Maps motor neuron names to Sibernetic muscle unit indices (references DD003 muscle mapping)
    - [ ] Returns connections for all 95 body-wall muscles + pharyngeal muscles
    - [ ] Unit tests verify: expected number of NMJ connections, known motor neuron→muscle pairs present
    - [ ] Used by sibernetic_c302.py coupling code
- **Sponsor Summary Hint:** The neuromuscular junction (NMJ) is where neural signals become physical movement — motor neurons connect to muscles, and those connections determine which muscles contract. This loader provides the exact wiring from the connectome: which motor neuron drives which muscle, and how strongly. The bridge between DD001 (neural circuit) and DD002 (muscle model).

---

### Issue 12: Create pharyngeal connectome loader for DD007

- **Title:** `[DD020] Create pharyngeal connectome view loader for DD007`
- **Labels:** `DD020`, `DD007`, `ai-workable`, `L1`
- **Roadmap Phase:** Phase 1+
- **Target Repo:** `openworm/c302`
- **Required Capabilities:** python
- **DD Section to Read:** [DD020 — Canonical Query Patterns](https://docs.openworm.org/design_documents/DD020_Connectome_Data_Access_and_Dataset_Policy/#canonical-query-patterns) (Pattern 4: pharyngeal view) and [DD007 Integration Contract](https://docs.openworm.org/design_documents/DD007_Pharyngeal_System_Architecture/)
- **Depends On:** Issue 10 (connectome loader)
- **Files to Modify:**
    - `c302/connectome_loader.py` (add `load_pharyngeal_connectome()` function)
    - `tests/test_connectome_loader.py` (add pharynx tests)
- **Test Commands:**
    - `python3 -c "from c302.connectome_loader import load_pharyngeal_connectome; pcds = load_pharyngeal_connectome(); print(f'{len(pcds.nodes)} pharyngeal neurons')"`
    - `pytest tests/test_connectome_loader.py -k pharynx`
- **Acceptance Criteria:**
    - [ ] `load_pharyngeal_connectome(dataset_name)` returns filtered `ConnectomeDataset` using `cds.get_connectome_view("Pharynx")`
    - [ ] Returns only pharyngeal neurons (20 neurons: I1-I6, M1-M5, MI, MCL/MCR, NSML/NSMR, etc.)
    - [ ] Includes pharyngeal muscles (pm1-pm8)
    - [ ] Config reads `data.connectome.pharyngeal_dataset` and `pharyngeal_view` from openworm.yml
    - [ ] Unit tests verify: ~20 neurons returned, known pharyngeal neuron M3L present, no somatic neurons included
- **Sponsor Summary Hint:** The pharynx has its own mini nervous system (20 neurons) that pumps bacteria into the worm's gut at ~3.5 Hz. It's semi-independent from the somatic nervous system. This loader extracts just the pharyngeal subset from the full 302-neuron connectome using cect's view filter — like looking at one department's org chart instead of the whole company's.

---

### Issue 13: Create neuropeptide and neurotransmitter loaders for DD006

- **Title:** `[DD020] Create neuropeptide network and neurotransmitter identity loaders for DD006`
- **Labels:** `DD020`, `DD006`, `ai-workable`, `L2`
- **Roadmap Phase:** Phase 1+
- **Target Repo:** `openworm/c302`
- **Required Capabilities:** python
- **DD Section to Read:** [DD020 — Canonical Query Patterns](https://docs.openworm.org/design_documents/DD020_Connectome_Data_Access_and_Dataset_Policy/#canonical-query-patterns) (Patterns 8 and 9) and [DD006 Integration Contract](https://docs.openworm.org/design_documents/DD006_Neuropeptidergic_Connectome_Integration/)
- **Depends On:** Issue 10 (connectome loader)
- **Files to Modify:**
    - `c302/connectome_loader.py` (add `load_neuropeptide_network()` and `load_neurotransmitter_identity()`)
    - `tests/test_connectome_loader.py` (add neuropeptide and neurotransmitter tests)
- **Test Commands:**
    - `python3 -c "from c302.connectome_loader import load_neuropeptide_network; rs = load_neuropeptide_network(); print(f'{len(rs.nodes)} peptidergic nodes')"`
    - `pytest tests/test_connectome_loader.py -k neuropeptide`
- **Acceptance Criteria:**
    - [ ] `load_neuropeptide_network(range_type)` loads Ripoll-Sanchez data via cect: short-range, mid-range, or long-range reader
    - [ ] Config reads `data.connectome.neuropeptide_dataset` from openworm.yml
    - [ ] `load_neurotransmitter_identity()` loads Wang2024 data via cect
    - [ ] Config reads `data.connectome.neurotransmitter_dataset` from openworm.yml
    - [ ] Returns `ConnectomeDataset` objects with peptide-receptor interaction data
    - [ ] Unit tests verify: expected node count for Ripoll-Sanchez data, known neuropeptide constants importable
    - [ ] Wang2024 reader returns 16 neurotransmitter systems
- **Sponsor Summary Hint:** Beyond fast electrical synapses, worm neurons communicate via 31,479 neuropeptide-receptor interactions (Ripoll-Sanchez 2023) and 16 neurotransmitter systems (Wang 2024). These loaders provide DD006 with clean access to both datasets through cect — the peptide signaling layer that modulates behavior over slower timescales and the neurotransmitter identity atlas that tells us what each synapse "says."

---

## Group 4: Multi-Dataset Validation (Phase 1+)

Target: Infrastructure for comparing simulations across multiple connectome datasets.

---

### Issue 14: Implement cross-dataset validation script

- **Title:** `[DD020] Implement cross-dataset validation: Cook2019 vs Witvliet8 comparison`
- **Labels:** `DD020`, `DD010`, `ai-workable`, `L2`
- **Roadmap Phase:** Phase 1+
- **Target Repo:** `openworm/OpenWorm`
- **Required Capabilities:** python
- **DD Section to Read:** [DD020 — Multi-Dataset Validation](https://docs.openworm.org/design_documents/DD020_Connectome_Data_Access_and_Dataset_Policy/#multi-dataset-validation) (validation protocol table)
- **Depends On:** Issue 5 (cached datasets)
- **Files to Modify:**
    - `scripts/cross_validate_connectome.py` (new)
    - `tests/test_cross_validate.py` (new)
- **Test Commands:**
    - `python3 scripts/cross_validate_connectome.py --primary Cook2019Herm --secondary Witvliet8`
    - `pytest tests/test_cross_validate.py`
- **Acceptance Criteria:**
    - [ ] Loads two datasets via cect and compares: neuron overlap, connection count delta, topology similarity
    - [ ] Reports: neurons present in both, neurons only in primary, neurons only in secondary
    - [ ] Reports: per-neuron-pair connection count differences
    - [ ] Computes graph-level metrics: degree distribution similarity, clustering coefficient comparison
    - [ ] Generates markdown comparison table suitable for pasting into issues
    - [ ] `--json` flag outputs structured JSON for programmatic use
    - [ ] Unit tests verify: comparing identical datasets produces zero delta
    - [ ] Documents expected discrepancy ranges (biological variability, not bugs)
- **Sponsor Summary Hint:** Different labs reconstructing different worms will find slightly different wiring. Cook 2019 and Witvliet 2021 (adult stage 8) are both adult hermaphrodite connectomes but report different connection counts for some neuron pairs. This script quantifies those differences — which connections are consistent (robust biology) and which differ (noise or biological variability). Essential for knowing how much to trust any single connectome dataset.

---

### Issue 15: Implement bilateral symmetry validation metric

- **Title:** `[DD020] Implement bilateral symmetry as a connectome quality and simulation validation metric`
- **Labels:** `DD020`, `DD010`, `ai-workable`, `L2`
- **Roadmap Phase:** Phase 1+
- **Target Repo:** `openworm/OpenWorm`
- **Required Capabilities:** python
- **DD Section to Read:** [DD020 — Bilateral Symmetry as a Validation Metric](https://docs.openworm.org/design_documents/DD020_Connectome_Data_Access_and_Dataset_Policy/#bilateral-symmetry-as-a-validation-metric)
- **Depends On:** Issue 5 (cached datasets)
- **Files to Modify:**
    - `scripts/validate_symmetry.py` (new)
    - `tests/test_validate_symmetry.py` (new)
- **Test Commands:**
    - `python3 scripts/validate_symmetry.py --dataset Cook2019Herm`
    - `python3 scripts/validate_symmetry.py --all-datasets`
    - `pytest tests/test_validate_symmetry.py`
- **Acceptance Criteria:**
    - [ ] Uses `cect.Analysis.convert_to_symmetry_array()` to compute bilateral symmetry for any dataset
    - [ ] Reports symmetry percentage per synapse class (chemical, electrical, neuropeptidergic)
    - [ ] `--all-datasets` mode compares symmetry across Cook2019, Witvliet stages, Varshney
    - [ ] Generates comparison table: dataset × synapse class → symmetry percentage
    - [ ] Flags datasets with <40% bilateral symmetry for chemical synapses (below biological expectation)
    - [ ] `--json` flag for CI integration
    - [ ] Unit tests verify: symmetry is in valid range (0-100%), known bilateral pairs (AVAL/AVAR) are detected
- **Sponsor Summary Hint:** The worm is largely bilaterally symmetric — left neurons mirror right neurons. If the simulation produces wildly asymmetric behavior (always turns left), this metric helps diagnose whether the problem is the connectome data or the model. Computing symmetry across all datasets also reveals which datasets are most/least symmetric — a quality indicator for the underlying EM reconstruction.

---

### Issue 16: Create dataset sensitivity analysis tool

- **Title:** `[DD020] Create dataset sensitivity analysis: which connections matter most for behavior?`
- **Labels:** `DD020`, `DD010`, `human-expert`, `L3`
- **Roadmap Phase:** Phase 1+
- **Target Repo:** `openworm/OpenWorm`
- **Required Capabilities:** python, neuroml, physics
- **DD Section to Read:** [DD020 — Multi-Dataset Validation](https://docs.openworm.org/design_documents/DD020_Connectome_Data_Access_and_Dataset_Policy/#multi-dataset-validation) (sensitivity analysis row)
- **Depends On:** Issue 14 (cross-validation script), DD013 Issue 11 (coupled sim loop)
- **Files to Modify:**
    - `scripts/connectome_sensitivity.py` (new)
- **Test Commands:**
    - `python3 scripts/connectome_sensitivity.py --perturbation remove_one --output sensitivity_report.json`
- **Acceptance Criteria:**
    - [ ] Implements "leave-one-connection-out" analysis: removes each connection individually and measures behavioral impact
    - [ ] Behavioral impact measured by: change in locomotion speed, wavelength, amplitude (DD010 Tier 3 metrics)
    - [ ] Ranks connections by impact: most critical connections that most affect behavior
    - [ ] Compares critical connection sets between Cook2019 and Witvliet8
    - [ ] Identifies connections present in both datasets that are always high-impact (robust functional predictions)
    - [ ] Generates ranked table: connection → behavioral impact score
    - [ ] Identifies connections that differ between datasets AND have high behavioral impact (uncertainty risk)
    - [ ] Output as JSON + markdown summary
- **Sponsor Summary Hint:** Not all 7,000 synaptic connections matter equally for behavior. Some are critical (remove them and the worm can't crawl), others are redundant. This analysis finds the VIP connections — the ones that most affect locomotion. Crucially, it compares this ranking across datasets: if a high-impact connection differs between Cook and Witvliet, that's a red flag for simulation reliability. This is how we identify where connectome uncertainty matters most.

---

### Issue 17: Create multi-dataset regression test suite

- **Title:** `[DD020] Create multi-dataset regression test suite for cect version updates`
- **Labels:** `DD020`, `ai-workable`, `L2`
- **Roadmap Phase:** Phase 1+
- **Target Repo:** `openworm/ConnectomeToolbox`
- **Required Capabilities:** python, testing
- **DD Section to Read:** [DD020 — Update Procedure](https://docs.openworm.org/design_documents/DD020_Connectome_Data_Access_and_Dataset_Policy/#update-procedure) (breaking change policy) and [DD020 — Quality Criteria](https://docs.openworm.org/design_documents/DD020_Connectome_Data_Access_and_Dataset_Policy/#quality-criteria)
- **Depends On:** Issue 5 (cached datasets)
- **Files to Modify:**
    - `tests/test_dataset_regression.py` (new — in ConnectomeToolbox repo)
    - `tests/baseline/` (new — baseline metric files per dataset)
- **Test Commands:**
    - `pytest tests/test_dataset_regression.py -v`
- **Acceptance Criteria:**
    - [ ] Baseline metrics captured for: Cook2019Herm, Cook2019Male, Witvliet8, RipollSanchezShortRange, Wang2024Herm
    - [ ] Each baseline records: node count, connection count, unique synclasses, top-10 highest-degree neurons
    - [ ] Test loads each dataset and compares against baseline
    - [ ] Fails if node count changes, connection count changes by >1%, or top-10 degree ranking changes
    - [ ] `--update-baseline` flag regenerates baseline files from current cect version
    - [ ] Baseline files committed to repo (small JSON)
    - [ ] Runs in <60 seconds total
- **Sponsor Summary Hint:** When cect releases a new version, these regression tests immediately tell us if any dataset's contents changed. Did a neuron disappear? Did a connection count change? Did the most-connected neurons shuffle? Catches silent data changes that would propagate into the simulation as mysterious behavioral shifts. The biological equivalent of a checksum.

---

## Group 5: Documentation & Notebooks (Any)

Target: New contributors can explore connectome data interactively and understand DD020's API patterns.

---

### Issue 18: Create connectome data exploration notebook

- **Title:** `[DD020] Create notebook: connectome data exploration with cect`
- **Labels:** `DD020`, `ai-workable`, `L1`
- **Roadmap Phase:** Any
- **Target Repo:** `openworm/OpenWorm`
- **Required Capabilities:** python, jupyter
- **DD Section to Read:** [DD020 — How to Visualize](https://docs.openworm.org/design_documents/DD020_Connectome_Data_Access_and_Dataset_Policy/#how-to-visualize) and [DD020 — Canonical Query Patterns](https://docs.openworm.org/design_documents/DD020_Connectome_Data_Access_and_Dataset_Policy/#canonical-query-patterns) (all 9 patterns)
- **Depends On:** DD013 Issue 23 (JupyterLab service)
- **Files to Modify:**
    - `notebooks/05_explore_connectome_datasets.ipynb` (new)
- **Test Commands:**
    - `jupyter nbconvert --execute notebooks/05_explore_connectome_datasets.ipynb`
- **Acceptance Criteria:**
    - [ ] Loads Cook2019Herm via cect and displays summary statistics (neuron count, connection count, synapse types)
    - [ ] Demonstrates all 9 canonical query patterns from DD020
    - [ ] Visualizes connectivity matrix using `cds.to_plotly_matrix_fig()`
    - [ ] Visualizes network graph using `cds.to_plotly_graph_fig()`
    - [ ] Demonstrates subgraph extraction (e.g., touch response circuit — sensory → interneuron → motor pathway)
    - [ ] Shows cell classification breakdown (sensory, inter, motor neuron counts)
    - [ ] Demonstrates bilateral symmetry analysis
    - [ ] Shows pharyngeal view filter
    - [ ] Each code cell has markdown explanation accessible to newcomers
    - [ ] Runs to completion without errors
- **Sponsor Summary Hint:** A hands-on tour of the worm's wiring diagram using cect. Load the connectome, query connections, visualize the network, explore bilateral symmetry — all in an interactive notebook. This is how newcomers learn to work with connectome data before diving into simulation code. Demonstrates every API pattern from DD020 with real data and live plots.

---

### Issue 19: Create multi-dataset comparison notebook

- **Title:** `[DD020] Create notebook: multi-dataset connectome comparison`
- **Labels:** `DD020`, `ai-workable`, `L2`
- **Roadmap Phase:** Any
- **Target Repo:** `openworm/OpenWorm`
- **Required Capabilities:** python, jupyter
- **DD Section to Read:** [DD020 — Multi-Dataset Validation](https://docs.openworm.org/design_documents/DD020_Connectome_Data_Access_and_Dataset_Policy/#multi-dataset-validation) and [DD020 — Developmental Connectome Support](https://docs.openworm.org/design_documents/DD020_Connectome_Data_Access_and_Dataset_Policy/#developmental-connectome-support)
- **Depends On:** Issue 18 (exploration notebook), Issue 14 (cross-validation script)
- **Files to Modify:**
    - `notebooks/06_compare_connectome_datasets.ipynb` (new)
- **Test Commands:**
    - `jupyter nbconvert --execute notebooks/06_compare_connectome_datasets.ipynb`
- **Acceptance Criteria:**
    - [ ] Loads Cook2019Herm and Witvliet8 side-by-side
    - [ ] Compares neuron counts, connection counts, degree distributions
    - [ ] Visualizes differences: which connections are unique to each dataset
    - [ ] Shows Witvliet developmental series (stages 1-8): how the connectome grows
    - [ ] Plots neuron count and connection count across developmental stages
    - [ ] Compares neuropeptidergic (Ripoll-Sanchez) vs structural (Cook) connectivity
    - [ ] Computes bilateral symmetry for each dataset
    - [ ] Markdown explanations interpret results biologically
    - [ ] Runs to completion without errors
- **Sponsor Summary Hint:** A deep dive into how different connectome datasets compare. Side-by-side Cook vs Witvliet. The developmental series showing the worm's brain literally wiring itself up from 180 neurons to 300+ across 8 larval stages. Neuropeptide network overlaid on structural connectivity. This notebook makes the biological complexity tangible and visual — essential for anyone who wants to understand why dataset selection matters.

---

### Issue 20: Write cect API usage guide for DD contributors

- **Title:** `[DD020] Write cect API usage guide for consuming DD contributors`
- **Labels:** `DD020`, `ai-workable`, `L1`
- **Roadmap Phase:** Any
- **Target Repo:** `openworm/openworm_docs`
- **Required Capabilities:** docs
- **DD Section to Read:** [DD020 — API Contract for Consumers](https://docs.openworm.org/design_documents/DD020_Connectome_Data_Access_and_Dataset_Policy/#api-contract-for-consumers) and [DD020 — Quality Criteria](https://docs.openworm.org/design_documents/DD020_Connectome_Data_Access_and_Dataset_Policy/#quality-criteria)
- **Depends On:** None
- **Files to Modify:**
    - `docs/Resources/cect_usage_guide.md` (new — in openworm_docs repo)
- **Test Commands:**
    - N/A (documentation task)
- **Acceptance Criteria:**
    - [ ] Quick-start: install cect, load a dataset, query connections — in 5 lines of code
    - [ ] Complete reference: all 9 canonical query patterns with copy-paste examples
    - [ ] Anti-patterns section: "Don't parse raw files", "Don't build custom cell name normalizers", "Don't use unnamed datasets"
    - [ ] Which dataset for which DD: table mapping each consuming DD to its recommended dataset
    - [ ] How to switch datasets: changing openworm.yml for experiments
    - [ ] Version update procedure: what to do when cect releases a new version
    - [ ] Links to DD020 for full specification
    - [ ] Aimed at L1-L2 contributors (comfortable with Python but new to connectome data)
- **Sponsor Summary Hint:** The practical handbook for anyone writing code that touches connectome data. Not the full DD020 spec (too detailed), but the "how do I actually load worm wiring data in my code?" cheat sheet. Every consuming DD contributor should read this before writing their first connectome query. Quick-start in 5 lines, anti-patterns to avoid, and copy-paste examples for every use case.

---

## Group 6: Future Work & Evaluation (Phase 3+)

Target: Research tasks to evaluate upcoming data sources and prepare for future cect evolution.

---

### Issue 21: Evaluate wormneuroatlas for versions.lock integration

- **Title:** `[DD020] Evaluate wormneuroatlas package for versions.lock and Docker integration`
- **Labels:** `DD020`, `ai-workable`, `L1`
- **Roadmap Phase:** Phase 3+
- **Target Repo:** `openworm/OpenWorm`
- **Required Capabilities:** python, git
- **DD Section to Read:** [DD020 — Existing Code Resources](https://docs.openworm.org/design_documents/DD020_Connectome_Data_Access_and_Dataset_Policy/#existing-code-resources) (wormneuroatlas section)
- **Depends On:** None
- **Files to Modify:**
    - None (research issue — output is a summary posted on the issue)
- **Test Commands:**
    - N/A (research task)
- **Acceptance Criteria:**
    - [ ] Install `wormneuroatlas` and verify it works alongside `cect`
    - [ ] Document: which data does wormneuroatlas provide that cect does not? (CeNGEN expression, Randi functional, peptide deorphanization)
    - [ ] Document: does wormneuroatlas duplicate any cect functionality? (both access WormNeuroAtlas data)
    - [ ] Document: which consuming DDs would benefit? (DD005 CeNGEN, DD006 peptide GPCR, DD010 functional validation)
    - [ ] Document: package size, dependencies, Python version compatibility
    - [ ] Recommend: add to versions.lock yes/no, with rationale
    - [ ] Post findings as issue comment
- **Sponsor Summary Hint:** wormneuroatlas is a companion package to cect that provides data cect doesn't: gene expression from CeNGEN (for DD005 cell-type specialization), Randi functional connectivity (for DD010 validation), and peptide-GPCR deorphanization (for DD006). Should we add it to our build? This evaluation determines if it's worth the extra dependency.

---

### Issue 22: Evaluate NemaNode for per-synapse spatial position data

- **Title:** `[DD020] Evaluate NemaNode for per-synapse spatial data needed by DD001 Level D`
- **Labels:** `DD020`, `DD001`, `human-expert`, `L2`
- **Roadmap Phase:** Phase 3+
- **Target Repo:** `openworm/OpenWorm`
- **Required Capabilities:** python, neuroscience
- **DD Section to Read:** [DD020 — Per-Synapse Spatial Position Data](https://docs.openworm.org/design_documents/DD020_Connectome_Data_Access_and_Dataset_Policy/#per-synapse-spatial-position-data) and [DD020 — Existing Code Resources](https://docs.openworm.org/design_documents/DD020_Connectome_Data_Access_and_Dataset_Policy/#existing-code-resources) (NemaNode section)
- **Depends On:** None
- **Files to Modify:**
    - None (research issue — output is a summary posted on the issue)
- **Test Commands:**
    - N/A (research task)
- **Acceptance Criteria:**
    - [ ] Inspect NemaNode codebase (openworm/NemaNode) and nemanode.org API
    - [ ] Document: does NemaNode expose per-synapse centroid coordinates from Witvliet EM data?
    - [ ] Document: what format? (x, y, z coordinates along neurites)
    - [ ] Document: how many synapses have spatial data? (subset or all?)
    - [ ] Assess: can this data be added to cect's WitvlietDataReader? (extending ConnectionInfo with position fields)
    - [ ] Assess: is Zhao et al. 2024 inverse Gaussian distribution model accessible in code form?
    - [ ] Document: effort estimate to integrate spatial synapse data into cect
    - [ ] Post findings as issue comment with go/no-go recommendation
- **Sponsor Summary Hint:** DD001 Level D (multicompartmental neurons) needs to know not just which neurons connect, but WHERE along the neurite each synapse sits. Witvliet's EM data has this information, and NemaNode may expose it. Zhao et al. (2024) showed synapse-to-soma distances follow an inverse Gaussian distribution. This evaluation determines whether we can extract per-synapse positions from NemaNode into cect — the data needed to place synapses on multicompartmental neuron models instead of treating each neuron as a point.

---

### Issue 23: Create OpenWormUnifiedReader stability monitoring test

- **Title:** `[DD020] Create stability monitoring test for OpenWormUnifiedReader`
- **Labels:** `DD020`, `human-expert`, `L2`
- **Roadmap Phase:** Phase 3+
- **Target Repo:** `openworm/ConnectomeToolbox`
- **Required Capabilities:** python, testing
- **DD Section to Read:** [DD020 — Known Issues](https://docs.openworm.org/design_documents/DD020_Connectome_Data_Access_and_Dataset_Policy/#known-issues-and-future-work) (Issue 1: OpenWormUnifiedReader is WIP) and [DD020 — Alternatives Considered](https://docs.openworm.org/design_documents/DD020_Connectome_Data_Access_and_Dataset_Policy/#5-default-to-openwormunifiedreader-instead-of-cook2019herm) (alternative 5)
- **Depends On:** None
- **Files to Modify:**
    - `tests/test_unified_reader_stability.py` (new — in ConnectomeToolbox repo)
    - `tests/baseline/unified_reader_baseline.json` (new — snapshot)
- **Test Commands:**
    - `pytest tests/test_unified_reader_stability.py -v`
- **Acceptance Criteria:**
    - [ ] Loads OpenWormUnifiedReader and snapshots: node count, connection count, synclass list, top-20 highest-degree neurons
    - [ ] Compares against baseline snapshot from previous run
    - [ ] If snapshot changes: test passes but prints WARNING: "OpenWormUnifiedReader changed — review before considering as default"
    - [ ] Tracks: number of consecutive runs without change (stability metric)
    - [ ] Documents: when WIP designation is removed (triggers review for default adoption)
    - [ ] `--update-baseline` flag saves new snapshot
    - [ ] Designed to run weekly (cron job or manual) rather than on every PR
- **Sponsor Summary Hint:** OpenWormUnifiedReader is intended to become the "best estimate" connectome, but it's currently WIP and changes without notice. This monitoring test takes regular snapshots of what the reader returns. When it stops changing (stable across multiple weeks) and the WIP designation is removed, that's the signal to consider adopting it as the new default — replacing Cook2019Herm. Until then, we just watch and wait.

---

## Summary Statistics

| Category | Count |
|----------|-------|
| **Total Issues** | 23 |
| **ai-workable** | 18 |
| **human-expert** | 5 |
| **L1** | 10 |
| **L2** | 10 |
| **L3** | 3 |

| Group | Issues | Target |
|-------|--------|--------|
| **1: Build Integration** | 1–5 | cect pinned, configured, cached in Docker |
| **2: CI & Quality Gates** | 6–9 | Automated compliance and version checking |
| **3: Consumer DD Integration** | 10–13 | Canonical data loaders for consuming DDs |
| **4: Multi-Dataset Validation** | 14–17 | Cross-validation and regression infrastructure |
| **5: Documentation & Notebooks** | 18–20 | Interactive exploration and API guide |
| **6: Future Work & Evaluation** | 21–23 | Research on upcoming data sources |

### Cross-References to Other DD Issues

| Other DD Issue | Title | How DD020 Relates |
|----------------|-------|-------------------|
| DD013 Issue 1 | Create openworm.yml config schema | DD020 Issue 2 adds `data.connectome` section |
| DD013 Issue 3 | Multi-stage Dockerfile | DD020 Issue 4 adds cect to neural stage |
| DD013 Issue 7 | Create versions.lock | DD020 Issue 1 adds cect entry |
| DD013 Issue 13 | CI Gate 1 | DD020 Issue 6 adds connectome test step |
| DD003 Issue 13 | WCON trajectory export | Uses cect cell classification for neuron identification |

### Dependency Graph (Critical Path)

```
DD013 Issue 1 (openworm.yml)
  └→ Issue 2 (data.connectome section)
       └→ Issue 3 (config validation)

DD013 Issue 7 (versions.lock)
  └→ Issue 1 (pin cect)
       └→ Issue 4 (cect in Docker)
            └→ Issue 5 (pre-cache datasets)
                 ├→ Issue 6 (CI gate) → Issue 9 (version update script)
                 ├→ Issue 14 (cross-validation script) → Issue 16 (sensitivity analysis)
                 ├→ Issue 15 (bilateral symmetry metric)
                 └→ Issue 17 (regression test suite)

Issue 4 (cect in Docker)
  └→ Issue 10 (c302 connectome loader)
       ├→ Issue 11 (neuron-to-muscle loader)
       ├→ Issue 12 (pharyngeal loader)
       └→ Issue 13 (neuropeptide + neurotransmitter loaders)

Issue 7 (audit) → Issue 8 (compliance checker)

DD013 Issue 23 (JupyterLab)
  └→ Issue 18 (exploration notebook) → Issue 19 (comparison notebook)

Issues 20, 21, 22, 23 — independent (docs/research)
```
