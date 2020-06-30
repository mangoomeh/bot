import urllib.request
import json
import requests

key = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6Ijc2YWYzMGJmLWFjYzgtNGE0Ny1hZmU2LWIwZjE0NzY2ZWNlYyIsImlhdCI6MTU5MjMxMzY0OSwic3ViIjoiZGV2ZWxvcGVyL2JjNzVkYTRmLTEyMGItOWU3Ny0xMTA0LWM0YmQxMDllMDc5OCIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyIxMjguMTI4LjEyOC4xMjgiXSwidHlwZSI6ImNsaWVudCJ9XX0.czFtTMv7pqaziRUiivFYyXdvwAvPQNpI7w9tNvrExj0cvzYFl20GHtdLL3LiVKM-ZUFs1wTXeSqfjXgygssT2g"
base_url = "https://proxy.royaleapi.dev/v1"

endpoint1 = "/clans/%23L2208GR9/members"
endpoint2 = "/clans/%23L2208GR9/currentwar"

request1 = requests.get(base_url+endpoint1, headers={"Authorization": "Bearer %s" %key})

request2 = requests.get(base_url+endpoint2, headers={"Authorization": "Bearer %s" %key})


response1 = urllib.request.urlopen(request1).read().decode("utf-8")
response2 = urllib.request.urlopen(request2).read().decode("utf-8")

data1 = json.loads(response1)
data2 = json.loads(response2)

tempdata = ""
for item in data1['items']:
    tempdata.append(
        "Name: {0} \nRank: {1} \nTrophies: {2} \nArena: {3} \nDonations: {4} \n\n".format(item['name'],
                                                                                          item['role'],
                                                                                          item["trophies"],
                                                                                          item['arena']['name'],
                                                                                          item["donations"]))
print(tempdata)
tempdata = ""
tempdata.append("\nCurrent War Data:")
for item in data2['participants']:
    tempdata.append(
        "Name:{0} \nCollection Day: {1}/3 \nBattles Played: {2}/{3} \nWins: {4}/{2} \n".format(item['name'],
                                                                                               item[
                                                                                                   'collectionDayBattlesPlayed'],
                                                                                               item[
                                                                                                   "battlesPlayed"],
                                                                                               item[
                                                                                                   'numberOfBattles'],
                                                                                               item['wins']))
print(tempdata)
