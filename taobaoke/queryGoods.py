# 淘口令转网址  查询商品,然后判断商品是否活动,判断返利多少,
# 查询商品网址,然后根据商品信息可以获取商品id(item_id),可以用商品id获取商品详情,
# 当前思路,用口令转网址,然后用爬虫查询商品信息,
import top.api
import requests
import json
import ZK_Model.globalModel
import urllib.parse

# productionUrl = "https://eco.taobao.com/router/rest"
# appkey = "25083490"
# secret = "77068d785fb6dc77d1865dc0737e1684"
# port = '80'
# pid = "28940900149"
# vekey = "V00000384Y70837048"

tempData = {'content': '极米无屏电视H2 高清智能小型家用投影机1080P无线WIFI家庭投影仪', 'title': '淘口令-宝贝',
            'pic_url': 'http://gw.alicdn.com/bao/uploaded/i2/2177009988/TB1VNTNbxTpK1RjSZFKXXa2wXXa_!!0-item_pic.jpg',
            'price': '4299.00',
            'url': 'https://item.taobao.com/item.htm?ut_sk=1.Wrj2yBh2FCsDALHjqOfHjZoP_21380790_1537438949665.TaoPassword-Weixin.1&id=566378533689&sourceType=item&price=4299&origin_price=4999&suid=27297AD8-0C2C-4AC9-86BD-7AEC87213663&un=47624531e6846aaa46e6040d6f65052e&share_crt_v=1&sp_tk=77+lYUZ1cWI0Y29GZGTvv6U=&spm=a211b4.23434152&visa=13a09278fde22a2e&disablePopup=true&disableSJ=1',
            'url1': 'http://item.taobao.com/item.htm?id=566378533689',
            'native_url': 'tbopen://m.taobao.com/tbopen/index.html?action=ali.open.nav&module=h5&h5Url=https%3A%2F%2Fitem.taobao.com%2Fitem.htm%3Fut_sk%3D1.Wrj2yBh2FCsDALHjqOfHjZoP_21380790_1537438949665.TaoPassword-Weixin.1%26id%3D566378533689%26sourceType%3Ditem%26price%3D4299%26origin_price%3D4999%26suid%3D27297AD8-0C2C-4AC9-86BD-7AEC87213663%26un%3D47624531e6846aaa46e6040d6f65052e%26share_crt_v%3D1%26sp_tk%3D77%2BlYUZ1cWI0Y29GZGTvv6U%3D%26spm%3Da211b4.23434152%26visa%3D13a09278fde22a2e%26disablePopup%3Dtrue%26disableSJ%3D1&appkey=23434152&visa=13a09278fde22a2e',
            'thumb_pic_url': 'http://gw.alicdn.com/bao/uploaded/i2/2177009988/TB1VNTNbxTpK1RjSZFKXXa2wXXa_!!0-item_pic.jpg_170x170.jpg'}
tempData2 = {'content': '淘口令  ', 'title': '淘口令-页面',
             'pic_url': 'https://gw.alicdn.com/tfs/TB1c.wHdh6I8KJjy0FgXXXXzVXa-580-327.png', 'price': None,
             'url': 'https://s.click.taobao.com/t?e=m%3D2%26s%3D%2FcwmR98BMqiw%2Bv2O2yX1MeeEDrYVVa64pRe%2F8jaAHci5VBFTL4hn2c9WtwgW5F0AJYccVKkURIhpYtXo3xzjPBdKaLEbMSeLBS0pFrpffJ5Elbd%2FHOpa6whqriF3K%2B6Rts4kLcowHDoFtROSrSejGX8KOGrok70ZomfkDJRs%2BhU%3D&ut_sk=1.utdid_null_1537861969752.TaoPassword-Outside.lianmeng-app&sp_tk=77+lR2lxQmJmWHBCVGTvv6U=&spm=a211b4.23434152&visa=13a09278fde22a2e&disablePopup=true&disableSJ=1',
             'url1': '',
             'native_url': 'tbopen://m.taobao.com/tbopen/index.html?action=ali.open.nav&module=h5&h5Url=https%3A%2F%2Fs.click.taobao.com%2Ft%3Fe%3Dm%253D2%2526s%253D%252FcwmR98BMqiw%252Bv2O2yX1MeeEDrYVVa64pRe%252F8jaAHci5VBFTL4hn2c9WtwgW5F0AJYccVKkURIhpYtXo3xzjPBdKaLEbMSeLBS0pFrpffJ5Elbd%252FHOpa6whqriF3K%252B6Rts4kLcowHDoFtROSrSejGX8KOGrok70ZomfkDJRs%252BhU%253D%26ut_sk%3D1.utdid_null_1537861969752.TaoPassword-Outside.lianmeng-app%26sp_tk%3D77%2BlR2lxQmJmWHBCVGTvv6U%3D%26spm%3Da211b4.23434152%26visa%3D13a09278fde22a2e%26disablePopup%3Dtrue%26disableSJ%3D1&appkey=23434152&visa=13a09278fde22a2e',
             'thumb_pic_url': 'https://gw.alicdn.com/tfs/TB1c.wHdh6I8KJjy0FgXXXXzVXa-580-327.png_170x170.jpg'}


