import json, operator, string, random, time
from datetime import datetime
from flask import Blueprint, request, redirect, url_for, session, render_template, g, jsonify, flash
from models import User, Organization, Competition, Log, Ques_and_answer, EmailCaptcha, Team, ActionLog, Notice, Post
from exts import db, mail
from bluePrints.form import Registration, LoginForm, Login_viaphForm, ModifyPswForm, UserDetailForm, RegisForm, ForgetPswForm, QAForm
from decorators import login_required
from flask_mail import Message

bp = Blueprint("user", __name__, url_prefix="/user")


# # 获取精确ip
# def get_ip():
#     response = requests.get('https://api64.ipify.org?format=json').json()
#     return response["ip"]
#
#
# # 获取ip位置
# def get_location():
#     ip_address = get_ip()
#     response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
#     location_data = {
#         "ip": ip_address,
#         "city": response.get("city"),
#         "region": response.get("region"),
#         "country": response.get("country_name")
#     }
#     return location_data


# 注册
@bp.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("sign-up.html")
    else:
        form = RegisForm(request.form)
        username = form.username.data
        gender = form.gender.data
        phone = form.phone.data
        email = form.email.data
        school = form.school.data
        role = form.role.data
        password = form.password.data
        password2 = form.password2.data
        agree = form.agree.data
        user_exist = User.query.filter_by(username=username).first()

        if not username or not gender or not phone or not school or not role or not password or not password2:
            flash("信息输入不完整！")
            return redirect(url_for("user.register"))
        if agree == "disagreed":
            flash("请勾选“同意政策、条款和协议”！")
            return redirect(url_for("user.register"))
        else:
            if user_exist:
                flash("存在重名用户，请联系管理员！")
                return redirect(url_for("user.register"))
            if password != password2:
                flash("两次密码输入不一致！")
                return redirect(url_for("user.register"))
            else:
                user = User(username=username, gender=gender, email=email, school=school, phone=phone, password=password, role=role, address="上海市", score=0, usertype=0, privacy=0)
                db.session.add(user)
                db.session.commit()
                action_log = ActionLog(action="用户注册", operator_id=user.id)
                db.session.add(action_log)
                db.session.commit()
                flash("注册成功，请登录！")
                return redirect(url_for("user.login"))


# 登录
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("log-in.html")
    else:
        form = LoginForm(request.form)
        username = form.username.data
        password = form.password.data
        agree = form.agree.data
        user = User.query.filter_by(username=username).all()
        if agree == "disagreed":
            flash("请勾选“同意政策、条款和协议”！")
            return redirect(url_for("user.login"))
        if len(user) == 0:
            flash("用户不存在！")
            return redirect(url_for("user.login"))
        elif len(user) == 1:
            if user[0].password != password:
                flash("密码错误！")
                return redirect(url_for("user.login"))
            else:
                # 登录成功，将用户id存入cookie
                session["user_id"] = user[0].id
                action_log = ActionLog(action="登录（姓名登录）", operator_id=user[0].id)
                db.session.add(action_log)
                db.session.commit()
                # print(get_location())
                return redirect('infor_index')
        else:
            flash("存在重名用户，请用手机号登录！")
            return redirect(url_for("user.login"))


# 用手机号登录
@bp.route('/login_viaph', methods=['GET', 'POST'])
def login_viaph():
    if request.method == 'GET':
        return render_template("log-in_viaph.html")
    else:
        form = Login_viaphForm(request.form)
        phone = form.phone.data
        password = form.password.data
        agree = form.agree.data
        user = User.query.filter_by(phone=phone).first()
        if agree == "disagreed":
            flash("请勾选“同意政策、条款和协议”！")
            return redirect(url_for("user.login_viaph"))
        if not user:
            flash("用户不存在！")
            return redirect(url_for("user.login_viaph"))
        if user.password != password:
            flash("密码错误！")
            return redirect(url_for("user.login_viaph"))
        else:
            # 登录成功，将用户id存入cookie
            session["user_id"] = user.id
            action_log = ActionLog(action="登录（手机号登录）", operator_id=user.id)
            db.session.add(action_log)
            db.session.commit()
            return redirect('infor_index')


