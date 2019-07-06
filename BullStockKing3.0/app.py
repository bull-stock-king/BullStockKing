from flask import Flask,render_template,request,url_for,redirect,session
import json
import requests
import pymysql
from bs4 import BeautifulSoup
from flask_bootstrap import Bootstrap
import jieba
import codecs
import urllib
import collections
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
#配置数据库地址
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://stardust@bullstockking:ZYY99c0e222@bullstockking.mysql.database.chinacloudapi.cn:3306/bullstockking?charset=utf8'
#app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:200507@localhost:3306/stock?charset=utf8'
# 该配置为True,则每次请求结束都会自动commit数据库的变动
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_COMMIT_TEARDOWN'] = True
app.config['SECRET_KEY'] = '21312412412dfafaivhoseiriuiqe2175887w'

db = SQLAlchemy(app)

class newsInfo:
    title=""
    description = ""
    article=""
    url=""

    def __init__(self,title,url,description,article):
        self.title = title
        self.url = url
        self.description = description
        self.article = article

class stockDetails:
    stockCode=""
    stockName =""
    stockNews = []
    stockHisData = []

    def __init__(self,stockCode):
        self.stockCode = stockCode



@app.route('/home_page/selectFill')
@app.route('/details/selectFill')
@app.route('/my_collection/selectFill')
@app.route('/selectFill',methods=['GET'])
def selectFill():
    conn = pymysql.connect(db="bullstockking", user="stardust@bullstockking", password="ZYY99c0e222",
                           host="bullstockking.mysql.database.chinacloudapi.cn", port=3306)
    cur = conn.cursor()
    cur.execute("select * from stocks;")
    data = cur.fetchall()
    conn.commit()
    conn.close()
    result = json.dumps(data)
    return result



@app.route('/details/?<string:stockCode>')
def details(stockCode):
    return render_template('stock_details.html')

@app.route('/getHis',methods=['GET','POST'])
def getHis():
    stockName = request.form.get("code")
    conn = pymysql.connect(db="bullstockking", user="stardust@bullstockking", password="ZYY99c0e222",
                           host="bullstockking.mysql.database.chinacloudapi.cn", port=3306)

    cur = conn.cursor()
    cur.execute("select stock_code from stocks where cns_name= \'" + stockName + "\';")
    stockCode = cur.fetchone()[0]
    conn.commit()
    conn.close()
    return redirect(url_for('details',stockCode=stockCode))

@app.route('/details/hisData',methods=["POST"])
def hisData():
    stockCode = request.form.get("code")
    details = stockDetails(stockCode)
    conn = pymysql.connect(db="bullstockking", user="stardust@bullstockking", password="ZYY99c0e222",
                           host="bullstockking.mysql.database.chinacloudapi.cn", port=3306)

    cur = conn.cursor()
    cur.execute("select date,open,close,low,high from historydata where stock_code = \'"+ str(stockCode)+"\';")
    details.stockHisData = cur.fetchall()
    cur.execute("select cns_name from stocks where stock_code = \'"+ str(stockCode)+"\';")
    details.stockName = cur.fetchone()[0]
    details.stockNews = getStockNews(details.stockName)
    cipin_list = cipin(details.stockNews)
    follow = judgecollect(session['user'],details.stockCode)
    result = json.dumps((details.stockName,details.stockNews,details.stockHisData,cipin_list,follow))
    conn.commit()
    conn.close()
    return result

def judgecollect(user_id,code):
    conn = pymysql.connect(db="bullstockking", user="stardust@bullstockking", password="ZYY99c0e222",
                           host="bullstockking.mysql.database.chinacloudapi.cn", port=3306)
    cur = conn.cursor()
    cur.execute("select * from collect where user_id="+user_id+" and stock_code="+code+"")
    result=cur.fetchall()
    if (result.__len__()!=0):
        return True
    else:
        return False

