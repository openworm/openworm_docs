How We Know It's Working: The Validation Framework
===================================================

Building a digital worm is one thing. Knowing it's *right* is another.

A simulation might produce something that looks like a worm crawling — but if the neurons inside are firing for the wrong reasons, the first change you make will break everything. OpenWorm's validation framework, specified in **[DD010: Validation Framework](design_documents/DD010_Validation_Framework.md)**, addresses this with a principle borrowed from software engineering: **test at every level, not just the final output**.

---

## The Core Idea: Multi-Level Testing

Think of it like checking a building. You could stand outside and say "it looks fine." But a structural engineer inspects the foundation, the steel, the wiring, and *then* checks the finished building. Our validation works the same way — we test at four levels, from individual cells up to whole-animal behavior.

### Tier 1: Do individual cells behave correctly?

We isolate single neurons in the simulation and compare their electrical behavior to laboratory recordings. For example, the AVA command interneuron has been studied extensively with patch-clamp electrodes by the Lockery lab — we can compare our model's voltage response curve to real data point by point.

About 7 neuron classes have detailed electrophysiology data. But *C. elegans* has 118 distinct neuron classes — what about the other 111?

For those, we use a clever workaround: **expression-consistency checks**. The [CeNGEN project](https://cengen.org) has measured which ion channel genes each neuron class expresses. If CeNGEN says a neuron expresses lots of L-type calcium channels (`egl-19`) but no A-type potassium channels (`shl-1`), then our model of that neuron had better show large calcium currents and no transient potassium currents. This catches the most common failure mode — a neuron modeled with the wrong dominant channel type — without requiring experimental recordings that don't exist.

**Status:** Non-blocking. A Tier 1 failure means a cell model needs tuning, not that the whole simulation is broken.

### Tier 2: Do neurons interact correctly as a network?

This is the heart of the validation. In 2023, [Randi et al.](https://doi.org/10.1038/s41586-023-06683-4) published something remarkable: whole-brain calcium imaging of all 302 neurons in *C. elegans*, capturing how every neuron's activity correlates with every other neuron's activity. This gives us a 302×302 matrix of real neural dynamics to compare against.

We run our simulation for 60 seconds, extract the same 302×302 correlation matrix, and ask: **how similar are the simulated and real matrices?** The metric is the correlation between the two (flattened) matrices — a single number that captures how well the model reproduces the global pattern of neural coordination.

**Threshold: r > 0.5.** Why this number? Because independent recordings of the *same* real worm produce inter-session correlations of r = 0.6–0.8. A model hitting r > 0.5 is approaching the reproducibility ceiling of the experimental data itself — the point where biological noise, not model error, is the limiting factor.

**Status:** Blocking. A pull request that degrades this score cannot be merged.

### The unc-31 Natural Experiment

One of the most elegant validation tests comes from a mutant worm called *unc-31*. The UNC-31 protein is required for releasing neuropeptides — the slower, modulatory chemical signals that complement fast synaptic transmission. An *unc-31* mutant has normal synapses but **zero neuropeptide signaling**.

[Randi et al.](https://doi.org/10.1038/s41586-023-06683-4) measured the 302×302 correlation matrix for both wild-type and *unc-31* worms. The *difference* between those two matrices isolates exactly what neuropeptides contribute to brain dynamics.

We can do the same thing in simulation: run the model with [neuropeptide signaling](design_documents/DD006_Neuropeptidergic_Connectome_Integration.md) on, then off, and compare the difference to the experimental difference. If our model of neuropeptide modulation is correct, the two difference matrices should match (r > 0.3 — a weaker threshold because the difference signal is smaller and noisier than the absolute signal).

This is a genuinely predictive test: the model must get the *mechanism* right, not just the final outcome.

### Tier 3: Does the organism move correctly?

Ultimately, the worm has to crawl like a real worm. The [Schafer lab](https://doi.org/10.1038/nmeth.2560) compiled a database of *C. elegans* locomotion from thousands of tracked animals, measuring five key properties:

| Metric | What It Measures | Real Worm Value |
|--------|-----------------|-----------------|
| **Speed** | Forward crawling velocity | ~0.2 mm/s |
| **Wavelength** | Body wave spatial period | ~1.5 mm |
| **Frequency** | Body wave temporal frequency | ~0.5 Hz |
| **Amplitude** | Body bend depth | ~0.15 mm |
| **Gait** | Overall movement pattern | Sinusoidal |

**Threshold: all 5 within ±15%.** Why 15%? Because that's roughly the coefficient of variation observed across real worms of the same genotype. A model matching the mean within one CV is performing within the biological noise floor. Going tighter would mean overfitting to a specific animal rather than capturing the population.

**Tool:** [open-worm-analysis-toolbox](https://github.com/openworm/open-worm-analysis-toolbox) — currently being revived per [DD021](design_documents/DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md).

**Status:** Blocking, but currently not automated — the analysis toolbox needs revival first.

### Tier 4: Does the organism respond correctly to perturbations?

This is the deepest level of validation and the hardest to pass. A model can reproduce normal behavior for the wrong reasons — what physicists call a "degenerate solution." As [Pearl & Mackenzie (2018)](https://www.hachettebookgroup.com/titles/judea-pearl/the-book-of-why/9780465097616/) argue, observational data alone cannot distinguish correlation from causation. To prove the model captures real causal relationships between neurons, we need to break things and see if the model breaks the same way.

For example:

- **Ablate touch neurons** (ALM, AVM, PLM) → the model should lose gentle touch response, matching [Chalfie et al. (1985)](https://doi.org/10.1523/JNEUROSCI.05-04-00956.1985)
- **Remove all gap junctions** → the correlation matrix should be disrupted more than removing chemical synapses, matching [Randi et al. (2023)](https://doi.org/10.1038/s41586-023-06683-4) and [Zhao et al. (2024)](https://doi.org/10.1038/s43588-024-00738-w)
- **Silence B-class motor neurons** → forward locomotion should stop

**Status:** Non-blocking (advisory) in early phases. Becomes blocking as more subsystems come online.

---

## Why All Four Tiers Matter

A model can pass any single tier while being fundamentally wrong:

- **Passes Tier 3 but fails Tier 1:** The worm crawls correctly, but the individual neurons are firing incorrectly. You got lucky with parameter compensation — and the next change will break it.
- **Passes Tiers 1–3 but fails Tier 4:** Everything looks right under normal conditions, but the model predicts that ablating a neuron has no effect when the real worm is paralyzed. The wiring diagram is wrong.
- **Passes Tiers 1–2 but fails Tier 3:** The cells and circuits look right in isolation, but something about how they couple to the body physics is off.

Multi-tier validation catches each of these failure modes. All tiers must pass for the model to be considered validated.

---

## Organ-Specific Validation

Beyond locomotion, organ systems have their own characteristic rhythms that serve as validation targets:

| Organ | DD | What to Measure | Expected Value |
|-------|----|-----------------|----------------|
| **Pharynx** | [DD007](design_documents/DD007_Pharyngeal_System_Architecture.md) | Pumping frequency | 3–4 Hz |
| **Intestine** | [DD009](design_documents/DD009_Intestinal_Oscillator_Model.md) | Defecation cycle period | 50 ± 10 seconds |
| **Egg-laying** | [DD018](design_documents/DD018_Egg_Laying_System_Architecture.md) | Active/inactive pattern | ~20 min inactive, ~2 min active |

These are beautiful validation targets because the rhythms are robust and well-characterized — a pharynx that pumps at 1 Hz or 10 Hz is clearly wrong.

---

## Current Status

| Tier | Status | What's Needed |
|------|--------|---------------|
| **Tier 1** (single cell) | Scripts exist, not in CI | Automate and integrate |
| **Tier 2a** (circuit) | Data ready via `wormneuroatlas` API | Wire into CI pipeline |
| **Tier 2b** (neuropeptides) | Data ready, awaiting [DD006](design_documents/DD006_Neuropeptidergic_Connectome_Integration.md) | Implement DD006 first |
| **Tier 3** (behavior) | **Blocked** — toolbox needs revival | [DD021](design_documents/DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md) revival (~33 hrs) |
| **Tier 4** (causal) | Future work | Phase 3+ |

The infrastructure priority is getting Tiers 2 and 3 automated in CI ([DD013](design_documents/DD013_Simulation_Stack_Architecture.md)) so every pull request is validated before merging.

---

## Continue Reading

- **[DD010: Validation Framework](design_documents/DD010_Validation_Framework.md)** — Complete specification: all thresholds, test commands, data sources, and CI integration
- **[DD021: Movement Analysis Toolbox](design_documents/DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md)** — Tier 3 toolbox revival plan
- **[DD024: Validation Data Acquisition](design_documents/DD024_Validation_Data_Acquisition_Pipeline.md)** — How we source experimental data for all tiers
- **[How It Works: Modeling](modeling.md)** — How the simulation components fit together