# 忘记密码
@bp.route('/forget_psw', methods=['GET', 'POST'])
def forget_psw():
    if request.method == 'GET':
        return render_template("forget-psw.html")
    else:
        form = ForgetPswForm(request.form)
        if form.validate():
            username = form.username.data
            user = User.query.filter_by(username=username).first()
            user.password = "123"
            action_log = ActionLog(action="用户重置密码", operator_id=user.id)
            db.session.add(action_log)
            db.session.commit()
            flash("身份验证成功！密码已被重置为123。")
            return redirect(url_for("user.login"))
        else:
            flash("身份验证失败，请重新发送验证码重试！")
            return redirect(url_for("user.forget_psw"))


# 忘记密码发送邮箱验证码
@bp.route('/send_captcha')
def send_captcha():
    username = request.args.get('username')
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({
            "status": -1,
            "message": "用户不存在！"
        })
    if not user.email:
        return jsonify({
            "status": -1,
            "message": "用户未绑定邮箱，无法重置密码！"
        })
    else:
        source = string.digits * 6
        captcha = random.sample(source, 6)
        captcha = "".join(captcha)
        message = Message(subject="TJTT乒乓球积分赛平台-忘记密码", recipients=[user.email], body=f"您正在进行重置密码操作，您的验证码是{captcha}，请勿泄露！若您未进行重置密码操作，请忽略此邮件。")
        mail.send(message)
        email_captcha = EmailCaptcha(email=user.email, captcha=captcha)
        db.session.add(email_captcha)
        db.session.commit()
        return jsonify({
            "status": 200,
            "message": f"{username}您好，已向您的绑定邮箱{user.email}发送验证码。"
        })


# 删除用户
@bp.route('/delete_user', methods=['GET', 'POST'])
def delete_user():
    if request.method == 'GET':
        return jsonify({
            "status": -1,
            "message": "请求方式错误！"
        })
    else:
        data = request.get_json()
        user = User.query.get(data['id'])
        me = User.query.get(data['my_id'])
        if not user:
            return jsonify({
                "status": -1,
                "message": "用户不存在!"
            })
        else:
            db.session.delete(user)
            action_log = ActionLog(action=f"（管理）删除用户『{user.username}』", operator_id=me.id)
            db.session.add(action_log)
            db.session.commit()
            return jsonify({
                "status": 200,
                "message": "删除成功！"
            })


# 添加用户（用户列表中）
@bp.route("/insert_user", methods=['GET', 'POST'])
def insert_user():
    if request.method == 'GET':
        organs = Organization.query.all()
        return render_template("info/user-insert.html", organs=organs)
    else:
        data = request.get_json()
        me = User.query.get(data['my_id'])
        username = data['username']
        gender = data['gender']
        email = data['email']
        school = data['school']
        phone = data['phone']
        stu_num = data['stu_num']
        password = data['password']
        score = data['score']
        address = data['address']
        role = data["role"]
        if score:
            user = User(username=username, gender=gender, email=email, school=school, phone=phone, stu_num=stu_num, password=password, score=score, role=role, address=address, usertype=0, privacy=0)
        else:
            user = User(username=username, gender=gender, email=email, school=school, phone=phone, stu_num=stu_num, password=password, score=0, role=role, address=address, usertype=0, privacy=0)
        db.session.add(user)
        action_log = ActionLog(action=f"（管理）添加用户『{username}』", operator_id=me.id)
        db.session.add(action_log)
        db.session.commit()
        return jsonify({
            "status": 200,
            "message": "添加成功！"
        })


# 更新用户
@bp.route("/update_user", methods=['POST'])
def update_user():
    data = request.get_json()
    user_id = data['id']
    user = User.query.get(user_id)
    if not user:
        return jsonify({
            "status": -1,
            "message": "用户不存在！"
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
        "message": "修改成功！"
    })


