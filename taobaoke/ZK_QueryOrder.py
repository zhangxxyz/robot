import top.api
import requests
import time
import ZK_Model.ZKOrderDataModel
import json
import threading
import ZK_Model.globalModel as global_models
import urllib.parse

sqlModel = ZK_Model.ZKOrderDataModel




# 自定义查询可以输入查询开始时间和结束时间进行查询 格式:2018-10-14 22:49:30
# 如果不输入结束时间,则默认查询一次开始时间 间隔为1200s
def customQueryOrder(startTime=None, endTime=None):
    print(startTime,endTime,'自定义查询订单')
    modelArray =[]
    t = time.strptime(startTime, '%Y-%m-%d %H:%M:%S')
    startTimeStamp = time.mktime(t)
    if not endTime:
        endTimeStamp = startTimeStamp + 1198
    else:
        e = time.strptime(endTime, '%Y-%m-%d %H:%M:%S')
        endTimeStamp = time.mktime(e)
    while startTimeStamp < endTimeStamp:
        current = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(startTimeStamp))
        url = 'http://apiorder.vephp.com/order?vekey=' + global_models.vekey + '&start_time='+str(current) + '&span=1200'
        print(url, current)
        print('自定义查询')
        try:
            resp = requests.get(url)
            dict = resp.json()
            print(dict)
            if dict['data']:
                orderArray = saveUserOrder(dict['data'])
                modelArray.extend(orderArray)

        except Exception as Error:
            print('自定义查询出错')
            print(Error)

        startTimeStamp += 1198

    successMsg = "补单成功:共{}条新数据".format(len(modelArray))
    return successMsg


# 循环查询函数
def queryAllOdrder():
    currentTime = time.time() - 1200
    currentTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(currentTime))

    # currentTime = '2018-11-11 02:40:00'
    # print(currentTime)
    # print('循环查询线程',threading.current_thread(),id(threading.current_thread()))
    # currentTime = urllib.parse.quote(currentTime)
    url = 'http://apiorder.vephp.com/order?vekey=' + global_models.vekey + '&start_time=' + str(
        currentTime) + '&span=1200'
    print(url, currentTime)
    print('循环查询')
    try:
        resp = requests.get(url)
        print(resp)
        dict = resp.json()
        print(dict)
        if dict['data']:
            returnData = saveUserOrder(dict['data'])
            if returnData:
                print(returnData)
                return returnData

    except Exception as Error:
        print('轮询订单出错')
        print(Error)


def saveUserOrder(data):

    sourceArray = []
    for dict in data:
        # for key, values in dict.items():
        #     print(key, values)
        res = sqlModel.select([sqlModel.alreadyOrder]).where(sqlModel.alreadyOrder.trade_id == dict['trade_id'])
        result = sqlModel.engine.connect().execute(res)
        try:
            exesitOrder = result.first().trade_id
        except:
            sourceArray.append(dict)
            order = sqlModel.alreadyOrder()
            order.returnMoney = global_models.returnMoneyRate(float(dict.get('pub_share_pre_fee',"0")),item_number=dict.get('item_num',"1"))
            order.adzone_id = dict.get('adzone_id',None)
            order.adzone_name = dict.get('adzone_name',None)
            order.alipay_total_price = dict.get('alipay_total_price',None)
            order.auction_category = dict.get('auction_category',None)
            order.commission = dict.get('commission', None)
            order.commission_rate = dict.get('commission_rate', None)
            order.create_time = str(dict.get('create_time',None))
            order.income_rate = dict.get('income_rate',None)
            order.item_num = dict.get('item_num',"1")
            order.item_title = dict.get('item_title',None)
            order.num_iid = dict.get('num_iid',None)
            order.pay_price = dict.get('pay_price',"0")
            order.price = dict.get('price',"0")
            order.pub_share_pre_fee = dict.get('pub_share_pre_fee',None)
            order.seller_nick = dict.get('seller_nick',None)
            order.seller_shop_title = dict.get('seller_shop_title',None)
            order.site_id = dict.get('site_id',None)
            order.site_name = dict.get('site_name',None)
            order.subsidy_fee = dict.get('subsidy_fee',None)
            order.subsidy_rate = dict.get('subsidy_rate',None)
            order.subsidy_type = dict.get('subsidy_type',None)
            order.terminal_type = dict.get('terminal_type',None)
            order.tk3rd_type = dict.get('tk3rd_type',None)
            order.tk_status = dict.get('tk_status',None)
            order.tk_statusDesc = orderStatus(dict['tk_status'])
            order.total_commission_fee = dict.get('total_commission_fee',None)
            order.total_commission_rate = dict.get('total_commission_rate',None)
            order.trade_id = dict.get('trade_id',None)
            order.trade_parent_id = dict.get('trade_parent_id',None)
            order.earning_time = dict.get('earning_time', "暂未结算")
            order.tk3rd_pub_id = dict.get('tk3rd_pub_id', "无第三方推广")
            order.order_type = dict.get('order_type',)
            order.relation_id = dict.get('relation_id', "暂无渠道关系")
            order.special_id = dict.get('special_id', "暂无会员")
            order.saveData(order)

    return sourceArray



# 监听付款订单
def listenOrder():
    print(threading.currentThread(), '第一次')
    re = sqlModel.select([sqlModel.alreadyOrder]).where(sqlModel.alreadyOrder.tk_status == '12')
    con = sqlModel.engine.connect()
    result = con.execute(re)
    sqlArray = []
    endOrderArray = []
    for order in result:
        print('查询订单开始睡眠',threading.current_thread(),id(threading.current_thread()))
        time.sleep(5)
        t = time.strptime(order.create_time, '%Y-%m-%d %H:%M:%S')
        startTimeStamp = time.mktime(t) - 200
        currentTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(startTimeStamp))
        url = 'http://apiorder.vephp.com/order?vekey=' + global_models.vekey + '&start_time=' + str(
            currentTime) + '&span=1200'
        print('监听订单查询')
        try:
            resp = requests.get(url)
            dict = resp.json()
            print(dict)
            for data in dict['data']:
                if (int(data['tk_status']) != 12) and (str(data['trade_id'])==str(order.trade_id)):
                    endTime = data.get('earning_time', '暂未结算')
                    re = sqlModel.update(sqlModel.alreadyOrder).where(
                        sqlModel.alreadyOrder.trade_id == order.trade_id).values(tk_status=data['tk_status'],
                                                                                 tk_statusDesc=orderStatus(
                                                                                     data['tk_status']),
                                                                                 earning_time=endTime)
                    sqlArray.append(re)
                if str(data['tk_status']) == '3' and (str(data['trade_id'])==str(order.trade_id)):
                        temp = ([data], order)
                        endOrderArray.append(temp)

        except Exception as Error:
            print('监听订单出错')
            print(threading.currentThread(), '第三次')
            print(Error)

    for sql in sqlArray:
        sqlModel.engine.connect().execute(sql)
    print('---------------------')

    return endOrderArray


def orderStatus(status):
    status = int(status)
    if status == 3:
        return "订单结算"
    if status == 12:
        return "订单付款"
    if status == 13:
        return "订单失效"
    if status == 14:
        return "订单成功"
    else:
        return status

