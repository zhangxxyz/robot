from sqlalchemy import create_engine, ForeignKey, Column, Integer, String, DateTime
from sqlalchemy.sql import and_, or_, not_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import select
from sqlalchemy import update
from sqlalchemy.orm import sessionmaker
import sqlalchemy.orm.query
from sqlalchemy import func
import os

path = os.path.abspath('.')
index = path.rfind('taobaoke')
path = path[0:index]
path = "mysql+mysqlconnector://root:123456@47.97.111.175:3306/test?charset=utf8mb4"

# path = 'sqlite:///%s/user.sqlite'%path
print(path)
engine = create_engine(path, echo=False,pool_recycle=3600)
Base = declarative_base()
DBSession = sessionmaker(bind=engine)
session = DBSession()
# DBSession.configure(bind=engine)
conn = engine.connect()


# 用户个人信息
class userData(Base):
    __tablename__ = "userData"
    id = Column(Integer, primary_key=True)
    # 备注
    rename = Column(String(32))
    # 昵称
    NickName = Column(String(40))
    # 一个类似于微信号的标识符,注册的比较早的号这个字段直接是微信号,后来的微信这个是一段不变的码
    WXIDName = Column(String(40))
    # 微信号
    WXID = Column(String(32))
    # 用户绑定淘宝pid
    usePid = Column(String(120))
    # 用户adconeid
    useAdzone_id = Column(String(32))
    # 个人签名
    personMood = Column(String(300))
    # 推荐人的微信标识符
    fromSourceusername = Column(String(30))
    # 推荐人标识符
    fromNickName = Column(String(32))
    # 推荐人微信号
    fromWXID = Column(String(32))
    # 推荐人备注
    fromRename = Column(String(32))
    # 推荐人个人签名
    fromWXDetails = Column(String(300))


    @classmethod
    def saveData(cls, data):
        session.add(data)
        session.commit()
        session.close()

class drawMoneyRecord(Base):
    __tablename__ = "drawMoneyRecord"
    id = Column(Integer, primary_key=True)
    # 申请提现时间
    drawTime = Column(String(40))
    # 提现金额
    drawMoney = Column(String(10))
    # 是否成功 1是 0等待体现
    isSuccess = Column(String(10),default='0')
    # 对应的的adzoneid
    adzoneid = Column(String(32))
    @classmethod
    def saveData(cls, data):
        session.add(data)
        session.commit()
        session.close()

# 用户查询过的商品记录
class queryRecord(Base):
    __tablename__ = "queryGoods"
    id = Column(Integer, primary_key=True)
    # 卖家id
    seller_id = Column(String(32))
    # 1、表示天猫，0、表示淘宝
    user_type = Column(String(4))
    # 商品链接地址
    item_url = Column(String(320))
    # 商品标题
    item_title = Column(String(160))
    # 商品id
    num_iid = Column(String(40))
    # 查询时间
    queryTime = Column(String(40))
    # 用户微信号
    useWXID = Column(String(40))
    # 用户标识符
    useWXName = Column(String(40))

    # 关联用户备注
    # renameId = Column(String(32),ForeignKey('userData.rename'))

    @classmethod
    def saveData(cls, data):
        session.add(data)
        session.commit()
        session.close()

class rate(Base):
    __tablename__ = "rate"
    id = Column(Integer, primary_key=True)
    money = Column(String(20))
    rate  = Column(String(20))

# 抓取订单
class alreadyOrder(Base):
    __tablename__ = "userOrder"
    id = Column(Integer, primary_key=True)
    # 付款金额
    alipay_total_price = Column(String(40))
    # 返利金额(经过等级计算之后的金额,是我要返给用户的)
    returnMoney = Column(String(10))
    # 淘客订单状态，  3：订单结算，  12：订单付款，   13：订单失效，  14：订单成功
    tk_status = Column(String(8))
    # 订单状态描述
    tk_statusDesc = Column(String(20))
    # 淘宝父订单号
    trade_parent_id = Column(String(40))
    # 淘宝订单号
    trade_id = Column(String(40),)
    # 推广者获得的收入金额，对应联盟后台报表“预估收入”
    commission = Column(String(12))
    # 推广者获得的分成比率，对应联盟后台报表“分成比率”
    commission_rate = Column(String(12))
    # 淘客订单创建时间
    create_time = Column(String(40))
    # 淘客订单结算时间
    earning_time = Column(String(40))
    # 订单提现状态 1 已经提现 2提现中
    drawTime = Column(String(40),default='0')
    # 商品id
    num_iid = Column(String(40))
    # 商品标题
    item_title = Column(String(60))
    # 商品数量
    item_num = Column(String(10))
    # 单价
    price = Column(String(10))
    # 实际支付金额
    pay_price = Column(String(10))
    # 卖家昵称
    seller_nick = Column(String(40))
    # 店铺名称
    seller_shop_title = Column(String(40))
    # 第三方服务来源，没有第三方服务，取值为“--”
    tk3rd_type = Column(String(32))
    # 第三方推广者ID
    tk3rd_pub_id = Column(String(64))
    # 订单类型，如天猫，淘宝
    order_type = Column(String(20))
    # 收入比率，卖家设置佣金比率+平台补贴比率
    income_rate = Column(String(40))
    # 效果预估，付款金额*(佣金比率+补贴比率)*分成比率
    pub_share_pre_fee = Column(String(40))
    # 补贴比率
    subsidy_rate = Column(String(40))
    # 补贴类型，天猫:1，聚划算:2，航旅:3，阿里云:4
    subsidy_type = Column(String(40))
    # 成交平台，PC:1，无线:2
    terminal_type = Column(String(10))
    # 类目名称 例:办公/耗材
    auction_category = Column(String(20))
    # 来源媒体id
    site_id = Column(String(40))
    # 来源媒体名称
    site_name = Column(String(40))
    # 广告位ID pid
    adzone_id = Column(String(40))
    # 广告位名称
    adzone_name = Column(String(40))
    # 佣金比率
    total_commission_rate = Column(String(40))
    # 佣金金额
    total_commission_fee = Column(String(40))
    # 补贴金额
    subsidy_fee = Column(String(40))
    # 渠道关系id
    relation_id = Column(String(40))
    # 会员运营id
    special_id = Column(String(40))
    # 对应微信号
    useWXID = Column(String(32))
    # 对应微信标识符
    useWXName = Column(String(40))

    @classmethod
    def saveData(cls, data):
        session.add(data)
        session.commit()
        session.close()

    # # “多”的一方的book表是通过外键关联到user表的:
    # user_id = Column(String(20), ForeignKey('user.id'))


class PIDList(Base):
    __tablename__ = "PIDs"
    id = Column(Integer, primary_key=True)
    # pid即淘宝联盟标识淘客用户推广位的ID，包含了推广类型、广告位标识（比如网站、导购还是其它方式），PID推广位是一串以mm_开头的三段数字数字。
    # 如：mm_98723245_44422162_465706573.其中，98723245为淘宝联盟账号的ID。
    # .44422162为媒体ID（即官方接口调用中常用的参数site_id）465706573,为推广位的ID（即官方接口调用中常用的参数adzone_id）。
    # adzoneid
    adzone_id = Column(String(40))
    # sitid
    site_id = Column(String(40))
    # 全的pid
    pid = Column(String(120))
    # 当前pid名称
    pidName = Column(String(32))
    # 对应微信号
    WXID = Column(String(40))
    # 对应微信标识符
    WXIDName = Column(String(64))

    @classmethod
    def saveData(cls, data):
        session.add(data)
        session.commit()
        session.close()


Base.metadata.create_all(engine)