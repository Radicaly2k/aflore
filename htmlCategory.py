import sys
import sqlite3

# Function definition is here
# Builds the header
def headerHTML():
  return '<head><h1>Category ' + id + '</h1><p>This is the challege of Python</p></head>';

# Builds the body section that has the parent information
def bodyParentHTML():
  cursor.execute("SELECT * FROM categories WHERE id=?", (id,))
  rows = cursor.fetchall()
  for row in rows:
    return '<blockquote><p><strong>CateogryID</strong>:' + str(row[0]) + '</p><p><strong>CateogryName</strong>:' + row[2] + '</p><p><strong>CategoryLevel</strong>:' + str(row[3]) + '</p><p><strong>BestOfferEnabled</strong>:' + ('YES', 'NO')[row[3] == 1] +'</p></blockquote>';

# Builds the body section with the list of childs of the category
def bodyChildHTML():
  query2 = cursor.execute("SELECT count(1) FROM categories WHERE parentId=?", (id,))
  if query2.fetchone()[0] == 0:
    print 'No Childs'
    htmlBody = ''
  else:
    cursor.execute("SELECT * FROM categories WHERE parentId=?", (id,))
    rows = cursor.fetchall()
    htmlBody = '<p>This is the sub categories list:</p><ul>'
    for row in rows:
      htmlBody = htmlBody + '<li><p><strong>CateogryID</strong>:' + str(row[0]) + '</p><p><strong>CateogryName</strong>:' + row[2] + '</p><p><strong>CategoryLevel</strong>:' + str(row[3]) + '</p><p><strong>BestOfferEnabled</strong>:' + ('YES', 'NO')[row[3] == 1] +'</p></li>';  
    htmlBody = htmlBody + '</ul>'
  return htmlBody;
   
# Builds the footer with the author  
def footerHTML():
  return '<p><strong>Created By:</strong>Christopher Contreras</p>';

# Obtains the argument in the position 1
id = sys.argv[1]
# Gets the conection with the DB
db = sqlite3.connect('mydb')
cursor = db.cursor()
query = cursor.execute("SELECT count(1) FROM categories WHERE parentId=? OR id=?", (id,id))
# Evaluates if the category exists if not the error message will be shown
if query.fetchone()[0] == 0:
  print 'Category ID not found in DB'
# If category is found will generate HTML file
else:
  f = open(sys.argv[1]+'.html', 'w')
  f.write(headerHTML())
  f.write(bodyParentHTML())
  f.write(bodyChildHTML())
  f.write(footerHTML())
db.close()
print 'Process finished'