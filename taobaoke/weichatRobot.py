import itchat, time
from itchat.content import *
import queryGoods
import zk_WiChatReplay
import json
import threading
import ZK_Model.ZKOrderDataModel
import copy
import ZK_QueryOrder
import random

sqlModel = ZK_Model.ZKOrderDataModel


class useInfo(object):
    def __init__(self, **kwargs):
        if kwargs.get('RemarkName', None):
            data = sqlModel.select(
                [sqlModel.userData.WXID, sqlModel.userData.WXIDName, sqlModel.userData.useAdzone_id,
                 sqlModel.userData.usePid]).where(
                sqlModel.userData.rename == kwargs['RemarkName'])
        if kwargs.get('NickName', None):
            data = sqlModel.select(
                [sqlModel.userData.WXID, sqlModel.userData.WXIDName, sqlModel.userData.useAdzone_id,
                 sqlModel.userData.usePid]).where(
                sqlModel.userData.NickName == kwargs['NickName'])
        else:
            raise Exception("没有这个参数")
        res = sqlModel.engine.connect().execute(data)
        for i in res:
            self.useWXID = i.WXID
            self.useWxName = i.WXIDName
            self.adzone_id = i.useAdzone_id
            self.pid = i.usePid


# 注册消息
# text:文本 map:地图 card:名片 note:通知 sharing:分享名称
# picture 图片 recording:语音 attachment:附件 video:视频
# friends 好友邀请 system：系统消息
@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def text_reply(msg):
    print(msg)
    print(msg.User, type(msg.User))
    b =''
    try:
        float(msg.User.RemarkName)
        b = '1'
    except:
        b = '2'
    if not msg.User.RemarkName or (int(b) ==2 ):
        friendInfo = useInfo(NickName=msg.User.NickName)
        re = sqlModel.select([sqlModel.PIDList]).where(sqlModel.PIDList.WXID == None)
        result = sqlModel.engine.connect().execute(re).first()
        pidUpdate = sqlModel.update(sqlModel.PIDList).where(sqlModel.PIDList.adzone_id == result.adzone_id).values(
            WXID=friendInfo.useWXID, WXIDName=friendInfo.useWxName)
        sqlModel.engine.connect().execute(pidUpdate)
        itchat.set_alias(userName=msg.fromUserName, alias=result.adzone_id)
        da = sqlModel.update(sqlModel.userData).where(sqlModel.userData.NickName == msg.User.NickName).values(
            rename=result.adzone_id, usePid=result.pid, useAdzone_id=result.adzone_id)
        sqlModel.engine.connect().execute(da)
        return

    p = queryGoods.zhuanLian(str(msg.text), use_pid=msg.User.RemarkName)
    time.sleep(2)
    try:
        if p['result']:
            replayContent = zk_WiChatReplay.successReplay(p['data'])
            return replayContent
    except Exception as Error:
        errDesc = p['error']
        replayMsg = ""
        # if int(errDesc) == 1:

        if int(errDesc) == 6001:
            replayMsg = '您好,分享给我商品链接,我才能帮助您省钱哦～～～'
        else:
            replayMsg = "抱歉,该商家暂无优惠活动,您可以换一家试试"
        temp = zk_WiChatReplay.other_replay(msg)
        if temp:
            replayMsg = temp
        # return replayMsg


# @itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
# def download_files(msg):
#     msg.download(msg.fileName)
#     typeSymbol = {
#         PICTURE: 'img',
#         VIDEO: 'vid', }.get(msg.type, 'fil')
#     return '@%s@%s' % (typeSymbol, msg.fileName)


