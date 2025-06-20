import wtforms
from wtforms.validators import Email, Length, EqualTo
from models import User, EmailCaptcha
from exts import db



class Registration(wtforms.Form):
    gender = wtforms.StringField(validators=[Length(min=1, max=1, message="性别格式错误!")])
    school = wtforms.StringField(validators=[Length(min=1, max=100, message="学校格式错误!")])
    phone = wtforms.StringField(validators=[Length(min=1, max=11, message="手机号格式错误!")])
    email = wtforms.StringField(validators=[Email(message="邮箱格式错误！")])
    username = wtforms.StringField(validators=[Length(min=1, max=16, message="用户名格式错误，6-16位!")])
    role = wtforms.StringField(validators=[Length(min=2, max=2, message="身份格式错误!")])
    password = wtforms.StringField(validators=[Length(min=1, max=20, message="密码1-20位!")])
    password_confirm = wtforms.StringField(validators=[EqualTo("password", message="请确认密码！")])

    # 自定义验证
    def validate_email(self, field):
        email = field.data
        user = User.query.filter_by(email=email).first()
        if user:
            return "邮箱已经存在！"

    def validate_username(self, field):
        username = field.data
        user = User.query.filter_by(username=username).first()  # 找到的第一个对象
        if user:
            return "用户名已经存在！"

    def validate_phone(self, field):
        phone = field.data
        user = User.query.filter_by(phone=phone).first()
        if user:
            return "手机号已经存在！"

class RegisForm(wtforms.Form):
    username = wtforms.StringField()
    gender = wtforms.StringField()
    school = wtforms.StringField()
    phone = wtforms.StringField()
    email = wtforms.StringField()
    role = wtforms.StringField()
    password = wtforms.StringField()
    password2 = wtforms.StringField()
    agree = wtforms.StringField()

class LoginForm(wtforms.Form):
    username = wtforms.StringField()
    password = wtforms.StringField()
    agree = wtforms.StringField()

class Login_viaphForm(wtforms.Form):
    phone = wtforms.StringField()
    password = wtforms.StringField()
    agree = wtforms.StringField()

class ForgetPswForm(wtforms.Form):
    username = wtforms.StringField()
    email = wtforms.StringField()
    captcha = wtforms.StringField()

    def validate_captcha(self, field):
        captcha = field.data
        username = self.username.data
        user = User.query.filter_by(username=username).first()
        all_his_captcha = EmailCaptcha.query.filter_by(email=user.email).all()
        email_captcha = EmailCaptcha.query.filter_by(email=user.email, captcha=captcha).first()
        if not email_captcha:
            raise wtforms.ValidationError(message="身份验证失败，请重试！")
        else:
            for captcha_x in all_his_captcha:
                db.session.delete(captcha_x)
                db.session.commit()


class ModifyPswForm(wtforms.Form):
    old_psw = wtforms.StringField()
    new_psw = wtforms.StringField()
    new_psw2 = wtforms.StringField()

class UpdateScoreForm(wtforms.Form):
    match_time = wtforms.StringField()
    winner = wtforms.StringField()
    loser = wtforms.StringField()
    confirm = wtforms.StringField()
    user_id = wtforms.StringField()

class UserDetailForm(wtforms.Form):
    id = wtforms.StringField()
    my_id = wtforms.StringField()
    usertype = wtforms.StringField()
    organ_id = wtforms.StringField()

class MatchDetailForm(wtforms.Form):
    id = wtforms.StringField()
    usertype = wtforms.StringField()
    organ_id = wtforms.StringField()
    restriction = wtforms.StringField()
    score_min = wtforms.StringField()
    score_max = wtforms.StringField()
    teamname = wtforms.StringField()
    description = wtforms.StringField()
    member_max = wtforms.StringField()

class MatchInsertForm(wtforms.Form):
    title = wtforms.StringField()
    description = wtforms.StringField()
    match_type = wtforms.StringField()
    address = wtforms.StringField()
    organ_id = wtforms.StringField()
    match_time = wtforms.StringField()
    sign_start_time = wtforms.StringField()
    sign_end_time = wtforms.StringField()
    place = wtforms.StringField()
    participant = wtforms.StringField()
    fee = wtforms.StringField()
    system = wtforms.StringField()
    usertype = wtforms.StringField()
    restriction = wtforms.StringField()
    score_min = wtforms.StringField()
    score_max = wtforms.StringField()

class MatchSignUpForm(wtforms.Form):
    match_id = wtforms.StringField()
    user_id = wtforms.StringField()
    agree = wtforms.StringField()
    player_username = wtforms.StringField()
    team_id = wtforms.StringField()

class QAForm(wtforms.Form):
    question_id = wtforms.StringField()
    answer = wtforms.StringField()