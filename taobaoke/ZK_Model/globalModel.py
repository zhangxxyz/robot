productionUrl = "https://eco.taobao.com/router/rest"
appkey = "25083490"
secret = "77068d785fb6dc77d1865dc0737e1684"
port = '80'
pid = "28940900149"
vekey = "V00000384Y70837048"
dictArray = {}

# 返利分级 money:预估收入 item_number:购买数量
def returnMoneyRate(money,item_number = 1):
    money = float(money) / float(item_number)
    scale = 0.00
    if not len(dictArray):
        print('去查询比例')
        getGlobalScale()
    try:
        # dict = dictArray.so
       for key,values in dictArray.items():
           print(key,values)
           if float(money) >= float(key):
                scale = float(values)
                break
    except Exception as error:
        print('获取返利比例出错',error)
        scale = 0.5
    print(money,scale,float(item_number))
    returnMoney = money * scale * float(item_number)
    return str('%.2f'%returnMoney)

def getGlobalScale():
    import ZK_Model.ZKOrderDataModel as sqlModel
    import threading
    global timer
    # global dictArray
    # dictArray = {}
    print('开始从数据库查询当前比例')

    timer = threading.Timer(28800,getGlobalScale)
    timer.setDaemon(True)
    timer.start()
    re = sqlModel.select([sqlModel.rate]).order_by("-money")
    result = sqlModel.engine.connect().execute(re)
    n = 0
    for i in result:
        print(i,'刷新比例',n)
        n+=1
        dictArray[i.money] = i.rate



