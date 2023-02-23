from github import Github
import base64
import json

# using an access token
token = "xxBwUVNpxX60URWO3d9ArUwf1yAegK"
g = Github(token)

repo = g.get_repo("ocsf/ocsf-schema")
contents = repo.get_contents("objects/device.json")

scontents = base64.b64decode(contents.content).decode("utf-8")

attributeKeys = json.loads(scontents)['attributes'].keys()

attributeList = list(attributeKeys)

attributeCSV = ",".join(attributeList)

print(attributeCSV)
