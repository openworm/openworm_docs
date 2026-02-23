# DD014: Dynamic Visualization and Multi-Scale Exploration Architecture

- **Status:** Proposed
- **Author:** OpenWorm Core Team
- **Date:** 2026-02-15
- **Supersedes:** WormBrowser (browser.openworm.org, 2012), WormSim (org.wormsim.frontend, 2014-2015), informal Geppetto coupling
- **Related:** [DD003](DD003_Body_Physics_Architecture.md) (Body Physics), [DD001](DD001_Neural_Circuit_Architecture.md) (Neural Circuit), [DD013](DD013_Simulation_Stack_Architecture.md) (Simulation Stack), All DDs (visualization consumes all subsystem outputs)

---

> **Phase:** [Phase 1](DD_PHASE_ROADMAP.md#phase-1-cell-type-differentiation-months-1-3), [Phase 2](DD_PHASE_ROADMAP.md#phase-2-slow-modulation-closed-loop-sensory-months-4-6), [Phase 4](DD_PHASE_ROADMAP.md#phase-4-mechanical-cell-identity-high-fidelity-visualization-months-13-18) | **Layer:** Visualization

## TL;DR

DD014 defines the three-scale visualization system (molecular, cellular, organism) for the OpenWorm simulation, connecting simulation data to real-time 3D rendering via OME-Zarr export and a Trame/Three.js viewer. The key success metric is that every simulation variable must be visually inspectable within 2 seconds, and the viewer must support full time playback in a web browser with toggleable layers for each subsystem.

## Context

### The Missing Layer

Design Documents [DD001](DD001_Neural_Circuit_Architecture.md)-[DD013](DD013_Simulation_Stack_Architecture.md) specify a scientifically rigorous simulation engine and its integration backbone. But **none of them describe what a human being actually sees when the simulation runs.** The current visual output is:

| What Exists | What You See |
|-------------|-------------|
| Sibernetic particle renderer | ~100,000 colored dots (blue/green/gray) deforming in a worm shape |
| Video capture (xvfb + tmux + ffmpeg) | Screen recording of particle renderer — **broken, OOMs at >2s** |
| PNG frames | Snapshots of particle cloud or matplotlib voltage plots |
| WCON trajectory file | Numerical data (not visual) |

There is no smooth-surfaced worm, no way to zoom into a firing neuron, no way for a non-scientist to understand what they're looking at, and no way to experience the multi-scale nature of the simulation (ion channels → neurons → muscles → body → behavior).

### The WormBrowser (2012): What People Actually Use

The most-used OpenWorm visualization tool is not a simulation viewer — it's the **WormBrowser** ([browser.openworm.org](https://browser.openworm.org)), a static 3D anatomy browser live since 2012.

| Feature | Description |
|---------|-------------|
| **3D anatomy** | Full *C. elegans* cellular anatomy from VirtualWorm meshes (Caltech/WormBase) |
| **Layer peeling** | Opacity slider revealing cuticle → organs → muscles → neurons |
| **Layer toggles** | Individual on/off for cuticle, organs, muscles, neurons |
| **Search** | Find any cell by name |
| **Click-to-select** | Click any entity to see its identity |
| **Zero installation** | WebGL in any modern browser — no Docker, no server |

**Technology:** jQuery 1.6.3, open-3d-viewer (WebGL), hosted on Google App Engine. Built by Giovanni Idili (2012). iOS version: `openworm/openwormbrowser-ios` (2013). Last code update: 2013, but the site remains live and widely referenced — papers, Wikipedia, Experiments with Google, talks.

**John White (Feb 12, 2026 meeting):** *"One of the things that gets OpenWorm known... that could do with an update."* Specific suggestions:

- **Multiple developmental stages** — L1, L4, adult, dauer reconstructions now exist
- **Male anatomy** — being reconstructed (Cook 2019 male connectome)
- **Comparative species** — *Pristionchus pacificus* and other nematodes now mapped
- **Click neuron → link to WormAtlas** — *"click on and identify a particular neuron and have a link"*
- **Work with WormAtlas team** (Nate Schroeder)

The WormBrowser is approaching end of life (legacy jQuery, no updates since 2013), but it's too important to abandon without a replacement that matches its features. **WormSim 2.0 must achieve WormBrowser feature parity before browser.openworm.org can redirect.**

### The WormSim Vision (2014)

The Kickstarter-funded WormSim project (`org.wormsim.frontend`) envisioned "A Digital Organism In Your Browser":

- Name your worm, pick its color, be guided through its biology
- Toggle between skin, muscles, and neurons in 3D
- Watch pre-recorded simulation results streamed like Netflix
- Neurons glow when they fire
- "Now you are having a look INSIDE MY MIND!"

WormSim's frontend has been dormant since December 2015. The underlying Geppetto platform is maintained but not connected to the current simulation pipeline. [DD013](DD013_Simulation_Stack_Architecture.md) explicitly declared Geppetto "out of scope."

### Worm3DViewer (2025): A Starting Point

The Neural Circuit L4 Maintainer created `openworm/Worm3DViewer` (v0.0.8, June-September 2025) as a prototype that composites three data sources into a single 3D scene:

| Data Source | What It Shows | Loader |
|-------------|--------------|--------|
| **Sibernetic replay** (`position_buffer.txt`) | SPH particles color-coded by type, with time slider for animation | `SiberneticReplay.py` |
| **NeuroML c302** (`*.net.nml` + `*.cell.nml`) | 302 neurons with full morphology (soma spheres + dendrite/axon tubes) | `neuromlmodel.py` |
| **VirtualWorm meshes** (`bwm.obj`, `neurons.obj`) | Smooth 3D anatomy (muscles in green, neurons in jet colormap) | `virtualworm.py` |

**Technology:** Streamlit + PyVista + stpyvista (VTK-based), Docker container, CI with NeuroML validation.

**Critical limitation:** stpyvista renders static iframes. The Sibernetic animation (time slider, play button) works in native VTK GUI mode but **does not function in the Streamlit web deployment**. The web user sees a single frozen frame.

### The 2026 Technology Landscape

The visualization technology available in 2026 is dramatically better than what WormSim had in 2014:

| Capability | 2014 (WormSim era) | 2026 (Now) |
|-----------|-------------------|-----------|
| Browser 3D rendering | WebGL 1.0 only | **WebGPU production-ready** in Chrome, Firefox, Safari |
| 3D library | THREE.js r69 | THREE.js r172+ with zero-config WebGPU + WebGL fallback |
| Large data streaming | Custom HDF5 via Geppetto | **OME-Zarr** (chunked, cloud-native, progressive loading) |
| Particle rendering | ~10K particles practical | **100K-1M+ particles at 60 FPS** via instanced rendering / compute shaders |
| Server requirement | Java Geppetto backend required | Fully **client-side** possible (static files + browser) |
| Python → web | None (Java was required) | **Trame** (Kitware) serves PyVista to browser; **VTK.wasm** runs VTK in browser |
| Multi-scale viewers | Nothing biological | **Neuroglancer**, **Vitessce**, **WEBKNOSSOS** — production tools for multi-scale bio data |
| Mobile | Not supported | WebGPU on Chrome Android, Safari iOS 26 |
| VR/AR | Not practical | **WebXR** with WebGPU (Safari 26.2 on Vision Pro) |

---

## Decision

### Build a Multi-Scale Dynamic Visualization Layer in Three Stages

The visualization layer is not a single tool. It is a **data export pipeline** (from simulation to viewable format), a **viewer application** (renders the data), and a **multi-scale exploration experience** (lets users zoom between organism, tissue/cell, and molecular scales).

### Three Visualization Scales

| Scale | What the User Sees | Data Sources | Analogy |
|-------|-------------------|-------------|---------|
| **Organism** | Smooth-surfaced worm crawling in an environment. Pharynx pumps. Body bends. Defecation events visible. | [DD003](DD003_Body_Physics_Architecture.md) particle positions → surface reconstruction, [DD007](DD007_Pharyngeal_System_Architecture.md) pumping state, [DD009](DD009_Intestinal_Oscillator_Model.md) defecation events | Google Earth from orbit |
| **Tissue / Cell** | Individual cells colored by activity. Click a muscle to see its calcium trace. Neurons glow when they fire. Intestinal calcium waves propagate as color gradients. | [DD001](DD001_Neural_Circuit_Architecture.md) neuron V/Ca, [DD002](DD002_Muscle_Model_Architecture.md) muscle activation, [DD004](DD004_Mechanical_Cell_Identity.md) cell IDs, [DD007](DD007_Pharyngeal_System_Architecture.md) pharynx cells, [DD009](DD009_Intestinal_Oscillator_Model.md) intestinal cells | Google Earth street view |
| **Molecular** | Ion channels opening/closing on a cell membrane. Calcium flowing through IP3 receptors. Neuropeptide clouds diffusing between cells. | [DD001](DD001_Neural_Circuit_Architecture.md) channel states, [DD005](DD005_Cell_Type_Differentiation_Strategy.md) conductance densities, [DD006](DD006_Neuropeptidergic_Connectome_Integration.md) peptide concentrations | Google Earth indoor view |

**DD014 Viewer Phases vs. Roadmap Phases:**

DD014 is developed incrementally across three Roadmap phases. To avoid confusion, the table below maps DD014's internal viewer stages to the [Phase Roadmap](DD_PHASE_ROADMAP.md):

| DD014 Viewer Stage | Roadmap Phase | Timeline | What Ships |
|--------------------|---------------|----------|------------|
| **Viewer Stage 1** — Post-hoc Trame viewer | [Phase 1](DD_PHASE_ROADMAP.md#phase-1-cell-type-differentiation-months-1-3) (Cell-Type Specialization, months 1-3) | Weeks 1-8 | Organism + Tissue/Cell scales. Smooth body surface, neurons/muscles visible and selectable, activity coloring, time scrubbing. |
| **Viewer Stage 2** — Interactive dynamic viewer | [Phase 2](DD_PHASE_ROADMAP.md#phase-2-slow-modulation-closed-loop-sensory-months-4-6) (Modulation + Closed-Loop, months 4-6) | Weeks 9-20 | All tissue-scale features enhanced: pharynx/intestine layers, neuropeptide volumetric clouds, validation overlay, full layer system. Three.js prototype begins. |
| **Viewer Stage 3** — WormSim 2.0 | [Phase 4](DD_PHASE_ROADMAP.md#phase-4-mechanical-cell-identity-high-fidelity-visualization-months-13-18) (Complete Organism, months 13-18) | Weeks 21-32+ | **Molecular scale** (ion channels, gene expression per [DD014.1](DD014.1_Visual_Rendering_Specification.md) Mockups 13-14), Three.js + WebGPU static site, narrative-guided exploration, deployed to wormsim.openworm.org. **browser.openworm.org redirects here after feature parity achieved.** |

Note: There is no DD014 work in Roadmap Phase 3 (Organ Systems). During Phase 3, the viewer built in Stage 2 is *used* to visualize pharynx/intestine/egg-laying, but no new viewer architecture is needed — the layer system from Stage 2 already supports it.

See **[DD014.1](DD014.1_Visual_Rendering_Specification.md) (Visual Rendering Specification)** for complete appearance specifications at all three scales. Note: [DD014.1](DD014.1_Visual_Rendering_Specification.md) Mockups 10-14 (membrane cross-section, calcium influx, nucleus, gene transcription, vesicle trafficking) are **Viewer Stage 3 only** (Roadmap Phase 4) — not part of Stage 1-2 deliverables.

**Viewer Stage 1 (Roadmap Phase 1): Post-hoc static viewer.** Simulation runs in Docker, exports OME-Zarr data. Trame viewer loads and renders organism + tissue scales. No live server during simulation. **Build on Worm3DViewer.**

**Viewer Stage 2 (Roadmap Phase 2): Interactive dynamic viewer.** Full interactivity with time scrubbing, layer toggling, cell selection, inspector panel. Served via Trame or static OME-Zarr + Three.js. Data stays pre-computed but viewer is fully interactive. Pharynx, intestine, neuropeptides visible if enabled.

**Viewer Stage 3 (Roadmap Phase 4): WormSim 2.0.** The "Digital Organism In Your Browser" — **adds molecular scale** (gene expression, channel dynamics, intracellular compartments per [DD014.1](DD014.1_Visual_Rendering_Specification.md)), narrative-guided exploration, educational overlays. Hosted as static site on GitHub Pages or CDN. No Docker, no server, no installation.

### Phase 1: Evolve Worm3DViewer into the Canonical Post-Hoc Viewer

**What changes from current Worm3DViewer:**

| Current (v0.0.8) | Phase 1 Target (v1.0) |
|------------------|----------------------|
| Streamlit + stpyvista (static iframe) | **Trame** (PyVista + live server, real animation) |
| Reads `position_buffer.txt` (custom text) | Reads **OME-Zarr** (standardized, chunked, streamable) |
| Three separate views side-by-side | **Single integrated scene** with layer toggle (body, neurons, muscles) |
| Hardcoded file paths | Reads from `openworm.yml` output directory |
| No time animation in web mode | **Full time scrubbing** with slider and play/pause |
| No cell selection | **Click any cell** to see its ID, type, and time-series data |
| No color-by-activity mapping | **Neurons/muscles colored by activity** (voltage → heatmap) |
| v0.0.8 prototype | v1.0 with Docker integration, CI, documentation |

**Key architectural decision:** Use **Trame** (not raw Streamlit) as the web framework. Trame is Kitware's production web framework for VTK/PyVista, supports both server-side rendering (for large datasets) and client-side vtk.js rendering (for small datasets), and is actively maintained. This preserves the existing PyVista investment in Worm3DViewer while solving the animation problem.

**Alternative considered — rewrite in Three.js now:** Rejected for Phase 1. A Three.js rewrite would require JavaScript expertise that may not exist in the community. Trame lets Python-fluent contributors (who already work with c302 and Sibernetic) build the viewer without learning a new language. Phase 2 or 3 may migrate to Three.js + WebGPU for the public experience.

### Simulation Output Format: OME-Zarr

All simulation subsystems must export their time-varying state to a common format that the viewer can consume. **OME-Zarr** is the standard:

```
output/
├── openworm.zarr/                    # Root Zarr store
│   ├── .zattrs                       # Global metadata (config, duration, dt)
│   ├── body/                         # [DD003](DD003_Body_Physics_Architecture.md): SPH particle positions
│   │   ├── positions/                # Shape: (n_timesteps, n_particles, 3)
│   │   ├── types/                    # Shape: (n_particles,) — liquid/elastic/boundary
│   │   ├── cell_ids/                 # Shape: (n_particles,) — [DD004](DD004_Mechanical_Cell_Identity.md) cell identity (when enabled)
│   │   └── .zattrs                   # Particle count, dt, coordinate units
│   ├── neural/                       # [DD001](DD001_Neural_Circuit_Architecture.md): Neuron state
│   │   ├── voltage/                  # Shape: (n_timesteps, 302)
│   │   ├── calcium/                  # Shape: (n_timesteps, 302)
│   │   ├── positions/                # Shape: (302, 3) — static neuron positions
│   │   ├── neuron_ids/               # Shape: (302,) — neuron names
│   │   └── .zattrs                   # Neuron count, dt, class labels
│   ├── muscle/                       # [DD002](DD002_Muscle_Model_Architecture.md): Muscle state
│   │   ├── activation/               # Shape: (n_timesteps, 95)
│   │   ├── calcium/                  # Shape: (n_timesteps, 95)
│   │   ├── positions/                # Shape: (95, 3) — muscle center positions
│   │   ├── muscle_ids/               # Shape: (95,) — muscle names (MDR01-MDR24, etc.)
│   │   └── .zattrs                   # Muscle count, quadrant mapping
│   ├── pharynx/                      # [DD007](DD007_Pharyngeal_System_Architecture.md): Pharyngeal state (when enabled)
│   │   ├── pumping_state/            # Shape: (n_timesteps, 3) — corpus/isthmus/terminal_bulb
│   │   └── .zattrs
│   ├── intestine/                    # [DD009](DD009_Intestinal_Oscillator_Model.md): Intestinal state (when enabled)
│   │   ├── calcium/                  # Shape: (n_timesteps, 20) — per intestinal cell
│   │   ├── defecation_events/        # Shape: (n_events, 3) — timestamp, type (pBoc/aBoc/Exp)
│   │   └── .zattrs
│   ├── neuropeptides/                # [DD006](DD006_Neuropeptidergic_Connectome_Integration.md): Peptide state (when enabled)
│   │   ├── concentrations/           # Shape: (n_timesteps, n_peptides, 302) — per-neuron concentrations
│   │   └── .zattrs
│   ├── validation/                   # [DD010](DD010_Validation_Framework.md): Validation results
│   │   ├── tier2_report.json
│   │   ├── tier3_report.json
│   │   └── .zattrs
│   └── geometry/                     # Static 3D geometry (loaded once)
│       ├── body_surface.obj          # Reconstructed smooth body surface from particles
│       ├── neuron_morphologies/      # NeuroML-derived neuron meshes (from Worm3DViewer)
│       ├── muscle_meshes/            # VirtualWorm body wall muscle mesh
│       └── .zattrs                   # Geometry metadata, coordinate systems
```

**Why OME-Zarr:**

- **Chunked:** Browser fetches only the time window being viewed, not the entire dataset
- **Cloud-native:** Can be served from S3/GCS or a simple HTTP server (no custom backend)
- **Standardized:** Supported by Neuroglancer, Vitessce, napari — not an OpenWorm-specific format
- **Progressive loading:** Start viewing immediately while more data loads in background
- **Versioned metadata:** `.zattrs` stores provenance (config hash, simulation version, timestamps)

### Surface Reconstruction (Particles → Smooth Body)

The SPH particle cloud must be converted to a smooth surface for the Organism-scale view. Two approaches:

**Option 1: Marching Cubes on density field (recommended for Phase 1)**

- Compute a density field from particle positions (Gaussian kernel smoothing)
- Extract an isosurface via marching cubes (VTK's `vtkMarchingCubes`)
- Result: smooth triangulated mesh of the body surface
- Can be done post-hoc during export (not during simulation)
- PyVista has built-in support: `pv.wrap(points).reconstruct_surface()`

**Option 2: Mesh skinning from reference anatomy**

- Start with the VirtualWorm OBJ mesh (smooth anatomical surface)
- Deform it to match particle positions at each timestep (skinning)
- Higher visual quality but requires mapping between particles and mesh vertices
- Phase 2 work

### Color Mapping for Activity

The viewer maps simulation state to visual properties:

| Data | Visual Mapping | Colormap | Scale |
|------|---------------|----------|-------|
| Neuron voltage | Sphere/tube brightness | Blue (rest) → Red (depolarized) | -80 mV to +20 mV |
| Neuron [Ca²⁺] | Sphere/tube brightness | Black (0) → Yellow (high) | 0 to max_ca |
| Muscle activation | Mesh face color | Green (relaxed) → Red (contracted) | 0.0 to 1.0 |
| Intestinal [Ca²⁺] | Cell color gradient | Blue (low) → Red (high) | 0 to max_intestinal_ca |
| Pharynx pumping | Section opacity | Transparent (relaxed) → Opaque (contracted) | 0.0 to 1.0 |
| Neuropeptide concentration | Volumetric cloud | Transparent (low) → Colored (high) | 0 to max_conc |
| Particle type | Point color | Blue/Green/Gray (liquid/elastic/boundary) | Categorical |
| Cell identity ([DD004](DD004_Mechanical_Cell_Identity.md)) | Cell outline color | Per-tissue-type color | Categorical |

### Layer System

The viewer has toggleable layers, inspired by WormSim's skin/muscles/neurons toggle:

| Layer | What It Shows | Default State | Prerequisite |
|-------|-------------|---------------|-------------|
| **Body surface** | Smooth reconstructed surface from SPH particles | ON | [DD003](DD003_Body_Physics_Architecture.md) output |
| **Body particles** | Raw SPH particle cloud (scientific view) | OFF | [DD003](DD003_Body_Physics_Architecture.md) output |
| **Neurons** | 302 neuron morphologies colored by voltage/calcium | OFF | [DD001](DD001_Neural_Circuit_Architecture.md) output |
| **Muscles** | 95 body wall muscles colored by activation | ON | [DD002](DD002_Muscle_Model_Architecture.md) output |
| **Pharynx** | 63 pharyngeal cells with pumping animation | OFF | [DD007](DD007_Pharyngeal_System_Architecture.md) output + enabled |
| **Intestine** | 20 intestinal cells with calcium wave | OFF | [DD009](DD009_Intestinal_Oscillator_Model.md) output + enabled |
| **Neuropeptides** | Volumetric peptide concentration clouds | OFF | [DD006](DD006_Neuropeptidergic_Connectome_Integration.md) output + enabled |
| **Cell boundaries** | Per-cell outlines from [DD004](DD004_Mechanical_Cell_Identity.md) tagging | OFF | [DD004](DD004_Mechanical_Cell_Identity.md) output + enabled |
| **Validation overlay** | Green/red markers showing pass/fail per metric | OFF | [DD010](DD010_Validation_Framework.md) output |
| **Annotations** | Text labels on cells/structures (educational) | OFF | Static data |

### Viewer UI Layout

```
┌─────────────────────────────────────────────────────────────────┐
│  OpenWorm Simulation Viewer                    [Layers ▼] [⚙]  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│                                                                 │
│                   ┌─────────────────────┐                       │
│                   │                     │                       │
│                   │    3D Viewport      │   ┌────────────────┐  │
│                   │                     │   │ Inspector      │  │
│                   │  [Smooth worm body  │   │                │  │
│                   │   crawling, neurons │   │ Selected:      │  │
│                   │   glowing, muscles  │   │ AVAL (neuron)  │  │
│                   │   contracting]      │   │ V: -52.3 mV    │  │
│                   │                     │   │ Ca: 0.012 µM   │  │
│                   │                     │   │ Class: Command  │  │
│                   │                     │   │ ───────────────│  │
│                   └─────────────────────┘   │ [Voltage plot] │  │
│                                             │ [Calcium plot] │  │
│                                             └────────────────┘  │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│  ◀ ▶ ■   ━━━━━━━━━●━━━━━━━━━━━━━━━━━━   t=7.2ms / 15.0ms     │
│           Time: 0.0ms                                  15.0ms   │
└─────────────────────────────────────────────────────────────────┘
```

**Key interactions:**

- **Click** any cell/neuron/muscle → Inspector panel shows identity, state, time series
- **Scroll wheel** zooms between scales (organism → tissue → cell)
- **Layer toggle** shows/hides different subsystems
- **Time scrubber** plays, pauses, or scrubs through simulation time
- **Playback speed** adjustable (0.1× to 10×)

---

## Alternatives Considered

### 1. Keep Particle Cloud Rendering Only

**Rejected:** The particle cloud is scientifically useful but communicates nothing to non-scientists. It does not show cellular structure, neural activity, or multi-scale dynamics. The worm looks like a colored blob.

### 2. Revive Geppetto as the Visualization Platform

**Rejected:** Geppetto is maintained but is a heavy Java-based platform with a complex deployment model. It requires per-client server processes and has not been updated for WebGPU. The WormSim frontend built on Geppetto is 10 years stale. Starting fresh on modern tooling (Trame → Three.js) is more practical.

### 3. Build Directly in Three.js + WebGPU (Skip Trame)

**Deferred to Phase 2/3:** A pure Three.js viewer would be optimal for the public experience (no server, static hosting, best performance). But it requires JavaScript expertise and a longer development timeline. Phase 1 builds on the existing PyVista/Python ecosystem to get a working viewer faster, then Phase 2 ports the interactive experience to the browser.

### 4. Use Neuroglancer

**Rejected for primary viewer:** Neuroglancer is optimized for volumetric EM data, not dynamic simulation state. It could be useful for viewing the static EM data that underlies cell boundary definitions ([DD004](DD004_Mechanical_Cell_Identity.md)), but it cannot play back time-varying particle simulations or display ion channel dynamics.

### 5. Use Unity/Unreal for a Game-Engine Experience

**Rejected:** Game engines produce beautiful results but create a walled garden. They don't run in a browser without heavy WASM builds, require proprietary toolchains, and are unfamiliar to scientific contributors. The web platform (WebGPU + Three.js) achieves comparable visual quality while remaining open and accessible.

---

## Quality Criteria

1. **Animation works in the browser.** The viewer must support full time playback (play, pause, scrub) when accessed via a web browser. Static iframes are not acceptable.

2. **Smooth body surface.** The organism-scale view must show a smooth, recognizable worm shape, not a particle cloud. Non-scientists must be able to identify it as a worm.

3. **Activity visualization.** Neuron voltage and muscle activation must be visually distinguishable in the tissue/cell-scale view. A human observer must be able to see which neurons are firing and which muscles are contracting.

4. **Layer independence.** Each layer must be independently toggleable without affecting other layers' rendering or performance.

5. **Performance.** The viewer must maintain >15 FPS for a standard simulation (100K particles, 302 neurons, 95 muscles) on a 2020-era laptop with integrated GPU.

6. **Data format compliance.** All simulation output consumed by the viewer must be in OME-Zarr format (or documented interim formats during migration).

7. **Cell selection.** A user must be able to click on any visible cell/neuron/muscle and see its identity and state in an inspector panel.

8. **Reproducible deployment.** The viewer must be launchable via `docker compose run viewer` with no additional setup.

---

## Integration Contract

### Inputs (What This Subsystem Consumes)

| Input | Source DD | Variable | Format | Units |
|-------|----------|----------|--------|-------|
| SPH particle positions (all timesteps) | [DD003](DD003_Body_Physics_Architecture.md) | Per-particle (x, y, z) over time | OME-Zarr: `body/positions/` | µm |
| Particle types | [DD003](DD003_Body_Physics_Architecture.md) | Per-particle type (liquid/elastic/boundary) | OME-Zarr: `body/types/` | enum |
| Particle cell IDs (when enabled) | [DD004](DD004_Mechanical_Cell_Identity.md) | Per-particle cell identity | OME-Zarr: `body/cell_ids/` | WBbt ID |
| Neuron voltage time series | [DD001](DD001_Neural_Circuit_Architecture.md) | Per-neuron membrane voltage | OME-Zarr: `neural/voltage/` | mV |
| Neuron calcium time series | [DD001](DD001_Neural_Circuit_Architecture.md) | Per-neuron [Ca²⁺]ᵢ | OME-Zarr: `neural/calcium/` | mol/cm³ |
| Neuron 3D positions | [DD001](DD001_Neural_Circuit_Architecture.md) / [DD008](DD008_Data_Integration_Pipeline.md) | Static 3D coordinates for 302 neurons | OME-Zarr: `neural/positions/` | µm |
| Neuron morphologies | [DD001](DD001_Neural_Circuit_Architecture.md) (c302) | NeuroML cell files with segment geometry | `.cell.nml` files (static) | µm |
| Muscle activation time series | [DD002](DD002_Muscle_Model_Architecture.md) | Per-muscle activation [0, 1] | OME-Zarr: `muscle/activation/` | dimensionless |
| Muscle calcium time series | [DD002](DD002_Muscle_Model_Architecture.md) | Per-muscle [Ca²⁺]ᵢ | OME-Zarr: `muscle/calcium/` | mol/cm³ |
| Muscle 3D positions | [DD002](DD002_Muscle_Model_Architecture.md) / [DD008](DD008_Data_Integration_Pipeline.md) | Static 3D coordinates for 95 muscles | OME-Zarr: `muscle/positions/` | µm |
| Muscle 3D meshes | VirtualWorm project | OBJ mesh of body wall muscles | `bwm.obj` (static) | µm |
| Neuron 3D meshes | VirtualWorm project | OBJ mesh of neuron anatomy | `neurons.obj` (static) | µm |
| Pharyngeal pumping state | [DD007](DD007_Pharyngeal_System_Architecture.md) | Per-section contraction over time | OME-Zarr: `pharynx/pumping_state/` | [0, 1] |
| Intestinal calcium per cell | [DD009](DD009_Intestinal_Oscillator_Model.md) | Per-cell [Ca²⁺] over time | OME-Zarr: `intestine/calcium/` | µM |
| Defecation events | [DD009](DD009_Intestinal_Oscillator_Model.md) | pBoc/aBoc/Exp timestamps | OME-Zarr: `intestine/defecation_events/` | ms |
| Neuropeptide concentrations | [DD006](DD006_Neuropeptidergic_Connectome_Integration.md) | Per-peptide, per-neuron concentration over time | OME-Zarr: `neuropeptides/concentrations/` | µM |
| Validation results | [DD010](DD010_Validation_Framework.md) | Tier 1/2/3 pass/fail + metrics | JSON in `validation/` | mixed |
| Simulation config | [DD013](DD013_Simulation_Stack_Architecture.md) | `openworm.yml` used for this run | Zarr `.zattrs` metadata | — |

### Outputs (What This Subsystem Produces)

| Output | Consumer | Variable | Format | Units |
|--------|----------|----------|--------|-------|
| Interactive 3D viewer | Human users (scientists, public) | Web application on port 8501 | HTML + WebGL/vtk.js | — |
| Screenshot / video export | [DD013](DD013_Simulation_Stack_Architecture.md) (output pipeline), publications | Static images or MP4 from viewer | PNG, MP4 | pixels |
| Selected cell state (inspector) | Human users | Time series for selected cell | In-app plot | mV, µM, etc. |

### Configuration (`openworm.yml` Section)

```yaml
visualization:
  enabled: true                      # Generate viewer-compatible output
  export_format: "zarr"              # "zarr" (OME-Zarr, recommended) or "legacy" (position_buffer.txt)
  surface_reconstruction: true       # Convert particles to smooth surface mesh
  export_interval: 10                # Export every Nth simulation timestep (reduces file size)

viewer:
  enabled: false                     # Launch viewer service in docker-compose
  port: 8501                         # Web UI port
  backend: "trame"                   # "trame" (Phase 1) or "threejs" (Phase 2/3, future)
  default_layers:                    # Which layers are ON by default
    - body_surface
    - muscles
  colormap:
    neurons: "coolwarm"              # Blue (rest) → Red (depolarized)
    muscles: "RdYlGn_r"             # Green (relaxed) → Red (contracted)
    intestine: "hot"                 # Black → Red → Yellow
```

### Docker Build

- **Repository:** `openworm/Worm3DViewer` (existing repo, to be evolved)
- **Docker stage:** `viewer` in multi-stage Dockerfile (new stage)
- **`versions.lock` key:** `worm3dviewer`
- **Build dependencies:** `pip install pyvista trame trame-vtk trame-vuetify zarr ome-zarr libneuroml pyneuroml`
- **Dockerfile addition:**

```dockerfile
# === Stage: Viewer ===
FROM base AS viewer
RUN pip install pyvista trame trame-vtk trame-vuetify zarr ome-zarr libneuroml pyneuroml
RUN apt-get update && apt-get install -y libxrender1 libgl1-mesa-glx xvfb
COPY --from=full /opt/openworm/output /opt/openworm/output
COPY viewer/ /opt/openworm/viewer/
```

### Docker Compose Service

```yaml
# docker-compose.yml (new service)
  viewer:
    build:
      context: .
      target: viewer
    command: >
      python3 /opt/openworm/viewer/app.py
        --data /opt/openworm/output/openworm.zarr
        --port 8501
    ports:
      - "8501:8501"
    volumes:
      - ./output:/opt/openworm/output
    depends_on:
      - simulation
```

**Usage:**
```bash
# Run simulation first, then launch viewer
docker compose run simulation
docker compose up viewer
# Open http://localhost:8501 in browser
```

### Integration Test

```bash
# Step 1: Verify OME-Zarr export is generated
docker compose run simulation
ls output/openworm.zarr/
# Verify: body/, neural/, muscle/ directories exist
# Verify: .zattrs contains simulation metadata

# Step 2: Verify viewer launches
docker compose up -d viewer
curl -s http://localhost:8501/ | grep -q "OpenWorm"
# Verify: HTTP 200, page contains "OpenWorm"

# Step 3: Verify data loads correctly
docker compose run shell python -c "
import zarr
z = zarr.open('output/openworm.zarr', mode='r')
assert 'body' in z, 'Missing body group'
assert 'neural' in z, 'Missing neural group'
assert z['body/positions'].shape[1] > 0, 'No particles'
assert z['neural/voltage'].shape[1] == 302, 'Expected 302 neurons'
print('Zarr validation passed')
"

# Step 4: Verify surface reconstruction
docker compose run shell python -c "
import pyvista as pv
import numpy as np
import zarr
z = zarr.open('output/openworm.zarr', mode='r')
points = np.array(z['body/positions'][0])  # First timestep
cloud = pv.PolyData(points)
surface = cloud.reconstruct_surface()
assert surface.n_cells > 0, 'Surface reconstruction failed'
print(f'Surface: {surface.n_cells} faces, {surface.n_points} vertices')
"

# Step 5: Verify backward compatibility
docker compose run quick-test  # with visualization.export_format: "legacy"
# Must still produce position_buffer.txt for Worm3DViewer v0.0.8 compatibility
```

### Coupling Dependencies

| I Depend On | DD | What Breaks If They Change |
|-------------|----|-----------------------------|
| Particle positions format | [DD003](DD003_Body_Physics_Architecture.md) | If SPH output format changes, Zarr export script must update |
| Neuron state output | [DD001](DD001_Neural_Circuit_Architecture.md) | If calcium/voltage file format or neuron count changes, neural Zarr group breaks |
| Muscle activation output | [DD002](DD002_Muscle_Model_Architecture.md) | If activation format changes, muscle Zarr group breaks |
| Cell identity (particle tagging) | [DD004](DD004_Mechanical_Cell_Identity.md) | If cell_id scheme changes, cell-based coloring/selection breaks |
| Pharyngeal output format | [DD007](DD007_Pharyngeal_System_Architecture.md) | If pumping state format changes, pharynx layer breaks |
| Intestinal output format | [DD009](DD009_Intestinal_Oscillator_Model.md) | If calcium per-cell format changes, intestine layer breaks |
| Neuropeptide output format | [DD006](DD006_Neuropeptidergic_Connectome_Integration.md) | If concentration format changes, neuropeptide volumetric layer breaks |
| Validation report format | [DD010](DD010_Validation_Framework.md) | If report JSON schema changes, validation overlay breaks |
| Docker compose structure | [DD013](DD013_Simulation_Stack_Architecture.md) | If output directory or service naming changes, viewer service breaks |
| VirtualWorm 3D meshes | External (Caltech/WormBase) | If mesh coordinates or structure change, anatomy layers break |
| NeuroML cell morphologies | [DD001](DD001_Neural_Circuit_Architecture.md) (c302) | If cell morphology files change, neuron rendering breaks |

| Depends On Me | DD | What Breaks If I Change |
|---------------|----|-----------------------------|
| Simulation stack (export step) | [DD013](DD013_Simulation_Stack_Architecture.md) | If Zarr schema changes, `master_openworm.py` export step must update |
| Contributor onboarding | [DD011](DD011_Contributor_Progression_Model.md) | If viewer Docker service changes, L0 orientation task B1 instructions must update |
| N2-Whisperer orientation | AI Agents | If viewer URL/port changes, N2-Whisperer "run simulation" instructions must update |
| Output pipeline | [DD013](DD013_Simulation_Stack_Architecture.md) | If screenshot/video export changes, automated output generation changes |

---

## Implementation Roadmap

### Viewer Stage 1: Post-Hoc Trame Viewer (Roadmap [Phase 1](DD_PHASE_ROADMAP.md#phase-1-cell-type-differentiation-months-1-3), Weeks 1-8)

Build on Worm3DViewer, evolve from Streamlit+stpyvista to Trame.

| Task | Owner | Effort | Dependency |
|------|-------|--------|------------|
| Add OME-Zarr export to `master_openworm.py` | Integration Maintainer | 16 hrs | [DD013](DD013_Simulation_Stack_Architecture.md) Phase A |
| Port Worm3DViewer from Streamlit to Trame | Visualization L4 | 24 hrs | None |
| Implement time scrubbing (slider + play/pause) | Visualization L4 | 8 hrs | Trame port |
| Implement layer toggle system | Visualization L4 | 8 hrs | Trame port |
| Implement surface reconstruction (marching cubes) | Visualization L4 | 8 hrs | OME-Zarr export |
| Add neuron voltage → color mapping | Visualization L4 | 4 hrs | OME-Zarr export |
| Add muscle activation → color mapping | Visualization L4 | 4 hrs | OME-Zarr export |
| Add cell click → inspector panel | Visualization L4 | 8 hrs | Trame port |
| Add Docker stage + compose service | Integration Maintainer | 4 hrs | [DD013](DD013_Simulation_Stack_Architecture.md) Phase A |
| Add to CI (build + smoke test) | Integration Maintainer | 4 hrs | Docker stage |

**Deliverable:** `docker compose up viewer` serves a web app with time-animated, multi-layer, interactive 3D worm at `localhost:8501`.

### Viewer Stage 2: Interactive Dynamic Viewer (Roadmap [Phase 2](DD_PHASE_ROADMAP.md#phase-2-slow-modulation-closed-loop-sensory-months-4-6), Weeks 9-20)

Enhance the viewer with deeper interactivity and begin Three.js migration for public deployment.

| Task | Owner | Effort | Dependency |
|------|-------|--------|------------|
| Add pharynx layer (when enabled) | Visualization L4 | 8 hrs | [DD007](DD007_Pharyngeal_System_Architecture.md) output |
| Add intestine layer (when enabled) | Visualization L4 | 8 hrs | [DD009](DD009_Intestinal_Oscillator_Model.md) output |
| Add neuropeptide volumetric layer (when enabled) | Visualization L4 | 16 hrs | [DD006](DD006_Neuropeptidergic_Connectome_Integration.md) output |
| Add validation overlay (green/red pass/fail markers) | Visualization L4 | 4 hrs | [DD010](DD010_Validation_Framework.md) output |
| Mesh skinning (VirtualWorm mesh deformed by particles) | Visualization L4 | 24 hrs | Stage 1 surface |
| Begin Three.js + WebGPU prototype | Visualization L4 + community | 40 hrs | Stage 1 data pipeline |
| Static OME-Zarr hosting (no server required for viewing) | Integration Maintainer | 8 hrs | OME-Zarr export |
| Multi-scale zoom (organism → tissue transition) | Visualization L4 | 16 hrs | All layers working |

**Deliverable:** Full tissue/cell-scale exploration. Early Three.js prototype for server-free deployment.

### Viewer Stage 3: WormSim 2.0 — "A Digital Organism In Your Browser" (Roadmap [Phase 4](DD_PHASE_ROADMAP.md#phase-4-mechanical-cell-identity-high-fidelity-visualization-months-13-18), Weeks 21-32+)

The full WormSim vision, rebuilt on modern technology. Deploys to `wormsim.openworm.org` as a static site. browser.openworm.org redirects here once WormBrowser feature parity is achieved (see Deployment Plan below).

| Task | Owner | Effort | Dependency |
|------|-------|--------|------------|
| Complete Three.js + WebGPU viewer | Visualization L4 + community | 80 hrs | Stage 2 prototype |
| OME-Zarr served from cloud storage (GitHub Pages, S3) | Integration Maintainer | 8 hrs | Stage 2 static hosting |
| Narrative-guided onboarding (tutorial mode) | Community contributor | 24 hrs | Three.js viewer |
| Educational annotations (cell labels, biology facts) | Community contributor | 16 hrs | Three.js viewer |
| Molecular-scale view (ion channels, Ca dynamics) | Visualization L4 | 40 hrs | Three.js viewer |
| Mobile-responsive design | Community contributor | 16 hrs | Three.js viewer |
| WebXR support (VR/AR exploration) | Community contributor | 24 hrs | Three.js viewer |
| Deploy to `wormsim.openworm.org` (static site) | Integration Maintainer | 4 hrs | Three.js viewer |
| Verify WormBrowser feature parity (see checklist) | Visualization L4 | 4 hrs | All Stage 3 features |
| Redirect browser.openworm.org → wormsim.openworm.org | Integration Maintainer | 2 hrs | Feature parity confirmed |
| MyBinder/Colab integration (zero-install demo) | Community contributor | 8 hrs | Stage 1 Trame viewer |

**Deliverable:** Anyone with a browser can visit `wormsim.openworm.org` and explore a dynamic, multi-scale simulation of *C. elegans* — no Docker, no installation, no server.

---

## The End-State Vision

When the full system is running (all phases complete), a user visiting `wormsim.openworm.org` would experience:

**Organism Scale (default view):**
A smooth, translucent *C. elegans* crawling across the screen. Body bends propagate anterior to posterior. The pharynx pumps rhythmically at 3-4 Hz at the head. Every ~50 seconds, a visible contraction wave runs posterior-to-anterior as the defecation motor program fires.

**Click "Show Muscles":**
The body becomes semi-transparent. 95 body wall muscles appear in four quadrants (dorsal right, ventral right, ventral left, dorsal left). As the worm crawls, you see alternating dorsal-ventral contraction waves — muscles flash red when contracting, green when relaxed. The undulatory locomotion pattern is immediately visible.

**Click "Show Neurons":**
302 neurons appear as glowing spheres and dendrite/axon tubes embedded in the body. Command interneurons (AVA, AVB, AVD, AVE, PVC) pulse with graded potentials. Motor neurons fire rhythmically, driving the muscle contraction pattern. You can see the neural basis of locomotion in real time.

**Click on a single neuron (e.g., AVAL):**
An inspector panel slides open showing: neuron name, class (command interneuron), WormBase ID, real-time voltage trace, calcium trace, all pre/post-synaptic partners highlighted in the 3D view. Links to WormBase and WormAtlas for biological context.

**Zoom into the pharynx:**
The 63-cell pharyngeal organ fills the viewport. 20 pharyngeal muscles contract synchronously in a pumping rhythm. Pharyngeal neurons (M1-M5, I1-I6, MC, MI, NSM) are visible with their distinct firing patterns. The grinder at the terminal bulb crushes (future: bacteria particles flowing through the lumen).

**Zoom into the intestine:**
20 intestinal cells arranged in a tube. A calcium wave propagates posterior-to-anterior, coloring cells from blue to red as [Ca²⁺] rises and falls. Every ~50 seconds, the wave triggers the defecation motor program — you see the contraction propagate through the body.

**Toggle "Neuropeptides":**
Faint volumetric clouds appear between neurons, showing neuropeptide diffusion fields. Slow modulatory signaling visible as colored mist that waxes and wanes on a seconds timescale, overlaid on the fast synaptic activity.

**Toggle "Validation":**
Green checkmarks appear on subsystems passing validation (locomotion speed within ±15% of experimental data, pumping frequency 3-4 Hz, defecation period 40-60s). Red marks highlight any deviations.

**This is WormSim 2.0** — the fulfillment of the 2014 Kickstarter promise, rebuilt with 2026 technology. Not a static anatomy browser, not a particle cloud, not a matplotlib plot — a living, dynamic, multi-scale simulation that anyone can explore in a web browser, backed by the most complete computational model of any organism ever built. When this launches, browser.openworm.org redirects here.

---

## Deployment Plan: From WormBrowser to WormSim 2.0

### What's Live Where, When

| Phase | browser.openworm.org | wormsim.openworm.org | Docker viewer |
|-------|---------------------|---------------------|---------------|
| Phase A | WormBrowser (legacy, live) | Does not exist | — |
| Phase 1 | **WormBrowser enhanced** — click neuron/cell → links to WormAtlas + WormBase | Does not exist | `docker compose up viewer` → Trame at localhost:8501 |
| Phase 2 | WormBrowser enhanced (continues) | Three.js prototype (may lack some WormBrowser features) | Trame viewer continues |
| Phase 3 | WormBrowser enhanced (continues) | Three.js with organ systems (approaching parity) | Trame viewer continues |
| Phase 4 | **Redirects → wormsim.openworm.org** | **WormSim 2.0** — full public experience | Trame viewer continues (local dev) |

### Phase 1 Quick Win: WormBrowser Enhancement

The existing WormBrowser at browser.openworm.org gets a targeted enhancement in Phase 1 — not a full rewrite, just adding click-to-identify with database links:

- **Click any neuron** → tooltip/panel shows: neuron name, class (sensory/inter/motor), [WormAtlas](https://wormatlas.org) link, [WormBase](https://wormbase.org) link
- **Click any muscle** → similar links
- JavaScript patch to the existing legacy codebase (jQuery + open-3d-viewer)
- Estimated effort: ~8-16 hours (AI-assisted)
- Directly addresses John White's Feb 12 request: *"click on and identify a particular neuron and have a link"*
- Ships to browser.openworm.org independently of WormSim 2.0 development
- Timeline: gives John a tangible result for the April 10, 2026 NYC prize meeting

### WormBrowser Feature Parity Checklist

WormSim 2.0 must have ALL of the following before browser.openworm.org redirects to it:

**WormBrowser features (must match):**

- [ ] 3D anatomy from VirtualWorm meshes (688 meshes, 37 material categories)
- [ ] Layer peeling / opacity control (opacity slider)
- [ ] Individual layer toggles (cuticle, organs, muscles, neurons)
- [ ] Search by cell name
- [ ] Click any cell → identify it (name, type, links to WormAtlas + WormBase)
- [ ] Zero installation (works in any WebGL/WebGPU browser)
- [ ] Static hosting (no server process required)

**WormSim 2.0 additions (why users switch):**

- [ ] Simulation data overlay (neurons fire, muscles contract, organs pump)
- [ ] Time scrubbing (play, pause, scrub through simulation)
- [ ] Inspector panel (click cell → voltage trace, calcium trace, connections)
- [ ] Multi-scale zoom (organism → tissue → molecular)
- [ ] Validation overlay (pass/fail vs. experimental data)

**John White requirements (phased):**

- [ ] Click neuron → links to WormAtlas and WormBase — **Phase 1 quick win on existing WormBrowser**
- [ ] Multiple developmental stages (L1, L4, adult) — from [Witvliet et al. 2021](https://doi.org/10.1038/s41586-021-03778-8) EM reconstructions (Phase 4+)
- [ ] Dauer larva anatomy — from [Yim et al. 2024](https://doi.org/10.1038/s41467-024-45943-3) (Phase 4+)
- [ ] Male anatomy — from [Cook et al. 2019](https://doi.org/10.1038/s41586-019-1352-7) male connectome (Phase 4+)
- [ ] Comparative species view — *Pristionchus pacificus* and other nematodes (Phase 5+)
- [ ] Stage/sex comparison mode (Phase 4+)

---

## Boundaries (Out of Scope)

1. **Running simulation in the browser.** The viewer displays pre-computed results. Client-side simulation (WebGPU compute shaders running SPH) is a moonshot idea but not part of this DD.

2. **Gamification / scoring.** The viewer is an exploration tool, not a game. No points, levels, or achievements.

3. **Live multi-user collaboration.** The viewer is single-user. Real-time collaborative annotation is future work.

4. **VR hardware requirements.** WebXR support (Phase 3) works with standard browsers. No dedicated VR headset required.

5. **Editing simulation parameters.** The viewer is read-only. Changing parameters and re-running requires Docker. A future "interactive mode" could allow parameter tweaking but is not in this DD.

---

### Existing Code Resources

**NemaNode** ([openworm/NemaNode](https://github.com/openworm/NemaNode), 2024, dormant):
Interactive web-based map of neural connections (formerly nemanode.org). May contain reusable graph layout algorithms and layer toggle patterns for DD014's neural circuit visualization layer.

---

## References

1. **WormBrowser:** `openworm/wormbrowser` (Idili, 2012, [browser.openworm.org](https://browser.openworm.org)) — Static 3D anatomy browser, still live
1. **WormBrowser iOS:** `openworm/openwormbrowser-ios` (2013) — iOS companion app
1. **WormSim original vision:** `openworm/org.wormsim.frontend` (2014 Kickstarter, $121K raised from 799 backers, dormant since 2015)
2. **Worm3DViewer:** `openworm/Worm3DViewer` (Gleeson, 2025, v0.0.8, Streamlit + PyVista)
3. **Trame (Kitware):** https://kitware.github.io/trame/ — Production web framework for VTK/PyVista
4. **OME-Zarr specification:** https://ngff.openmicroscopy.org/ — Cloud-native bioimaging format
5. **Three.js WebGPU renderer:** https://threejs.org/ — r172+ with production WebGPU support
6. **VirtualWorm project:** 3D anatomical models of *C. elegans* (Caltech/WormBase)
7. **Neuroglancer:** https://github.com/google/neuroglancer — Multi-scale biological data viewer
8. **PyVista surface reconstruction:** https://docs.pyvista.org/ — `reconstruct_surface()` for marching cubes

---

- **Approved by:** Pending
- **Implementation Status:** Proposed
- **Next Actions:**

1. Evolve Worm3DViewer from Streamlit to Trame (Phase 1, critical path)
2. Implement OME-Zarr export in `master_openworm.py`
3. Implement surface reconstruction pipeline
4. Identify / recruit Visualization L4 Maintainer
5. Coordinate with Neural Circuit L4 Maintainer on Worm3DViewer evolution roadmap