# 设为私密用户
@bp.route("/private_user", methods=["POST"])
def private_user():
    organs = Organization.query.all()
    my_id = request.form.get("my_id")
    me = User.query.filter_by(id=my_id).first()
    user_id = request.form.get("user_id")
    user = User.query.filter_by(id=user_id).first()
    privacy = request.form.get("privacy")
    if not user:
        me.privacy = privacy
        if privacy == "0":
            action_log = ActionLog(action=f"取消私密用户", operator_id=my_id)
        else:
            action_log = ActionLog(action=f"设为私密用户", operator_id=my_id)
        db.session.add(action_log)
        db.session.commit()
        flash("设置成功！")
        return render_template("info/my-profile.html")
    else:
        if me.usertype == "K10" or me.usertype == "K11":
            user.privacy = privacy
            if privacy == "0":
                action_log = ActionLog(action=f"（管理）将用户『{user.username}』取消私密用户", operator_id=my_id)
            else:
                action_log = ActionLog(action=f"（管理）将用户『{user.username}』设为私密用户", operator_id=my_id)
            db.session.add(action_log)
            db.session.commit()
            flash("设置成功！")
            return render_template("info/user-detail.html", user1=user, organs=organs)
        else:
            flash("权限不足！")
            return render_template("info/user-detail.html", user1=user, organs=organs)


# 个人信息/用户详情中修改信息
@bp.route("/modify_user", methods=['POST'])
def modify_user():
    data = request.get_json()
    user_id = data['id']
    user = User.query.get(user_id)
    my_id = data['my_id']
    me = User.query.get(my_id)
    if not user:
        return jsonify({
            "status": -1,
            "message": "用户不存在！"
        })
    user.email = data['email']
    user.phone = data['phone']
    user.school = data['school']
    user.stu_num = data['stu_num']
    user.gender = data['gender']
    user.address = data['address']
    user.hand = data['hand']
    user.grip = data['grip']
    user.blade = data['blade']
    user.forehand = data['forehand']
    user.backhand = data['backhand']
    user.particle = data['particle']
    if user != me:
        action_log = ActionLog(action=f"（管理）修改用户『{user.username}』个人信息", operator_id=my_id)
    else:
        action_log = ActionLog(action="修改/完善个人信息", operator_id=user_id)
    db.session.add(action_log)
    db.session.commit()
    return jsonify({
        "status": 200,
        "message": "修改成功！"
    })


# 用户详情中变更所属组织
@bp.route("/organ_change", methods=["GET", "POST"])
def organ_change():
    if request.method == 'GET':  # 无法到达
        return render_template("info/user-detail.html")
    else:
        form = UserDetailForm(request.form)
        my_id = form.my_id.data
        me = User.query.filter_by(id=my_id).first()
        user1_id = form.id.data
        user1 = User.query.filter_by(id=user1_id).first()
        organ_id = form.organ_id.data
        organs = Organization.query.all()
        if me.usertype == "K10" or me.usertype == "K11":
            if not organ_id:
                flash("请选择所属组织！")
                return render_template("info/user-detail.html", user1=user1, organs=organs)
            user1.organ_id = organ_id
            action_log = ActionLog(action=f"（管理）变更用户『{user1.username}』所属组织", operator_id=my_id)
            db.session.add(action_log)
            db.session.commit()
            flash("变更成功！")
            return render_template("info/user-detail.html", user1=user1, organs=organs)
        else:
            flash("权限不足！")
            return render_template("info/user-detail.html", user1=user1, organs=organs)


# 用户详情中变更用户权限级别
@bp.route("/is_admin", methods=["GET", "POST"])
def is_admin():
    if request.method == 'GET':
        return render_template("user-detail.html")
    else:
        form = UserDetailForm(request.form)
        my_id = form.my_id.data
        me = User.query.filter_by(id=my_id).first()
        id = form.id.data
        user1 = User.query.filter_by(id=id).first()
        usertype = form.usertype.data
        organs = Organization.query.all()
        if me.usertype == "K11":
            if not usertype:
                flash("请选择用户权限级别！")
                return render_template("info/user-detail.html", user1=user1, organs=organs)
            user1.usertype = usertype
            action_log = ActionLog(action=f"（管理）变更用户『{user1.username}』权限级别", operator_id=my_id)
            db.session.add(action_log)
            db.session.commit()
            flash("变更成功！")
            return render_template("info/user-detail.html", user1=user1, organs=organs)
        else:
            flash("权限不足！")
            return render_template("info/user-detail.html", user1=user1, organs=organs)


