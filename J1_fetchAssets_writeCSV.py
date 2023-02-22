import requests
import json
import csv
import os.path


def const():

    # Account-Level API Key - Admin Group
    acct = "xx-4cf7-4271-aa69-4a34d302347d"
    token = "xx89ed1579eace262c1e6d9399b0a771bdd0b6d553b31363736393230383636353039"

    return [acct, token]


def make_headers(token, acct):

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(token),
        "Jupiterone-Account": acct
    }

    return headers


def make_request(method, url, headers, data):

    if method == "POST":
        r = requests.post(url, headers=headers, json=data, verify=True)
        return r
    else:
        return "method not implemented"


def get_assets():
    # GraphQL query to get alerts
    query = '''
            query J1QL($query: String!, $variables: JSON, $cursor: String, $scopeFilters: [JSON!], $flags: QueryV1Flags) {
          queryV1(query: $query, variables: $variables, cursor: $cursor, scopeFilters: $scopeFilters, flags: $flags) {
            type
            data
            cursor
          }
        }
            '''

    data = {
        "query": query,
        "variables": {
            "query": "FIND (Device | Host)"
        }
    }

    headers = make_headers(const()[1], const()[0])
    r = make_request("POST", "https://graphql.us.jupiterone.io", headers, data)
    rdict = json.loads(r.content.decode('utf-8'))
    return rdict


if __name__ == '__main__':

    # Run GraphQL query to fetch all Device & Host entities from J1
    r = get_assets()
    # print(json.dumps(r, indent=1))

    asset_data_list = r['data']['queryV1']['data']
    # print(json.dumps(asset_data_list[0], indent=1))

    asset_csv_list = []

    for asset in asset_data_list:

        entityname = asset['entity']['displayName']

        try:
            owner = asset['properties']['owner']
        except KeyError as e:
            owner = "Not Found"

        asset_data_row = [entityname, owner]
        asset_csv_list.append(asset_data_row)

    # csv_headers = [ip,mac,nt_host,dns,owner,priority,lat,long,city,country,bunit,category \
    # pci_domain,is_expected,should_timesync,should_update,requires_av,cim_entity_zone]
    csv_headers = ['nt_host', 'owner']

    # write Asset List to CSV for Upload
    with open('j1_asset_data.csv', 'w', newline='') as csvfile:
        wr = csv.writer(csvfile, quoting=csv.QUOTE_ALL)

        # write lookup headers
        wr.writerow(csv_headers)

        # loop list and write row per item
        for i in asset_csv_list:
            wr.writerow(i)

    if os.path.isfile('j1_asset_data.csv'):
        print('CSV File written successfully')
    else:
        print('Error Occurred.. Check Script')
