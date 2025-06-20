import json, operator, requests, string, random, time, re, base64
from datetime import datetime, timedelta
from flask import Blueprint, request, redirect, url_for, session, render_template, g, jsonify
from models import User, Organization, Competition, Log, Ques_and_answer, EmailCaptcha, Team, ActionLog, Notice, Post, Season, TJTTer, Motto
from exts import db, mail
from config import APPID, APPSECRET
from flask_mail import Message
from sqlalchemy import and_, or_, func

bp = Blueprint("user", __name__, url_prefix="/user")


# 字符串编码
def encode(input_string):
    byte_string = input_string.encode('utf-8')
    base64_bytes = base64.b64encode(byte_string)
    encoded_string = base64_bytes.decode()
    return encoded_string


# 字符串解码
def decode(encoded_string):
    base64_bytes = encoded_string.encode('utf-8')
    byte_string = base64.b64decode(base64_bytes)
    decoded_string = byte_string.decode()
    return decoded_string


# 刷新个人信息
@bp.route("/refresh", methods=["POST"])
def refresh():
    if request.json:
        my_id = request.json["my_id"]
    else:
        return jsonify({
            "status": 200,
            "message": "刷新成功",
            "user": None,
        })
    me = User.query.get(my_id)
    return jsonify({
        "status": 200,
        "message": "刷新成功",
        "user": me.jsonify_user(),
    })


# 获取用户openid
@bp.route("/fetch_openid", methods=["POST"])
def fetch_openid():
    code = request.json["code"]
    appid = APPID
    app_secret = APPSECRET
    url = f'https://api.weixin.qq.com/sns/jscode2session?appid={appid}&secret={app_secret}&js_code={code}&grant_type=authorization_code'
    response = requests.get(url)
    data = response.json()
    if "openid" in data:
        return jsonify({
            'status': 200,
            'message': '用户openid获取成功',
            'openid': data["openid"],
        })
    else:
        return jsonify({
            'status': -1,
            'message': '用户openid获取失败',
            'openid': None,
        })


# 检查用户openid
@bp.route("/check_openid", methods=["POST"])
def check_openid():
    openid = request.json["open_id"]
    user = User.query.filter_by(openid=openid).first()
    if not user:
        return jsonify({
            'status': 200,
            'message': '该openid未被占用',
            'openid': openid,
        })
    else:
        return jsonify({
            "status": 200,
            "message": "该openid已被占用",
            'openid': None,
        })


# 储存用户openid
@bp.route("/store_openid", methods=['POST'])
def store_openid():
    data = request.json
    me = User.query.get(data['my_id'])
    me.openid = data['openid']
    db.session.commit()
    return jsonify({
        "status": 200,
        "messages": "openid储存成功"
    })


# 微信登录
@bp.route("/wx_login", methods=["POST"])
def wx_login():
    openid = request.json["open_id"]
    user = User.query.filter_by(openid=openid).first()
    if user:
        # 登录成功
        action_log = ActionLog(action="登录（微信登录）", operator_id=user.id)
        user_token = encode(str(user.id) + '=logined_user_id[ATTENTION]timestamp=' + str(time.time()))
        db.session.add(action_log)
        db.session.commit()
        return jsonify({
            'status': 200,
            'message': '登录成功',
            'user_token': user_token,
        })
    else:
        return jsonify({
            "status": -1,
            "message": "该微信未被绑定",
        })


# 获取信息
@bp.route("/get_info", methods=["POST"])
def get_info():
    user_length = len(User.query.all())
    male_length = len(User.query.filter(User.gender == "男").all())
    female_length = len(User.query.filter(User.gender == "女").all())
    student_length = len(User.query.filter(User.role == "学生").all())
    teacher_length = len(User.query.filter(User.role == "教师").all())
    matches = Competition.query.all()
    c_matches = []
    for match in matches:
        if match.match_time >= datetime.now():
            c_matches.append(match)
    match_length = len(c_matches)
    TJTTers_length = len(TJTTer.query.all())
    admin_length = len(User.query.filter(User.usertype != "0").all())
    foreign_admins = len(User.query.filter(User.usertype == "K9").all())
    return jsonify({
        "status": 200,
        "message": "信息获取成功",
        "user_length": user_length,
        "male_length": male_length,
        "female_length": female_length,
        "student_length": student_length,
        "teacher_length": teacher_length,
        "match_length": match_length,
        "TJTTers_length": TJTTers_length,
        "foreign_admins": foreign_admins,
        "admin_length": admin_length,
    })


