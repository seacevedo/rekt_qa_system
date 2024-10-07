# Rekt-Chat

This cryptocurrency space is ridden with hacks and exploits, and as such it has been heavily criticized. Many articles, webistes, blogs, and the like have been written about the crypto space shortcomings. One such website is https://www.web3isgoinggreat.com/, a project by Molly White, that displays the hacks that involve in this new technology. This project aims to use Retrieval-Augemented Generation (RAG) to synthesize the hack data provided by https://www.web3isgoinggreat.com/ to generate a knowledgebase that can be queried by a user to explore these hacks and aid in learning.

# Technologies and Requirements

* [Selenium](https://www.selenium.dev/) to scrape for hack data on https://www.web3isgoinggreat.com/.
* [Google Cloud](https://cloud.google.com/) to upload data to a google cloud bucket and use BigQuery as our data warehouse. We will use this mainly to host our monitoring solution.
* [Terraform](https://www.terraform.io/) for version control of our infrastructure.
* [Prefect](https://www.prefect.io/) will be used to orchestrate and monitor our pipeline. 
* [Elasticsearch](https://github.com/elastic/elasticsearch) to perform document retrieval for our RAG application.
* [Ollama](https://ollama.com/) to locally host our LLM models for our app. 
* [Looker Studio](https://lookerstudio.google.com/overview) to visualize our monitoring metrics. 
* [Pandas](https://pandas.pydata.org/) to import and transform our dataset.
* [Docker](https://www.docker.com/) to containerize our deployed model and application architecture
* [Docker Compose](https://docs.docker.com/compose/) for managing multiple docker containers used in this project

This project was developed and tested in a local environment with the following characteristics:

* **Operating System**: Ubuntu 22.04.1 LTS (Windows Subsystem for Linux)
* **CPU**:  AMD Ryzen 5 2600 Six-Core Processor
* **RAM**: 16 GB
* **GPU**: NVIDIA GeForce RTX 2060


# Architecture

# Environmental Setup and Configuration

Before you get started, ensure you have installed Pipenv (https://pipenv.pypa.io/en/latest/) to enable proper use of the environment bu running the command `pip install --user pipenv`. After installing, run the command `pipenv install` to install all the necessary libraries. 

## Setup Google Cloud 

1. Create a google cloud account
2. Setup a new google cloud [project](https://cloud.google.com/).
3. Create a new service account. Give the service account the `Compute Admin`, `Service Account User`, `Storage Admin`, `Storage Object Admin`, `Cloud Run Admin`, and `BigQuery Admin` Roles.
4. After the service account has been created, click on `Manage Keys` under the `Actions` Menu. Click on the `Add Key` dropdown and click on `Create new key`. A prompt should pop up asking to download it as a json or P12 file. Choose the json format and click `Create`. Save your key file.
5. Install the the [Google Cloud CLI](https://cloud.google.com/sdk/docs/install-sdk). Assuming you have an Ubuntu linux distro or similar as your environment, follow the directions for `Debian/Ubuntu`. Make sure you log in by running `gcloud init`. Choose the cloud project you created to use.
6. Set the environment variable to point to your downloaded service account keys json file:

`export GOOGLE_APPLICATION_CREDENTIALS=<path/to/your/service-account-authkeys>.json`

7. Refresh token/session, and verify authentication
`gcloud auth application-default login`

8. Make sure these APIs are enabled for your project:

* https://console.cloud.google.com/apis/library/iam.googleapis.com
* https://console.cloud.google.com/apis/library/iamcredentials.googleapis.com
* https://console.cloud.google.com/apis/library/compute.googleapis.com
* https://console.cloud.google.com/apis/library/run.googleapis.com

