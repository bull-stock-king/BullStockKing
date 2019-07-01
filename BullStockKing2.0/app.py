from flask import Flask,render_template,request
import json
import pymysql
from flask_bootstrap import Bootstrap

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template("home_page.html")

@app.route('/getHis',methods=['GET','POST'])
def getHis():

    stockCode = request.form.get("code")
    print(stockCode)
    conn = pymysql.connect(db="stock", user="root", password="1101", host="127.0.0.1",
                           port=3306)
    cur = conn.cursor()
    cur.execute("select date,open,close,low,high from historydata where stock_code = \'"+ str(stockCode)+"\';")
    hisRow = cur.fetchall()
    result = json.dumps(hisRow)
    conn.commit()
    conn.close()
    return result

@app.route('/home_page')
def homePage():
    return render_template("home_page.html")


@app.route('/details')
def details():
    return render_template("stock_details.html")

@app.route('/my_collection')
def my_collection():
    return render_template("my_collection.html")

if __name__ == '__main__':
    app.debug = True
    bootstrap = Bootstrap(app)
    app.run()