# 获取用户赛季记录
@bp.route("/get_user_season_recording", methods=["POST"])
def get_user_season_recording():
    data = request.json
    my_id = data["my_id"]
    me = User.query.get(my_id)
    season_id = data["season_id"]
    this_season = Season.query.get(season_id)
    matches_in_this_season = Competition.query.filter(
        and_(
            Competition.match_time.between(this_season.start_time, this_season.end_time),
            Competition.players.any(id=me.id)
        )
    ).all()
    logs = Log.query.filter(
        and_(
            Log.time.between(this_season.start_time, this_season.end_time),
            or_(
                Log.winner_name == me.username,
                Log.loser_name == me.username
            )
        )
    ).order_by(Log.time).all()
    win_logs = []
    lose_logs = []
    for log in logs:
        if log.winner_name == me.username and log.loser_name:
            win_logs.append(log)
        elif log.loser_name == me.username and log.winner_name:
            lose_logs.append(log)
    earliest_log = logs[0] if logs else None
    # latest_log = logs[-1] if logs else None
    if earliest_log:
        if earliest_log.winner_name == me.username:
            start_score = earliest_log.winner_score_before
        elif earliest_log.loser_name == me.username:
            start_score = earliest_log.loser_score_before
    else:
        start_score = me.score
    # if latest_log.winner_name == me.username:
    #     end_score = latest_log.winner_score_after
    # elif latest_log.loser_name == me.username:
    #     end_score = latest_log.loser_score_after
    end_score = me.score
    return jsonify({
        "status": 200,
        "message": "用户赛季记录获取成功",
        "matches_length": len(matches_in_this_season),
        "win_length": len(win_logs),
        "lose_length": len(lose_logs),
        "start_score": start_score,
        "end_score": end_score,
    })


# 获取所有用户
@bp.route("/get_users", methods=["POST"])
def get_users():
    all_users = User.query.order_by(User.score.desc()).all()
    users = []
    school_list = ['请选择学校']
    for user in all_users:
        if user.school and user.school not in school_list:
            school_list.append(user.school)
        users.append({
            "id": user.id,
            "username": user.username,
            "gender": user.gender,
            "school": user.school,
            "score": user.score,
            "address": user.address,
            "active": user.active,
            "role": user.role,
            "privacy": user.privacy,
            "profile_img": user.profile_img,
        })
    return jsonify({
        "status": 200,
        "message": "全部用户获取成功",
        "users": users,
        "school_list": school_list,
    })


# 获取所有用户（用户列表）
@bp.route("/get_users_by_join_time", methods=["POST"])
def get_users_by_join_time():
    all_users = User.query.order_by(User.join_time.desc()).all()
    users = []
    for user in all_users:
        users.append({
            "id": user.id,
            "username": user.username,
            "gender": user.gender,
            "school": user.school,
            "score": user.score,
            "address": user.address,
            "active": user.active,
            "role": user.role,
            "privacy": user.privacy,
            "profile_img": user.profile_img,
        })
    return jsonify({
        "status": 200,
        "message": "全部用户获取成功",
        "users": users,
    })


# 获取男性用户
@bp.route("/get_male_users", methods=["POST"])
def get_male_users():
    all_male_users = User.query.filter_by(gender='男').order_by(User.score.desc()).all()
    male_users = []
    for user in all_male_users:
        male_users.append({
            "id": user.id,
            "username": user.username,
            "gender": user.gender,
            "school": user.school,
            "score": user.score,
            "address": user.address,
            "active": user.active,
            "privacy": user.privacy,
            "profile_img": user.profile_img,
        })
    return jsonify({
        "status": 200,
        "message": "男性用户获取成功",
        "male_users": male_users,
    })


