from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import os
from dotenv import load_dotenv
import datetime
import hashlib
import cloudinary.uploader
import string, random

load_dotenv()

def uploadImage(image, user):
    uniqueCode = ""
    for i in range(8):
        uniqueCode += random.choice(string.ascii_letters)
    response=cloudinary.uploader.upload(image, public_id = "stuylostandfound/"+user+"/"+uniqueCode)
    return response["url"]

def isAuthorized(user, auth):
    if((not user) or (not auth)):
        return False
    db = mysql.connector.connect(user=os.environ.get("DBUSER"), password=os.environ.get("DBPASSWORD"), host=os.environ.get("DBHOST"), database="lostandfound")
    c = db.cursor()
    c.execute("select * from users where user = (%s);", (user,))
    result = list(c.fetchall())
    db.commit()
    db.close()
    hashedAuth = hashlib.sha256(auth.encode("utf-8")).hexdigest()
    if not result:
        return False
    return(hashedAuth == result[0][2])

def database_add(type, date, description, image1, image2):
    db = mysql.connector.connect(user=os.environ.get("DBUSER"), password=os.environ.get("DBPASSWORD"), host=os.environ.get("DBHOST"), database="lostandfound")
    c = db.cursor()
    updatedAt = datetime.datetime.now()
    c.execute("insert into lost (type, date, description, image1, image2, updatedAt) values (%s, %s, %s, %s, %s, %s)", (type, date, description, image1, image2, updatedAt))
    db.commit()
    db.close() 

def database_delete(idnum):
    db = mysql.connector.connect(user=os.environ.get("DBUSER"), password=os.environ.get("DBPASSWORD"), host=os.environ.get("DBHOST"), database="lostandfound")
    c = db.cursor()
    c.execute("delete from lost where id = (%s);", (idnum,))
    db.commit()
    db.close() 

def database_display_all(type):
    db = mysql.connector.connect(user=os.environ.get("DBUSER"), password=os.environ.get("DBPASSWORD"), host=os.environ.get("DBHOST"), database="lostandfound")
    c = db.cursor()
    c.execute("select date, description, image1, image2 from lost WHERE type = %s;", (type,))
    result = list(c.fetchall())
    db.close()
    return result

def database_display_full():
    db = mysql.connector.connect(user=os.environ.get("DBUSER"), password=os.environ.get("DBPASSWORD"), host=os.environ.get("DBHOST"), database="lostandfound")
    c = db.cursor()
    c.execute("select * from lost;")
    result = list(c.fetchall())
    db.close()
    return result

def database_display_date():
    db = mysql.connector.connect(user=os.environ.get("DBUSER"), password=os.environ.get("DBPASSWORD"), host=os.environ.get("DBHOST"), database="lostandfound")
    c = db.cursor()
    c.execute("select date from lost;")
    result = list(c.fetchall())
    db.close()
    return result

def database_display_description():
    db = mysql.connector.connect(user=os.environ.get("DBUSER"), password=os.environ.get("DBPASSWORD"), host=os.environ.get("DBHOST"), database="lostandfound")
    c = db.cursor()
    c.execute("select description from lost;")
    result = list(c.fetchall())
    db.close()
    return result
