import requests
import xml.etree.ElementTree as ET

url = input("URL to sitemap: ")
r = requests.get(url, allow_redirects=True)
open('sitemap.xml', 'wb').write(r.content)

tree = ET.parse('sitemap.xml')
root = tree.getroot()

f = open("urls.txt", "w")
# In find/findall, prefix namespaced tags with the full namespace in braces
print("Processing...")

for url in root.findall('{http://www.sitemaps.org/schemas/sitemap/0.9}url'):
    loc = url.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc').text
    f.write(loc + '\n')
    
f.close()