@itchat.msg_register(FRIENDS)
def add_friend(msg):
    saveFriendData(msg.Content)
    msg.user.verify()
    replayContent = '  您好,我是小淘,您身边的省钱专家,我们的目标只有一个,那就是省钱!省钱!!省钱!!!' + '\n' + '  当您在淘宝购物的时候,只要点击商品右上角分享按钮,分享给小淘,小淘会在全网检索优惠活动,并生成带有优惠的原商品链接给您,您只要长按复制后到淘♂寳♀,即可自动弹出.' + '\n' + '  在您确认收货以后,我们就会将商家所做活动的优惠金额返还给您,' + '\n' + ' 简单粗暴,赶紧分享给小淘试试吧!!!~~~'
    nextContent = '  推荐好友奖励现金红包的活动开启,成功推荐好友,双方都会得到0.01-200随机现金红包的奖励！！！'+'赶紧来参加吧～'
    msg.user.send(replayContent)
    msg.user.send(nextContent)


@itchat.msg_register(TEXT, isGroupChat=True)
def text_reply(msg):
    if msg.isAt:
        pass
        # msg.user.send(u'@%s\u2005I received: %s' % (
        #     msg.actualNickName, msg.text))
# 发给所有好友的通告
def sendAllFriendMsg(content):
    friends = itchat.get_friends(update=True)
    for i in  friends:
        i.send(content)

# 关于订单状态变化对应消息的回复 order:刷新的订单数组 finis_order:订单结算完成之后才会有的,数据库数据
def orderReplay(order, finish_order=None):
    print(order)
    print("6666")
    for dict in order:
        time.sleep(10)
        try:
            adzoneid = dict['adzone_id']
            orderStatus = int(dict['tk_status'])
            print(adzoneid, orderStatus)
            res = sqlModel.select([sqlModel.userData]).where(sqlModel.userData.useAdzone_id == adzoneid)
            result = sqlModel.engine.connect().execute(res).first()
            nameaArray = [result.rename, result.WXID]
            for i in nameaArray:
                friend = itchat.search_friends(name=i)
                print(i)
                print(friend)
                if friend:
                    break
            returnMoney = zk_WiChatReplay.returnMoneyRate(float(dict['pub_share_pre_fee']))
            print(orderStatus, type(orderStatus))
            if orderStatus == 12:
                msg = '亲爱的' + str(friend[0].NickName) + ':' + '\n' + '' + '  恭喜您下单成功' + '\n' + ' 【商品名称】:' + str(
                    dict['item_title']) + '\n' + '  订单结算完成后预计可返:' + str('%.2f' % returnMoney) + '元' + '\n'+'  请注意：返利金额会根据您的付款金额变动而发生变化'+'\n\n'
                friend[0].send(msg)
            if orderStatus == 3:
                msg = '亲爱的' + str(friend[0].NickName) + ':' + '\n' + '' + '  确认收货成功,红包已入账' + '\n' + ' 【商品名称】:' + str(
                    dict['item_title']) + '\n' + ' 【完成时间】:' + str(
                    dict.get('earning_time', "null")) + '\n' + ' 【预计可返】:' + str(
                    finish_order.returnMoney) + '元' + '\n\n' + '  发送"提现"可进行提现操作'
                print(msg)
                friend[0].send(msg)

        except Exception as  Error:
            print(Error, '错误')
            pass

    pass

# 暂时没有存
def saveQueryRecord(data, remarkName):
    queryRecord = ZK_Model.ZKOrderDataModel.queryRecord()
    queryRecord.seller_id = data['seller_id']
    queryRecord.user_type = data['user_type']
    queryRecord.item_url = data['user_type']
    queryRecord.num_iid = data['num_iid']
    queryRecord.item_title = data['title']
    currentTime = time.time()
    currentTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(currentTime))
    queryRecord.queryTime = currentTime
    user = useInfo(RemarkName=remarkName)
    print(user, user.useWXID, '124444444444444')
    queryRecord.useWXID = user.useWXID
    queryRecord.useWXName = user.useWxName
    queryRecord.saveData(queryRecord)


