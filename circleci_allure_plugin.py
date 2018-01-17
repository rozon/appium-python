import os
import requests
import json
import subprocess
import sys

# pass xml allure dir and generated html allure dir arguments
xml_dir = sys.argv[1]
html_dir = sys.argv[2]
xml_history_dir = xml_dir + "/history"
html_history_dir = html_dir + "/history"


# get build id and job name
CIRCLE_BUILD_NUM = os.environ['CIRCLE_BUILD_NUM']
CIRCLE_JOB = os.environ['CIRCLE_JOB']
CIRCLE_BUILD_URL = os.environ['CIRCLE_BUILD_URL']
CIRCLE_PROJECT_USERNAME = os.environ['CIRCLE_PROJECT_USERNAME']
CIRCLE_PROJECT_REPONAME = os.environ['CIRCLE_PROJECT_REPONAME']
TOKEN = os.environ['TOKEN']

buildName = "build #" + CIRCLE_BUILD_NUM
reporturl = True


# create executor json file
# add trend and executor information to allure report
def create_executor_json():
    executor = {}
    executor["buildName"] = buildName
    executor["buildOrder"] = CIRCLE_BUILD_NUM
    executor["reportName"] = "AllureReport"
    executor["name"] = "CircleCI"
    executor["buildUrl"] = CIRCLE_BUILD_URL
    if reporturl is True:
        executor["reportUrl"] = get_current_allure_url()
    executor["type"] = "circleci"
    executor["url"] = "https://circleci.com/gh/" + CIRCLE_PROJECT_USERNAME + \
        '/' + CIRCLE_PROJECT_REPONAME
    with open('./' + xml_dir + '/executor.json', 'w') as file:
        file.write(json.dumps(executor))


# create executor.json and exit if current build is the first successful build
try:
    CIRCLE_PREVIOUS_BUILD_NUM = os.environ['CIRCLE_PREVIOUS_BUILD_NUM']
except KeyError:
    reporturl = False
    create_executor_json()
    quit()


# requests get the allure artifact url via circleci api
def get_current_allure_url():
    api_url = "https://circleci.com/api/v1.1/project/"
    vcs_type = "github"
    url = api_url + vcs_type + '/' + CIRCLE_PROJECT_USERNAME + '/' +\
        CIRCLE_PROJECT_REPONAME + '/' + CIRCLE_PREVIOUS_BUILD_NUM

    response = requests.get(url + "/artifacts?circle-token=" + TOKEN)
    data = json.loads(response.text)
    header = 'https://' + CIRCLE_PREVIOUS_BUILD_NUM
    for i in data:
        if header in i['url'] and '/index.html' in i['path']:
            allure_artifact_url = i['url']
            html_path = i['path']
    allure_url = allure_artifact_url.replace(
        CIRCLE_PREVIOUS_BUILD_NUM, str(CIRCLE_BUILD_NUM), 1)
    current_allure_url = allure_url.replace(
        html_path, html_dir + "/index.html")
    return current_allure_url


'''
os.system('export CIRCLE_ALLURE_REPORT="' + CIRCLE_ALLURE_REPORT + '"')

subprocess.call(['export', 'CIRCLE_ALLURE_REPORT="' + /
    CIRCLE_ALLURE_REPORT + '"'])

payload = '{"build_parameters": {"CIRCLE_ALLURE_REPORT": "' + \
    CIRCLE_ALLURE_REPORT + '"}}'
requests.post(url + '?circle-token=' + TOKEN, data = payload)
'''

# execute command line, move history dir from last build to current build
try:
    subprocess.call(['rm', '-rf', xml_history_dir])
    subprocess.call(['mv', html_history_dir, xml_history_dir])
except:
    pass


# execute function to create executor.json file
# add information to allure report
create_executor_json()
