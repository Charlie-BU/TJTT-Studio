# 数据库配置
USERNAME = "Charlie"
PASSWORD = "Tjtt2024"
HOSTNAME = "120.55.171.190"
PORT = 3306
DATABASE = "tjtt"
DB_URI = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4'
# DB_URI2 = 'sqlite:///TJTT.sqlite'
SQLALCHEMY_DATABASE_URI = DB_URI

SECRET_KEY = "qwfsdgkdfhkbld"

# 邮箱配置
MAIL_SERVER = "smtp.163.com"  # 邮件服务器地址
MAIL_USE_SSL = True
MAIL_PORT = 465  # 邮件服务器端口
MAIL_USERNAME = "tjttgroup@163.com"  # 发件邮箱
MAIL_PASSWORD = "PKKYMGHSRZIIPUKY"  # 授权码
MAIL_DEFAULT_SENDER = "tjttgroup@163.com"


# 小程序配置
APPID = "wxc242084b7f37b770"
APPSECRET = "225e1cba5068437e7c29a77f18464a61"

# 微信支付配置
MCH_ID = '1692701590'                                   # 商户号
NOTIFY_URL = 'https://tjtt.asia/applicaiton/pay_notify'     # 通知地址
MERCHANT_KEY = 'Tjtt2024Tjtt2024Tjtt2024Tjtt2024'       # 商户KEY
# TRADE_TYPE = 'JSAPI'                                    # 交易类型
