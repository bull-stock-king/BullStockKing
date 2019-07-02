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
conn = pymysql.connect(db="stock", user="stardust@bullstockking", password="ZYY99c0e222", host="bullstockking.mysql.database.chinacloudapi.cn",port=3306)
``` 
 *需将各自的ip记录下来并发送给我，经授权的ip才能连接云数据库*   
   
 云数据库现有数据库相关信息： 
   
数据库名（db）：stock    
  
stock中表（table）列表：  
表名（table）：stocks 

|stock_code | cns_name|  
|:-:|:-:|  
|000001|平安银行 | 

表名（table）：historydata

|stock_code|date|open|high|close|low | 
|:-:| :---: |:-:|:-:|:-:|:-:|  
|000001|2019-01-07|9.84|9.85|9.74|9.63 |

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

# BullStockKing2.0版本说明  
ByllStockKing2.0对之前的大部分功能进行了淘汰与重构，代码结构如下：  
#### 项目目录结构  
├── Readme.md                  //项目说明文档    
├── BullStockKing2.0           //项目主体    
│   ├──static  
│   │  ├──css  
│   │  ├──fonts    
│   │  └──js  
│   ├──templates   
│   │  ├──commen    
│   │  ├──home_page.html  
│   │  ├──my_collection.html  
│   │  ├──stock_details.html  
│   │  └──test.html  
│   ├──venv  
│   └──app.py  
  
第二周任务分工说明：  
  
  
王文龙：  
* 情感分析预测图（已完成）  
* 股票列表页面  

王一丹：  
* 前端框架（已完成）  
* 股票详情界面  

陈卓群：  
* logo设计（已完成）  
* 主页面设计  

周永逸：  
* 云数据库搭建（已完成）  
* 主页面  
* 用户操作  
#### 以后任务完成状况需在README中更新完成度以跟踪任务完成情况（可添加细节和已实现小功能）