# 获取女性用户
@bp.route("/get_female_users", methods=["POST"])
def get_female_users():
    all_female_users = User.query.filter_by(gender='女').order_by(User.score.desc()).all()
    female_users = []
    for user in all_female_users:
        female_users.append({
            "id": user.id,
            "username": user.username,
            "gender": user.gender,
            "school": user.school,
            "score": user.score,
            "address": user.address,
            "active": user.active,
            "privacy": user.privacy,
            "profile_img": user.profile_img,
        })
    return jsonify({
        "status": 200,
        "message": "女性用户获取成功",
        "female_users": female_users,
    })


# 获取某学校用户
@bp.route("/get_users_by_school", methods=["POST"])
def get_users_by_school():
    data = request.json
    all_users = User.query.filter_by(school=data["school"]).order_by(User.score.desc()).all()
    users = []
    for user in all_users:
        users.append({
            "id": user.id,
            "username": user.username,
            "gender": user.gender,
            "school": user.school,
            "score": user.score,
            "address": user.address,
            "active": user.active,
            "privacy": user.privacy,
            "profile_img": user.profile_img,
        })
    return jsonify({
        "status": 200,
        "message": "某学校用户获取成功",
        "users": users,
    })


# 通过id获取某用户
@bp.route("/get_this_user", methods=["POST"])
def get_this_user():
    data = request.json
    user = User.query.get(data["user_id"])
    return jsonify({
        "status": 200,
        "message": "用户获取成功",
        "user": user.jsonify_user(),
    })


# 通过姓名获取某用户id
@bp.route("/get_user_id_by_username", methods=["POST"])
def get_user_id_by_username():
    data = request.json
    user = User.query.filter_by(username=data["username"]).first()
    return jsonify({
        "status": 200,
        "message": "用户id获取成功",
        "user_id": user.id,
    })


# 计算活跃度
@bp.route("/cal_active", methods=["POST"])
def cal_active():
    now = datetime.now()
    this_season = Season.query.filter(
        and_(Season.start_time <= now, now <= Season.end_time)
    ).first()
    data = request.json
    me = User.query.get(data["user_id"])
    my_valid_matches = Competition.query.filter(
        and_(
            Competition.match_time.between(this_season.start_time, now),
            Competition.players.any(id=me.id),
        )
    ).all()

    my_posts = Post.query.filter(
        and_(
            Post.couple.any(id=me.id),
            Post.play_time.between(this_season.start_time, now),
        )
    ).all()
    my_valid_posts = []
    for post in my_posts:
        if len(post.couple) > 1:
            my_valid_posts.append(post)

    my_questions = Ques_and_answer.query.filter(
        and_(
            Ques_and_answer.person_id == me.id,
            Ques_and_answer.time.between(this_season.start_time, this_season.end_time),
        )
    ).all()
    my_valid_questions = []
    for question in my_questions:
        if question.answer:
            my_valid_questions.append(question)
    my_active = (len(my_valid_matches) * 0.7 + len(my_valid_posts) * 0.1 + len(my_valid_questions) * 0.1) * 100
    me.active = round(my_active)
    db.session.commit()
    return jsonify({
        "status": 200,
        "message": "活跃度计算完成",
        "my_valid_posts_length": len(my_valid_posts),
        "my_valid_questions_length": len(my_valid_questions),
    })


# 通过id获取某TJTT工作室成员
@bp.route("/get_this_TJTTer", methods=["POST"])
def get_this_TJTTer():
    data = request.json
    Ter = TJTTer.query.get(data["TJTTer_id"])
    return jsonify({
        "status": 200,
        "message": "TJTT工作室成员获取成功",
        "TJTTer": Ter.jsonify_TJTTer(),
    })


# 修改TJTT工作室成员信息
@bp.route("/modify_TJTTer_info", methods=["POST"])
def modify_TJTTer_info():
    data = request.json
    me = User.query.get(data["my_id"])
    if me.usertype != 'K11':
        return jsonify({
            "status": -1,
            "message": "权限不足",
        })
    Ter = TJTTer.query.get(data["TJTTer_id"])
    department = data["department"]
    job = data["job"]
    prop = data["property"]
    description = data["description"]
    if department:
        Ter.department = department
    if job:
        Ter.job = job
    if prop:
        Ter.property = prop
    if description:
        Ter.description = description
    action_log = ActionLog(action=f"（管理）修改TJTT工作室成员『{Ter.name}』信息", operator_id=me.id)
    db.session.add(action_log)
    db.session.commit()
    return jsonify({
        "status": 200,
        "message": "修改TJTT工作室成员信息成功",
    })


