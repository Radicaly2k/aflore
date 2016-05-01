# -*- coding: utf-8 -*-
import requests
import xml.etree.ElementTree as ET
import sqlite3
import os

categories = []

xml = """<?xml version="1.0" encoding="utf-8"?>
<GetCategoriesRequest xmlns="urn:ebay:apis:eBLBaseComponents">
  <RequesterCredentials>
    <eBayAuthToken>AgAAAA**AQAAAA**aAAAAA**PMIhVg**nY+sHZ2PrBmdj6wVnY+sEZ2PrA2dj6wFk4GhCpaCpQWdj6x9nY+seQ**L0MCAA**AAMAAA**IahulXaONmBwi/Pzhx0hMqjHhVAz9/qrFLIkfGH5wFH8Fjwj8+H5FN4NvzHaDPFf0qQtPMFUaOXHpJ8M7c2OFDJ7LBK2+JVlTi5gh0r+g4I0wpNYLtXnq0zgeS8N6KPl8SQiGLr05e9TgLRdxpxkFVS/VTVxejPkXVMs/LCN/Jr1BXrOUmVkT/4Euuo6slGyjaUtoqYMQnmBcRsK4xLiBBDtiow6YHReCJ0u8oxBeVZo3S2jABoDDO9DHLt7cS73vPQyIbdm2nP4w4BvtFsFVuaq6uMJAbFBP4F/v/U5JBZUPMElLrkXLMlkQFAB3aPvqZvpGw7S8SgL7d2s0GxnhVSbh4QAqQrQA0guK7OSqNoV+vl+N0mO24Aw8whOFxQXapTSRcy8wI8IZJynn6vaMpBl5cOuwPgdLMnnE+JvmFtQFrxa+k/9PRoVFm+13iGoue4bMY67Zcbcx65PXDXktoM3V+sSzSGhg5M+R6MXhxlN3xYfwq8vhBQfRlbIq+SU2FhicEmTRHrpaMCk4Gtn8CKNGpEr1GiNlVtbfjQn0LXPp7aYGgh0A/b8ayE1LUMKne02JBQgancNgMGjByCIemi8Dd1oU1NkgICFDbHapDhATTzgKpulY02BToW7kkrt3y6BoESruIGxTjzSVnSAbGk1vfYsQRwjtF6BNbr5Goi52M510DizujC+s+lSpK4P0+RF9AwtrUpVVu2PP8taB6FEpe39h8RWTM+aRDnDny/v7wA/GkkvfGhiioCN0z48</eBayAuthToken>
  </RequesterCredentials>
  <ViewAllNodes>True</ViewAllNodes>
  <DetailLevel>ReturnAll</DetailLevel>
  <CategorySiteID>0</CategorySiteID>
</GetCategoriesRequest>"""
headers = {
            'Content-Type': 'application/xml',
            'X-EBAY-API-CALL-NAME': 'GetCategories',
            'X-EBAY-API-APP-NAME': 'EchoBay62-5538-466c-b43b-662768d6841',
            'X-EBAY-API-CERT-NAME': '00dd08ab-2082-4e3c-9518-5f4298f296db',
            'X-EBAY-API-DEV-NAME': '16a26b1b-26cf-442d-906d-597b60c41c19',
            'X-EBAY-API-SITEID': '0',
            'X-EBAY-API-COMPATIBILITY-LEVEL': '861'
          } # set what your server accepts
r = requests.post('https://api.sandbox.ebay.com/ws/api.dll', data=xml, headers=headers)
xmldoc = ET.fromstring(r.text.encode('utf-8'))
# Namespace defined in the requests
namespace = '{urn:ebay:apis:eBLBaseComponents}'
# Establish the root tag
categoryList = xmldoc.find(namespace + 'CategoryArray')
if os.path.exists('mydb'):
    os.remove('mydb')
filelist = [ f for f in os.listdir(".") if f.endswith(".html") ]
for f in filelist:
    os.remove(f)    
db = sqlite3.connect('mydb')
cursor = db.cursor()
query = cursor.execute("SELECT count(1) FROM sqlite_master WHERE type='table' AND name=?", ('categories',))
# Evaluates if the table exists
if query.fetchone()[0] == 0:
  print ('Creating table...')
  cursor.execute('''
      CREATE TABLE categories(id INTEGER PRIMARY KEY, parentId INTEGER, category_name TEXT,
                        category_level INTEGER, bestOfferEnabled INTEGER)
  ''')
  db.commit()
# If the table has records they will be deleted
else:
  print ('Deleting content of the table...')
  cursor.execute("DELETE FROM categories")
  db.commit()
# Navigate this root's childs to obtain the information we need
for category in categoryList:
  id = int(category.find(namespace + 'CategoryID').text)
  parentId = int(category.find(namespace + 'CategoryParentID').text)
  categoryName = category.find(namespace + 'CategoryName').text
  categoryLevel = int(category.find(namespace + 'CategoryLevel').text)
  try:
    bestOfferEnabled = (0, 1)[(category.find(namespace + 'BestOfferEnabled').text == 'true')]
  except Exception as e:
    bestOfferEnabled = 0
  pass
  categories.append((id, parentId, categoryName, categoryLevel, bestOfferEnabled))
    
cursor.executemany("INSERT INTO categories VALUES (?,?,?,?,?)", categories)
db.commit()
db.close()
print ('Process finished!!')
  
  
