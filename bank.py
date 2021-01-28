#!/usr/bin/python3
#this script simply creates a cookie with two fields and then redirects the browser to dest_page.py
import cgi, cgitb, os, string
import html_pages
from random import *
import pymysql

cgitb.enable()

"""
BRIAN SAWA
EVAN Taylor

PURPOSE: BANKING WEB APP

LAST LOCATION:
FINISHED QUESTION 5 IN THE ASSIGNMENT SPECIFICATIONS. Transfer.py makes the form needed and has the capabilities to send the information desired to making_transfer.py. we have not touched making_transfer.py at all yet.

"""

#used for random CSRF token generation
min_char = 16
max_char = 16
allchar = string.ascii_letters + string.digits
token = "".join(choice(allchar) for x in range(randint(min_char, max_char)))

#connects to database
conn = pymysql.connect(db='project2', user='root', passwd='qwerty', host='localhost')
cursor = conn.cursor()

rowcount = 0

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

#query to determine validity of cookies
query= "select * from bank WHERE username='{username}' and hashed_password='{hashed_password}'"
cursor.execute(query.format(username=cookie_dict["username"], hashed_password=cookie_dict["password"]))
conn.commit()

#query to determine checking balance of account
query= "select checkings_balance from bank WHERE username='{username}' and hashed_password='{hashed_password}'"
cursor.execute(query.format(username=cookie_dict["username"], hashed_password=cookie_dict["password"]))
conn.commit()
temp1 = cursor.fetchone()

#query to determine savings balance of account
query= "select savings_balance from bank WHERE username='{username}' and hashed_password='{hashed_password}'"
cursor.execute(query.format(username=cookie_dict["username"], hashed_password=cookie_dict["password"]))
conn.commit()
temp2 = cursor.fetchone()

#declared here so that i may use them in the following print statement of the main page (scope issue)
checking = " "
savings = " "


#get the cookie info
if cursor.rowcount > 0:
    #strips the output of awkward characters
    for i in temp1:
        checking = i
        if i != " ":
            break
    for i in temp2:
        savings = i

    #prints mainpage
    print(html_pages.mainpage.format(username=cookie_dict["username"], checking=checking, savings=savings))
else :
    #main login page if there are no cookies
    print(html_pages.loginpage.format(token=token))

