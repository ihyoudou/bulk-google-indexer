import requests
import sqlite3
import xml.etree.ElementTree as ET

con = sqlite3.connect('sqlite3.db')
cur = con.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS urls
               (
                   url TEXT NOT NULL UNIQUE,
                   processed_at TEXT
                )''')

url = input("URL to sitemap: ")
r = requests.get(url, allow_redirects=True)
open('sitemap.xml', 'wb').write(r.content)

tree = ET.parse('sitemap.xml')
root = tree.getroot()

# In find/findall, prefix namespaced tags with the full namespace in braces
print("Processing...")

for url in root.findall('{http://www.sitemaps.org/schemas/sitemap/0.9}url'):
    loc = url.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc').text

    cur.execute("INSERT or IGNORE INTO urls VALUES (?, ?)",(loc, None))

con.commit()
con.close()  