# 获取主页用户信息
@bp.route("/get_index_info", methods=["POST"])
def get_index_info():
    if request.json["user_id"]:
        user = User.query.get(request.json["user_id"])
        return jsonify({
            "status": 200,
            "message": "通知公告获取成功",
            "username": user.username,
            "usertype": user.usertype,
        })


# 注册
@bp.route("/register", methods=['POST'])
def register():
    data = request.json
    username = data["username"]
    gender = data["gender"]
    phone = data["phone"]
    email = data["email"]
    school = data["school"]
    role = data["role"]
    password = data["password"]
    password2 = data["password2"]
    agree = data["agree"]
    user_exist = User.query.filter_by(username=username).first()

    if not username or not gender or not phone or not school or not role or not password or not password2:
        return jsonify({
            'status': -1,
            'message': '信息输入不完整',
        })
    phone_pattern = r'^(\d+|(\+\d{1,2}-?\d{3}-?\d{3,4}-?\d{4}))$'
    if not re.match(phone_pattern, phone):
        return jsonify({
            'status': -1,
            'message': '请输入正确的手机号',
        })
    email_pattern = r'^[\w.-]+@\w+[\.\w+]+$'
    if not re.match(email_pattern, email):
        return jsonify({
            'status': -1,
            'message': '请输入正确的邮箱',
        })
    if school[-2:] != '大学' and school[-2:] != '学院' and school[-2:] != '学校' and school[-2:] != '中学' and school[-2:] != '小学':
        return jsonify({
            'status': -1,
            'message': '请输入完整学校名',
        })
    if agree != "agreed":
        return jsonify({
            'status': -1,
            'message': '请阅读并同意小程序的协议与隐私政策',
        })
    else:
        if user_exist:
            return jsonify({
                'status': -1,
                'message': '存在重名用户，请联系管理员',
            })
        if password != password2:
            return jsonify({
                'status': -1,
                'message': '两次密码输入不一致',
            })
        pwd_pattern = r'^.{4,}$'
        if not re.match(pwd_pattern, password):
            return jsonify({
                'status': -1,
                'message': '密码需大于3位',
            })
        else:
            openid = data['openid']
            user = User(username=username, gender=gender, email=email, school=school, phone=phone, password=password, role=role, score=0, active=0, usertype=0, privacy=0, present=0, is_TJTT=0,
                        openid=openid)
            db.session.add(user)
            db.session.commit()
            action_log = ActionLog(action="用户注册", operator_id=user.id)
            db.session.add(action_log)
            db.session.commit()
            return jsonify({
                'status': 200,
                'message': '注册成功',
            })


# 登录
@bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data["username"]
    password = data["password"]
    agree = data["agree"]
    user = User.query.filter_by(username=username).all()
    if not username or not password:
        return jsonify({
            'status': -1,
            'message': '输入不完整',
        })
    if agree != "agreed":
        return jsonify({
            'status': -1,
            'message': '请阅读并同意小程序的协议与隐私政策',
        })
    if len(user) == 0:
        return jsonify({
            'status': -1,
            'message': '用户不存在',
        })
    elif len(user) == 1:
        if user[0].password != password:
            return jsonify({
                'status': -1,
                'message': '密码错误',
            })
        else:
            # 登录成功
            action_log = ActionLog(action="登录（姓名登录）", operator_id=user[0].id)
            user_token = encode(str(user[0].id) + '=logined_user_id[ATTENTION]timestamp=' + str(time.time()))
            db.session.add(action_log)
            db.session.commit()
            return jsonify({
                'status': 200,
                'message': '登录成功',
                'user_token': user_token,
            })
    else:
        return jsonify({
            'message': '存在重名用户，请用手机号登录',
        })