def getStockNews(stockName):
    stockNews = []
    result = []
    headers={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36' }

    url = "https://www.baidu.com/s?ie=utf-8&cl=2&medium=2&rtt=4&bsst=1&rsv_dl=news_t_sk&tn=news&word=股+"+stockName
    #解析html，获取链接
    r = requests.get(url,headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")
    div = soup.select('#content_left .result .c-title a')

    divSummary = soup.select('#content_left .result div')
    for each,each1 in zip(div,divSummary):
        article=""
        linkurl=each.get('href')
        description = each1.text
        title = each.text
        r = requests.get(linkurl, headers=headers)
        soup = BeautifulSoup(r.text, "html.parser")
        div=soup.select('.article-content p span')
        for eachDiv in div:
            article= article + eachDiv.text +'\n\n'
        stockNews.append((title,linkurl,description,article))
    return stockNews

def cipin(stockNews):
    articles = ""
    for each in stockNews:
        articles += each[3]
    # 分词
    articles=articles.replace("\n","")
    articles=articles.replace(" ","")
    seg_list = jieba.cut(articles)
    seg_result = []
    for w in seg_list:
        seg_result.append(w)
    # 读取停用词
    stopwords = set()  # 集合
    fr = codecs.open('./static/stop.txt', 'r', 'utf-8')
    for word in fr:
        stopwords.add(word.strip())
    fr.close()

    result = list(filter(lambda x: x not in stopwords, seg_result))

    mycount = collections.Counter(result)
    cipin_list = []
    for key, val in mycount.most_common(1000):
        cipin = (key, str(val))
        cipin_list.append(cipin)
    return cipin_list


@app.route('/my_collection/',methods=['POST', 'GET'])
def my_collection():
    from models import User
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 1, type=int)
    #user = User.query.filter(User.id == '1').first()
    pagination = User.query.filter(User.id == session['user']).paginate(page, per_page)
    return render_template("my_collection.html", pagination =pagination,per_page=per_page)


@app.route('/uncollect/<code>',methods=['POST', 'GET'])
def uncollect(code):
    conn = pymysql.connect(db="bullstockking", user="stardust@bullstockking", password="ZYY99c0e222",
                           host="bullstockking.mysql.database.chinacloudapi.cn", port=3306)
    cur = conn.cursor()
    cur.execute("delete from collect where user_id=%s and stock_code= %s;",[session['user'],code])
    conn.commit()
    conn.close()
    return redirect(url_for('my_collection'))


@app.route('/details/follow',methods=['POST'])
def follow():
    stockCode = request.form.get("stockCode")
    conn = pymysql.connect(db="bullstockking", user="stardust@bullstockking", password="ZYY99c0e222",
                           host="bullstockking.mysql.database.chinacloudapi.cn", port=3306)
    cur = conn.cursor()
    cur.execute("insert into collect(user_id, stock_code) values (%s,%s);",[session['user'],stockCode])
    conn.commit()
    conn.close()

    result = json.dumps(True)
    return result

@app.route('/details/unfollow',methods=['POST'])
def unfollow():
    stockCode = request.form.get("stockCode")
    conn = pymysql.connect(db="bullstockking", user="stardust@bullstockking", password="ZYY99c0e222",
                           host="bullstockking.mysql.database.chinacloudapi.cn", port=3306)
    cur = conn.cursor()
    cur.execute("delete from collect where user_id = %s and stock_code = %s;" ,[session['user'],stockCode])
    conn.commit()
    conn.close()

    result = json.dumps(True)
    return result

@app.route('/login/',methods=['GET'])
def login():
    return render_template('login.html')


@app.route('/login/',methods=['POST'])
def servlet():
    id = request.form.get("username")
    password = request.form.get("password")
    session['user'] = id
    conn = pymysql.connect(db="bullstockking", user="stardust@bullstockking", password="ZYY99c0e222",
                           host="bullstockking.mysql.database.chinacloudapi.cn", port=3306)
    cur = conn.cursor()
    cur.execute("select id,password from user_info where id = %s and password = %s", [id, password])
    userinfo = cur.fetchall()
    conn.commit()
    conn.close()
    if len(userinfo) > 0:
        return redirect(url_for('homePage'))
    else:
        return redirect(url_for('register'))


@app.route('/home_page/')
def homePage():
    username = session.get('user')
    userlen = len(username)
    print(username)
    conn = pymysql.connect(db="bullstockking", user="stardust@bullstockking", password="ZYY99c0e222",
                           host="bullstockking.mysql.database.chinacloudapi.cn", port=3306)
    cur = conn.cursor()
    cur.execute("select name,code from stock_detail_info where changepercent > 0")
    namelist = cur.fetchall()
    list = namelist[0:30]
    conn.commit()
    conn.close()
    resp = urllib.request.urlopen('https://www.quantinfo.com/API/Argus/predict')
    showlist = json.loads(resp.read())
    return render_template("home_page.html", list=list, namelist=namelist, showlist=showlist,username = username,userlen = userlen)


@app.route('/')
def hello_world():
    conn = pymysql.connect(db="bullstockking", user="stardust@bullstockking", password="ZYY99c0e222", host="bullstockking.mysql.database.chinacloudapi.cn",port=3306)
    cur = conn.cursor()
    cur.execute("select name,code from stock_detail_info where changepercent > 0")
    namelist = cur.fetchall()
    list = namelist[0:30]
    conn.commit()
    conn.close()
    resp = urllib.request.urlopen('https://www.quantinfo.com/API/Argus/predict')
    showlist = json.loads(resp.read())
    return render_template("home_page.html",list = list,namelist = namelist,showlist = showlist)


@app.route('/register/',methods=['GET'])
def register():
    return render_template('register.html')

@app.route('/register/',methods=['POST'])
def success():
    username = request.form.get("username")
    password = request.form.get("password")
    email = request.form.get("email")
    conn = pymysql.connect(db="bullstockking", user="stardust@bullstockking", password="ZYY99c0e222",
                           host="bullstockking.mysql.database.chinacloudapi.cn", port=3306)
    cur = conn.cursor()
    cur.execute("insert into user_info values (%s, %s, %s)", [username, password, email])
    conn.commit()
    conn.close()
    return redirect(url_for('homePage'))


if __name__ == '__main__':
    app.debug = True
    bootstrap = Bootstrap(app)
    db.metadata.clear()
    app.run()
