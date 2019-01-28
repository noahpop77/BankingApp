#!/usr/bin/python3

import cgi, cgitb, os, string
import html_pages
from random import *
import pymysql

cgitb.enable()

form = cgi.FieldStorage()

header = """Content-Type: text/html

"""

print(header)

#connects to database
conn = pymysql.connect(db='project2', user='root', passwd='qwerty', host='localhost')
cursor = conn.cursor()

#grabs information from cookies, if they exist then they are added to a dictionary, if not then they are pre set
cookie_dict = dict()
if "HTTP_COOKIE" in os.environ :
    cookie_info = os.environ["HTTP_COOKIE"]
    cookies = cookie_info.split(';')
    for cookie in cookies :
        cookie_split = cookie.split('=')
        cookie_dict[cookie_split[0].strip()] = cookie_split[1].strip()
else:
    cookie_dict["username"] = "Undefined"
    cookie_dict["password"] = "Undefined"
    cookie_dict["token"] = "Undefined"


query= "select * from bank WHERE username='{username}' and current_csrf_token='{token}'"
cursor.execute(query.format(username=cookie_dict["username"], token=cookie_dict["token"]))
conn.commit()

if cursor.rowcount > 0:
    if form["senders_account"].value == "checking":
        query= "select checkings_balance from bank WHERE username='{username}'"
        cursor.execute(query.format(username=cookie_dict["username"]))
        checkbalsender = int(cursor.fetchall())
        conn.commit()

        query= "select checkings_balance from bank WHERE username='{username}'"
        cursor.execute(query.format(username=form["name_of_rec"].value))
        checkbalreciever = int(cursor.fetchall())
        conn.commit()

        if checkbalsender > int(form["trans_amount"].value):
            subtotal = checkbalsender - int(form["trans_amount"].value)
            query = "UPDATE bank SET checkings_balance='{transamount}' WHERE username='{username}'"
            cursor.execute(query.format(username=cookie_dict["username"], transamount=subtotal))
            conn.commit()
            
            addtotal = checkbalreciever + int(form["trans_amount"].value)
            query = "UPDATE bank SET checkings_balance='{transamount}' WHERE username='{username}'"
            cursor.execute(query.format(username=form["name_of_rec"].value, transamount=addtotal))
            conn.commit()

            print(html_pages.succ_page)
        else:
            print(html_pages.nomatch)

    elif form["trans_amount"].value == "savings":
        query= "select savings_balance from bank WHERE username='{username}'"
        cursor.execute(query.format(username=cookie_dict["username"]))
        checkbal = int(cursor.fetchall())
        conn.commit()

        if checkbal < int(form["trans_amount"].value):
            newtotal = checkbal + int(form["trans_amount"].value)
            query = "UPDATE bank SET savings_balance='{transamount}' WHERE username='{username}' and current_csrf_token='{token}'"
            cursor.execute(query.format(username=cookie_dict["username"], token=cookie_dict["token"], transamount=newtotal))
            conn.commit()
        else:
            print(html_pages.nomatch)
    else:
        print(html_pages.nomatch)
else:
    print(html_pages.nomatch)