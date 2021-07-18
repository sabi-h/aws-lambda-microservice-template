# README #

This README documents necessary steps to get this application up and running.


### OnMusic Data Pipeline


#### Copy/Sync data across s3 buckets or folders
    prod-aws s3 sync s3://[SRC_BUCKET_NAME]/[SRC_KEY]/ s3://[SRC_BUCKET_NAME]/[SRC_KEY]/


#### Stream function logs into your terminal
    prod-sls logs --function backfill --stage prod --tail


#### Testing:
    prod-python -m pytest utils_test.py


#### Linting:
    black . --line-length 120


#### Create requirements.txt file:
    pipenv lock -r > requirements.txt


#### Invoke a function locally using dev and prod
    dev-sls invoke local -f [FUNCTION_NAME] --path ./data/event.json
    prod-sls invoke local -f [FUNCTION_NAME] --path ./data/event.json


#### Invoke a function
    sls invoke -f [FUNCTION_NAME] --log


#### Deploy function
    sls deploy -v

### Setup

#### Install serverless plugin
    sls plugin install --name serverless-python-requirements
    sls plugin install --name serverless-dotenv-plugin


#### Install psycopg2 module

Download and copy this folder inside the lambda repo, and rename from `psycopg2-3.8` to `psycopg2`:
https://github.com/jkehler/awslambda-psycopg2/tree/master/psycopg2-3.8


#### Use Boto3 to query data in redshift
https://aws.amazon.com/blogs/big-data/using-the-amazon-redshift-data-api-to-interact-with-amazon-redshift-clusters/


## Arcticles to read:

- **[Lambda Orchestration Example](https://docs.aws.amazon.com/step-functions/latest/dg/sample-lambda-orchestration.html)**

- **[Multiple ETL Jobs using Lambdas](https://aws.amazon.com/blogs/big-data/orchestrate-multiple-etl-jobs-using-aws-step-functions-and-aws-lambda/)**

- [Functional Data Processing](https://maximebeauchemin.medium.com/functional-data-engineering-a-modern-paradigm-for-batch-data-processing-2327ec32c42a)

- [MonoRepo vs PolyRepo](https://www.fourtheorem.com/blog/monorepo#:~:text=Polyrepo%20is%20when%20multiple%20source,kept%20in%20a%20single%20repository.)
    - "A new developer should be able to start working on your product as quickly as possible. Avoid unnecessary ceremony and any learning curve that is unique to your team or company."

- [CSV - READ and WRITE using python](https://thepythonguru.com/python-how-to-read-and-write-csv-files/)

- [Redshift replacing existing rows](https://docs.aws.amazon.com/redshift/latest/dg/merge-replacing-existing-rows.html)
