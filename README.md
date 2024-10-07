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