# 好友资料入库
def saveFriendData(content):
    print('加好友资料')
    print(content)
    # 我自推自加
    # D = '<msg fromusername="wxid_kwscs91sfsjq12" encryptusername="v1_540963d3f03e6fb16c3632395512e8c8b1b80b2ccb83495fa24885cbc4b159b032a6078100e6ba7de1d5f3c2e8c209b7@stranger" fromnickname="😱 🙄 😳 😜 😂" content="我是😱 🙄 😳 😜 😂"  shortpy="?????" imagestatus="3" scene="17" country="CN" province="" city="" sign="宠辱不惊，看庭前花开花落         去留无意，望天空云卷云舒" percard="1" sex="1" alias="zhangxyz12345677" weibo="" albumflag="0" albumstyle="0" albumbgimgid="" snsflag="1" snsbgimgid="http://shmmsns.qpic.cn/mmsns/wjVtTPhRGGibXnVmxE9nSCVPHXqJKKcXHpiang4aoka7YY96aFdRtKAFqMDMgeIw18GaYbPKibSDBI/0" snsbgobjectid="12758414557951111441" mhash="1eb52baae0281ce1051819888f0e63c7" mfullhash="1eb52baae0281ce1051819888f0e63c7" bigheadimgurl="http://wx.qlogo.cn/mmhead/ver_1/NEel6JCYaYhTjJIJWsI9ZVuicCibZlarOdDjSMzxwhWSdfFsMyKyykWG7be0ehW2HVCg7VugQjqdjv9GwOK1fgYtWA2WWjNdEPJ8ZqLVkWEog/0" smallheadimgurl="http://wx.qlogo.cn/mmhead/ver_1/NEel6JCYaYhTjJIJWsI9ZVuicCibZlarOdDjSMzxwhWSdfFsMyKyykWG7be0ehW2HVCg7VugQjqdjv9GwOK1fgYtWA2WWjNdEPJ8ZqLVkWEog/132" ticket="v2_7e78e08edd889e438d535180bc59afa8f2ade1c23038197394ff346a9da246fefb47de7523e83bea0ecbf36a6b4fd1e433e8975bcc41096b3f10d6c1bf575dd4@stranger" opcode="2" googlecontact="" qrticket="" chatroomusername="" sourceusername="wxid_kwscs91sfsjq12" sourcenickname="😱 🙄 😳 😜 😂"><brandlist count="0" ver="672649033"></brandlist></msg>'
    # 我推亚加
    # content = '<msg fromusername="wxid_6l6y8kneda2i22" encryptusername="v1_82d789a41179eb7ecf9ef4f00d32237def49bc493232ee37c25a9870ea2dcd650fdacd2f3fc976b95ff615ba5a94dd9f@stranger" fromnickname="tyfighting" content="我是张亚琦"  shortpy="TYFIGHTING" imagestatus="3" scene="17" country="CN" province="" city="" sign="" percard="1" sex="2" alias="zyq981796707" weibo="" albumflag="0" albumstyle="0" albumbgimgid="" snsflag="1" snsbgimgid="http://mmsns.qpic.cn/mmsns/PiajxSqBRaELLJ06Y4YV3pskTMZKkt5pSnvIicbzz2uhq6NJVdzCUV47EwdubrG4RG/0" snsbgobjectid="11713839254557504215" mhash="113f915720c99f1b3e1398d0ae49a10c" mfullhash="113f915720c99f1b3e1398d0ae49a10c" bigheadimgurl="http://wx.qlogo.cn/mmhead/ver_1/cQXddgYHkKXiaHrmqRc4RhHbGsTF2vpsTSQqgqibFpZOpyO6wuM6WzaiauaEs3z331rBwPLubKzpgfOJ2Bekjhucsp8BFxH5MVibEPNc06LIaTQ/0" smallheadimgurl="http://wx.qlogo.cn/mmhead/ver_1/cQXddgYHkKXiaHrmqRc4RhHbGsTF2vpsTSQqgqibFpZOpyO6wuM6WzaiauaEs3z331rBwPLubKzpgfOJ2Bekjhucsp8BFxH5MVibEPNc06LIaTQ/96" ticket="v2_85e8380195a96f4cb958fa50100abb2625005817916f9ac0059fbd7b4a25ec5c6c21261dda96f67de4ba92d07e0dee4370cf606292dceb5c8a7e2a21825c21f3@stranger" opcode="2" googlecontact="" qrticket="" chatroomusername="" sourceusername="wxid_kwscs91sfsjq12" sourcenickname="😱 🙄 😳 😜 😂"><brandlist count="0" ver="672649033"></brandlist></msg>'
    # 我推李加
    # content = '<msg fromusername="Acid_Eater" encryptusername="v1_bbc7a9bcbc6f4a65a7c09f9177c1daf90339c39641138e165094f1955b308225@stranger" fromnickname="YJ" content=""  shortpy="YJ" imagestatus="3" scene="17" country="CN" province="Beijing" city="Haidian" sign="努力攀登不问高" percard="1" sex="2" alias="" weibo="" albumflag="3" albumstyle="0" albumbgimgid="" snsflag="17" snsbgimgid="http://shmmsns.qpic.cn/mmsns/fhicotyX5dAcia0Ndia6PtrTfuQUfZib7RepLJ9xAibZUe1kHTafng3dhluibykB455Q17lzn77mA590A/0" snsbgobjectid="12906563367542198348" mhash="98bfe78d718bcb734fb5794bf921c250" mfullhash="98bfe78d718bcb734fb5794bf921c250" bigheadimgurl="http://wx.qlogo.cn/mmhead/ver_1/jbLPLRH3wRvyY5ibtibwfUrxyUyqpZIU8553YucbSMkBJXsFky3aVqnhwa4PNdJvzgX5JrgjYcRL74oHIUhBxavFUUyLCpKRzIR0m5UiaTvduQ/0" smallheadimgurl="http://wx.qlogo.cn/mmhead/ver_1/jbLPLRH3wRvyY5ibtibwfUrxyUyqpZIU8553YucbSMkBJXsFky3aVqnhwa4PNdJvzgX5JrgjYcRL74oHIUhBxavFUUyLCpKRzIR0m5UiaTvduQ/96" ticket="v2_3007fc7792372b0e521bb4e5594d074b79284224968a9255ae9c9983baab5244afa6ce1cab8be0871bcb5ca029317a0aede73df09a595360a9e7399c2e11fc18@stranger" opcode="2" googlecontact="" qrticket="" chatroomusername="" sourceusername="wxid_kwscs91sfsjq12" sourcenickname="YJ"><brandlist count="0" ver="672648810"></brandlist></msg>'
    # 李推我加
    # content = '<msg fromusername="wxid_kwscs91sfsjq12" encryptusername="v1_540963d3f03e6fb16c3632395512e8c8b1b80b2ccb83495fa24885cbc4b159b032a6078100e6ba7de1d5f3c2e8c209b7@stranger" fromnickname="😱 🙄 😳 😜 😂" content="我是😱 🙄 😳 😜 😂"  shortpy="?????" imagestatus="3" scene="17" country="CN" province="" city="" sign="宠辱不惊，看庭前花开花落         去留无意，望天空云卷云舒" percard="1" sex="1" alias="zhangxyz12345677" weibo="" albumflag="0" albumstyle="0" albumbgimgid="" snsflag="1" snsbgimgid="http://shmmsns.qpic.cn/mmsns/wjVtTPhRGGibXnVmxE9nSCVPHXqJKKcXHpiang4aoka7YY96aFdRtKAFqMDMgeIw18GaYbPKibSDBI/0" snsbgobjectid="12758414557951111441" mhash="1eb52baae0281ce1051819888f0e63c7" mfullhash="1eb52baae0281ce1051819888f0e63c7" bigheadimgurl="http://wx.qlogo.cn/mmhead/ver_1/NEel6JCYaYhTjJIJWsI9ZVuicCibZlarOdDjSMzxwhWSdfFsMyKyykWG7be0ehW2HVCg7VugQjqdjv9GwOK1fgYtWA2WWjNdEPJ8ZqLVkWEog/0" smallheadimgurl="http://wx.qlogo.cn/mmhead/ver_1/NEel6JCYaYhTjJIJWsI9ZVuicCibZlarOdDjSMzxwhWSdfFsMyKyykWG7be0ehW2HVCg7VugQjqdjv9GwOK1fgYtWA2WWjNdEPJ8ZqLVkWEog/132" ticket="v2_7e78e08edd889e438d535180bc59afa813164a23716ca7a8de8735bd4a7d58ccf261c0c490f0f486e17d2a2afa7adc12ffcb665d993c7c3403fb66b3e4dfb99f@stranger" opcode="2" googlecontact="" qrticket="" chatroomusername="" sourceusername="Acid_Eater" sourcenickname="YJ"><brandlist count="0" ver="672649033"></brandlist></msg>'
    d1 = str(content).split('><')[0][4::].split('" ')
    friend = ZK_Model.ZKOrderDataModel.userData()
    friend.WXIDName = (getFriendData("fromusername", d1))
    alias = (getFriendData("alias", d1))
    if not alias:
        alias = (getFriendData("fromusername", d1))
    friend.WXID = alias
    friend.NickName = (getFriendData("fromnickname", d1))
    friend.personMood = (getFriendData("sign", d1))
    friend.fromSourceusername = (getFriendData("sourceusername", d1))
    friend.fromNickName = getFriendData("sourcenickname", d1)
    friend.fromWXDetails = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    s = ZK_Model.ZKOrderDataModel.select([ZK_Model.ZKOrderDataModel.userData.WXID]).where(
        ZK_Model.ZKOrderDataModel.userData.WXIDName == (getFriendData("sourceusername", d1)))
    res = ZK_Model.ZKOrderDataModel.engine.connect().execute(s)
    for i in res:
        print(i.WXID)
        friend.fromWXID = i.WXID
    friend.saveData(friend)


