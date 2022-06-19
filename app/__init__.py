from flask import Flask, render_template, request, redirect, url_for
import base64
#import io
#import whatimage
#import pyheif
#from PIL import Image
from lostandfounddatabase import *
app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
@app.route("/home", methods=["GET","POST"])
def home():
    return render_template(
        "home.html",
    )

@app.route("/credits", methods=["GET","POST"])
def credits():
    return render_template(
        "credits.html",
    )

@app.route("/databaseupload", methods=["GET","POST"])
def hello():
    return render_template(
        "databasetest.html", 
        bookspapers=database_display_all('bookspapers'),
        outerwear=database_display_all('outerwear'),
        gloves=database_display_all('gloveshatsscarves'),
        personalschool=database_display_all('personalschoolsupplies'),
        smallitems=database_display_all('smallitems'),
        full=database_display_full(),
    )

@app.route("/boxinfo", methods=["GET","POST"])
def boxinfo():
    return render_template(
        "boxinfo.html",
    )

@app.route("/bookspapers", methods=["GET","POST"])
def itsme():
    return render_template(
        "bookspapers.html", 
        bookspapers=database_display_all('bookspapers')
    )

@app.route("/outerwear", methods=["GET","POST"])
def iwaswondering():
    return render_template(
        "outerwear.html", 
        outerwear=database_display_all('outerwear')
    )

@app.route("/gloveshatsscarves", methods=["GET","POST"])
def ifafteralltheseyears():
    return render_template(
        "gloveshatsscarves.html", 
        gloves=database_display_all('gloveshatsscarves')
    )

@app.route("/personalschoolsupplies", methods=["GET","POST"])
def youdliketomeet():
    return render_template(
        "personalschoolsupplies.html", 
        personalschool=database_display_all('personalschoolsupplies')
    )

@app.route("/smallitems", methods=["GET","POST"])
def togoovereverything():
    return render_template(
        "smallitems.html", 
        smallitems=database_display_all('smallitems')
    )

@app.route("/unauthorized", methods=["GET","POST"])
def unauthorized():
    return render_template(
        "unauthorized.html",
    )

@app.route("/submit", methods=["POST"])
def submit():
    type = request.form.get("type")
    date = request.form.get("date")
    description = request.form.get("description")
    user = request.form.get("user")
    auth = request.form.get("auth")
    authorized = isAuthorized(user, auth)
    #print("Authorized:" + str(authorized))
    if not authorized:
        return redirect(url_for('unauthorized'))
    images = [None, None]
    image_names = ['image1', 'image2']
    for index, image_name in enumerate(image_names):
        if image_name in request.files:
            image = request.files[image_name].read()
            if not image:
                images[index] = ""
                #print("test")
                continue
            #Attempt to add a HEIC to JPEG converter
            """fmt = whatimage.identify_image(image)
            if fmt in ['heic', 'avif']:
                i = pyheif.read_heif(image)
                # Convert to other file format like jpeg
                s = io.BytesIO()
                image = Image.frombytes(
                    mode=i.mode, size=i.size, data=i.data)

                image.save(s, format="jpeg")
                image = image.read()"""

            image_string = base64.b64encode(image)
            image_to_upload = image_string.decode('utf-8')
            images[index] = uploadImage("data:image/png;base64," + image_to_upload, user)

    database_add(type, date, description, images[0], images[1])
    return redirect(url_for('hello'))

@app.route("/confirm", methods=["GET","POST"])
def delete():
    idnum = request.form.get("idn")
    user = request.form.get("user")
    auth = request.form.get("auth")
    authorized = isAuthorized(user, auth)
    #print("Authorized:" + str(authorized))
    if not authorized:
        return redirect(url_for('unauthorized'))
    database_delete(idnum)
    return redirect(url_for('hello'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=(os.environ.get("DEBUG_MODE", "True") == "TRUE"), port=os.environ.get("DEBUG_MODE", 5000))