# 个人信息中修改密码
@bp.route("/modify_psw", methods=["GET", "POST"])
def modify_psw():
    if request.method == 'GET':
        return render_template("my-profile.html")
    else:
        my_id = request.form.get("user_id")
        user = User.query.get(my_id)
        old_psw = request.form.get("old_psw")
        new_psw = request.form.get("new_psw")
        new_psw2 = request.form.get("new_psw2")
        if user.password != old_psw:
            flash("原密码输入错误！")
            return redirect(url_for("user.my_profile", info=0))
        if new_psw != new_psw2:
            flash("两次密码输入不一致！")
            return redirect(url_for("user.my_profile", info=1))
        if new_psw == user.password:
            flash("原密码与新密码不能相同！")
            return redirect(url_for("user.my_profile", info=2))
        else:
            flash("修改成功！")
            user.password = new_psw
            action_log = ActionLog(action="修改个人密码", operator_id=user.id)
            db.session.add(action_log)
            db.session.commit()
            return redirect(url_for("user.my_profile", info=3))

    # （ajax版，fetch不到）
    # data = request.get_json()
    # user = User.query.get(data['id'])
    #
    # if data['old_psw'] != user.password:
    #     return jsonify({
    #         "status": -1,
    #         "message": "原密码输入错误！"
    #     })
    # if data['new_psw'] != data['new_psw2']:
    #     return jsonify({
    #         "status": -1,
    #         "message": "两次密码输入不一致！"
    #     })
    # user.password = data['new_psw']
    # db.session.commit()
    # return jsonify({
    #     "status": 200,
    #     "message": "修改成功！"
    # })


# 根据用户名查找用户（用户列表中）
@bp.route('/findUserByName/<keywords>')
def findUserByName(keywords):
    if keywords == '':
        users = User.query.all()
    else:
        users = User.query.filter(User.username.contains(keywords)).all()
        scores = operator.attrgetter('score')
        users.sort(key=scores, reverse=True)  # operator库，对users里的score属性逆序排序
        students = []
        teachers = []
        admins = []
        for x in range(len(users)):
            if users[x].role == "学生":
                students.append(users[x])
            else:
                teachers.append(users[x])
            if users[x].usertype == "K9" or users[x].usertype == "K10" or users[x].usertype == "K11":
                admins.append(users[x])
    return render_template("info/user-list.html", users=users, students=students, teachers=teachers, admins=admins)


# 登出（退出登录）
@bp.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# 进入信息管理页面
@bp.route("/infor_index")
@login_required
def infor_index():
    users = User.query.all()
    K9 = User.query.filter_by(usertype="K9").all()
    K10 = User.query.filter_by(usertype="K10").all()
    K11 = User.query.filter_by(usertype="K11").all()
    organs = Organization.query.all()
    matches = Competition.query.all()
    c_matches = []
    now = datetime.now()
    for match in matches:
        if match.match_time >= now:
            c_matches.append(match)
    elite1 = User.query.filter_by(id=1).first()
    elite4 = User.query.filter_by(id=4).first()
    elite5 = User.query.filter_by(id=5).first()
    notices = Notice.query.order_by(Notice.time.desc()).all()
    return render_template("info/index.html", users=users, K9=K9, organs=organs, c_matches=c_matches, elite1=elite1, elite4=elite4, elite5=elite5, notices=notices)


# 发布通知公告
@bp.route("/issue_notice", methods=["POST"])
@login_required
def issue_notice():
    my_id = request.form.get("my_id")
    me = User.query.filter_by(id=my_id).first()
    title = request.form.get("title")
    content = request.form.get("content")
    if me.usertype != "K9" and me.usertype != "K10" and me.usertype != "K11":
        flash("权限不足！")
        return redirect(url_for("user.infor_index"))
    notice = Notice(title=title, content=content, announcer_id=my_id)
    db.session.add(notice)
    action_log = ActionLog(action="（管理）发布通知公告", operator_id=my_id)
    db.session.add(action_log)
    db.session.commit()
    flash("发布成功！")
    return redirect(url_for("user.infor_index"))


# 删除问题
@bp.route('/delete_notice', methods=['GET', 'POST'])
def delete_notice():
    if request.method == 'GET':
        return jsonify({
            "status": -1,
            "message": "请求方式错误！"
        })
    else:
        data = request.get_json()
        my_id = data['my_id']
        notice = Notice.query.get(data['id'])
        if not notice:
            return jsonify({
                "status": -1,
                "message": "公告不存在!"
            })
        else:
            db.session.delete(notice)
            action_log = ActionLog(action="（管理）删除通知公告", operator_id=my_id)
            db.session.add(action_log)
            db.session.commit()
            return jsonify({
                "status": 200,
                "message": "删除成功！"
            })