# 淘口令转链接 用的91tool
# url		原始网址
# url1    干净的商品链接，去除pid
# native_url	移动端调起地址
def taoKouLingChangeHTTP(tkl):
    params = {"tkl": tkl, "user_key": "1gQODe4MGwToFY0j"}
    try:
        resp = requests.get("http://api.kfsoft.net/api/tb/tklQuery/v1.php", params)
        dict = resp.json()
        print(dict['data'])
        if dict['status'] == "success":
            getGoodsId(dict['data'])

    except Exception as error:
        print(error)


# num_iid	Number	123	商品ID
# title	String	连衣裙	商品标题
# pict_url	String	http://gi4.md.alicdn.com/bao/uploaded/i4/xxx.jpg	商品主图
# small_images	String[]	http://gi4.md.alicdn.com/bao/uploaded/i4/xxx.jpg	商品小图列表
# reserve_price	String	102.00	商品一口价格
# zk_final_price	String	88.00	商品折扣价格
# user_type	Number	1	卖家类型，0表示集市，1表示商城
# provcity	String	杭州	宝贝所在地
# item_url	String	http://detail.m.tmall.com/item.htm?id=xxx	商品地址
# nick	String	demo	卖家昵称
# seller_id	Number	123	卖家id
# volume	Number	1	30天销量
def getGoodsId(data):
    req = top.api.TbkItemGetRequest()
    req.set_app_info(top.appinfo(appkey, secret))
    req.fields = 'num_iid,title,pict_url,small_images,reserve_price,zk_final_price,user_type,provcity,item_url,seller_id,volume,nick'
    req.q = data['content']
    # req.cat="16,18"
    # req.itemloc="杭州"
    # req.sort="tk_rate_des"
    # req.is_tmall=false
    # req.is_overseas=false
    # req.start_price=10
    # req.end_price=10
    # req.start_tk_rate=123
    # req.end_tk_rate=123
    # req.platform=1
    # req.page_no=123
    req.page_size = 100
    try:
        resp = req.getResponse()
        print(resp)
        array = resp['tbk_item_get_response']['results']['n_tbk_item']
        print(type(array), type(resp['tbk_item_get_response']))
        if type(resp['tbk_item_get_response']).__name__ == 'dict':
            print('2222222222222222222222222')
        i = 0
        while i < len(array):
            url = array[i]['item_url']
            if url == data['url1']:
                for key, values in array[i].items():
                    print(key, values)
                    print(type(values))
                    # print('找到了')
                break
            i += 1
        print(len(array))

    except Exception as result:
        print(result)


# 维易淘宝客api
# data: 商品的链接
# category_id ：分类ID
#
# coupon_click_url ：已转链后的您的二合一链接（有券产品）或s.click链接（无券产品），可直接使用
#
# coupon_end_time：优惠券过期时间 （有优惠券时才有此字段）
#
# coupon_info：优惠券信息，格式都是“满xx元减xx元”（有优惠券时才有此字段）
#
# coupon_remain_count：剩余优惠券数量，当为0时优惠券失效。（有优惠券时才有此字段）
#
# coupon_start_time：优惠券开始时间（有优惠券时才有此字段）
#
# coupon_total_count：优惠券发放总量 （有优惠券时才有此字段）
#
# coupon_type：优惠券类型：1 公开券，2 私有券，3 妈妈券 （有优惠券时才有此字段）
#
# commission_rate：该产品佣金，多级代理依此值计算
#
# num_iid：产品ID
#
# tbk_pwd：淘口令，此口令是已转化成你自己PID的口令，可直接使用
#
# coupon_short_url：短链接，如有QQ推广等场景，已转化成你自己PID的口令，可直接使用。
#
# original_uland_link ： 无券产品的原始二合一链接。（无券时才有此字段，不推荐使用，仅做为原始数据返回，直接使用会提示优惠券失效）
# title：产品标题
#
# zk_final_price：产品折后价
#
# reserve_price：原价
#
# volume：最近30天销量
#
# cat_name：分类名
#
# cat_leaf_name：分类子叶
#
# seller_id：卖家id
#
# user_type：1、表示天猫，0、表示淘宝
#
# material_lib_type : 商品库类型，支持多库类型输出，以“，”区分，1: 表示为营销商品主推库
#
# item_url：表示产品链接地址（天猫国际有的也是taobao.com链接，要结合user_type分析）

def zhuanLian(data,use_pid=None):
    # data = str(data).encode('utf-8')
    dataUrlEndocde = urllib.parse.quote(data)
    url = 'http://api.vephp.com/hcapi?vekey=' + ZK_Model.globalModel.vekey + '&para=' + str(dataUrlEndocde) + '&detail=1'+'&pid='+'mm_32900145_121950227_'+str(use_pid)
    print(url)
    try:
        resp = requests.get(url)
        dict = resp.json()

        print(dict)
        return dict
        # print(dict)
        # for key, value in dict['data'].items():
        #     print(key, value)
    except Exception as Error:
        print('高佣接口错误')
        return Error


# 超级搜索功能
def superSearch(data):
    url = 'http://api.vephp.com/super?vekey=' + ZK_Model.globalModel.vekey + '&para=' + data
    try:

        resp = requests.get(url)
        dict = resp.json()
        for key, values in dict.items():
            print(key, values)
        # return dict

    except Exception as Error:

        return Error



