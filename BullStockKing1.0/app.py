from flask import Flask,render_template,request,flash,session
from  hashlib import  sha1
import  json
import tushare as ts
import pymysql

app = Flask(__name__)

@app.route('/search',methods=['GET','POST'])
def search():
    stockName = request.form.get("stockName")
    print(stockName)
    return render_template("search.html")

@app.route('/',methods=['GET','POST'])
def hello_world():
    if request.method == "GET":
        return render_template("login.html")
    else:
        return render_template("candlestick-sh.html")


@app.route('/demo_test.txt')
def get():
    return ("1")

@app.route('/getHis',methods=['GET','POST'])
def getHis():

    stockCode = request.form.get("code")
    print(stockCode)
    conn = pymysql.connect(db="stock", user="root", password="740312", host="localhost",
                           port=3306)
    cur = conn.cursor()
    cur.execute("select date,open,close,low,high from historydata where stock_code = \'"+ str(stockCode)+"\';")
    hisRow = cur.fetchall()
    result = json.dumps(hisRow)
    conn.commit()
    conn.close()
    return result


if __name__ == '__main__':
    app.debug = True
    app.run()
