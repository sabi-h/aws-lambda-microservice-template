### Template Data Pipeline


#### Stream function logs into your terminal
    sls logs --function [FUNCTION_NAME] --stage prod --tail


#### Initiate a new project
    python template/initiate_new_project.py


#### Install npm packages
    npm init
    npm install serverless@2.64 --save


#### Install Python dependencies
    cd REPOSITORY_NAME
    pipenv install


#### Stream function logs into your terminal
    prod-sls logs --function main --stage prod --tail


#### Testing:
    pytest . -v


#### Linting:
    black . --line-length 120


#### Create requirements.txt file:
    pipenv lock -r > requirements.txt


#### Invoke a function locally using dev and prod
    sls invoke local -f [FUNCTION_NAME] --path ./data/event.json
    sls invoke local -f [FUNCTION_NAME] --path ./data/event.json


#### Invoke a function
    sls invoke -f main --log


#### Deploy function
    prod-sls deploy --stage prod --verbose


### Setup

#### Install serverless plugin
    sls plugin install --name serverless-python-requirements
