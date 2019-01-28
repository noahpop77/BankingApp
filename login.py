#!/usr/bin/python3
#possible dest_page.py with a parsed cookie
import cgitb, cgi, os
import hashlib
import pymysql
import html_pages

cgitb.enable()

form = cgi.FieldStorage()

#grabs information from cookies, if they exist then they are added to a dictionary, if not then they are pre set
cookie_dict = dict()
if "HTTP_COOKIE" in os.environ :
    cookie_info = os.environ["HTTP_COOKIE"]
    cookies = cookie_info.split(';')
    for cookie in cookies :
        cookie_split = cookie.split('=')
        cookie_dict[cookie_split[0].strip()] = cookie_split[1].strip()

else:
    cookie_dict["username"] = form["username"].value
    cookie_dict["password"] = form["password"].value
    cookie_dict["token"] = form["token"].value

#code to encrypt passwords
passin = cookie_dict["password"]
encoded_password = passin.encode(encoding='UTF-8')
hashed_password = hashlib.sha256(encoded_password)
hashed_string = hashed_password.hexdigest()

#connects to the databse
conn = pymysql.connect(db='project2', user='root', passwd='qwerty', host='localhost')
cursor = conn.cursor()

#query to determine validity of the cookies
query= "select * from bank WHERE username='{username}' and hashed_password='{hashed_password}'"
cursor.execute(query.format(username=cookie_dict["username"], hashed_password=hashed_string))
conn.commit()

#page to set cookies and redirect back to bank.py
redirect_to_bank= """Content-Type: text/html
Set-Cookie: username={username}; Expires=28 Nov 2021 10:00:00 GMT
Set-Cookie: password={hashed_string}; Expires=10 Jun 2021 12:10:00 GMT
Set-Cookie: token={token}; Expires=10 Jun 2021 12:10:00 GMT

<!DOCTYPE html>
<html>
  <head>
     <meta http-equiv="refresh" content="0;URL=bank.py">
  </head>
</html>
"""

#if the data is retrieved successfully then it will update the CSRF token and redirect the page to bank.py's welcome page
if cursor.rowcount > 0:
    query = "UPDATE bank SET current_csrf_token='{token}' WHERE username='{username}'"
    cursor.execute(query.format(username=cookie_dict["username"], token=cookie_dict["token"]))
    conn.commit()

    print(redirect_to_bank.format(username=cookie_dict["username"], hashed_string=hashed_string, token=cookie_dict["token"]))

#page for if nothing was found
else:
    print(html_pages.nomatch)