# 用手机号登录
@bp.route('/login_viaph', methods=['POST'])
def login_viaph():
    data = request.json
    phone = data["phone"]
    password = data["password"]
    agree = data["agree"]
    user = User.query.filter_by(phone=phone).first()
    if not phone or not password:
        return jsonify({
            'status': -1,
            'message': '输入不完整',
        })
    if agree != "agreed":
        return jsonify({
            'status': -1,
            'message': '请阅读并同意小程序的协议与隐私政策',
        })
    if not user:
        return jsonify({
            'status': -1,
            'message': '用户不存在',
        })
    if user.password != password:
        return jsonify({
            'status': -1,
            'message': '密码错误',
        })
    else:
        # 登录成功
        action_log = ActionLog(action="登录（姓名登录）", operator_id=user.id)
        user_token = encode(str(user.id) + '=logined_user_id[ATTENTION]timestamp=' + str(time.time()))
        db.session.add(action_log)
        db.session.commit()
        return jsonify({
            'status': 200,
            'message': '登录成功',
            'user_token': user_token,
        })


# 忘记密码
@bp.route('/forget_psw', methods=['POST'])
def forget_psw():
    data = request.json
    username = data["username"]
    captcha = data["captcha"]
    if not username or not captcha:
        return jsonify({
            'status': -1,
            'message': '信息输入不完整',
        })
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({
            'status': -1,
            'message': '用户不存在',
        })
    all_his_captcha = EmailCaptcha.query.filter_by(email=user.email).all()
    this_captcha = EmailCaptcha.query.filter_by(email=user.email, captcha=captcha).first()
    if not this_captcha:
        return jsonify({
            'status': -1,
            'message': '身份验证失败，请重试',
        })
    else:
        user.password = "123"
        for captcha_x in all_his_captcha:
            db.session.delete(captcha_x)
        action_log = ActionLog(action="用户重置密码", operator_id=user.id)
        db.session.add(action_log)
        db.session.commit()
        return jsonify({
            'status': 200,
            'message': '身份验证成功密码已被重置为123。',
        })


# 忘记密码发送邮箱验证码
@bp.route('/send_captcha', methods=['POST'])
def send_captcha():
    data = request.json
    username = data["username"]
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({
            "status": -1,
            "message": "用户不存在"
        })
    if not user.email:
        return jsonify({
            "status": -1,
            "message": "用户未绑定邮箱，无法重置密码"
        })
    else:
        source = string.digits * 6
        captcha = random.sample(source, 6)
        captcha = "".join(captcha)
        message = Message(subject="TJTT乒乓球积分赛平台-忘记密码", recipients=[user.email], body=f"您正在进行重置密码操作，您的验证码是{captcha}，请勿泄露若您未进行重置密码操作，请忽略此邮件。")
        mail.send(message)
        email_captcha = EmailCaptcha(email=user.email, captcha=captcha)
        db.session.add(email_captcha)
        db.session.commit()
        return jsonify({
            "status": 200,
            "message": f"{username}您好，已向您的绑定邮箱{user.email}发送验证码"
        })


# 绑定微信
@bp.route('/bind_wx', methods=['POST'])
def bind_wx():
    data = request.json
    username = data["username"]
    password = data["password"]
    if not data["username"] or not data["password"]:
        return jsonify({
            "status": -1,
            "message": "输入不完整"
        })
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({
            "status": -1,
            "message": "用户不存在"
        })
    if user.password != password:
        return jsonify({
            "status": -1,
            "message": "密码错误"
        })
    openid = data["openid"]
    exist_users = User.query.filter_by(openid=openid).all()
    for e_user in exist_users:
        e_user.openid = None
    user.openid = openid
    db.session.commit()
    return jsonify({
        "status": 200,
        "message": "微信绑定成功"
    })


# 删除用户
@bp.route('/delete_user', methods=['POST'])
def delete_user():
    data = request.json
    user = User.query.get(data['user_id'])
    me = User.query.get(data['my_id'])
    if me.usertype != "K11":
        return jsonify({
            "status": -1,
            "message": "权限不足"
        })
    if not user:
        return jsonify({
            "status": -1,
            "message": "用户不存在"
        })
    else:
        db.session.delete(user)
        action_log = ActionLog(action=f"（管理）删除用户『{user.username}』", operator_id=me.id)
        db.session.add(action_log)
        db.session.commit()
        return jsonify({
            "status": 200,
            "message": "删除成功"
        })


