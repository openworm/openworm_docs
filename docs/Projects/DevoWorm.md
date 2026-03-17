
# DevoWorm

The DevoWorm website is located at [devoworm.weebly.com](https://devoworm.weebly.com/). The website features links to 
educational, academic, media-related and collaborative opportunities associated with the project. DevoWorm is affiliated with the [OpenWorm Foundation](https://www.openworm.org/) and the [Orthogonal Research Laboratory](https://orthogonal-research.weebly.com/). We engage in Open Science, an encourage the use of Jupyter Notebooks, short video descriptions of research, and demos.

## Roadmap

DevoWorm is currently divided into three loosely-knit interest areas: developmental dynamics, cybernetics and digital morphogenesis, and reproduction and developmental plasticity. While our main interest is in the nematode _Caenorhabditis elegans_, we are also interested in cross-species comparative work.

**Developmental Dynamics** currently involves using secondary data collected from embryos along with bioinformatic and data science techniques to answer questions regarding the process of early embryogenesis and the timing of later morphogenesis. To address these problems, we have used number of innovative approaches. 

**Cybernetics and Digital Morphogenesis** has involved using platforms such as Morphozoic (Cellular Automata) or CompuCell3D (Cellular Potts Model) to better understand physical interactions during embryogenesis and morphogenesis. We have also explored the use of cybernetic models and concepts to better understand the general process of embryogenesis.

**Reproduction and Developmental Plasticity** involves utilizing an evo-devo approach to understand _Caenorhabditis elegans_ more generally. Our existing datasets and papers include a focus on larval development and life-history processes. This area of the project also features primary empirical data, based on formal experimental design.

Objective                                        | Examples                    
---                                              | ---
Developmental Dynamics (DD)                      | [Comparative Quantitative Embryogenesis](https://www.mdpi.com/2079-7737/5/3/33)
DD                                               | [Differentiation Trees and Maps](https://www.biorxiv.org/content/early/2016/07/07/062539)
DD                                               | [Embryo Networks and Developmental Connectomes](https://doi.org/10.1101/146035)
DD                                               | Time-series of Terminal Differentiation
Cybernetics and Digital Morphogenesis (C-DM)     | [Morphozoic (Cellular Automata)](https://www.researchgate.net/publication/311738597_Morphozoic_Cellular_Automata_with_Nested_Neighborhoods_as_a_Metamorphic_Representation_of_Morphogenesis)
C-DM                                             | [Cybernetic Embryo](https://www.academia.edu/33002276/Origins_of_the_Embryo_self-organization_through_cybernetic_regulation)
C-DM                                             | CompuCell 3D
Reproduction and Developmental Plasticity (R-DP) | [Experimental Evolution](https://rsos.royalsocietypublishing.org/content/3/11/160496)
R-DP                                             | [Life-history Plasticity](https://www.biorxiv.org/content/early/2016/03/24/045609)

## Repos in DevoWorm Github

Repo Name                                                                       | Description               
---                                                                             | ---                       
[Google Summer of Code 2017](https://github.com/devoworm/GSoC-2017)             | GSoC Activities for 2017
[CC3D](https://github.com/devoworm/CC3D-local)                                  | CompuCell 3D Models
[Embryogenetic Connectome](https://github.com/devoworm/embryogenetic-connectome)| Embryogenetic Connectome Analysis
[Assorted Notebooks](https://github.com/devoworm/devoworm.github.io)            | Project-related Jupyter Notebooks
[Graphical Visualization](https://github.com/devoworm/Graph-Code)               | Code for Graph Creation
[Datasets and Analysis](https://github.com/devoworm/DevoWorm)                   | Tools for Developmental Data Science
[Morphozoic](https://github.com/devoworm/Morphozoic)                            | Morphozoic Models

---

## Related Design Documents

DevoWorm's developmental dynamics work connects to several aspects of the OpenWorm simulation:

- **[Phase 6: Developmental Modeling](../design_documents/DD_PHASE_ROADMAP.md#phase-6-developmental-modeling-year-2)** — DevoWorm is the primary existing project for Phase 6 ("Worm That Grows"), which targets multi-stage simulation from L1 larva to adult
- **[DD005: Cell-Type Specialization](../design_documents/DD005_Cell_Type_Differentiation_Strategy.md)** — DevoWorm's differentiation trees add temporal dynamics to DD005's CeNGEN-based cell-type specification
- **[DD004: Mechanical Cell Identity](../design_documents/DD004_Mechanical_Cell_Identity.md)** — DevoWorm's CompuCell3D morphogenesis models inform body-scaling mechanics across developmental stages

---

## Continue Reading

- **[Design Documents](../design_documents/index.md)** — The complete technical roadmap
- **[How It Works: Modeling](../modeling.md)** — Multi-scale architecture overview
- **[Projects Overview](../projects.md)** — All active projects and their governing DDs
