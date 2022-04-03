from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build 
from googleapiclient.http import BatchHttpRequest
import httplib2
import json
import requests

MaxURL = 200
URLlist = {}
err = False
JSON_KEY_FILE = "credentials.json"
DiscordWebhookURL = ""

# https://gist.github.com/Bilka2/5dd2ca2b6e9f3573e0c2defe5d3031b2
def sendDiscordWebhook(msg):
    # if discord webhook url is set
    if DiscordWebhookURL:
        #for all params, see https://discordapp.com/developers/docs/resources/webhook#execute-webhook
        data = {
            "content" : str(msg),
            "username" : "Google Bulk Indexer"
        }

        result = requests.post(DiscordWebhookURL, json = data)

        try:
            result.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print(err)
        else:
            print("Payload delivered successfully, code {}.".format(result.status_code))

        
# loading urls.txt file to dictionary

with open("urls.txt", "r") as file:  # the a opens it in append mode
    for i in range(MaxURL):
        try:
            line = next(file).strip()
            print(line)
            URLlist[str(line)] = 'URL_UPDATED'
        except Exception as e:
            sendDiscordWebhook("cannot load text file: {}".format(e))
            err = True


# https://www.jcchouinard.com/google-indexing-api-with-python/
SCOPES = [ "https://www.googleapis.com/auth/indexing" ]
ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"
 
# Authorize credentials
credentials = ServiceAccountCredentials.from_json_keyfile_name(JSON_KEY_FILE, scopes=SCOPES)
http = credentials.authorize(httplib2.Http())
 
# Build service
service = build('indexing', 'v3', credentials=credentials)
 
def insert_event(request_id, response, exception):
    if exception is not None:
      print(exception)
      sendDiscordWebhook("error sending request: {}".format(exception))
      err = True
    else:
      print(response)
 
batch = service.new_batch_http_request(callback=insert_event)
 
for url, api_type in URLlist.items():
    batch.add(service.urlNotifications().publish(
        body={"url": url, "type": api_type}))
 
batch.execute()


# after _probably_ successful batch run, removing urls from file
if not err:
    try:
        with open('urls.txt') as f:
            lines = f.readlines()

        def remove_n_lines_from_top(lines, n):
            if n <= len(lines):
                return lines[n:]
            else:
                return lines

        lines = remove_n_lines_from_top(lines, MaxURL)

        f = open("urls.txt", "w+") # replace new file
        f.writelines(lines)
        f.close()
        sendDiscordWebhook("Batch job completed! URL's: {}".format(URLlist))
    except Exception as e:
        sendDiscordWebhook("error while removing links from text file: {}".format(e))