#   循环遍历字符串获取数据
def getFriendData(key, array):
    for i in array:
        if i.find(key) >= 0:
            temp = i.strip()
            temp = temp.strip('"')
            st = temp[len(key) + 2::]
            return st

# 抓订单
def getOrder():
    timer = threading.Timer(555, getOrder)
    timer.setDaemon(True)
    timer.start()
    print('循环抓订单')
    orderArray = ZK_QueryOrder.queryAllOdrder()
    if orderArray:
        orderReplay(orderArray)


# 刷新一遍付款订单的状态
def listenOrder():
    timeNow = time.time()
    timeNow = time.strftime('%Y%m%d%H:%M:%S', time.localtime(timeNow))
    timeNow = time.strptime(timeNow, '%Y%m%d%H:%M:%S')
    if timeNow.tm_hour < 16:
        s = (16 - timeNow.tm_hour) * 3600
    elif timeNow.tm_hour > 19:
        s = (24 - (timeNow.tm_hour - 19)) * 3600
    else:
        print('开始监听订单')
        s = 24 * 3600
        finish = ZK_QueryOrder.listenOrder()
        if finish:
            try:
                print('开始回复')
                for i in finish:
                    print(type(i), type(i[0]), type(i[1]))
                    orderReplay(i[0], finish_order=i[1])
            except Exception as error:
                print(error)
                pass
    print(s,'当前延迟刷新订单状态的延迟')
    timer = threading.Timer(s, listenOrder)
    timer.setDaemon(True)
    timer.start()


def cleanUseInfo(NickName):
    pass


# friend = itchat.search_friends(name=NickName)
# print(friend[0].UserName)
# itchat.set_alias(userName=friend[0].UserName, alias='')
# print(friend)
# print('--------------')

# friendArray = itchat.get_friends(update=True)
# for i in friendArray:
#     print(i)
# friend[0].send(msg)

def pingMsg():
    s = random.randint(29,2000)
    timer = threading.Timer(s, pingMsg)
    timer.setDaemon(True)
    timer.start()
    friend = itchat.search_friends(name='44341000355')
    friend[0].send(str(s))


def getChatStatus():
    print(threading.currentThread(), '当前线程订单')
    # cleanUseInfo('666')
    # pingMsg()
    getOrder()
    # listenOrder()


def runChat():
    print(threading.currentThread(), '当前线程聊天')
    itchat.auto_login(False)
    itchat.run(True)


timer = threading.Timer(20, getChatStatus)
timer.setDaemon(True)
timer.start()
p1 = threading.Thread(target=runChat)
p1.start()


