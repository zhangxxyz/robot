productionUrl = "https://eco.taobao.com/router/rest"
appkey = "25083490"
secret = "77068d785fb6dc77d1865dc0737e1684"
port = '80'
pid = "28940900149"
vekey = "V00000384Y70837048"

# 返利分级 money:预估收入 item_number:购买数量
def returnMoneyRate(money,item_number = 1):
    money = float(money) / float(item_number)
    scale = 0.00

    try:
       for key,values in dictArray.items():
           # print(key,values)
           if float(money) >= float(key):
                scale = float(values)
    except Exception as error:
        print('获取返利比例出错',error)
        scale = 0.5

    returnMoney = money * scale * float(item_number)
    return str('%.2f'%returnMoney)


def getGlobalScale():
    import ZK_Model.ZKOrderDataModel as sqlModel
    import threading
    global timer
    global dictArray
    dictArray = {}
    print('开始从数据库查询当前比例')

    timer = threading.Timer(28800,getGlobalScale)
    re = sqlModel.select([sqlModel.rate])
    result = sqlModel.engine.connect().execute(re)
    for i in result:
        dictArray[i.money] = i.rate



