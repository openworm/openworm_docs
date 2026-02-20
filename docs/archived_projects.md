Archived Projects & Historical Context
=======================================

OpenWorm has evolved significantly since 2011. These projects were important milestones but have been **superseded by current [Design Documents](design_documents/index.md)**.

**Principle:** We don't delete history — we contextualize it. Understanding where we came from helps explain where we're going.

---

## CyberElegans (2010-2014)

**Repository:** [openworm/CyberElegans](https://github.com/openworm/CyberElegans)

**What it was:** Our original neuromechanical prototype demonstrating feasibility — the first proof that coupling neurons, muscles, and body physics in a computer could produce locomotion-like behavior.

[Watch the CyberElegans prototype](https://www.youtube.com/watch?v=3uV3yTmUlgo)

**What it proved:**

- SPH is the right approach for body physics (now formalized in [DD003](design_documents/DD003_Body_Physics_Architecture.md))
- Graded synapses match _C. elegans_ biology better than spiking models (now formalized in [DD001](design_documents/DD001_Neural_Circuit_Architecture.md))
- Muscle calcium is the coupling variable between neural and mechanical domains (now formalized in [DD002](design_documents/DD002_Muscle_Model_Architecture.md))

**Current status:** Superseded by [DD001](design_documents/DD001_Neural_Circuit_Architecture.md)–[DD003](design_documents/DD003_Body_Physics_Architecture.md) (the formal, validated core chain). Preserved as historical reference and [DD017](design_documents/DD017_Hybrid_Mechanistic_ML_Framework.md) comparison point.

**See today's version:** [Sibernetic](Projects/sibernetic.md) (body physics) and [c302](Projects/c302.md) (neural modeling)

---

## Geppetto Web Platform (2014-2020)

**Repository:** [openworm/org.geppetto](https://github.com/openworm/org.geppetto)

**Website:** [geppetto.org](http://geppetto.org)

**What it was:** A Java-based, open-source modular platform for multi-scale and multi-algorithm interactive simulation of biological systems. Featured WebGL visualization, OSGi modularity, and Tomcat deployment.

**Technologies:** Java, OSGi, Spring Framework, Three.js, WebGL, Maven, Eclipse Virgo

**What it achieved:**

- Proved web-based simulation visualization was possible
- Grew into a general-purpose platform used by other neuroscience projects
- Demonstrated multi-algorithm integration concepts that inform [DD013](design_documents/DD013_Simulation_Stack_Architecture.md)

**Why the evolution:** [DD014 (Dynamic Visualization)](design_documents/DD014_Dynamic_Visualization_Architecture.md) chose Trame (Python + PyVista) over Geppetto because:

- Geppetto is Java-based — most OpenWorm contributors write Python
- Requires a server process per client — doesn't scale for public viewer
- Not updated for WebGPU — the next generation of browser graphics
- Trame is lighter, Python-native, and actively maintained

**Current status:** Dormant in OpenWorm (last commit ~2020). Still maintained upstream at [geppetto.org](http://geppetto.org). Could be re-evaluated if needs change.

**See today's version:** [Geppetto project page](Projects/geppetto.md) (historical context and DD014 evolution roadmap)

**What replaced it:** [DD014](design_documents/DD014_Dynamic_Visualization_Architecture.md) specifies a 3-phase evolution:

1. **Phase 1:** Trame viewer (PyVista + live server)
2. **Phase 2:** Interactive layers with validation overlays
3. **Phase 3:** Three.js + WebGPU static site at viewer.openworm.org

---

## movement_validation (Original Analysis Toolbox)

**Repository:** [openworm/movement_validation](https://github.com/openworm/movement_validation) (archived)

**What it was:** Original Python port of the Schafer lab's MATLAB behavioral analysis code. Used to compare simulated worm behavior against the WormBehavior database.

**What it achieved:**

- Established the principle of quantitative behavioral validation
- Ported key feature extraction algorithms from MATLAB to Python

**Current status:** Superseded by [open-worm-analysis-toolbox](https://github.com/openworm/open-worm-analysis-toolbox), which is being revived per [DD021](design_documents/DD021_Movement_Analysis_Toolbox_and_WCON_Policy.md). The toolbox revival is an infrastructure priority, as it enables [Tier 3 behavioral validation](validation.md).

**See today's version:** [Movement Analysis](Projects/worm-movement.md) project page

---

## NeuroConstruct Connectome

**What it was:** The original 3D anatomical model of the _C. elegans_ nervous system in NeuroML format, loaded and simulated via NeuroConstruct + NEURON.

**What it evolved into:** [c302](https://github.com/openworm/c302) — the current multi-scale modeling framework specified by [DD001](design_documents/DD001_Neural_Circuit_Architecture.md). c302 generates NeuroML2 networks at multiple biophysical detail levels (A-D) and uses [ConnectomeToolbox (cect)](https://github.com/openworm/ConnectomeToolbox) for data access ([DD020](design_documents/DD020_Connectome_Data_Access_and_Dataset_Policy.md)).

**See today's version:** [c302 project page](Projects/c302.md)

---

## Connectome Engine / Lego Robot

**What it was:** A simplified version of the _C. elegans_ connectome integrated into a Lego Mindstorms EV3 robot, demonstrating that connectome-derived dynamics could control physical movement.

[Watch the Lego robot in action](https://www.youtube.com/watch?v=D8ogHHwqrkI)

**What it proved:** Connectome-derived neural dynamics can produce meaningful sensorimotor behavior even in a simplified robot body.

**Current status:** Historical demonstration. The underlying principle (connectome-driven behavior) is now formalized in [DD001](design_documents/DD001_Neural_Circuit_Architecture.md) + [DD019 (closed-loop touch response)](design_documents/DD019_Closed_Loop_Touch_Response.md).

**See today's version:** [C. elegans Robots](Projects/c-elegans-robot.md) project page

---

## Pattern

Each archived project follows the same story:

1. **Prototype proved a concept** (2011-2016)
2. **Concept was formalized into Design Documents** (2018-2026)
3. **Design Documents now specify quantitative acceptance criteria** that the prototypes never had

The journey from "cool demo" to "validated engineering blueprint" is what makes OpenWorm's current approach fundamentally different from where we started.

---

**See [Design Documents](design_documents/index.md) for the current formal specifications.**

---

## Continue Reading

- **[Design Documents](design_documents/index.md)** — The complete roadmap from 302 neurons to 959 cells
- **[How It Works: Modeling](modeling.md)** — The current multi-scale simulation architecture
- **[Full History](fullhistory.md)** — Detailed timeline from 1900 to present
- **[Projects](projects.md)** — Active projects and their governing DDs
