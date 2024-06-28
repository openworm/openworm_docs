Geppetto Simulation Engine
==========================

In order to allow the world to play with the model easily, we are engineering [Geppetto](http://geppetto.org), an open-source modular platform to enable multi-scale and multi-algorithm interactive simulation of biological systems. Geppetto features a built-in WebGL visualizer that offers out-of-the-box visualization of simulated models right in the browser. You can read about architectural concepts and learn more about the different plug-in bundles we are working on.

Geppetto, is written in Java and leverages technologies like [OSGi](http://www.osgi.org/), [Spring Framework](http://www.springsource.org/spring-framework), [OpenCL](http://www.khronos.org/opencl/) and [Maven](http://maven.apache.org/).

Geppetto's frontend is written using [THREE.js](https://github.com/mrdoob/three.js) and [WebGL](http://www.khronos.org/webgl/). Back-end / front-end communication happens via [JSON](http://www.json.org/) messages through [WebSocket](http://www.websocket.org/).

The engine runs on on Eclipse Virgo WebServer deployed on an Amazon [Elastic Compute Cloud](http://aws.amazon.com/ec2/) Linux instance.

The definitive documentation for Geppetto [is available online](http://docs.geppetto.org).
