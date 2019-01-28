#!/usr/bin/python3

import cgi, cgitb, os, string
import html_pages
from random import *
import pymysql

cgitb.enable()

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

#runs query on DB to determine validity of cookie
query= "select * from bank WHERE username='{username}' and hashed_password='{hashed_password}'"
cursor.execute(query.format(username=cookie_dict["username"], hashed_password=cookie_dict["password"]))
conn.commit()


#get the cookie info
if cursor.rowcount > 0:
    #transfer.py form which gets info and redirects to making_transfer.py
    print(html_pages.transfer_form.format(token=cookie_dict["token"]))
else :
    #the you messed up page
    print(html_pages.nomatch)