# 提问
@bp.route("/issue_question", methods=["GET"])
def issue_question():
    person_id = request.args.get("person_id")
    question = request.args.get("question")
    if not question:
        flash("请输入问题！")
        return redirect("/#QandA")
    if not person_id:
        QA = Ques_and_answer(person_id="", question=question)
    else:
        QA = Ques_and_answer(person_id=person_id, question=question)
    db.session.add(QA)
    db.session.commit()
    flash("提问成功！")
    return redirect("/#QandA")


# 回答问题
@bp.route("/answer_questions", methods=['GET', "POST"])
@login_required
def answer_questions():
    if request.method == 'GET':
        QAs = Ques_and_answer.query.order_by(Ques_and_answer.time.desc()).all()
        return render_template("info/answer-questions.html", QAs=QAs)
    else:
        QAs = Ques_and_answer.query.order_by(Ques_and_answer.time.desc()).all()
        my_id = request.form.get("my_id")
        me = User.query.filter_by(id=my_id).first()
        question_id = request.form.get("question_id")
        question = Ques_and_answer.query.get(question_id)
        answer = request.form.get("answer")
        if me.usertype == "K9" or me.usertype == "K10" or me.usertype == "K11":
            if not question:
                flash("问题不存在！")
                return render_template("info/answer-questions.html", QAs=QAs)
            question.answer = answer
            action_log = ActionLog(action="（管理）回答问题", operator_id=my_id)
            db.session.add(action_log)
            db.session.commit()
            flash("回答成功！")
            return render_template("info/answer-questions.html", QAs=QAs)
        else:
            flash("权限不足！")
            return render_template("info/answer-questions.html", QAs=QAs)


# 删除问题
@bp.route('/delete_question', methods=['GET', 'POST'])
def delete_question():
    if request.method == 'GET':
        return jsonify({
            "status": -1,
            "message": "请求方式错误！"
        })
    else:
        data = request.get_json()
        my_id = data['my_id']
        question = Ques_and_answer.query.get(data['id'])
        if not question:
            return jsonify({
                "status": -1,
                "message": "问题不存在!"
            })
        else:
            db.session.delete(question)
            action_log = ActionLog(action="（管理）删除问题", operator_id=my_id)
            db.session.add(action_log)
            db.session.commit()
            return jsonify({
                "status": 200,
                "message": "删除成功！"
            })


# 进入个人信息页面
@bp.route("/my_profile", methods=["GET", "POST"])
@login_required
def my_profile():
    return render_template("info/my-profile.html")


# 约球
@bp.route("/play_post", methods=["GET", "POST"])
@login_required
def play_post():
    if request.method == 'GET':
        my_id = session.get("user_id")
        me = User.query.get(my_id)
        posts_all = Post.query.order_by(Post.play_time).all()
        posts = []     # 从现在开始所有的帖
        now = datetime.now()
        for post in posts_all:
            if post.play_time >= now:
                posts.append(post)
            else:
                db.session.delete(post)
                db.session.commit()
        posts_male = []
        posts_female = []
        posts_ordered = []
        my_posts = me.posts
        my_posts_accepted = []
        for post in my_posts:
            if len(post.couple) != 1:
                my_posts_accepted.append(post)
        for post in posts:
            if post.couple[0].gender == '男':
                posts_male.append(post)
            else:
                posts_female.append(post)
            if "无" not in post.table_vacant and "没" not in post.table_vacant:
                posts_ordered.append(post)

        return render_template("info/play-post.html", posts=posts, posts_male=posts_male, posts_female=posts_female, posts_ordered=posts_ordered, my_posts=my_posts, my_posts_accepted=my_posts_accepted)
    else:     # 发布约球帖
        now = datetime.now()
        my_id = request.form.get("my_id")
        me = User.query.filter_by(id=my_id).first()
        play_time = request.form.get("play_time")
        if not play_time:
            flash("请输入约球时间！")
            return redirect(url_for("user.play_post"))
        play_time = datetime.strptime(play_time, "%Y-%m-%dT%H:%M")
        if play_time < now:
            flash("约球时间不能为过去！")
            return redirect(url_for("user.play_post"))
        table_vacant = request.form.get("table_vacant")
        description = request.form.get("description")
        if not table_vacant:
            flash("请确定有无球台！")
            return redirect(url_for("user.play_post"))
        post = Post(play_time=play_time, table_vacant=table_vacant, description=description)
        db.session.add(post)
        post.couple.append(me)
        action_log = ActionLog(action="发布约球帖", operator_id=my_id)
        db.session.add(action_log)
        db.session.commit()
        flash("发布成功！")
        return redirect(url_for("user.play_post"))


