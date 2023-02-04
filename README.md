# kpmg-pipeline
Pipeline for the KPMG use case made for BeCode trainees.

# Prerequisites
- Python (we used version 3.8+)
- Docker

Before running the code you need to provide .env file with the following credentials

## Algolia Database
APP_ID=

API_SEARCH_KEY=

API_ADMIN_KEY=

DB_NAME=

## OpenAI API Key
API_KEY_OPENAI=

## Azure Blob storage
AZURE_CONNECTION_STRING=

STORAGE_CONTAINER=

# Steps to make it run

1. After cloning the repos to your computer, create a virtual environment using python `python -m venv venv_kpmg_uc`
2. Install python dependencies `pip install -r requirements.txt`
3. To make sure the start script is executable open a terminal and inside the **scripts** folder run `chmod +x start.sh` (if there is an issue, do the command with root privileges) 
4. Run the ***start.sh*** script from the root of the project `bash scripts/start.sh` or `./scripts/start.sh` (again, you might have to use the root privileges to run the script depending on how you configured docker)
5. Wait until the docker images are built, you'll know when you see in your terminal that Airflow has setup the webserver.
6. Open a browser and go the your localhost using port 8080 `127.0.0.1:8080` or `localhost:8080` (the port can be changed in the docker-compose.yaml file)
7. Connect to the Airflow webserver with the user `airflow` and password `airflow` (which can also be changed in the docker-compose.yaml file)

Now you can see the Airflow dashboard and run the DAG manually or leave it scheduled and wait for it to run (which should be every 15 minutes)

# API
Here is the link to the repo's API project

https://github.com/isidoracupara/kpmg-pipeline_API_deployment

# Dashboard
In the dashboard folder you will have access to the Tableau file.

## Presentation
[Here is the presentation about the project](https://github.com/KNobles/kpmg-pipeline/blob/3994fc59e09e878d42ff5e88d219e4ac22a57a54/2022%2012%2023%20BeCode%20Brussels%20KPMG%20UseCase.pdf)
