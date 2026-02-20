Docker simulation stack
==========================

We have created a [Docker container](https://docs.docker.com/guides/docker-concepts/the-basics/what-is-a-container/) which contains all of the major components of the simulation stack we have built so far (including [Sibernetic](../sibernetic/) and [c302](../c302/)). It can be used to run a preliminary model of the worm in 3D on your computer. 

![Docker](../../images/worm-crawling.gif)

Details on installing and using the OpenWorm Docker simulation stack can be found [here](https://github.com/openworm/OpenWorm/blob/master/README.md#quickstart).

The source code for this project can be found [here](https://github.com/openworm/OpenWorm).

!!! info "Governed by DD013"
    The Docker simulation stack architecture is specified by [DD013: Simulation Stack Architecture](../design_documents/DD013_Simulation_Stack_Architecture.md), which defines the containerized environment, CI/CD pipeline, and `openworm.yml` configuration format.

---

## Continue Reading

- **[DD013: Simulation Stack Architecture](../design_documents/DD013_Simulation_Stack_Architecture.md)** — Full specification of the Docker-based stack
- **[Sibernetic](sibernetic.md)** — The body physics engine inside the stack
- **[c302](c302.md)** — The neural network framework inside the stack
- **[How It Works: Modeling](../modeling.md)** — How all simulation components fit together
- **[Projects Overview](../projects.md)** — All active projects and their governing DDs