# 受邀约球帖
@bp.route('/accept_post', methods=['POST'])
def accept_post():
    data = request.get_json()
    my_id = data['my_id']
    me = User.query.filter_by(id=my_id).first()
    post = Post.query.get(data['id'])
    if not post:
        return jsonify({
            "status": -1,
            "message": "约球帖不存在!"
        })
    else:
        if me in post.couple:
            return jsonify({
                "status": -1,
                "message": "不能受邀自己的约球帖!"
            })
        post.couple.append(me)
        action_log = ActionLog(action=f"受邀『{post.couple[0].username}』的约球帖", operator_id=my_id)
        db.session.add(action_log)
        db.session.commit()
        return jsonify({
            "status": 200,
            "message": "受邀成功！"
        })


# 取消约球
@bp.route('/cancel_post', methods=['POST'])
def cancel_post():
    data = request.get_json()
    my_id = data['my_id']
    me = User.query.filter_by(id=my_id).first()
    post = Post.query.get(data['id'])
    if not post:
        return jsonify({
            "status": -1,
            "message": "约球帖不存在!"
        })
    else:
        if me not in post.couple:
            return jsonify({
                "status": -1,
                "message": "未受邀该约球帖!"
            })
        action_log = ActionLog(action=f"取消『{post.couple[0].username}』、『{post.couple[1].username}』的约球", operator_id=my_id)
        me.posts.remove(post)
        db.session.add(action_log)
        db.session.commit()
        return jsonify({
            "status": 200,
            "message": "取消约球成功！"
        })


# 更新约球帖
@bp.route("/update_post", methods=['POST'])
def update_post():
    now = datetime.now()
    data = request.get_json()
    my_id = data['my_id']
    post = Post.query.get(data['id'])
    table_vacant = data['table_vacant']
    if not table_vacant:
        return jsonify({
            "status": -1,
            "message": "请确定有无球台！"
        })
    description = data['description']
    play_time = datetime.strptime(data['play_time'], "%Y-%m-%d %H:%M:%S")
    if play_time < now:
        return jsonify({
            "status": -1,
            "message": "约球时间不能为过去！"
        })
    post.table_vacant = table_vacant
    post.description = description
    post.play_time = play_time
    action_log = ActionLog(action="更新约球帖", operator_id=my_id)
    db.session.add(action_log)
    db.session.commit()
    return jsonify({
        "status": 200,
        "message": "修改成功！"
    })


# 删除约球帖
@bp.route('/delete_post', methods=['GET', 'POST'])
def delete_post():
    if request.method == 'GET':
        return jsonify({
            "status": -1,
            "message": "请求方式错误！"
        })
    else:
        data = request.get_json()
        my_id = data['my_id']
        post = Post.query.get(data['id'])
        if not post:
            return jsonify({
                "status": -1,
                "message": "约球帖不存在!"
            })
        else:
            db.session.delete(post)
            action_log = ActionLog(action="删除约球帖", operator_id=my_id)
            db.session.add(action_log)
            db.session.commit()
            return jsonify({
                "status": 200,
                "message": "删除成功！"
            })


# 进入用户列表
@bp.route("/user_list", methods=["GET", "POST"])
@login_required
def user_list():
    if request.method == 'POST':
        organ_id = request.form.get("organ_id")
        team_id = request.form.get('team_id')
        if organ_id:
            organ = Organization.query.filter_by(id=organ_id).first()
            users = []
            for user in organ.users:
                users.append(user)
            scores = operator.attrgetter('score')
            users.sort(key=scores, reverse=True)  # operator库，对users里的score属性逆序排序
            return render_template("info/user-list.html", users=users)
        elif team_id:
            team = Team.query.filter_by(id=team_id).first()
            members = []
            for member in team.members:
                members.append(member)
            scores = operator.attrgetter('score')
            members.sort(key=scores, reverse=True)
            return render_template("info/user-list.html", users=members)
    else:
        users = User.query.order_by(User.score.desc()).all()
        K9 = User.query.filter_by(usertype="K9").all()
        K10 = User.query.filter_by(usertype="K10").all()
        K11 = User.query.filter_by(usertype="K11").all()
        admins = K9 + K10 + K11
        students = User.query.filter_by(role="学生").all()
        teachers = User.query.filter_by(role="教师").all()
        return render_template("info/user-list.html", users=users, admins=admins, students=students, teachers=teachers)


