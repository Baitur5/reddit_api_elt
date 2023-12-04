
# Reddit ELT pipilene
------
A data pipeline that extracts Reddit data for a Google Data Studio report, focusing on a specific subreddit. Motivated by interest in the subject and a desire to enhance skills, the project includes tools like dbt, Airflow, Docker, and cloud-based storage for added complexity.

## Architecture
![architecture](./images/architecture.png)

------

## Overview 
1. Data Extraction from [Reddit API](https://www.reddit.com/dev/api/)
2. Data Upload to [S3](https://aws.amazon.com/s3/)
3. To provision and manage AWS Resources with [Terraform](https://developer.hashicorp.com/terraform/intro)
4. Data Loading to [Redshift Serverless](https://aws.amazon.com/redshift/redshift-serverless/)
5. Data Transformation with [dbt](https://www.getdbt.com/)
6. [Apache Airflow](https://airflow.apache.org/) Orchestration in [Docker](https://www.docker.com/)
7. Visualizes transformed data with [Google Looker Studio](https://lookerstudio.google.com/)

## Result
[Link](https://lookerstudio.google.com/reporting/fdfc7645-fbee-47cc-a06f-25a40b2a61fa)



------
## Setup
- Clone the repository:
```bash
git clone https://github.com/Baitur5/reddit_api_elt.git
cd reddit_api_elt
```
- Get reddip api keys from [here](https://www.reddit.com/prefs/apps)
- You must have configured [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html)
- Create **variables.tf** file in the root directory and setup the following variables:
```terraform
variable "s3_bucket"{
    type = string
    default = ""
}

variable "namespace_name"{
    type = string
    default = ""
}

variable "workgroup_name"{
    type = string
    default = ""
}

# password for db admin
variable "password"{
    type = string
    default = ""
}
```
- Initialize terraform and Create resources:
```bash
terraform init
terraform apply
```
- Create **.env** file in the root directory and setup the following variables:
```bash
AIRFLOW_UID=
#client id from reddit api
CLIENT_ID =''
#secret key from reddit api
SECRET_KEY= ''
IAM_ROLE =''
S3_BUCKET =''
SUBREDDIT =''
WORKGROUP=''
```
- Setup airflow in docker:
```bash
docker compose up airflow-init
docker compose up
```
- Open http://localhost:8080/ and trigger dag
- [Transform data in Redshift with dbt](https://www.getdbt.com/partners/redshift)
- Setup Google Data Looker Studio and extract data from Redshift Serverless. For some tutorials
check [this out](https://support.google.com/looker-studio/answer/6283323?hl=en)

## Contributions and Issues
Contribute or report issues. Pull requests are welcome! Securely handle sensitive information like API keys and credentials.
