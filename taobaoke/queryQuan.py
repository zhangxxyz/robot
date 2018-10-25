import taobaoke.ZK_Model.ZKOrderDataModel as  mysqlModel
import  taobaoke.ZK_Model.ZKOrderDataModel2 as  sqliteModel
import threading




def movePid():
    res = sqliteModel.select([sqliteModel.PIDList])
    result = sqliteModel.engine.connect().execute(res)
    array = []
    for i in result:
        array.append(i)

    for i in array:
        pids = mysqlModel.PIDList()
        pids.adzone_id = i.adzone_id
        pids.WXID = i.WXID
        pids.pid = i.pid
        pids.site_id = i.site_id
        pids.pidName = i.pidName
        pids.WXIDName = i.WXIDName
        pids.saveData(pids)

    print('pids数据库迁移完毕')

def moveUserData():
    re = sqliteModel.select([sqliteModel.userData])
    result = sqliteModel.engine.connect().execute(re)
    array = []
    for i in result:
        array.append(i)
    for i in array:
        usedata = mysqlModel.userData()
        usedata.WXIDName = i.WXIDName
        usedata.WXID = i.WXID
        usedata.fromWXDetails = i.fromWXDetails
        usedata.rename = i.rename
        usedata.useAdzone_id = i.useAdzone_id
        usedata.usePid = i.usePid
        usedata.NickName = i.NickName
        usedata.fromWXID = i.fromWXID
        usedata.fromNickName = i.fromNickName
        usedata.personMood = i.personMood
        usedata.fromRename = i.fromRename
        usedata.fromSourceusername = i.fromSourceusername
        usedata.saveData(usedata)
    print('用户数据迁移完毕')

# movePid()
moveUserData()
