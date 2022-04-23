from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build 
from googleapiclient.http import BatchHttpRequest
import httplib2
import sqlite3
import json
import time
import requests

MaxURL = 1
URLlist = {}
err = False
JSON_KEY_FILE = "credentials.json"
DiscordWebhookURL = ""

con = sqlite3.connect('sqlite3.db')
cur = con.cursor()


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

        
# loading urls that haven't been checked
cur.execute('''SELECT url FROM urls WHERE processed_at IS NULL LIMIT ?''', (MaxURL,))
rows = cur.fetchall()
for row in rows:
    URLlist[str(row[0])] = 'URL_UPDATED'


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
    cur.execute("UPDATE urls SET processed_at=? WHERE url=?",(time.time(), url))

batch.execute()

con.commit()
con.close()

sendDiscordWebhook("Batch job completed!")
    