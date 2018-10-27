import re
import ZK_Model.ZKOrderDataModel as sqlModel
import ZK_QueryOrder
import time
import ZK_Model.globalModel as globa_Model


# 商品为联盟产品的回复
def successReplay(dict):
    beforeCouponPrice = float(dict['zk_final_price'])
    try:
        copupon = dict['coupon_info']
        print(copupon)
        money = re.findall('\d+', copupon)
        if beforeCouponPrice >= float(money[0]):
            beforeCouponPrice = beforeCouponPrice - float(money[1])
    except Exception as  error:
        print(error)
        print('查到商品并且回复的错误')
        pass
    returnMoney = beforeCouponPrice * float(dict['commission_rate']) / 100
    returnMoney = globa_Model.returnMoneyRate(returnMoney)
    replay_text = "约返您：" + str('%.2f' % returnMoney) + "  券后：" + str(
        '%.2f' % beforeCouponPrice) + " 復·制这段描述" + '《' + str(dict[
                                                                 'tbk_pwd'])[
                                                         1:-1] + ')' + "后到淘*寳♀" + '\n' + '  收货成功后返利直接划到您当前账户'
    return replay_text

    pass


# 非商品的回复
def other_replay(content):
    msg = ""
    print(content.text)
    if str(content.text).strip() == '提现':
        print(drawMoney(content))
        msg = drawMoney(content)
    print(content.text)
    if str(content.text).isdigit() and len(content.text) == 18:
        msg = bind_Order(content)
    # 二次补订单 cm1：后面为开始时间和结束时间，中间以都好分割，若为20分钟以内则结束时间为： 时间格式为2018-10-11 10:10:30
    if content.text[0:5] == 'cmd1:':
        msg = commandOperate(content)
    if len(msg):
        return msg


# 口令模式 执行一些特殊命令
def commandOperate(content):
    try:
        timeStr = str(content.text)[5::]
        timeArray = str(timeStr).split(',')
        print(timeArray, '时间数组')
        beginTime = timeArray[0]
        if not str(timeArray[1]) == ':':
            fishTime = str(timeArray[1])
        else:
            fishTime = None
        result = ZK_QueryOrder.customQueryOrder(startTime=str(beginTime), endTime=fishTime)
        print(result, '查询口令模式完成')
        return result
    except Exception as error:
        print(error)
        return '补单出错'


# 手动绑定订单
def bind_Order(content):
    re = sqlModel.update(sqlModel.alreadyOrder).where(sqlModel.alreadyOrder.trade_id == content.text).values(
        adzone_id=content.User.RemarkName)
    try:
        print('开始提交')
        sqlModel.engine.connect().execute(re)
        commitdata = commitResult = sqlModel.select([sqlModel.alreadyOrder]).where(
            sqlModel.and_(sqlModel.alreadyOrder.trade_id == content.text,
                          sqlModel.alreadyOrder.adzone_id == content.User.RemarkName))
        result = sqlModel.engine.connect().execute(commitdata).first().id
        print(result)
        s = '◇ ◇ 订 单 绑 定 成 功 ◇ ◇ ' + '\n\n' + '  主人,您终于来找奴家了,我还以为您不要我了,嘤嘤嘤[大哭][大哭][大哭]'
        return s
    except Exception as error:
        print('提交失败')
        print(error)
        return '  订单绑定失败,暂无该订单,您可以稍等十分钟再重新绑定,或者检查下是否使用了小淘的口令进行购买'


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
