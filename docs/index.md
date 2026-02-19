Introduction to OpenWorm
========================

Welcome
-------

[OpenWorm](http://www.openworm.org) is an open source project and open science community dedicated to creating the world's first whole organism in a computer, a _C. elegans_ nematode, via bottom-up "systems biology" computational modeling.

It is an association of highly motivated scientists, engineers, coders, and curious citizens from around the world who believe in open science and open access.

Table Of Contents
-----------------

- **[Design Documents](design_documents/)** — Technical roadmap to 959-cell organism
- [Modeling Approach](modeling/) — How we model at 5 scales simultaneously
- [Validation](validation/) — How we know it's working (3-tier framework)
- [Projects](projects/) — Active repositories and their governing DDs
- [Community](community/) — Get involved, contribute, join meetings
- [Background](background/) — History, why _C. elegans_, modeling concepts
- [Resources](Resources/resources/) — Simulation engines, data sets, tools
- [Frequently Asked Questions](faq/)

The Path to 959 Cells
---------------------

OpenWorm is on a **quantified, validated path** from today's 302-neuron simulation to a complete 959-cell adult hermaphrodite, organized into **7 implementation phases** over ~18 months:

| Phase | Milestone | What Gets Added |
|-------|-----------|----------------|
| **Phase 0** | First Whole-Nervous-System Simulation | 302 neurons + 95 muscles + body physics (working today) |
| **Infrastructure Bootstrap** | Containerized Stack with Automated Validation | Docker, CI/CD, contributor workflow (4 weeks) |
| **Phase 1** | Biologically Distinct Neurons | 128 neuron classes from CeNGEN (3 months) |
| **Phase 2** | The Worm Can Feel and Modulate | Neuropeptides + closed-loop touch (3 months) |
| **Phase 3** | Multi-Organ Digital Organism | Pharynx, intestine, egg-laying (6 months) |
| **Phase 4** | 959-Cell Photorealistic Organism | All somatic cells, public web viewer (6 months) |
| **Future** | Intracellular, Developmental, Male | Gene regulation, growth, mating (Year 2+) |

**See [Design Documents](design_documents/)** for the complete technical specifications.

Mission/Vision
--------------

The complexity of computational neuroscience and biology make it extremely difficult to sort through the myriad of facts, data, and biological processes that are uncovered on a daily basis by researchers around the world.

OpenWorm believes that the challenges of solving brain simulation, even for the simplest of model organisms, require open access and collaborative solutions.

OpenWorm is actively working to achieve its goal of creating the world's first virtual organism in a computer by:

> -   bringing together highly motivated scientists and engineers in an open space
> -   pushing away all the red tape by taking open science to the extreme
> -   fostering growth of a completely open computational biology community

Goal
----

Our main goal is to build the world's first virtual organism - an <i>in-silico</i> implementation of a living creature - for the purpose of achieving an understanding of the events and mechanisms of living cells. Our secondary goal is to enable, via simulation, unprecedented <i>in-silico</i> experiments of living cells to power the next generation of advanced systems biology analysis, synthetic biology, computational drug discovery and dynamic disease modeling.

Navigating OpenWorm
-------------------

We've created this documentation to help orient you to the different locations on the web where OpenWorm material is found and where contributions can be made.

The **[Design Documents](design_documents/)** provide the complete technical roadmap — 25 architectural specifications (DD001-DD023) defining how we build from 302 neurons to 959 cells, validated against experimental data at every level. **Start here** if you want to understand the engineering blueprint.

The [modeling approach page](modeling/) explains how we model at five scales simultaneously (molecular, channel, cellular, tissue, organism) and how the current architecture evolved from the CyberElegans prototype.

The [validation page](validation/) explains our 3-tier framework (DD010) for ensuring the simulation matches real worm behavior at single-cell, circuit, and behavioral levels.

The [resources page](Resources/resources/) has a gallery of content that has been produced by the project, including simulation engines, visualization environments, and data sets.

There are a lot of additional questions you may have about the project. We have assembled a [frequently asked questions (FAQ)](faq/) document to help you. You may also wish to use the search feature in our documentation (top left).

Contributing to OpenWorm
------------------------

We primarily use Slack to communicate and coordinate our daily activities, you are welcome to join us! For an invitation, fill out our [volunteer application form](https://goo.gl/3ncZWn).

**New contributors:** Check the [Design Documents](design_documents/) for areas matching your skills, then follow the [DD contribution workflow](Community/github/#contributing-to-design-document-implementation). The [contributor progression model (DD011)](design_documents/DD011_Contributor_Progression_Model.md) describes the path from Observer to Senior Contributor.

Then, please browse our [project list](projects/) to understand the different areas where work is happening. To put the projects in context, you will find it useful to read more about the big picture idea of the [modeling approach](modeling/) we are taking.

If you are interested in a specific programming language, check out links to issues specifically for [Python](https://github.com/openworm/OpenWorm/issues?direction=desc&labels=python&page=1&sort=comments&state=open) or [C++](https://github.com/openworm/OpenWorm/issues?direction=desc&labels=c%2B%2B&page=1&sort=comments&state=open).

If you have questions about specific things you find, please reach out on [Slack](http://openworm.org/contacts.html).

More information about the process of making a contribution is available on our [community page](community/).

While the heart of OpenWorm is computational modeling, we are always looking for people with talents beyond programming to contribute. Are you a graphic designer, writer, PR specialist or simply someone with a love of science and expertise to share? Please reach out to us at <info@openworm.org> to discuss opportunities with OpenWorm.