# （管理）添加用户
@bp.route("/add_user", methods=['POST'])
def add_user():
    data = request.json
    username = data['username']
    gender = data['gender']
    phone = data['phone']
    email = data['email']
    address = data['address']
    school = data['school']
    role = data["role"]
    stu_num = data['stu_num']
    password = data['password']
    score = data['score']
    if not username or not gender or not role or not password:
        return jsonify({
            "status": -1,
            "message": "信息输入不完整"
        })
    if score:
        user = User(username=username, gender=gender, email=email, school=school, phone=phone, stu_num=stu_num, password=password, score=score, active=0, role=role, address=address, usertype=0,
                    privacy=0,
                    present=0, is_TJTT=0)
    else:
        user = User(username=username, gender=gender, email=email, school=school, phone=phone, stu_num=stu_num, password=password, score=0, active=0, role=role, address=address, usertype=0, privacy=0,
                    present=0, is_TJTT=0)
    db.session.add(user)
    action_log = ActionLog(action=f"（管理）添加用户『{username}』", operator_id=data['my_id'])
    db.session.add(action_log)
    db.session.commit()
    return jsonify({
        "status": 200,
        "message": "添加成功"
    })


# 更新用户
@bp.route("/update_user", methods=['POST'])
def update_user():
    data = request.json
    user_id = data['id']
    user = User.query.get(user_id)
    if not user:
        return jsonify({
            "status": -1,
            "message": "用户不存在"
        })
    user.username = data['username']
    user.school = data['school']
    user.gender = data['gender']
    user.role = data['role']
    my_id = data["my_id"]

    if user.score < int(data["score"]):  # 积分加
        # 写进积分变动日志
        log = Log(operator_id=my_id, winner_name=user.username, winner_score_before=user.score, winner_score_after=data['score'], loser_name="", loser_score_before="", loser_score_after="")
        db.session.add(log)
    elif user.score > int(data["score"]):  # 积分减
        # 写进积分变动日志
        log = Log(operator_id=my_id, winner_name="", winner_score_before="", winner_score_after="", loser_name=user.username, loser_score_before=user.score, loser_score_after=data['score'])
        db.session.add(log)
    user.score = data['score']
    action_log = ActionLog(action=f"（管理）更新用户『{user.username}』个人信息", operator_id=my_id)
    db.session.add(action_log)
    db.session.commit()
    return jsonify({
        "status": 200,
        "message": "修改成功"
    })


# 用户积分变更
@bp.route("/modify_score", methods=['POST'])
def modify_score():
    data = request.json
    user_id = data['user_id']
    user = User.query.get(user_id)
    if not user:
        return jsonify({
            "status": -1,
            "message": "用户不存在"
        })
    if not data["score"]:
        return jsonify({
            "status": -1,
            "message": "请输入变更积分"
        })
    try:
        int(data["score"])
    except ValueError:
        return jsonify({
            "status": -1,
            "message": "积分输入有误"
        })
    if int(data["score"]) < 0 or int(data["score"]) > 3000:
        return jsonify({
            "status": -1,
            "message": "积分范围有误（0-3000）"
        })
    if user.score < int(data["score"]):  # 积分加
        # 写进积分变动日志
        log = Log(operator_id=data["my_id"], winner_name=user.username, winner_score_before=user.score, winner_score_after=data['score'], loser_name="", loser_score_before="", loser_score_after="")
        db.session.add(log)
    elif user.score > int(data["score"]):  # 积分减
        # 写进积分变动日志
        log = Log(operator_id=data["my_id"], winner_name="", winner_score_before="", winner_score_after="", loser_name=user.username, loser_score_before=user.score, loser_score_after=data['score'])
        db.session.add(log)
    user.score = int(data["score"])
    user.fixed_score = int(data["score"])
    action_log = ActionLog(action=f"（管理）变更用户『{user.username}』积分", operator_id=data["my_id"])
    db.session.add(action_log)
    db.session.commit()
    return jsonify({
        "status": 200,
        "message": "积分变更成功"
    })


