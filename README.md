# Bulk Google indexing

## What this is?
This is a tool i duct-taped together based on a couple of code snippets. It's main purpouse is to automate big website indexion on Google, as in free version of API, Google only allows 200 requests with URL a day.

## How to run it?
This repo contains two scripts   
First - the ```prep.py``` one - generate text file (urls.txt) from XML. It will prompt user for URL to download sitemap.
    
The second one - ```batchjob.py``` is responsible for the batchjob - it loads first 200 lines from urls.txt to dictionary, then making requests to Google API. If the API requests gone fine - it will remove the 200 lines from text file.


Batchjob requires credentials to Google API in JSON format. I also added Discord webhook option - it will send a message on error and success (I suggest creating seperate channel for webhook). You can define own Discord Webhook URL in ```batchjob.py``` on line 12.

## Why don't just parse XML directly instead of converting it back to basic text file?
As i mentioned before - that is a duct-taped, temporary solution. Yes - I do understand that it is probably a bad practice.

## How to run
To obtain credentials.json i suggest following [this great tutorial](https://www.jcchouinard.com/google-indexing-api-with-python/)
After that, put credentials.json in work folder

```
git clone https://github.com/ihyoudou/bulk-google-indexer
cd bulk-google-indexer
pip3 install -r requirements.txt
python3 prep.py
```
`prep.py` needs to be run just once, to extract URLs from XML file

Crontab:
```
5 */24 * * * /usr/bin/python3 /path/to/script/batchjob.py > /tmp/gindexer-batchjob.log 2>&1
```

## Credits
[https://www.jcchouinard.com/google-indexing-api-with-python/](https://www.jcchouinard.com/google-indexing-api-with-python/)
