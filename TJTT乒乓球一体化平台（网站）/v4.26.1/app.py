from flask import Flask, request, redirect, url_for, session, g, render_template
from exts import db, mail
import config, datetime
from bluePrints.user import bp as user_bp
from bluePrints.competition import bp as competition_bp
from bluePrints.competition import sort_id
from bluePrints.organization import bp as organization_bp
from flask_migrate import Migrate
from bluePrints.form import Registration, LoginForm, Login_viaphForm
from models import User, Ques_and_answer, Competition, Notice
from flask_cors import CORS
from flask_babel import Babel, gettext as _
from babel import Locale

app = Flask(__name__)
CORS(app)
# 加载配置
app.config.from_object(config)
# 注册蓝图
app.register_blueprint(user_bp)
app.register_blueprint(competition_bp)
app.register_blueprint(organization_bp)
# 绑定数据库
db.init_app(app)
migrate = Migrate(app, db)
# 发送邮件初始化
mail.init_app(app)

# 设置babel默认的地区语言和区时
app.config['BABEL_DEFAULT_LOCALE'] = 'zh'
app.config['BABEL_DEFAULT_TIMEZONE'] = 'CST'
lang = "zh"
babel = Babel(app)


# 设置语言
@babel.localeselector
def get_locale():
    global lang
    if lang == "zh":
        return request.accept_languages.best_match(['zh'])
    elif lang == "en":
        return request.accept_languages.best_match(["en"])


# 换语言
@app.route('/change_language', methods=['POST'])
def change_language():
    global lang
    lang = request.form.get('lang')
    matches = Competition.query.all()
    QAs = Ques_and_answer.query.order_by(Ques_and_answer.time.desc()).all()
    notices = Notice.query.order_by(Notice.time.desc()).all()
    users = User.query.order_by(User.score.desc()).all()
    ids = sort_id(users)
    return render_template("index.html", matches=matches, QAs=QAs, notices=notices, users=users, ids=ids)


@app.route('/')
def index():
    # matches = Competition.query.all()
    # QAs = Ques_and_answer.query.order_by(Ques_and_answer.time.desc()).all()
    # notices = Notice.query.order_by(Notice.time.desc()).all()
    # users = User.query.order_by(User.score.desc()).all()
    # ids = sort_id(users)
    # # 计算活跃度
    # h_matches = []
    # now = datetime.datetime.now()
    # for match in matches:
    #     if match.match_time < now:
    #         h_matches.append(match)
    # for user in users:
    #     attended_matches = []
    #     for attend in user.matches:
    #         if attend.match_time < now:
    #             attended_matches.append(attend)
    #     attended = len(attended_matches)
    #     user.active = round(attended / (len(h_matches) - 1) * 100)      # 减掉第一场乒协内测
    #     db.session.commit()
    # return render_template("index.html", matches=matches, QAs=QAs, notices=notices, users=users, ids=ids)
    return render_template("index1.html")

@app.route('/article')
def article():  # put application's code here
    return render_template("article.html")


@app.route('/terms')
def terms():  # put application's code here
    return render_template("terms.html")


@app.route('/privacy')
def privacy():  # put application's code here
    return render_template("privacy.html")


# 请求前检查是否有用户登录
@app.before_request
def my_before_request():
    user_id = session.get("user_id")
    if user_id:
        user = User.query.get(user_id)
        setattr(g, "user", user)
    else:
        setattr(g, "user", None)


@app.context_processor
def my_context_processor():
    return {"user": g.user}


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
else:
    application = app
