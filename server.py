from flask import Flask,render_template, request, redirect, url_for
import mysql.connector as mysql
import datetime

mydb = mysql.connect(
    user = "root", passwd = "harish1040",
    host = "localhost", database ="codebase"
)

server = Flask(__name__)

def timeDate():
    current_date = datetime.date.today()
    current_time = datetime.datetime.now().strftime('%H:%M:%S')
    return current_time,current_date

@server.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        return saveIdPass()
    return render_template("index.html")

@server.route("/login",methods=["POST","GET"])
def saveIdPass():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        if mydb.is_connected():
            cursor = mydb.cursor()
            current_time, current_date = timeDate()
            query = f"INSERT INTO LOGIN VALUES('{username}','{password}','{current_time}','{current_date}');"
            cursor.execute(query)
            mydb.commit()
            return redirect(url_for('errorMsg', status=1))
        else:
            return redirect(url_for('errorMsg', status=0))
    else:
        return render_template("login.html")
        
@server.route("/<status>")
def errorMsg(status):
    if status == "1":
        return "<h1>saved data</h1>"
    else:
        return "<h1>error occur while connection to database</h1>" 

if __name__ == "__main__":
    server.run(debug=True)


