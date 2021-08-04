from github import Github
import json
import requests
import os


data_url = "https://data.go.th/dataset/9f6d900f-f648-451f-8df4-89c676fce1c4/resource/0092046c-db85-4608-b519-ce8af099315e/download/"
filename = "covtest.json"
g_token = os.getenv("G_TOKEN")


def request_data(filename):
    response = requests.get(data_url)
    i = 0
    records = []
    for line in response.text.splitlines():
        if i > 0:
            col = line.split(",")
            try:
                date_split = col[0].split("/")
                day = f"{int(date_split[0]):02d}"
                month = f"{int(date_split[1]):02d}"
                year = date_split[2]
                convert_date = f"{year}-{month}-{day} 00:00:00"
            except Exception:
                convert_date = col[0]
            record = {
                "_id": i,
                "Date": convert_date,
                "Pos": int(col[1]),
                "Total": int(col[2])
            }
            records.append(record)
        i += 1
    response = {
        "result": {
            "records": records
        }
    }
    json_string = json.dumps(response)
    json_file = open(filename, "w")
    json_file.write(json_string)
    json_file.close()
    return response


def push_github(g_token, filename, message):
    g = Github(g_token)
    content = open(filename, "rb")
    repo = g.get_user().get_repo('ThaiCovidTestData')
    contents = repo.get_contents(filename)
    response = repo.update_file(contents.path, message, content.read(), contents.sha, branch="main")
    content.close()
    return response


if __name__ == "__main__":
    response = request_data(filename)
    print(response)
    g_response = push_github(g_token, filename, "Update Cov Test Data")
