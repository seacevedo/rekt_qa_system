# Rekt-Chat

This cryptocurrency space is ridden with hacks and exploits, and as such it has been heavily criticized. Many articles, webistes, blogs, and the like have been written about the crypto space shortcomings. One such website is https://www.web3isgoinggreat.com/, a project by Molly White, that displays the hacks that involve in this new technology. This project aims to use Retrieval-Augemented Generation (RAG) to synthesize the hack data provided by https://www.web3isgoinggreat.com/ to generate a knowledgebase that can be queried by a user to explore these hacks and aid in learning. We will use the LLAMA 3.1 Model to generate responses to a user's question in a containerized application.

# Technologies and Requirements

* [Selenium](https://www.selenium.dev/) to scrape for hack data on https://www.web3isgoinggreat.com/.
* [Google Cloud](https://cloud.google.com/) to upload data to a google cloud bucket and use BigQuery as our data warehouse. We will use this mainly to host our monitoring solution.
* [Terraform](https://www.terraform.io/) for version control of our infrastructure.
* [Prefect](https://www.prefect.io/) will be used to orchestrate and monitor our pipeline. 
* [Elasticsearch](https://github.com/elastic/elasticsearch) to perform document retrieval for our RAG application.
* [Ollama](https://ollama.com/) to locally host our LLM models for our app.
* [LLama 3.1](https://ai.meta.com/blog/meta-llama-3-1/) to generate responses for our user's questions. 
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

Before you get started, clone this repo ensure you have installed Pipenv (https://pipenv.pypa.io/en/latest/) to enable proper use of the environment bu running the command `pip install --user pipenv`. After installing, run the command `pipenv install` to install all the necessary libraries. 

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

9. Install [Terraform](https://www.terraform.io/)
10. `cd` to the `terraform` directory and enter the commands `terraform init`, `terraform plan`, and `terraform apply`. You can remove the corresponding infrastructure by using `terraform destroy`. For the plan and destroy commands you will be prompted to input the following variables:

| Variable       | Description  |
| ------------- |:-------------:|
| GOOGLE_CLOUD_PROJECT_ID      | ID of the google cloud project | 
| GOOGLE_CLOUD_REGION     | Region that your google cloud project is hosted in  | 
| BQ_DATASET_ID | ID of your bigquery dataset   | 
| GOOGLE_CLOUD_BUCKET_NAME | Bucket name you want to add csv files too   |

11. Create a new bigquery table named `documents` in your BigQuery dataset schema by clicking on the ellipsis next to it and then selecting `Create`. Upload the file `datasets/web3isgoinggreat_test_bq_dataset.csv` to create the `documents` table. Follow the same steps to create the `metrics` table, but leave it blank.

## Setup Docker

You should now install Docker. Use the following commands, in order:

 *  `sudo apt-get install ca-certificates curl gnupg`
 *  `sudo install -m 0755 -d /etc/apt/keyrings`
 *  `curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg`
 *  `sudo chmod a+r /etc/apt/keyrings/docker.gpg`
 *  `echo "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null`
 *  `sudo apt-get update -y`
 *  `sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y`
 *  `sudo apt install docker-compose -y`

## Setup Prefect

1. Move into the `flows` directory using the `cd flows` command. Then run the docker containers using the following commands, in order:
   * `docker compose build`
   * `docker compose up`
2. You should now have an environment setup to run your Prefect pipeline. This pipeline extracts new hack data that is from the past week. You may need to adjust the `is_date_in_current_week` function in `fetch_hack_data.py` file to simulate retrieving data from a single week if no hacks have been reported in the past week.
3. Access `http://localhost:4200/` to access the Prefect dashboard. Set up the following blocks to access GCP credentials, Buckets, and BigQuery:

| Block Name       | Description  |
| ------------- |:-------------:|
| gcp-creds      | Block pertaining to your Google cloud credentials. You need the JSON keyfile you downloaded earlier to set it up | 
| rekt-gcs   | Block pertaining to the bucket you wish to load the data into | 

4. Run the command `docker-compose exec prefect sh` to access the shell withing the Docker environment. Run `python3 -m main_flow` to set up a deployment. You can run the deployment by accessing the Prefect dashboard and clickin on `deployments`. On the top-right corner, click `Run`` and the `Quick Run`. You will be prompted to add the folloeing parameters

| Parameter       | Description  |
| ------------- |:-------------:|
| file_name      | Base Name of dataset file scrapped fromweb3isgoinggreat.com | 
| data_path   | path where datasets will be saved to | 

Set file_name to `crypto_hacks` and data_path to `/home/seacevedo/flows/datasets/` and confirm. You should see an instance of this Pipeline running.

## Setup RAG Application

1. Move into the `app` directory using the `cd app` command. Then run the docker containers using the following commands, in order:
   * `docker compose build`
   * `docker compose up`
2. Your Docker environment should be ready and your app should be able to be accessed from the `http://localhost:8501/` url. You are ready to use the application and ask any questions. Data is retrieved from the `documents` table you set up earlier. After a user's response is generated, they have the option to upload their feedback which is uploaded to the `metrics` table.

## Setup Monitoring using Looker Studio

1. Navigate to Looker Studio (https://lookerstudio.google.com/overview) and log in using your Google account. Click on `Blank Report`, and then select `BigQuery`, followed by `My Projects`. Select your project followed by the appropriate dataset, and select the `metrics` table. AN example of this can be seen in the following link: https://lookerstudio.google.com/reporting/44d64c0f-b66e-4bcb-96d0-401d981b2f1a. 

# Retrieval Evaluation

1. Retrieval Evaluation tests how well a system retrieves documents that answer a given query. For this project we use the Hit Rate (HR) and Mean Reciprocal Rank (MRR) metrics to evaluate retrieval performance:

**Hit Rate Formula:**

\[
\text{Hit Rate} = \frac{\text{Number of Hits}}{\text{Total Opportunities}} \times 100
\]

Where:
- **Number of Hits** = successful outcomes (e.g., successful sales, accurate predictions)
- **Total Opportunities** = total number of attempts or chances
