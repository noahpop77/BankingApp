#!/usr/bin/python3

import cgi, cgitb, os, string

#on bank.py
mainpage = """Content-Type: text/html

<!DOCTYPE html>
<html>
<head>
    <title>Simple Form</title>
</head>
<body>
    <p>WELCOME {username}!!</p>
    <table style="width:50%" border="1">
        <tr>
            <th>Checking</th>
            <th>Saving</th>
        </tr>
        <tr>
            <td>{checking}</td>
            <td>{savings}</td>
        </tr>
    </table> 
    <a href="transfer.py">Transfer Money</a>
</body>
</html>
"""

#on bank.py
loginpage = """Content-Type: text/html

<!DOCTYPE html>
<html>
<head>
    <title>Simple Form</title>
</head>
<body>
    <form action="login.py" method="POST">
        Username:<br>
        <input type="text" name="username"><br>
        Password:<br>
        <input type="text" name="password"><br>
        <input type="hidden" name="token" value="{token}">
        <input type="submit" value="Submit">
    </form>
</body>
</html>
"""

#on login.py
nomatch= """Content-Type: text/html

<!DOCTYPE html>
<html>
<head>
    <title>Title for the tab</title>
</head>
<body>
    <h1>YOU GOOFED UP</h1>
    
    <p> STINKY BOI</p>
    
</body>
</html>
"""

succ_page = """Content-Type: text/html

<!DOCTYPE html>
<html>
<head>
    <title>Title for the tab</title>
</head>
<body>
    <h1>YOU DID THE GOOD</h1>
    
    <p> GOOD BOI</p>
    
</body>
</html>
"""

#on transfer.py
transfer_form = """Content-Type: text/html

<!DOCTYPE html>
<html>
<head>
    <title>Simple Form</title>
</head>
<body>
    <form action="making_transfer.py" method="POST">

        username of recipient:<br>
        <input type="text" name="name_of_rec"><br>

        Senders account(ie. checking, or savings):<br>
        <input type="text" name="senders_account"><br>

        Recipients account(ie. checking, or savings):<br>
        <input type="text" name="rec_account"><br>

        Amount To Transfer:<br>
        <input type="text" name="trans_amount"><br>

        <input type="hidden" name="token" value="{token}">
        <input type="submit" value="Submit">
    </form>
</body>
</html>
"""



