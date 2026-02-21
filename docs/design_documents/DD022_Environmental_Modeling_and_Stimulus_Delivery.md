# DD022: Environmental Modeling and Stimulus Delivery

**Status:** Proposed ([Phase 2](DD_PHASE_ROADMAP.md#phase-2-slow-modulation-closed-loop-sensory-months-4-6))  
**Author:** OpenWorm Core Team  
**Date:** 2026-02-19  
**Supersedes:** None  
**Related:** [DD003](DD003_Body_Physics_Architecture.md) (Body Physics — boundary particles), [DD019](DD019_Closed_Loop_Touch_Response.md) (Touch Response — tap stimulus), [DD017](DD017_Hybrid_Mechanistic_ML_Framework.md) (Hybrid ML — learned sensory)

---

## TL;DR

The worm doesn't live in a void — it crawls on agar, swims in liquid, navigates chemical gradients, seeks preferred temperatures, and eats bacteria. This DD specifies how to model substrates (agar stiffness, liquid viscosity, soil mechanics), deliver stimuli (NaCl gradients, temperature ramps, tap impulses), and represent food (OP50 bacterial particles in pharyngeal lumen). Success: reproduce chemotaxis (CI index >0.5) and thermotaxis (navigate to cultivation temp) on simulated gradients.

---

## Quick Action Reference

| Question | Answer |
|----------|--------|
| **Phase** | [Phase 2](DD_PHASE_ROADMAP.md#phase-2-slow-modulation-closed-loop-sensory-months-4-6) |
| **Layer** | Environment — see [Phase Roadmap](DD_PHASE_ROADMAP.md#phase-2-slow-modulation-closed-loop-sensory-months-4-6) |
| **What does this produce?** | Substrate models (agar stiffness, liquid viscosity, soil), chemical/thermal gradient fields, geometric obstacles, bacterial lawn particle system |
| **Success metric** | Chemotaxis on NaCl gradient (CI chemotaxis index >0.5), thermotaxis to cultivation temp (±2°C), tap withdrawal on agar vs. liquid (latency difference reproduced) |
| **Repository** | `openworm/sibernetic` (substrate mechanics) + `openworm/c302` (stimulus coupling to sensory neurons) — issues labeled `dd022` |
| **Config toggle** | `environment.substrate: "agar"`, `environment.chemical_gradient: true`, `environment.food_particles: true` in `openworm.yml` |
| **Build & test** | `docker compose run quick-test --config chemotaxis` (worm navigates gradient?), `docker compose run validate` (CI index validation) |
| **Visualize** | [DD014](DD014_Dynamic_Visualization_Architecture.md) `environment/substrate/` layer (agar surface heatmap), `environment/gradients/` (chemical/thermal field visualization), `environment/food/` (bacterial particles) |
| **CI gate** | Behavioral validation (chemotaxis, thermotaxis) blocks merge; substrate mechanics must not destabilize body physics |
---

## Mission Alignment

**OpenWorm Mission:** "Creating the world's first virtual organism."

**[DD022](DD022_Environmental_Modeling_and_Stimulus_Delivery.md) serves this by:** An organism doesn't exist in isolation — it interacts with its environment. Chemotaxis (navigating toward food), thermotaxis (seeking optimal temperature), and mechanosensation (detecting surfaces) are core *C. elegans* behaviors that require environmental context. Without gradients and substrates, the worm can't exhibit naturalistic behavior.

**Core Principle:** "Building in the physics... because it matters."

**[DD022](DD022_Environmental_Modeling_and_Stimulus_Delivery.md) delivers:** Physical substrates (agar = viscoelastic solid, liquid = low-Reynolds-number fluid, soil = granular medium) with realistic mechanical properties, enabling validation against environment-dependent behaviors.

---

## Goal & Success Criteria

| Criterion | Target | [DD010](DD010_Validation_Framework.md) Tier |
|-----------|--------|------------|
| **Primary:** Chemotaxis behavior | CI (chemotaxis index) >0.5 on NaCl gradient (Iino & Yoshida 2009) | Tier 3 (blocking) |
| **Primary:** Thermotaxis behavior | Navigate to cultivation temperature (20°C) within ±2°C on thermal gradient | Tier 3 (blocking) |
| **Secondary:** Substrate-dependent locomotion | Crawling speed on agar vs. swimming speed in liquid matches experimental ratio (~2:1) | Tier 3 (blocking) |
| **Tertiary:** Tap withdrawal latency | Tap on agar (firm) vs. tap in liquid (soft) produces different reversal latencies | Tier 1 (non-blocking) |

**Before:** Worm exists in an infinite, featureless void. No substrate, no gradients, no food. Cannot exhibit naturalistic navigation behaviors.

**After:** Worm crawls on agar (or swims in liquid, or burrows in soil), senses chemical/thermal gradients via [DD019](DD019_Closed_Loop_Touch_Response.md)/DD017 sensory transduction, navigates toward attractants (food, optimal temperature), avoids repellents.

---

## Deliverables

| Artifact | Path | Format | Example |
|----------|------|--------|---------|
| Agar substrate model | `sibernetic/substrates/agar.cpp` | C++ (viscoelastic solid) | Young's modulus 3-10 kPa, Poisson ratio 0.45 |
| Liquid substrate model | `sibernetic/substrates/liquid.cpp` | C++ (Navier-Stokes) | Viscosity 1e-3 Pa·s (water), Re ~0.01 |
| Chemical gradient field | `sibernetic/stimuli/chemical_gradient.py` | Python | NaCl diffusion, concentration vs. position |
| Thermal gradient field | `sibernetic/stimuli/thermal_gradient.py` | Python | Linear or radial temperature profile |
| Food particle system | `sibernetic/food/bacterial_particles.cpp` | C++ (SPH particles) | OP50 bacteria as deformable particles in lumen |
| Geometric obstacles | `sibernetic/obstacles/*.obj` | OBJ meshes | Pillars, channels, barriers for boundary conditions |
| Environment config | `openworm.yml` environment section | YAML | substrate, gradients, food, obstacles |
| Chemotaxis trajectory (viewer) | OME-Zarr: `environment/chemotaxis_path/` | Shape (n_timesteps, 2) | (x, y) centroid on gradient |
| Gradient fields (viewer) | OME-Zarr: `environment/gradients/` | Shape (n_x, n_y, n_fields) | Concentration or temperature per spatial bin |

---

## Technical Approach

### Component 1: Substrate Mechanics (Agar vs. Liquid vs. Soil)

**Agar (most common experimental substrate):**

- Viscoelastic solid (not purely elastic, not purely viscous)
- Young's modulus: 3-10 kPa (depends on agarose concentration, typically 2%)
- Poisson ratio: 0.45 (nearly incompressible)
- [DD003](DD003_Body_Physics_Architecture.md) boundary particles model agar as fixed constraints; extend to deformable substrate

**Liquid (swimming experiments):**

- Newtonian fluid (same Navier-Stokes as [DD003](DD003_Body_Physics_Architecture.md) pseudocoelom)
- Viscosity: 1e-3 Pa·s (water) to 1e-2 Pa·s (M9 buffer)
- No solid substrate → worm swims, different gait (higher frequency, lower amplitude)

**Soil (naturalistic environment):**

- Granular medium (sand, decomposed organic matter)
- Modeled as additional SPH particles or DEM (discrete element method)
- Phase 5+ work (complex, low priority)

### Component 2: Chemical Gradient Delivery

**For chemotaxis experiments (ASEL/ASER neurons respond to NaCl):**

Diffusion equation in 2D (agar surface):
```
∂C/∂t = D ∇²C
```

- D = diffusion coefficient (~1e-5 cm²/s for small molecules in agar)
- Boundary conditions: Source (high concentration) at one end, sink (low) at other
- Steady-state: Linear or exponential gradient

**Simplified implementation:**

- Pre-compute steady-state gradient field (no time evolution during simulation)
- Lookup concentration at worm's (x, y) position each timestep
- Feed to [DD019](DD019_Closed_Loop_Touch_Response.md)/DD017 chemosensory transduction model

### Closed-Loop Sensorimotor Interaction for Chemotaxis

The defining feature of naturalistic chemotaxis is the closed-loop interaction between sensation and movement. Zhao et al. (2024) demonstrated this with their MetaWorm model, achieving zigzag navigation toward food attractors that matches experimentally observed trajectories (Pierce-Shimomura et al. 1999).

**Closed-loop cycle (each simulation timestep):**

1. **Body position** ([DD003](DD003_Body_Physics_Architecture.md)) provides the worm's current location in the environment
2. **Local concentration** (DD022 gradient field) sampled at the worm's head position
3. **Temporal derivative** `dC/dt = (C(t) - C(t-dt)) / dt` computed — this implements the biased random walk strategy where the worm responds to concentration *changes*, not absolute levels
4. **Sensory neuron activation** ([DD001](DD001_Neural_Circuit_Architecture.md)/[DD017](DD017_Hybrid_Mechanistic_ML_Framework.md)): `dC/dt` converted to current injection on chemosensory neurons (AWC for odors, ASEL/ASER for salt)
5. **Neural circuit computation** ([DD001](DD001_Neural_Circuit_Architecture.md)): sensory input propagates through interneurons to motor neurons
6. **Motor output** ([DD002](DD002_Muscle_Model_Architecture.md)): motor neuron calcium drives muscle contraction
7. **Body movement** ([DD003](DD003_Body_Physics_Architecture.md)): muscles deform the body, propelling it through the environment
8. Return to step 1

**Key biological insight:** Sensory activation uses the temporal derivative `dC/dt`, not the absolute concentration `C(t)`. This is because *C. elegans* employs a biased random walk strategy: it extends forward runs when moving up-gradient (positive dC/dt) and initiates turns/reversals when moving down-gradient (negative dC/dt) (Pierce-Shimomura et al. 1999).

**OpenWorm's approach differs from Zhao et al.** in a critical way: they used a linear readout layer from motor neuron membrane potentials to muscle activations (treating the neural circuit as a 'reservoir computer'). OpenWorm instead uses biophysical neuromuscular junction synapses ([DD002](DD002_Muscle_Model_Architecture.md)), producing a fully mechanistic chain from sensation to movement with no learned components in the motor pathway.

**Validation target:** The simulated worm's trajectory in a chemical gradient should exhibit the characteristic zigzag pattern toward the food source, with a chemotaxis index (CI) > 0.5 on a standard NaCl gradient assay (Iino & Yoshida 2009).

### Component 3: Thermal Gradient Delivery

**For thermotaxis experiments (AFD neuron responds to temperature):**

Similar to chemical gradient but for temperature:

- Cultivation temperature (20°C) at one end, 15°C or 25°C at other
- Linear or radial gradient
- Feed to [DD017](DD017_Hybrid_Mechanistic_ML_Framework.md) Component 4 learned thermosensory model

### Component 4: Food Particles (OP50 Bacteria)

**For pharyngeal pumping + feeding behavior:**

- Bacteria modeled as small deformable SPH particles (~1 µm diameter)
- Delivered to pharyngeal lumen via pumping ([DD007](DD007_Pharyngeal_System_Architecture.md))
- Grinder crushes bacteria (future: mechanical food processing)

**Phase 3 work** (not required for basic pumping frequency validation).

---

## Alternatives Considered

### 1. Ignore Environment (Worm in Void)

**Rejected:** Cannot model naturalistic behaviors (chemotaxis, thermotaxis, food seeking) without environmental context. The worm's sensory system evolved to detect gradients — testing it requires gradients.

### 2. Simplified: Boundary Conditions Only (No Substrate Mechanics)

**Description:** Keep boundary particles fixed (current [DD003](DD003_Body_Physics_Architecture.md)), just add chemical/thermal fields.

**Partially adopted:** For Phase 2-3, this is the pragmatic approach. Substrate mechanics (agar deformability) can be deferred to Phase 5+.

---

## Quality Criteria

1. **Chemotaxis reproduction:** Simulated worm on NaCl gradient produces CI (chemotaxis index) >0.5 (Iino & Yoshida 2009 experimental data).
2. **Thermotaxis reproduction:** Worm navigates to 20°C on 15-25°C gradient within ±2°C.
3. **Substrate-dependent gait:** Crawling on agar vs. swimming in liquid produces ~2:1 speed ratio (matches experiments).
4. **No destabilization:** Adding environment must not break [DD003](DD003_Body_Physics_Architecture.md) body physics (no particle escape, no NaN).

---

## Boundaries (Explicitly Out of Scope)

1. **Multi-worm environments:** Social aggregation, pheromone communication. Single-worm only.
2. **Complex geometries:** Microfluidic mazes, 3D terrains. Flat gradients for Phase 2-3.
3. **Food consumption dynamics:** Bacterial digestion, nutrient absorption. Food particles are visual only (Phase 3).
4. **Soil microbial ecology:** Bacteria, fungi, nematode predators. Simple soil mechanics only (Phase 5+).

---

## Integration Contract

### Inputs

| Input | Source DD | Variable | Format |
|-------|----------|----------|--------|
| Worm body position | [DD003](DD003_Body_Physics_Architecture.md) | Centroid (x, y) from SPH particles | Computed from body/ OME-Zarr |
| Sensory neuron positions | [DD001](DD001_Neural_Circuit_Architecture.md) / [DD008](DD008_Data_Integration_Pipeline.md) | Per-neuron (x, y, z) | Static coordinates |

### Outputs

| Output | Consumer DD | Variable | Format |
|--------|------------|----------|--------|
| Local chemical concentration | [DD017](DD017_Hybrid_Mechanistic_ML_Framework.md) Component 4 (chemosensory) | Concentration at worm position | Scalar (mM) |
| Local temperature | [DD017](DD017_Hybrid_Mechanistic_ML_Framework.md) Component 4 (thermosensory) | Temperature at worm position | Scalar (°C) |
| Substrate reaction force | [DD003](DD003_Body_Physics_Architecture.md) | Boundary particle forces | SPH force vectors |

---

## References

1. **Iino Y, Yoshida K (2009).** "Parallel use of two behavioral mechanisms for chemotaxis in *Caenorhabditis elegans*." *J Neurosci* 29:5370-5380. *NaCl chemotaxis assay — chemotaxis index (CI) metric and experimental benchmarks.*
2. **Pierce-Shimomura JT, Morse TM, Lockery SR (1999).** "The fundamental role of pirouettes in *Caenorhabditis elegans* chemotaxis." *J Neurosci* 19:9557-9569. *Biased random walk strategy — temporal derivative of concentration drives run/pirouette decisions.*
3. **Zhao M, Wang N, Jiang X, et al. (2024).** "An integrative data-driven model simulating *C. elegans* brain, body and environment interactions." *Nature Computational Science* 4(12):978-990. *MetaWorm model — closed-loop chemotaxis demonstration with zigzag trajectories matching experimental observations.*

---

**Approved by:** Pending
**Implementation Status:** Proposed ([Phase 2](DD_PHASE_ROADMAP.md#phase-2-slow-modulation-closed-loop-sensory-months-4-6))
**Next Actions:**

1. Write detailed substrate mechanics spec (agar viscoelasticity parameters)
2. Implement steady-state gradient solver (chemical, thermal)
3. Test with [DD019](DD019_Closed_Loop_Touch_Response.md) closed-loop touch + chemotaxis
4. Validate against Iino & Yoshida 2009 chemotaxis data
