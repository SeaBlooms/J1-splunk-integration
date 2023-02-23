from github import Github
import base64
import json

# using an access token
token = "x"
try:
    g = Github(token)
except Exception as e:
    print('GitHub Client Setup Failed. Exception: {}'.format(e))

repo = g.get_repo("ocsf/ocsf-schema")
contents = repo.get_contents("objects/device.json")

scontents = base64.b64decode(contents.content).decode("utf-8")

attributeKeys = json.loads(scontents)['attributes'].keys()

attributeList = list(attributeKeys)

attributeCSV = ",".join(attributeList)

print(attributeCSV)
