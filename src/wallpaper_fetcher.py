import json
import requests

# default args
default_args = {
    "tagname": "",
    "categories": 100,
    "purity": 100,
    "sorting": "random",
    "atleast": "",
    "ratio": "",
    "pages": 1
}


def wallFetcher(wallheaven_api, args):
    global default_args
    if wallheaven_api == "":
        isWallheavenApi = False
        print("NO API")
        BASE_URL = "https://wallhaven.cc/api/v1/search?"
    else:
        isWallheavenApi = True
        BASE_URL = f"https://wallhaven.cc/api/v1/search?apikey={wallheaven_api}"

    try:
        tagname = args["tagname"]
    except KeyError:
        tagname = default_args["tagname"]
    tagname.replace(" ", "+")
    try:
        categories = args["categories"]
    except KeyError:
        categories = default_args["categories"]
    try:
        purity = args["purity"]
    except KeyError:
        purity = default_args["purity"]
    try:
        sorting = args["sorting"]
    except KeyError:
        sorting = default_args["sorting"]
    try:
        atleast = args["atleast"]
    except KeyError:
        atleast = default_args["atleast"]
    try:
        ratio = args["ratio"]
    except KeyError:
        ratio = default_args["ratio"]
    try:
        pages = args["pages"]
    except KeyError:
        pages = default_args["pages"]
    query_url = f"{BASE_URL}&q={tagname}&categories={categories}&purity={purity}&sorting={sorting}&atleast={atleast}&ratio={ratio}&page={pages}"
    print(query_url)
    data = requests.get(query_url)
    data = data.json()["data"]
    # print(json.dumps(data, indent=2))
    data_to_return = {}
    for i in range(len(data)):
        t = [data[i]["id"], data[i]["path"], data[i]["resolution"],
             data[i]["file_type"], data[i]["file_size"]]
        data_to_return[i] = t
    return data_to_return
