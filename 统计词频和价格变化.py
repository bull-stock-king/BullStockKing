from openpyxl import load_workbook
import jieba.posseg as pseg  # 解析词性
import jieba  # 分词
import sys
import collections

remark = []
fluctuate = []
remark_cipin = []


def readXls():
    wb = load_workbook("/Users/yidan/Documents/2019实训-牛股王/BullStockKing-master/采集数据/data1.xlsx")
    sheet = wb.get_sheet_by_name("sheet1")
    
    for each in sheet["G"]:
        remark.append(each.value)
    
    for each in sheet["H"]:
        fluctuate.append(each.value)


# 去掉无关字符
def fenci():
    i = 0
    for each in remark:
        i = i + 1
        each = each.replace("，", "")
        each = each.replace("；", "")
        each = each.replace("。", "")
        each = each.replace("《", "")
        each = each.replace("》", "")
        each = each.replace("（", "")
        each = each.replace("）", "")
        each = each.replace(" ", "")
        each = each.replace("…", "")
        each = each.replace("·", "")
        each = each.replace("、", "")
        each = each.replace("“", "")
        each = each.replace("•", "")
        each = each.replace("“", "")
        each = each.replace("【", "")
        each = each.replace("】", "")
        
        word = []
        result = pseg.cut(each)
        print(result)
        for w in result:  # 将每个类型的词单独存入一个文档中
            word.append(w.word)
        mycount = collections.Counter(word)
        cipin_list = []
        for key, val in mycount.most_common(100000):
            cipin = (key, str(val))
            cipin_list.append(cipin)
        remark_cipin.append(cipin_list)
        
        if (i > 20):
            break;


if __name__ == "__main__":
    readXls()
    fenci()
    
    for flu, each in zip(fluctuate, remark_cipin):
        print(flu)
        print(each)