# 进入用户详情页面
@bp.route("/user_detail", methods=['GET', "POST"])
@login_required
def user_detail():
    if request.method == 'GET':
        return render_template("info/user-detail.html")
    else:
        id = request.form.get('id')
        username = request.form.get('username')
        if id:
            user1 = User.query.filter_by(id=id).first()
        elif username:
            user1 = User.query.filter_by(username=username).first()
        organs = Organization.query.all()
        return render_template("info/user-detail.html", user1=user1, organs=organs)


# 进入积分变动日志
@bp.route("/log", methods=['GET', "POST"])
@login_required
def log():
    if request.method == 'GET':
        all_score_logs = Log.query.all()
        if len(all_score_logs) > 300:
            for x in range(0, len(all_score_logs)-300):
                db.session.delete(all_score_logs[x])
                db.session.commit()
        logs = Log.query.order_by(Log.time.desc()).all()
        return render_template("info/log.html", logs=logs)
    else:  # 还没设置
        return render_template("info/log.html")


# 清空积分变动日志
@bp.route('/clear_all_logs', methods=['GET', 'POST'])
def clear_all_logs():
    if request.method == 'GET':
        return jsonify({
            "status": -1,
            "message": "请求方式错误！"
        })
    else:
        data = request.get_json()
        me = User.query.get(data['id'])
        if me.usertype == "K11":
            logs = Log.query.all()
            for log in logs:
                db.session.delete(log)
            action_log = ActionLog(action="清空积分变动日志", operator_id=me.id)
            db.session.add(action_log)
            db.session.commit()
            return jsonify({
                "status": 200,
                "message": "清空完成！"
            })
        else:
            return jsonify({
                "status": -1,
                "message": "权限不足！"
            })


# 进入用户操作日志
@bp.route("/action_log", methods=['GET', "POST"])
@login_required
def action_log():
    if request.method == 'GET':
        all_action_logs = ActionLog.query.all()
        if len(all_action_logs) > 200:
            for x in range(0, len(all_action_logs)-200):
                db.session.delete(all_action_logs[x])
                db.session.commit()
        action_logs = ActionLog.query.order_by(ActionLog.time.desc()).all()
        return render_template("info/action-log.html", action_logs=action_logs)
    else:  # 还没设置
        return render_template("info/log.html")


# 清空用户操作日志
@bp.route('/clear_all_action_logs', methods=['GET', 'POST'])
def clear_all_action_logs():
    if request.method == 'GET':
        return jsonify({
            "status": -1,
            "message": "请求方式错误！"
        })
    else:
        data = request.get_json()
        me = User.query.get(data['id'])
        if me.usertype == "K11":
            action_logs = ActionLog.query.all()
            for log_x in action_logs:
                db.session.delete(log_x)
            db.session.commit()
            return jsonify({
                "status": 200,
                "message": "清空完成！"
            })
        else:
            return jsonify({
                "status": -1,
                "message": "权限不足！"
            })


# -------------------------------------------------
# ----------------- Applications --------------------
# -------------------------------------------------
@bp.route("/ticket_list")
@login_required
def ticket_list():
    return render_template("info/ticket-list.html")


@bp.route("/app_chat")
@login_required
def app_chat():
    return render_template("info/app-chat.html")


@bp.route("/calendar")
@login_required
def calendar():
    return render_template("info/app-calendar.html")


# -------------------------------------------------
# ----------------- Forms --------------------
# -------------------------------------------------
@bp.route("/form_input")
@login_required
def form_input():
    return render_template("info/form-inputs.html")


@bp.route("/form_input_grid")
@login_required
def form_input_grid():
    return render_template("info/form-input-grid.html")


