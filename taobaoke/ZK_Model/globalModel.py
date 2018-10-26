productionUrl = "https://eco.taobao.com/router/rest"
appkey = "25083490"
secret = "77068d785fb6dc77d1865dc0737e1684"
port = '80'
pid = "28940900149"
vekey = "V00000384Y70837048"

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
