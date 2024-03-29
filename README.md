# BullStockKing
To make the best project
## 环境依赖<br>
python3.7<br>
PyCharm<br>
flask<br>

## 连接云数据库说明   
先在命令行中输入如下指令：  
```
mysql --host bullstockking.mysql.database.chinacloudapi.cn --user stardust@bullstockking -p
```  
如果未授权，cmd会报错：错误 2003 (28000): 不允许 IP 地址为 123.456.789.0 的客户端访问服务器 （ip地址每个人不同）  
只需将报错的ip发给我即可连接。  
  
  
应用程序中连接指令（python）：  
```
import pymysql
conn = pymysql.connect(db="bullstockking", user="stardust@bullstockking", password="ZYY99c0e222", host="bullstockking.mysql.database.chinacloudapi.cn",port=3306)
``` 
或者：
```
from sqlalchemy import create_engine  
connect = create_engine('mysql+pymysql://stardust@bullstockking:ZYY99c0e222@bullstockking.mysql.database.chinacloudapi.cn:3306/bullstockking?charset=utf8')  
```
 *需将各自的ip记录下来并发送给我，经授权的ip才能连接云数据库*   
   
 云数据库现有数据库相关信息： 
   
数据库名（db）：bullstockking    
  
stock中表（table）列表：  
表名（table）：user_info 

|id | password|  email| name | country | phone |
|:-:|:-:| :-:| :-:|:-:|:-:| 
|916333607|123456 | NULL |  zyy|china|15827528566|
  
id: &emsp;  VARCHAR(45) &emsp; PK &emsp; NN  
password:&emsp;  VARCHAR(45) &emsp; NN  
email: &emsp;  VARCHAR(45)   

表名（table）：stock_detail_info

|code|name |changepercent|trade|open|high|low | settlement |    
|:-:| :-:|:---: |:-:|:-:|:-:|:-:|:-:|    
|300362|平安银行|-10.056|4.83|4.86|5.22 |4.83 | 5.37|   


code：&emsp; &emsp;  &emsp; &emsp; 代码  &emsp;  VARCHAR(45) &emsp; PK &emsp; NN  
name: &emsp; &emsp;  &emsp; &emsp; 名称   &emsp; TEXT  
changepercent:&emsp; 涨跌幅 &emsp; DOUBLE  
trade: &emsp; &emsp;  &emsp; &emsp; 现价 &emsp; &ensp;DOUBLE  
open: &emsp;  &emsp;  &emsp; &emsp; 开盘价 &emsp; DOUBLE  
high:  &emsp; &emsp; &emsp;  &emsp; 最高价 &emsp; DOUBLE  
low:   &emsp; &emsp;  &emsp; &emsp; &ensp; 最低价 &emsp; DOUBLE  
settlement:&emsp; &emsp;  昨日收盘价 &emsp; DOUBLE  

表名(table):stocks  

| stock_code | cns_name     |  
|:-:|:-:|   
| 600511     | 国药股份     |  


表名(table):historydata


| stock_code | date       | open  | high  | close | low   |   
|:-:| :-:|:---: |:-:|:-:|:-:|  
| 600511     | 2019-06-27 | 23.37 | 23.55 | 23.35 | 23.28 |    

表名(table):collect

| user_id | stock_code |
|:-:|:-:|
| 916333607|000001|

## 使用git提交说明  
从本地提交到远程库：
### ！！提交前请先从远程库pull一遍以免造成分支合并冲突！！
```
git add .   
git commit -m "修改了README"   //" "中为提交说明信息  
git push origin master  
```
从远程库拉取到本地：
```
git pull origin master
```
第一次拉取项目：
```
//clone后面为git链接
git clone https://github.com/mbr/flask-bootstrap.git
```

# BullStockKing4.5版本说明  
BullStockKing4.5是现可发布的完成版本  
* 修复了用户未登录时出现的若干bug  
* 修复了用户注册时可能出现的若干bug  
* 修复了用户无法注销的bug  
* 新增了情感分析图、邮件预警系统  
* 优化了主界面、用户登录页面、用户注册页面、股票详情页面  

## 情感字典：  
### 功能：  
接受一段文本，返回情感值，正值表示正面情感，负值表示负面情感  
### 使用  
需要使用到停用词表：stop.txt,程度副词表和情感字典  
###### 详细使用方法见代码注释


  
#### 第二、三周任务分工说明：  
  
  
王文龙：  
* 情感分析预测图（已完成）  
* 股票列表页面  
* 添加收藏股票和取消收藏股票功能  

王一丹：  
* 前端框架（已完成）  
* 股票详情界面 (搜索框、股票的历史echars图，股票的新闻展示） （已完成）
* 股票详情界面（词频echarts图，添加预测图）（完成一部分，词频的算法有待更新）
* 股票详情界面（涨跌） （未完成）

陈卓群：  
* logo设计（已完成）  
* 主页面设计  
* 微信小程序端开发  

周永逸：  
* 云数据库搭建（已完成）  
* 主页面设计及优化（已完成）  
* 用户相关操作及bug修复（已完成）  
#### 以后任务完成状况需在README中更新完成度以跟踪任务完成情况（可添加细节和已实现小功能）
### 每个人在各自的部分中记得添加备注！！！以免增添其他人解读代码的时间！！！