# 设为私密/公开用户
@bp.route("/set_privacy", methods=["POST"])
def set_privacy():
    data = request.json
    my_id = data['my_id']
    me = User.query.filter_by(id=my_id).first()
    user_id = data['user_id']
    user = User.query.filter_by(id=user_id).first()
    set = data['set']
    if not user:
        if set == "private":
            me.privacy = 1
            action_log = ActionLog(action=f"设为私密用户", operator_id=my_id)
        elif set == "public":
            me.privacy = 0
            action_log = ActionLog(action=f"设为公开用户", operator_id=my_id)
        db.session.add(action_log)
        db.session.commit()
        return jsonify({
            "status": 200,
            "message": "设置成功"
        })
    else:
        if me.usertype == "K10" or me.usertype == "K11":
            if set == "private":
                user.privacy = 1
                action_log = ActionLog(action=f"（管理）将用户『{user.username}』设为私密用户", operator_id=my_id)
            elif set == "public":
                user.privacy = 0
                action_log = ActionLog(action=f"（管理）将用户『{user.username}』设为公开用户", operator_id=my_id)
            db.session.add(action_log)
            db.session.commit()
            return jsonify({
                "status": 200,
                "message": "设置成功"
            })
        else:
            return jsonify({
                "status": -1,
                "message": "权限不足"
            })


# 个人信息/用户详情中修改信息
@bp.route("/modify_user", methods=['POST'])
def modify_user():
    data = request.json
    user_id = data['user_id']
    user = User.query.get(user_id)
    my_id = data['my_id']
    me = User.query.get(my_id)
    if not user:
        return jsonify({
            "status": -1,
            "message": "用户不存在"
        })
    if data['gender']:
        user.gender = data['gender']
    if data['address']:
        user.address = data['address']
    if data['phone']:
        phone_pattern = r'^(\d+|(\+\d{1,2}-?\d{3}-?\d{3,4}-?\d{4}))$'
        if not re.match(phone_pattern, data['phone']):
            return jsonify({
                'status': -1,
                'message': '请输入正确的手机号',
            })
        user.phone = data['phone']
    if data['email']:
        email_pattern = r'^[\w.-]+@\w+[\.\w+]+$'
        if not re.match(email_pattern, data['email']):
            return jsonify({
                'status': -1,
                'message': '请输入正确的邮箱',
            })
        user.email = data['email']
    if data['school']:
        if data['school'][-2:] != '大学' and data['school'][-2:] != '学院' and data['school'][-2:] != '学校' and data['school'][-2:] != '中学' and data['school'][-2:] != '小学':
            return jsonify({
                'status': -1,
                'message': '请输入完整学校名',
            })
        user.school = data['school']
    if data['role']:
        user.role = data['role']
    try:
        if data['organ_id']:
            user.organ_id = data['organ_id']
    except KeyError:
        pass
    if data['stu_num']:
        user.stu_num = data['stu_num']
    if data['hand']:
        user.hand = data['hand']
    if data['grip']:
        user.grip = data['grip']
    if data['blade']:
        user.blade = data['blade']
    if data['forehand']:
        user.forehand = data['forehand']
    if data['backhand']:
        user.backhand = data['backhand']
    if data['particle']:
        user.particle = data['particle']
    if user != me:
        action_log = ActionLog(action=f"（管理）修改用户『{user.username}』个人信息", operator_id=my_id)
    else:
        action_log = ActionLog(action="修改/完善个人信息", operator_id=user_id)
    db.session.add(action_log)
    db.session.commit()
    return jsonify({
        "status": 200,
        "message": "修改成功",
    })


# 用户详情中变更用户权限级别
@bp.route("/modify_usertype", methods=["POST"])
def modify_usertype():
    data = request.json
    my_id = data['my_id']
    me = User.query.filter_by(id=my_id).first()
    user_id = data['user_id']
    user1 = User.query.filter_by(id=user_id).first()
    usertype = data['usertype']
    if me.usertype == "K11":
        if not usertype:
            return jsonify({
                "status": -1,
                "message": "请选择用户权限级别"
            })
        user1.usertype = usertype
        action_log = ActionLog(action=f"（管理）变更用户『{user1.username}』权限级别", operator_id=my_id)
        db.session.add(action_log)
        db.session.commit()
        return jsonify({
            "status": 200,
            "message": "变更成功"
        })
    else:
        return jsonify({
            "status": -1,
            "message": "权限不足"
        })


