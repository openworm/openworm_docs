NeuroMechanical Modeling - Sibernetic
=====================================

Sibernetic implements **[DD003 (Body Physics Architecture)](../design_documents/DD003_Body_Physics_Architecture.md)** — the formal specification for SPH-based body mechanics.

## What It Does

Simulates the _C. elegans_ body as ~100K particles using Smoothed Particle Hydrodynamics (SPH):

| Particle Type | Count | Role | DD Reference |
|---------------|-------|------|--------------|
| Liquid | ~50K | Surrounding fluid medium | [DD003](../design_documents/DD003_Body_Physics_Architecture.md) |
| Elastic | ~30K | Body wall, muscles, cuticle | [DD003](../design_documents/DD003_Body_Physics_Architecture.md) |
| Boundary | ~20K | Substrate surface | [DD003](../design_documents/DD003_Body_Physics_Architecture.md), [DD022](../design_documents/DD022_Environmental_Modeling_and_Stimulus_Delivery.md) |

**Key algorithm:** PCISPH (Predictive-Corrective Incompressible SPH) pressure solver, implemented in C++ with GPU acceleration (OpenCL).

## Current Status (Phase 0)

**Accepted and working:**

- 3D body model with fluid-structure interaction
- Muscle activation produces emergent undulatory locomotion
- Validated against Schafer lab kinematics ([DD010](../design_documents/DD010_Validation_Framework.md) Tier 3: speed, wavelength, frequency within +/-15%)

To get a quick idea of what this looks like, check out the [latest movie](https://www.youtube.com/watch?v=SaovWiZJUWY). In this movie you can see a simulated 3D _C. elegans_ being activated in an environment. Its muscles are located around the outside of its body, and as they turn red, they are exerting forces on the body that cause the bending to happen.

## Roadmap

**Phase 1-2 ([DD004](../design_documents/DD004_Mechanical_Cell_Identity.md)):** Mechanical cell identity

- Per-particle cell IDs (map each SPH particle to one of 959 somatic cells)
- Cell-type-specific elasticity (neurons vs. muscles vs. hypodermal)

**Phase 2 ([DD022](../design_documents/DD022_Environmental_Modeling_and_Stimulus_Delivery.md)):** Environmental modeling

- Substrate types (agar, liquid, soil)
- Chemical/thermal gradients
- Food particles and obstacles

**Phase 4 ([DD014.2](../design_documents/DD014.2_Anatomical_Mesh_Deformation_Pipeline.md)):** Mesh deformation

- GPU skinning from SPH particles to Virtual Worm anatomical meshes
- Photorealistic rendering

## Previous accomplishments

-   Physics tests
-   Initial worm crawling
-   Published: [Sarma et al. 2018](https://doi.org/10.1098/rstb.2017.0382)

## Issues list

All issues related to the [Sibernetic code base](https://github.com/openworm/OpenWorm/issues?direction=desc&labels=sibernetic&page=1&sort=comments&state=open) can be found on GitHub.

## Associated Repositories

| Repository | Description | Language |
|------------|-------------|----------|
| [Smoothed-Particle-Hydrodynamics](https://github.com/openworm/Smoothed-Particle-Hydrodynamics) | The Sibernetic code base — C++ implementation of SPH customised for OpenWorm | C++ |
| [ConfigurationGenerator](https://github.com/openworm/ConfigurationGenerator) | Generation of start scene configuration for PCISPH solver | JavaScript |
| [CyberElegans](https://github.com/openworm/CyberElegans) | Circa 2010 neuromechanical prototype ([archived](../archived_projects.md#cyberelegans-2010-2014)) | C++ |

---

## Continue Reading

- **[DD003: Body Physics Architecture](../design_documents/DD003_Body_Physics_Architecture.md)** — The governing specification for Sibernetic
- **[c302](c302.md)** — The neural network framework that drives Sibernetic
- **[Docker simulation stack](docker.md)** — Running the complete simulation
- **[Validation Framework](../validation.md)** — How body physics outputs are validated
- **[Projects Overview](../projects.md)** — All active projects and their governing DDs
