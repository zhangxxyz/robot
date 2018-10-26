import re
import ZK_Model.ZKOrderDataModel as sqlModel
import time


# 商品为联盟产品的回复
def successReplay(dict):
    beforeCouponPrice = float(dict['zk_final_price'])
    try:
        copupon = dict['coupon_info']
        print(copupon)
        money = re.findall('\d+', copupon)
        if beforeCouponPrice >= float(money[0]):
            beforeCouponPrice = beforeCouponPrice - float(money[1])
    except:
        pass
    returnMoney = beforeCouponPrice * float(dict['commission_rate']) / 100
    returnMoney = returnMoneyRate(returnMoney)
    replay_text = "约返您：" + str('%.2f' % returnMoney) + "  券后：" + str(beforeCouponPrice) + " 復·制这段描述" + '《'+str(dict[
        'tbk_pwd'])[1:-1] +')' + "后到淘*寳♀"+'\n'+'  收货成功后返利直接划到您当前账户'
    return replay_text

    pass


# 返利分级
def returnMoneyRate(money):
    scale = 0.00
    if money < 0.1:
        scale = 0.9
    if 0.1 <= money < 1:
        scale = 0.85
    if 1 <= money < 5:
        scale = 0.7
    if 5 <= money < 10:
        scale = 0.55
    if 10 <= money < 20:
        scale = 0.5
    if 20 <= money < 50:
        scale = 0.4
    if 50 <= money < 100:
        scale = 0.35
    if money >= 100:
        scale = 0.32
    return money * scale
# 非商品的回复
def other_replay(content):
    msg = ""
    print(content.text)
    if str(content.text) == '提现':
        return drawMoney(content)
    if str(content.text).isdigit() and len(content.text) == 18:
        bind_Order(content)


def bind_Order(content):
    pass

#        提现的操作
def drawMoney(content):
    data = sqlModel.select(
        [sqlModel.alreadyOrder]).where(
        sqlModel.and_(sqlModel.alreadyOrder.drawTime != 1, sqlModel.alreadyOrder.adzone_id == content.User.RemarkName,
                      sqlModel.or_(sqlModel.alreadyOrder.tk_status == 3, sqlModel.alreadyOrder.tk_status == 14)))
    result = sqlModel.engine.connect().execute(data)
    totalMoney = 0.00
    sqlArray = []
    for i in result:
        totalMoney += float(i.returnMoney)
        re = sqlModel.update(sqlModel.alreadyOrder).where(sqlModel.alreadyOrder.trade_id == i.trade_id).values(
            drawTime='2')
        sqlArray.append(re)
        print(i)
    for i in sqlArray:
        sqlModel.engine.connect().execute(i)

    if float(totalMoney) > 0:
        re = sqlModel.select([sqlModel.drawMoneyRecord]).where(
            sqlModel.drawMoneyRecord.adzoneid == content.User.RemarkName)
        res = sqlModel.engine.connect().execute(re).first()
        if res:
            sq = sqlModel.update(sqlModel.drawMoneyRecord).where(
                sqlModel.drawMoneyRecord.adzoneid == content.User.RemarkName).values(
                drawTime=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), drawMoney=str(totalMoney),
                isSuccess='0')
            sqlModel.engine.connect().execute(sq)
        else:
            record = sqlModel.drawMoneyRecord()
            record.drawTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            record.drawMoney = str(totalMoney)
            record.isSuccess = '0'
            record.adzoneid = content.User.RemarkName
            record.saveData(record)
        msg = '◇ ◇ ◇ 申 请 成 功 ◇ ◇ ◇ ' + '\n' + ' 【金额】:' + str(
            totalMoney) + '元' + '\n' + '  工作人员会在一到三个工作日内处理' + '\n' + '◇ ◇ ◇ 温馨提示 ◇ ◇ ◇' + '\n' + '  提现发红包是人工客服操作，因提现人数较多需排队处理,请耐心等待哦'
    else:
        msg = '抱歉,您当前账户余额为0元,暂时无法提现'
    if msg:
        return msg