# 个人信息中修改密码
@bp.route("/modify_psw", methods=["POST"])
def modify_psw():
    data = request.json
    my_id = data['my_id']
    user = User.query.get(my_id)
    old_psw = data['old_psw']
    new_psw = data['new_psw']
    new_psw2 = data['new_psw2']
    if user.password != old_psw:
        return jsonify({
            "status": -1,
            "message": "原密码输入错误"
        })
    if new_psw != new_psw2:
        return jsonify({
            "status": -1,
            "message": "两次密码输入不一致"
        })
    if new_psw == user.password:
        return jsonify({
            "status": -1,
            "message": "原密码与新密码不能相同"
        })
    pwd_pattern = r'^.{4,}$'
    if not re.match(pwd_pattern, new_psw):
        return jsonify({
            'status': -1,
            'message': '密码需大于3位',
        })
    else:
        user.password = new_psw
        action_log = ActionLog(action="修改个人密码", operator_id=user.id)
        db.session.add(action_log)
        db.session.commit()
        return jsonify({
            "status": 200,
            "message": "修改成功"
        })


# 根据姓名查找用户
@bp.route('/findUserByName', methods=['POST'])
def findUserByName():
    data = request.json
    search_user = data['search_user']
    where = data['where']
    users = []
    if search_user == '':
        all_users = User.query.order_by(User.score.desc()).all()
    else:
        if where == "score_rank":
            all_users = User.query.filter_by(privacy=False).filter(User.username.contains(search_user)).order_by(User.score.desc()).all()
        else:
            all_users = User.query.filter(User.username.contains(search_user)).order_by(User.score.desc()).all()
        scores = operator.attrgetter('score')
        all_users.sort(key=scores, reverse=True)  # operator库，对users里的score属性逆序排序
    for user in all_users:
        users.append({
            "id": user.id,
            "username": user.username,
            "gender": user.gender,
            "school": user.school,
            "score": user.score,
            "role": user.role,
            "address": user.address,
            "active": user.active,
            "privacy": user.privacy,
            "profile_img": user.profile_img,
        })
    return jsonify({
        "status": 200,
        "message": "查找成功",
        "users": users,
    })


# 用户反馈
@bp.route("/send_feedback", methods=['POST'])
def send_feedback():
    data = request.json
    me = User.query.get(data['my_id'])
    feedback = data['feedback']
    if not me:
        return jsonify({
            "status": -1,
            "message": "请登录后进行反馈"
        })
    if not feedback:
        return jsonify({
            "status": -1,
            "message": "请填写反馈内容"
        })
    if not me.phone:
        return jsonify({
            "status": -1,
            "message": "您尚未完善手机号，无法进行反馈"
        })
    message = Message(subject="用户反馈",
                      recipients=["tjttgroup@163.com"],
                      body=f"反馈用户：{me.username}\n手机号：{me.phone}\n反馈内容：{feedback}")
    mail.send(message)
    action_log = ActionLog(action="用户反馈", operator_id=data["my_id"])
    db.session.add(action_log)
    db.session.commit()
    return jsonify({
        "status": 200,
        "message": "提交成功！我们将主动联系您，请保持来电畅通"
    })


# 更换用户头像
@bp.route("/modify_user_profile_img", methods=['POST'])
def modify_user_profile_img():
    data = request.json
    user_id = data['user_id']
    profile_img = data['profile_img']
    if not profile_img:
        return jsonify({
            "status": -1,
            "message": "请输入用户头像URL"
        })
    user = User.query.get(user_id)
    user.profile_img = profile_img
    if user.is_TJTT:
        this_TJTTer = TJTTer.query.get(user.id)
        this_TJTTer.avatar_url = profile_img
    action_log = ActionLog(action=f"更换用户『{user.username}』头像", operator_id=data["my_id"])
    db.session.add(action_log)
    db.session.commit()
    return jsonify({
        "status": 200,
        "message": "用户头像更换成功"
    })


# 删除用户头像
@bp.route("/delete_user_profile_img", methods=['POST'])
def delete_user_profile_img():
    data = request.json
    user_id = data['user_id']
    user = User.query.get(user_id)
    user.profile_img = None
    if user.is_TJTT:
        this_TJTTer = TJTTer.query.get(user.id)
        this_TJTTer.avatar_url = None
    action_log = ActionLog(action=f"删除用户『{user.username}』头像", operator_id=data["my_id"])
    db.session.add(action_log)
    db.session.commit()
    return jsonify({
        "status": 200,
        "message": "用户头像删除成功"
    })
