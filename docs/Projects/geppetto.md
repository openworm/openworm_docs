Geppetto Simulation Engine
==========================

!!! note "Platform Evolution"
    Geppetto served as OpenWorm's primary simulation and visualization platform from 2014-2020. For Phase 1-2 work, it has been superseded by **[DD014 (Dynamic Visualization Architecture)](../design_documents/DD014_Dynamic_Visualization_Architecture.md)**, which specifies a Trame-based (Python) approach. See [Archived Projects](../archived_projects/#geppetto-web-platform-2014-2020) for full historical context.

[Geppetto](http://geppetto.org) is an open-source modular platform to enable multi-scale and multi-algorithm interactive simulation of biological systems. Geppetto features a built-in WebGL visualizer that offers out-of-the-box visualization of simulated models right in the browser.

Geppetto is written in Java and leverages technologies like [OSGi](http://www.osgi.org/), [Spring Framework](http://www.springsource.org/spring-framework), [OpenCL](http://www.khronos.org/opencl/) and [Maven](http://maven.apache.org/).

Geppetto's frontend is written using [THREE.js](https://github.com/mrdoob/three.js) and [WebGL](http://www.khronos.org/webgl/). Back-end / front-end communication happens via [JSON](http://www.json.org/) messages through [WebSocket](http://www.websocket.org/).

The definitive documentation for Geppetto [is available online](http://docs.geppetto.org).

## Why the Evolution?

[DD014](../design_documents/DD014_Dynamic_Visualization_Architecture.md) evaluated Geppetto against alternatives and chose Trame because:

- **Language mismatch:** Geppetto is Java; most OpenWorm contributors write Python
- **Scalability:** Requires a server process per client; doesn't work for a public viewer
- **Maintenance:** Not updated for WebGPU (the next generation of browser graphics)
- **Weight:** Trame is lighter and actively maintained

## Current Visualization Roadmap ([DD014](../design_documents/DD014_Dynamic_Visualization_Architecture.md))

| Phase | Technology | Capability |
|-------|-----------|------------|
| Phase 1 | Trame (PyVista) | Organism + tissue scales, live server |
| Phase 2 | Trame + layers | Neuropeptides, organs, validation overlay |
| Phase 3 | Three.js + WebGPU | Molecular scale, static site at viewer.openworm.org |

---

## Continue Reading

- **[DD014: Dynamic Visualization Architecture](../design_documents/DD014_Dynamic_Visualization_Architecture.md)** — The next-generation visualization specification
- **[Archived Projects](../archived_projects.md#geppetto-web-platform-2014-2020)** — Geppetto's historical context
- **[Worm Browser](browser.md)** — The original WebGL anatomy browser
- **[Projects Overview](../projects.md)** — All active projects and their governing DDs
