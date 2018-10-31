productionUrl = "https://eco.taobao.com/router/rest"
appkey = "25083490"
secret = "77068d785fb6dc77d1865dc0737e1684"
port = '80'
pid = "28940900149"
vekey = "V00000384Y70837048"
dictArray = {}

# 返利分级 money:预估收入 item_number:购买数量
def returnMoneyRate(money,item_number = 1):
    money_One = float(money) / float(item_number)
    scale = 0.00
    try:
        scale = getGlobalScale(money_One)

    except Exception as error:
        print('获取返利比例出错',error)
        scale = 0.5
    print(money,scale,float(item_number))
    returnMoney = money_One * scale * float(item_number)
    return str('%.2f'%returnMoney)

def getGlobalScale(money):
    import ZK_Model.ZKOrderDataModel as sqlModel
    import threading
    global timer
    # global dictArray
    # dictArray = {}
    print('开始从数据库查询当前比例')

    # timer = threading.Timer(28800,getGlobalScale)
    # timer.setDaemon(True)
    # timer.start()
    re = sqlModel.select([sqlModel.rate]).order_by("-money")
    result = sqlModel.engine.connect().execute(re)

    for i in result:
        print(i,'刷新比例')
        if money > float(i.money):
            return float(i.rate)


