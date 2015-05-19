# LCI-FIC2-SE
Source code for modules of the Context Aware Recommendation specific enabler.
Two server side modules are available:
  - Activity and Context Recognition module for classification of user activity and putting it in context. Additional information in the corresponding folder.
  - Recommendation Matrix Preparation module for composing recommendation matrix based on context/activity profiles and POI attributes. Additional information in the corresponding folder.

We also provide the Mobile application module for collecting contextual and sensory data from mobile devices. Additional information in the corresponding folder.

## Requirements:
- Django
- Python
- Cordova
- JavaScript

## Using Docker containers

Docker installation guide: https://docs.docker.com/installation/#installation

Dockeruser guide for starting Docker images: https://docs.docker.com/userguide/

Docker file for the Activity and Context Recognition module is located here: https://github.com/VizLoreLabs/LCI-FIC2-SE/tree/master/Activity_and_Context_Recognition
- Run it on port 8089: docker run -d -p 8089:8089 docker_id
- You can use the smoke test script (https://github.com/VizLoreLabs/LCI-FIC2-SE/tree/master/Activity_and_Context_Recognition/tests) to see if REST APIs are up:  ./docker_smoketest.sh host port

Docker file for the Recommendation Matrix Preparation module is located here: https://github.com/VizLoreLabs/LCI-FIC2-SE/tree/master/Recommendation_Matrix_Preparation
- Run it on port 4545:  docker run -d -p 4545:4545 docker_id
- You can use the smoke test script (https://github.com/VizLoreLabs/LCI-FIC2-SE/tree/master/Recommendation_Matrix_Preparation) to see if REST APIs are up:  ./docker_smoketest.sh host port

When Docker images are up and running and smoke test is successful, you can use the demo Android application to test activity and context aware POI recommendation: https://github.com/VizLoreLabs/LCI-FIC2-SE/tree/master/Mobile_App_Module
- Make sure to specify base URL (host:port) for both Docker instances in the settings menu of the installed demo application.

