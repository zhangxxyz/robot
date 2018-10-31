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
    replay_text =  "【当前价格】：" +str(dict['zk_final_price'])+'元\n'+ "【券后价格】：" + str(
        '%.2f'%beforeCouponPrice)+ '元\n'+ "【券后再返】：" + returnMoney+ '元\n' + " 復·制这段描述" + '《' + str(dict[
                                                                 'tbk_pwd'])[
                                                         1:-1] + ')' + "后到淘*寳♀" + '\n' + '---------------\n 收货成功后返利直接划到您当前账户'
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
    # if str(content.text).strip() == '帮助':
    #     msg = '您好,您可以这样说：\n  001:订单统计\n  002:我的邀请\n  003:会员系统'
    # if str(content.text).strip() == '001':
    #     msg = order_Statistical(content)
    # if str(content.text).strip() == '002':
    #     msg = myInvite(content)
    if len(msg):
        return msg

def myInvite(content):
    re = sqlModel.select([sqlModel.userData]).where(sqlModel.userData.rename == content.User.RemarkName)
    usedata = sqlModel.engine.connect().execute(re).first()
    query = sqlModel.select([sqlModel.userData]).where(sqlModel.userData.fromWXID==usedata.WXID)
    result = sqlModel.engine.connect().execute(query)
    allName = ""
    index = 0
    for i in result:
        index+=1
        allName = "{},'{}'".format(allName,i.NickName)
        print(i)
    replay_text = '  您好,您总共邀请了%d位好友,他们分别是%s'%(index,allName)
    print(replay_text)
    return replay_text



# 订单统计
def order_Statistical(content):
    re = sqlModel.select([sqlModel.alreadyOrder]).where(
        sqlModel.and_(sqlModel.alreadyOrder.adzone_id == content.User.RemarkName,
                      sqlModel.alreadyOrder.tk_status != '13'))
    queryRe = sqlModel.engine.connect().execute(re)

    orderTotal = 0
    successOrder = 0
    waitIngOrder = 0
    drawMoneyOrder = 0
    failureOrder = 0
    canDrawMoneyOrder = 0
    drawMoneyZhongOrder = 0
    orderTotalMoney = 0.00
    canDrawMoneyOrderMoney = 0.00
    drawMoneyZhongMoney = 0.00
    drawMoney = 0.00
    successMoney = 0.00
    waitMoney = 0.00
    for i in queryRe:
        orderTotal += 1
        orderTotalMoney += float(i.returnMoney)
        if str(i.tk_status) == '3' or str(i.tk_status) == '14':
            print('看这里看这里')
            successOrder += 1
            successMoney += float(i.returnMoney)
            if str(i.drawTime) == '1':
                drawMoney += float(i.returnMoney)
                drawMoneyOrder += 1
            if str(i.drawTime) == '2':
                drawMoneyZhongOrder += 1
                drawMoneyZhongMoney += float(i.returnMoney)
            if str(i.drawTime) == '0':
                canDrawMoneyOrder += 1
                canDrawMoneyOrderMoney += float(i.returnMoney)

        if str(i.tk_status) == '12':
            waitIngOrder += 1
            waitMoney += float(i.returnMoney)

    replay_text = '  您当前共有{}笔订单,其中待收货订单为{}笔,可返您{}元,已收货订单为{}笔,其中{}笔订单已经提现,总金额为{}元,{}笔订单处于提现中,金额为{}元,{}笔订单可提现,金额为{}元'.format(orderTotal,
                                 waitIngOrder,str('%.2f'%waitMoney),successOrder,drawMoneyOrder,str('%.2f'%drawMoney),drawMoneyZhongOrder,str('%.2f'%drawMoneyZhongMoney),canDrawMoneyOrder,str('%.2f'%canDrawMoneyOrderMoney))
    print(replay_text)
    return replay_text


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
    re = sqlModel.update(sqlModel.alreadyOrder).where(sqlModel.alreadyOrder.trade_parent_id == content.text).values(
        adzone_id=content.User.RemarkName)
    try:
        print('开始提交')
        sqlModel.engine.connect().execute(re)
        commitdata = commitResult = sqlModel.select([sqlModel.alreadyOrder]).where(
            sqlModel.and_(sqlModel.alreadyOrder.trade_parent_id == content.text,
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
                drawTime=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), drawMoney=str('%.2f'%totalMoney),
                isSuccess='0')
            sqlModel.engine.connect().execute(sq)
        else:
            record = sqlModel.drawMoneyRecord()
            record.drawTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            record.drawMoney = str(totalMoney)
            record.isSuccess = '0'
            record.adzoneid = content.User.RemarkName
            record.saveData(record)
        msg = '◇ ◇ ◇ 申 请 成 功 ◇ ◇ ◇ ' + '\n' + ' 【金额】:' + str('%.2f'%
            totalMoney) + '元' + '\n' + '  工作人员会在一到三个工作日内处理' + '\n' + '---------------------' + '\n' + '  提现发红包是人工客服操作，因提现人数较多需排队处理,请耐心等待哦'
    else:
        msg = '抱歉,您当前账户余额为0元,暂时无法提现'
    if msg:
        return msg
