[![MIT License][license-shield]][license-url]
<a name="readme-top"></a>
<!-- PROJECT LOGO -->
<br />
<div align="center">

<h1 align="center">Cast.AI API Bot Helper 🤖</h1>

  <p align="center">
    A mechanism intended to run in k8s as a workload (e.g. cronjob) and consume Cast.AI API.<br />
    This sub-repo is provided as a blueprint - so one can clone and design their own functions/docker-image. <br />
    Please regard this project as a framework, additional functions may be added in the future.  <br />
  </p>
</div>



<!-- GETTING STARTED -->
## Getting Started

First things first - Install cluster hibernate and configure it. https://github.com/castai/hibernate
- This project relies on an API key stored in one of the projects secrets.
- Secret can also be created manually (instructions on how to set key in hibernate project)
- Defined in both pod and cronjob as follows
```    - name: API_KEY
      valueFrom:
        secretKeyRef:
          name: castai-hibernate
          key: API_KEY
```
Next there are several steps to achieve your end-goal of a custom CAST.AI API consuming bot.
1) Design your function (see [src/functions/example.py](../castai-api-bot-helper/src/functions/example.py) for an example)
   1) The function is built to digest a BotExecutionConfig ([src/models/bot_execution_config.py](../castai-api-bot-helper/src/models/bot_execution_config.py)) to make it easier to define inputs and env vars
   2) The config is passed via a config-map that needs to be deployed (see [api-bot-helper-function-config-example_configmap.yaml](../castai-api-bot-helper/api-bot-helper-function-config-example_configmap.yaml) for an example)
   3) The config can also be passed for testing purposed using [src/function_config.json](../castai-api-bot-helper/src/function_config.json)
2) Build you image using [helper_scripts/build-and_push.py](../castai-api-bot-helper/helper_scripts/build-and-push.py)
   1) Rename [helper_scritps/secrets.env.template](../castai-api-bot-helper/helper_scripts/secrets.env.template) to **helper_scritps/secrets.env** for registry credentials
   2) Set your Image name/tag in helper_scritps/constants.py
   3) Run [build-and-push.py](../castai-api-bot-helper/helper_scripts/build-and-push.py) to create your image that will be used in the k8s bot workload
   4) Set your image name/tag in either [api-bot-helper_pod.yaml](../castai-api-bot-helper/api-bot-helper_pod.yaml) or [api-bot-helper_cronjob.yaml](../castai-api-bot-helper/api-bot-helper_cronjob.yaml)
      1) you can also create your own type of k8s workload
   5) A configmap like api-bot-helper-function-config-example_configmap.yaml and the workload needs to be deployed in your cluster
3) In order to test the functionality locally before deploying:
   1) Configure [src/function_config.json](../castai-api-bot-helper/src/function_config.json) with right settings
   2) Set the `TEST_RUN` in [main.py](../castai-api-bot-helper/src/main.py) to True


### Folder Structure - And files documentation

