import requests
import json


import requests
import json
import csv


def make_request(method, host, lookup_name, lookup_content):

    baseurl = "https://{}:8089".format(host)

    # GET requests to this endpoint will execute get_lookup_contents()
    # POST requests to this endpoint will execute post_lookup_contents()
    # from the lookup_editor_rest_handler.py in the lookup-editor app
    splunk_management_service = "/services/data/lookup_edit/lookup_contents"  # endpoint lookup-editor
    splunk_lookup_table_service = "/servicesNS/admin/search/data/lookup-table-files"

    if method == "POST":

        r = requests.post(baseurl + splunk_management_service,
                          auth=("admin", "xx"),
                          verify=False,
                          data={"output_mode": "json",
                               "namespace": "search",
                               "lookup_file": lookup_name,
                               "contents": json.dumps(lookup_content)}
                          )

        return r

    elif method == "GET":
        r = requests.get(baseurl + splunk_lookup_table_service + lookup_name,
                         auth=("admin", "xx"),
                         verify=False).content
        return r
    else:
        return "method not implemented"


def fetch_csv(path):

    lookup_content = []

    try:
        with open(path, 'r') as file:
            csvreader = csv.reader(file)
            for row in csvreader:
                lookup_content.append(row)
    except Exception as e:
        print("Error reading {} : {}".format(path, e))

    return lookup_content


if __name__ == '__main__':

    r = make_request("GET", host="10.0.0.xx", lookup_name="assets.csv", lookup_content=None)
    print(r)

    # r = make_request(method="POST", lookup_name="assets.csv", lookup_content=fetch_csv("j1_asset_data.csv"))
    # print(r)