@bp.route("/form_checkbox_radio")
@login_required
def form_checkbox_radio():
    return render_template("info/form-checkbox-radio.html")


# -------------------------------------------------
# -----------------Tables --------------------
# -------------------------------------------------
@bp.route("/table_basic")
@login_required
def table_basic():
    return render_template("info/table-basic.html")


@bp.route("/table_dark_basic")
@login_required
def table_dark_basic():
    return render_template("info/table-dark-basic.html")


@bp.route("/table_sizing")
@login_required
def table_sizing():
    return render_template("info/table-sizing.html")


@bp.route("/table_layout_coloured")
@login_required
def table_layout_coloured():
    return render_template("info/table-layout-coloured.html")


@bp.route("/table_datatable_basic")
@login_required
def table_datatable_basic():
    return render_template("info/table-datatable-basic.html")


# -------------------------------------------------
# -----------------Charts --------------------
# -------------------------------------------------
@bp.route("/chart_morris")
@login_required
def chart_morris():
    return render_template("info/chart-morris.html")


@bp.route("/chart_chart_js")
@login_required
def chart_chart_js():
    return render_template("info/chart-chart-js.html")


@bp.route("/chart_knob")
@login_required
def chart_knob():
    return render_template("info/chart-knob.html")


@bp.route("/ui_cards")
@login_required
def ui_cards():
    return render_template("info/ui-cards.html")


# -------------------------------------------------
# -----------------UI Elements --------------------
# -------------------------------------------------
@bp.route("/ui_buttons")
@login_required
def ui_buttons():
    return render_template("info/ui-buttons.html")


@bp.route("/ui_modals")
@login_required
def ui_modals():
    return render_template("info/ui-modals.html")


@bp.route("/ui_tabs")
@login_required
def ui_tabs():
    return render_template("info/ui-tab.html")


@bp.route("/ui_tooltip_popover")
@login_required
def ui_tooltip_popover():
    return render_template("info/ui-tooltip-popover.html")


@bp.route("/ui_popover")
@login_required
def ui_popover():
    return render_template("info/ui-popover.html")


@bp.route("/ui_notification")
@login_required
def ui_notification():
    return render_template("info/ui-notification.html")


@bp.route("/ui_progressbar")
@login_required
def ui_progressbar():
    return render_template("info/ui-progressbar.html")


@bp.route("/ui_typography")
@login_required
def ui_typography():
    return render_template("info/ui-typography.html")


@bp.route("/ui_bootstrap")
@login_required
def ui_bootstrap():
    return render_template("info/ui-bootstrap.html")


@bp.route("/ui_breadcrumb")
@login_required
def ui_breadcrumb():
    return render_template("info/ui-breadcrumb.html")


@bp.route("/ui_list_media")
@login_required
def ui_list_media():
    return render_template("info/ui-list-media.html")


@bp.route("/ui_grid")
@login_required
def ui_grid():
    return render_template("info/ui-grid.html")


@bp.route("/ui_carousel")
@login_required
def ui_carousel():
    return render_template("info/ui-carousel.html")


@bp.route("/ui_scrollspy")
@login_required
def ui_scrollspy():
    return render_template("info/ui-scrollspy.html")


@bp.route("/ui_toasts")
@login_required
def ui_toasts():
    return render_template("info/ui-toasts.html")


@bp.route("/ui_spinner")
@login_required
def ui_spinner():
    return render_template("info/ui-spinner.html")


# -------------------------------------------------
# ----------------- Authentication ----------------
# -------------------------------------------------
@bp.route("/authentication_login1")
def authentication_login1():
    return render_template("info/authentication-login1.html")


@bp.route("/authentication_register1")
def authentication_register1():
    return render_template("info/authentication-register1.html")


@bp.route("/icon_fontawesome")
@login_required
def icon_fontawesome():
    return render_template("info/icon-fontawesome.html")


@bp.route("/icon_simple_lineicon")
@login_required
def icon_simple_lineicon():
    return render_template("info/icon-simple-lineicon.html")


# 发送测试邮件
@bp.route("/mail_test")
def mail_test():
    message = Message(subject="Test Message", recipients=["15947513567@163.com"], body="This is a test mail!")
    mail.send(message)
    return "成功！"


# # 测试ip定位
# @bp.route("/ip_position")
# def ip_position():
#     get_location()
#     return get_location()