castai-api-bot-helper\
    ├── helper_scripts  
    │  ├── [build-and-push.py](#build-and-push.py)\
    │  ├── [constants.py](#constants.py)\
    │  ├── [md_repo_structure_print.py](#md_repo_structure_print.py)\
    │  ├── [requirements.txt](#requirements.txt)\
    │  ├── [secrets.env](#secrets.env)\
    │  └── [secrets.env.template](#secrets.env.template)\
    ├── src  
    │  ├─ functions  
    │  │ └── [example.py](#example.py)\
    │  ├─ models  
    │  │  ├── [bot.py](#bot.py)\
    │  │  └── [bot_execution_config.py](#bot_execution_config.py)\
    │  ├── services  
    │  │  ├── [api_requests_svc.py](#api_requests_svc.py)\
    │  │  └── [request_handle_svc.py](#request_handle_svc.py)\
    │  ├── [constants.py](#constants.py)\
    │  ├── [function_confi.json](#function_confi.json)\
    │  ├── [main.py](#main.py)\
    │  ├── [requirements.txt](#requirements.tx)\
    │  ├── [test_config.env](#est_config.env)\
    │  └── [test_config.env.template](#test_config.env.template)\
    ├── [.dockerignore](#.dockerignore)\
    ├── [.gitignore](#.gitignore)\
    ├── [api-bot-helper-function-config-example_configmap.yaml](#api-bot-helper-function-config-example_configmap.yaml)\
    ├── [api-bot-helper_cronjob.yaml](#api-bot-helper_cronjob.yaml)\
    ├── [api-bot-helper_pod.yaml](#api-bot-helper_pod.yaml)\
    ├── [Dockerfile](#Dockerfile)\
    ├── [LICENSE.txt](#LICENSE.txt)\
    └── [README.md](#README.md)

| Item Number | Item Name                                                                                                                 | Documentation                              |
|-------------|---------------------------------------------------------------------------------------------------------------------------|--------------------------------------------|
| 1           | <a name="build-and-push.py"></a>build-and-push.py                                                                         | Creates docker image for the bot           |
| 2           | <a name="constants.py"></a>constants.py                                                                                   | Constants like the image name/tag          |
| 3           | <a name="md_repo_structure_print.py"></a>md_repo_structure_print.py                                                       | Created printout for README.md             |
| 4           | <a name="requirements.txt"></a>requirements.txt                                                                           | requirements for helper scripts            |
| 5           | <a name="secrets.env"></a>secrets.env                                                                                     | provides credentials for image registry    |
| 6           | <a name="secrets.env.template"></a>secrets.env.template                                                                   | .template needs to be removed to get #6    |
| 10          | <a name="example.py"></a>example.py                                                                                       | an example of a bot function               |
| 12          | <a name="bot.py"></a>bot.py                                                                                               | Bot Class                                  |
| 13          | <a name="bot_execution_config.py"></a>bot_execution_config.py                                                             | Bot Execution Configuration                |
| 15          | <a name="api_requests_svc.py"></a>api_requests_svc.py                                                                     | Used to consume Cast.AI API                |
| 16          | <a name="request_handle_svc.py"></a>request_handle_svc.py                                                                 | Actually handles the API request           |
| 17          | <a name="constants.py"></a>constants.py                                                                                   | Bot high-level constants                   |
| 18          | <a name="function_config.json"></a>function_config.json                                                                   | Used for local testing                     |
| 19          | <a name="main.py"></a>main.py                                                                                             | Entry point (can be augmented for testing) |
| 20          | <a name="requirements.txt"></a>requirements.txt                                                                           | Requirements.txt for Bot                   |
| 21          | <a name="test_config.env"></a>test_config.env                                                                             | Used for testing (cluster_id/API_KEY)      |
| 22          | <a name="test_config.env.template"></a>test_config.env.template                                                           | .template needs to be removed to get #21   |
| 23          | <a name=".dockerignore"></a>.dockerignore                                                                                 | For building the image                     |
| 24          | <a name=".gitignore"></a>.gitignore                                                                                       | Git ignore for repo                        |
| 25          | <a name="api-bot-helper-function-config-example_configmap.yaml"></a>api-bot-helper-function-config-example_configmap.yaml | Bot ConfigMap example                      |
| 26          | <a name="api-bot-helper_cronjob.yaml"></a>api-bot-helper_cronjob.yaml                                                     | Bot Cronjob example                        |
| 27          | <a name="api-bot-helper_pod.yaml"></a>api-bot-helper_pod.yaml                                                             | Bot Pod example                            |
| 28          | <a name="Dockerfile"></a>Dockerfile                                                                                       | Dockerfile for building the image          |
| 29          | <a name="LICENSE.txt"></a>LICENSE.txt                                                                                     | License File                               |
| 30          | <a name="README.md"></a>README.md                                                                                         | Repo README File                           |

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[license-shield]: https://img.shields.io/github/license/castai/solutions-engineering-lab.svg?style=for-the-badge
[license-url]: https://github.com/castai/solutions-engineering-lab/blob/main/castai-api-bot-helper/LICENSE.txt