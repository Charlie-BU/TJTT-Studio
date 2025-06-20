import json, operator, string, random, time, re, base64
from datetime import datetime, timedelta
from flask import Blueprint, request, redirect, url_for, session, render_template, g, jsonify, flash
from sqlalchemy import and_, or_
from models import User, Organization, Competition, Log, Ques_and_answer, EmailCaptcha, Team, ActionLog, Notice, Post, \
    Season, TJTTer, Motto, Athlete, Table
from exts import db
from wxpay import *
from hooks import inform

bp = Blueprint("application", __name__, url_prefix="/application")


# 随机获取名言金句
@bp.route("/get_random_motto", methods=["POST"])
def get_random_motto():
    count = Motto.query.count()
    random_offset = random.randint(0, count - 1)
    random_motto = Motto.query.offset(random_offset).first()
    return jsonify({
        "status": 200,
        "message": "名言金句获取成功",
        "random_motto": random_motto.jsonify_motto(),
    })


# （管理）添加乒乓语录
@bp.route("/add_motto", methods=["POST"])
def add_motto():
    data = request.json
    me = User.query.get(data["user_id"])
    if not me.usertype in ["K9", "K10", "K11"]:
        return jsonify({
            "status": -1,
            "message": "权限不足",
        })
    author = data["author"]
    content = data["content"]
    if not author or not content:
        return jsonify({
            "status": -1,
            "message": "输入不完整",
        })
    motto = Motto(author=author, content=content)
    action_log = ActionLog(action="（管理）添加乒乓语录", operator_id=data["user_id"])
    db.session.add_all([motto, action_log])
    db.session.commit()
    return jsonify({
        "status": 200,
        "message": "乒乓语录添加成功",
    })


# 获取通知公告
@bp.route("/get_notice", methods=["POST"])
def get_notice():
    all_notices = Notice.query.order_by(Notice.time.desc()).all()
    notices = []
    for notice in all_notices:
        if notice.released:
            notices.append(notice.jsonify_notice())
    return jsonify({
        "status": 200,
        "message": "通知公告获取成功",
        "notices": notices,
    })


# 获取问题回答
@bp.route("/get_QAs", methods=["POST"])
def get_QAs():
    all_QAs = Ques_and_answer.query.order_by(Ques_and_answer.time.desc()).all()
    QAs = []
    for QA in all_QAs:
        if QA.answer and QA.answer is not None:
            QAs.append(QA.jsonify_QA())
    return jsonify({
        "status": 200,
        "message": "问题回答获取成功",
        "QAs": QAs,
    })


# 获取隐藏通知（待办中）
@bp.route("/get_hidden_notices", methods=["POST"])
def get_hidden_notices():
    all_notices = Notice.query.filter_by(released=0).order_by(Notice.time.desc()).all()
    notices = []
    for notice in all_notices:
        notices.append(notice.jsonify_notice())
    return jsonify({
        "status": 200,
        "message": "隐藏通知获取成功",
        "hidden_notices": notices,
    })


# 获取待回答问题（待办中）
@bp.route("/get_unanswered_Qs", methods=["POST"])
def get_unanswered_Qs():
    all_QAs = Ques_and_answer.query.order_by(Ques_and_answer.time.desc()).all()
    QAs = []
    for QA in all_QAs:
        if not QA.answer or QA.answer is None:
            QAs.append(QA.jsonify_QA())
    return jsonify({
        "status": 200,
        "message": "待回答问题获取成功",
        "unanswered_Qs": QAs,
    })


# 获取隐藏赛事（待办中）
@bp.route("/get_hidden_matches", methods=["POST"])
def get_hidden_matches():
    matches = Competition.query.filter_by(visible=0).order_by(Competition.match_time.desc()).all()
    all_matches = []
    for match in matches:
        all_matches.append({
            "id": match.id,
            "title": match.title,
            "place": match.place,
            "match_time": match.match_time,
        })
    return jsonify({
        "status": 200,
        "message": "隐藏赛事获取成功",
        "hidden_matches": all_matches,
    })


# 更新TJTT Studio成员
@bp.route("/update_TJTTers", methods=["POST"])
def update_TJTTers():
    potential_TJTTers = User.query.filter_by(is_TJTT=True).all()
    all_TJTTers = TJTTer.query.all()
    existing_ids = []
    for Ter in all_TJTTers:
        existing_ids.append(Ter.id)
        this_user = User.query.get(Ter.id)
        if not this_user.is_TJTT:
            db.session.delete(Ter)
    for potential_TJTTer in potential_TJTTers:
        if potential_TJTTer.id not in existing_ids:
            new_TJTTer = TJTTer(id=potential_TJTTer.id, name=potential_TJTTer.username)
            db.session.add(new_TJTTer)
    db.session.commit()
    return jsonify({
        "status": 200,
        "message": "TJTT Studio成员更新成功",
    })


# 获取TJTT Studio成员
@bp.route("/get_TJTTers", methods=["POST"])
def get_TJTTers():
    all_TJTTers = TJTTer.query.order_by(TJTTer.department).all()
    TJTTers = []
    for this_TJTTer in all_TJTTers:
        this_user = User.query.get(this_TJTTer.id)
        jsonify_data1 = this_user.jsonify_user()
        jsonify_data2 = this_TJTTer.jsonify_TJTTer()
        jsonify_data = {**jsonify_data1, **jsonify_data2}
        TJTTers.append(jsonify_data)
    return jsonify({
        "status": 200,
        "message": "TJTT Studio成员获取成功",
        "TJTTers": TJTTers,
    })


# 获取技术端TJTT Studio成员
@bp.route("/get_dept_technology_TJTTers", methods=["POST"])
def get_dept_technology_TJTTers():
    all_TJTTers = TJTTer.query.filter_by(department='技术端').all()
    TJTTers = []
    for this_TJTTer in all_TJTTers:
        this_user = User.query.get(this_TJTTer.id)
        jsonify_data1 = this_user.jsonify_user()
        jsonify_data2 = this_TJTTer.jsonify_TJTTer()
        jsonify_data = {**jsonify_data1, **jsonify_data2}
        TJTTers.append(jsonify_data)
    return jsonify({
        "status": 200,
        "message": "TJTT Studio技术端成员获取成功",
        "TJTTers": TJTTers,
    })


# 获取组织端TJTT Studio成员
@bp.route("/get_dept_organizing_TJTTers", methods=["POST"])
def get_dept_organizing_TJTTers():
    all_TJTTers = TJTTer.query.filter_by(department='组织端').all()
    TJTTers = []
    for this_TJTTer in all_TJTTers:
        this_user = User.query.get(this_TJTTer.id)
        jsonify_data1 = this_user.jsonify_user()
        jsonify_data2 = this_TJTTer.jsonify_TJTTer()
        jsonify_data = {**jsonify_data1, **jsonify_data2}
        TJTTers.append(jsonify_data)
    return jsonify({
        "status": 200,
        "message": "TJTT Studio组织端成员获取成功",
        "TJTTers": TJTTers,
    })


# 获取文化端TJTT Studio成员
@bp.route("/get_dept_culture_TJTTers", methods=["POST"])
def get_dept_culture_TJTTers():
    all_TJTTers = TJTTer.query.filter_by(department='文化端').all()
    TJTTers = []
    for this_TJTTer in all_TJTTers:
        this_user = User.query.get(this_TJTTer.id)
        jsonify_data1 = this_user.jsonify_user()
        jsonify_data2 = this_TJTTer.jsonify_TJTTer()
        jsonify_data = {**jsonify_data1, **jsonify_data2}
        TJTTers.append(jsonify_data)
    return jsonify({
        "status": 200,
        "message": "TJTT Studio文化端成员获取成功",
        "TJTTers": TJTTers,
    })


# 用户加入/移出TJTT Studio
@bp.route("/modify_TJTTer", methods=["POST"])
def modify_TJTTer():
    data = request.json
    this_user = User.query.get(data['user_id'])
    if this_user.is_TJTT:
        this_user.is_TJTT = 0
        action_log = ActionLog(action=f"用户『{this_user.username}』移出TJTT Studio", operator_id=data['my_id'])
        db.session.add(action_log)
        db.session.commit()
        return jsonify({
            "status": 200,
            "message": "用户成功移出TJTT Studio",
        })
    else:
        this_user.is_TJTT = 1
        action_log = ActionLog(action=f"用户『{this_user.username}』加入TJTT Studio", operator_id=data['my_id'])
        db.session.add(action_log)
        db.session.commit()
        return jsonify({
            "status": 200,
            "message": "用户成功加入TJTT Studio",
        })


# 获取用户操作日志
@bp.route("/get_action_logs", methods=["POST"])
def get_action_logs():
    all_action_logs = ActionLog.query.all()
    if len(all_action_logs) > 200:
        for x in range(0, len(all_action_logs) - 200):
            db.session.delete(all_action_logs[x])
            db.session.commit()
    all_action_logs = ActionLog.query.order_by(ActionLog.time.desc()).all()
    action_logs = []
    for action_log in all_action_logs:
        action_logs.append(action_log.jsonify_action_log())
    return jsonify({
        "status": 200,
        "message": "用户操作日志获取成功",
        "action_logs": action_logs,
    })


# 获取全部乒乓球运动员
@bp.route("/get_athletes", methods=["POST"])
def get_athletes():
    all_athletes = Athlete.query.order_by(Athlete.name).all()
    athletes = []
    for athlete in all_athletes:
        athletes.append(athlete.jsonify_athlete())
    return jsonify({
        "status": 200,
        "message": "乒乓球运动员获取成功",
        "athletes": athletes,
    })


# 获取中国乒乓球运动员
@bp.route("/get_Chinese_athletes", methods=["POST"])
def get_Chinese_athletes():
    all_athletes = Athlete.query.filter_by(nationality='中国').order_by(Athlete.name).all()
    athletes = []
    for athlete in all_athletes:
        athletes.append(athlete.jsonify_athlete())
    return jsonify({
        "status": 200,
        "message": "中国乒乓球运动员获取成功",
        "athletes": athletes,
    })


# 获取外国乒乓球运动员
@bp.route("/get_foreign_athletes", methods=["POST"])
def get_foreign_athletes():
    all_athletes = Athlete.query.filter(Athlete.nationality != '中国').order_by(Athlete.name).all()
    athletes = []
    for athlete in all_athletes:
        athletes.append(athlete.jsonify_athlete())
    return jsonify({
        "status": 200,
        "message": "外国乒乓球运动员获取成功",
        "athletes": athletes,
    })


# 获取男子乒乓球运动员
@bp.route("/get_male_athletes", methods=["POST"])
def get_male_athletes():
    all_athletes = Athlete.query.filter_by(gender='男').order_by(Athlete.name).all()
    athletes = []
    for athlete in all_athletes:
        athletes.append(athlete.jsonify_athlete())
    return jsonify({
        "status": 200,
        "message": "男子乒乓球运动员获取成功",
        "athletes": athletes,
    })


# 获取女子乒乓球运动员
@bp.route("/get_female_athletes", methods=["POST"])
def get_female_athletes():
    all_athletes = Athlete.query.filter_by(gender='女').order_by(Athlete.name).all()
    athletes = []
    for athlete in all_athletes:
        athletes.append(athlete.jsonify_athlete())
    return jsonify({
        "status": 200,
        "message": "女子乒乓球运动员获取成功",
        "athletes": athletes,
    })


# 根据姓名查找运动员
@bp.route('/find_athlete_by_name', methods=['POST'])
def find_athlete_by_name():
    data = request.json
    search_athlete = data['search_athlete']
    athletes = []
    if search_athlete == '':
        all_athletes = Athlete.query.order_by(Athlete.name).all()
    else:
        all_athletes = Athlete.query.filter(Athlete.name.contains(search_athlete)).order_by(Athlete.name).all()
    for athlete in all_athletes:
        athletes.append(athlete.jsonify_athlete())
    return jsonify({
        "status": 200,
        "message": "运动员查找成功",
        "athletes": athletes,
    })


# 发布通知公告
@bp.route("/issue_notice", methods=["POST"])
def issue_notice():
    data = request.json
    my_id = data["my_id"]
    me = User.query.filter_by(id=my_id).first()
    title = data["title"]
    content = data["content"]
    if me.usertype != "K9" and me.usertype != "K10" and me.usertype != "K11":
        return jsonify({
            "status": -1,
            "message": "权限不足"
        })
    if not title or not content:
        return jsonify({
            "status": -1,
            "message": "输入不完整"
        })
    notice = Notice(title=title, content=content, announcer_id=my_id, released=1)
    db.session.add(notice)
    action_log = ActionLog(action="（管理）发布通知公告", operator_id=my_id)
    db.session.add(action_log)
    db.session.commit()
    return jsonify({
        "status": 200,
        "message": "发布成功"
    })


# 隐藏通知公告
@bp.route('/hide_notice', methods=['POST'])
def hide_notice():
    data = request.json
    notice = Notice.query.get(data['notice_id'])
    if not notice:
        return jsonify({
            "status": -1,
            "message": "公告不存在!"
        })
    else:
        notice.released = 0
        action_log = ActionLog(action="（管理）隐藏通知公告", operator_id=data['my_id'])
        db.session.add(action_log)
        db.session.commit()
        return jsonify({
            "status": 200,
            "message": "隐藏成功"
        })


# 取消隐藏通知公告（待办中）
@bp.route('/unhide_notice', methods=['POST'])
def unhide_notice():
    data = request.json
    notice = Notice.query.get(data['notice_id'])
    notice.released = 1
    action_log = ActionLog(action=f"（管理）取消隐藏通知公告『{notice.title}』", operator_id=data["my_id"])
    db.session.add(action_log)
    db.session.commit()
    return jsonify({
        "status": 200,
        "message": "取消隐藏成功"
    })


# 删除通知公告
@bp.route('/delete_notice', methods=['POST'])
def delete_notice():
    data = request.json
    notice = Notice.query.get(data['notice_id'])
    if not notice:
        return jsonify({
            "status": -1,
            "message": "公告不存在!"
        })
    else:
        db.session.delete(notice)
        action_log = ActionLog(action="（管理）删除通知公告", operator_id=data['my_id'])
        db.session.add(action_log)
        db.session.commit()
        return jsonify({
            "status": 200,
            "message": "删除成功"
        })


# 提问
@bp.route("/ask_question", methods=["POST"])
def ask_question():
    data = request.json
    my_id = data["my_id"]
    question = data["question"]
    if not question:
        return jsonify({
            "status": -1,
            "message": "请输入问题",
        })
    if not my_id:
        QA = Ques_and_answer(person_id="", question=question)
    else:
        QA = Ques_and_answer(person_id=my_id, question=question)
    db.session.add(QA)
    db.session.commit()
    return jsonify({
        "status": 200,
        "message": "提问成功！经回答后将在此处展示",
    })


# 回答问题
@bp.route("/answer_question", methods=['POST'])
def answer_question():
    data = request.json
    me = User.query.get(data["my_id"])
    question_id = data["question_id"]
    question = Ques_and_answer.query.get(question_id)
    answer = data["answer"]
    if me.usertype == "K9" or me.usertype == "K10" or me.usertype == "K11":
        if not answer:
            return jsonify({
                "status": -1,
                "message": "请输入回答",
            })
        question.answer = answer
        action_log = ActionLog(action="（管理）回答问题", operator_id=me.id)
        db.session.add(action_log)
        db.session.commit()
        return jsonify({
            "status": 200,
            "message": "回答成功",
        })
    else:
        return jsonify({
            "status": -1,
            "message": "权限不足",
        })


# 修改问题回答
@bp.route('/modify_QA', methods=['POST'])
def modify_QA():
    data = request.json
    question = Ques_and_answer.query.get(data['QA_id'])
    answer = data['answer']
    if not answer:
        return jsonify({
            "status": -1,
            "message": "请输入回答!"
        })
    else:
        question.answer = answer
        action_log = ActionLog(action="（管理）修改问题回答", operator_id=data['my_id'])
        db.session.add(action_log)
        db.session.commit()
        return jsonify({
            "status": 200,
            "message": "修改成功"
        })


# 删除问题
@bp.route('/delete_QA', methods=['POST'])
def delete_QA():
    data = request.json
    question = Ques_and_answer.query.get(data['QA_id'])
    if not question:
        return jsonify({
            "status": -1,
            "message": "问题不存在!"
        })
    else:
        db.session.delete(question)
        action_log = ActionLog(action="（管理）删除问题", operator_id=data['my_id'])
        db.session.add(action_log)
        db.session.commit()
        return jsonify({
            "status": 200,
            "message": "删除成功"
        })


# 获取约球帖
@bp.route("/get_play_posts", methods=["POST"])
def get_play_posts():
    play_posts = Post.query.order_by(Post.play_time).all()
    all_play_posts = []
    male_play_posts = []
    female_play_posts = []
    now = datetime.now()
    for post in play_posts:
        if post.play_time + timedelta(hours=2) >= now:
            if len(post.couple) > 1:
                play_post = {
                    "id": post.id,
                    "post_time": post.post_time,
                    "play_time": post.play_time,
                    "place": post.place,
                    "table_vacant": post.table_vacant,
                    "description": post.description,
                    "playerA_name": post.couple[0].username,
                    "playerA_gender": post.couple[0].gender,
                    "playerA_score": post.couple[0].score,
                    "playerA_phone": post.couple[0].phone,
                    "playerB_name": post.couple[1].username,
                    "playerB_gender": post.couple[1].gender,
                    "playerB_score": post.couple[1].score,
                    "playerB_phone": post.couple[1].phone,
                }
            else:
                play_post = {
                    "id": post.id,
                    "post_time": post.post_time,
                    "play_time": post.play_time,
                    "place": post.place,
                    "table_vacant": post.table_vacant,
                    "description": post.description,
                    "playerA_name": post.couple[0].username,
                    "playerA_gender": post.couple[0].gender,
                    "playerA_score": post.couple[0].score,
                    "playerA_phone": post.couple[0].phone,
                    "playerB_name": None,
                    "playerB_gender": None,
                    "playerB_score": None,
                    "playerB_phone": None,
                }
            all_play_posts.append(play_post)
            if post.couple[0].gender == "男":
                male_play_posts.append(play_post)
            else:
                female_play_posts.append(play_post)
    return jsonify({
        "status": 200,
        "message": "约球帖获取成功",
        "all_play_posts": all_play_posts,
        "male_play_posts": male_play_posts,
        "female_play_posts": female_play_posts,
    })


# 发布约球帖
@bp.route("/send_play_post", methods=["POST"])
def send_play_post():
    data = request.json
    now = datetime.now()
    me = User.query.filter_by(id=data["my_id"]).first()
    play_time = data["play_time"]
    if not play_time:
        return jsonify({
            "status": -1,
            "message": "请输入约球时间"
        })
    try:
        play_time = datetime.strptime(play_time, "%Y-%m-%d %H:%M")
    except ValueError:
        return jsonify({
            "status": -1,
            "message": "约球时间格式错误"
        })
    if play_time < now:
        return jsonify({
            "status": -1,
            "message": "约球时间不能为过去"
        })
    table_vacant = data["table_vacant"]
    description = data["description"]
    place = data["place"]
    post = Post(play_time=play_time, table_vacant=table_vacant, description=description, place=place)
    db.session.add(post)
    post.couple.append(me)
    action_log = ActionLog(action="发布约球帖", operator_id=data["my_id"])
    db.session.add(action_log)
    db.session.commit()
    return jsonify({
        "status": 200,
        "message": "发布成功"
    })


# 受邀约球帖
@bp.route('/accept_play_post', methods=['POST'])
def accept_play_post():
    data = request.json
    me = User.query.filter_by(id=data['my_id']).first()
    post = Post.query.get(data['post_id'])
    if not post:
        return jsonify({
            "status": -1,
            "message": "约球帖不存在"
        })
    if me in post.couple:
        return jsonify({
            "status": -1,
            "message": "不能受邀自己的约球帖"
        })
    if len(post.couple) != 1:
        return jsonify({
            "status": -1,
            "message": "该约球帖已受邀"
        })
    post.couple.append(me)
    action_log = ActionLog(action=f"受邀『{post.couple[0].username}』的约球帖", operator_id=data['my_id'])
    db.session.add(action_log)
    db.session.commit()
    return jsonify({
        "status": 200,
        "message": "受邀成功"
    })


# 取消约球
@bp.route('/cancel_post', methods=['POST'])
def cancel_post():
    data = request.json
    me = User.query.filter_by(id=data['my_id']).first()
    post = Post.query.get(data['post_id'])
    if not post:
        return jsonify({
            "status": -1,
            "message": "约球帖不存在!"
        })
    if me not in post.couple:
        return jsonify({
            "status": -1,
            "message": "未受邀该约球帖!"
        })
    action_log = ActionLog(action=f"取消『{post.couple[0].username}』、『{post.couple[1].username}』的约球",
                           operator_id=data['my_id'])
    me.posts.remove(post)
    db.session.add(action_log)
    db.session.commit()
    answer_post('约球取消通知')
    return jsonify({
        "status": 200,
        "message": "取消约球成功"
    })


# 删除约球帖
@bp.route('/delete_play_post', methods=['POST'])
def delete_play_post():
    data = request.json
    me = User.query.get(data['my_id'])
    post = Post.query.get(data['post_id'])
    if not post:
        return jsonify({
            "status": -1,
            "message": "约球帖不存在!"
        })
    if (me not in post.couple) and (me.usertype != 'K10' and me.usertype != 'K11'):
        return jsonify({
            "status": -1,
            "message": "权限不足"
        })
    db.session.delete(post)
    action_log = ActionLog(action="删除约球帖", operator_id=data['my_id'])
    db.session.add(action_log)
    db.session.commit()
    return jsonify({
        "status": 200,
        "message": "删除成功"
    })


# 回应约球贴
@bp.route('/answer_post', methods=['POST'])
def answer_post(description='约球受邀通知'):
    data_request = request.json
    post_id = data_request['post_id']
    post = Post.query.get(post_id)
    poster_id = post.couple[0].id
    my_id = data_request['my_id']
    template_id = "pSBm6ewDwG2_kTS3K2_n9kniQsDamkIUeSwjw1F381g"
    if post.place or post.table_vacant:  # 地点
        place = post.place + " " + post.table_vacant
    else:
        place = "请通过电话详询"
    # 应约人数据
    me = User.query.get(my_id)
    data = {
        "name1": {  # 姓名#10个以内纯汉字或20个以内纯字母或符号
            "value": me.username,
        },
        "thing2": {  # 地点#20个以内字符
            "value": place,
        },
        "date3": {  # 时间
            "value": post.play_time.strftime("%Y-%m-%d %H:%M")
        },
        "phone_number4": {  # 电话#17位以内，数字、符号
            "value": me.phone
        },
        "thing7": {  # 备注#20个以内字符
            "value": description
        }
    }
    inform_poster = inform(poster_id, template_id, data)
    # 发帖人数据
    poster = User.query.get(poster_id)
    data["name1"]["value"] = poster.username
    data["phone_number4"]["value"] = poster.phone
    inform_me = inform(my_id, template_id, data)
    if inform_me == 200 or inform_poster == 200:
        return jsonify({
            "status": 200,
            "message": "发送成功"
        })
    return jsonify({
        "status": -1,
        "message": "存在一方发送失败"
    })


# 获得所有球台信息
@bp.route("/get_all_tables", methods=["POST"])
def get_all_tables():
    tables = []
    time_list = ["全部时间"]
    place_list = ["全部地点"]
    all_tables = Table.query.order_by(Table.place).all()
    for table in all_tables:
        tables.append(table.jsonify_table())
        # 给前端提供可选时间和地点
        if table.place not in place_list:
            place_list.append(table.place)
        if table.activity_time not in time_list:
            time_list.append(table.activity_time)
    return jsonify({
        "status": 200,
        "message": "所有球台获取成功",
        "tables": tables,
        "time_list": time_list,
        "place_list": place_list,
    })


# 根据限制条件获取球台
@bp.route("/get_tables_by_condition", methods=["POST"])
def get_tables_by_condition():
    data = request.json
    time_condition = data["time_condition"]
    place_condition = data["place_condition"]
    tables = []
    if time_condition == "全部时间":
        conditioned_tables = Table.query.filter(Table.place == place_condition).order_by(Table.place).all()
    elif place_condition == "全部地点":
        conditioned_tables = Table.query.filter(Table.activity_time == time_condition).order_by(Table.place).all()
    else:
        conditioned_tables = Table.query.filter(
            and_(
                Table.activity_time == time_condition,
                Table.place == place_condition,
            )
        ).order_by(Table.place).all()
    for table in conditioned_tables:
        tables.append(table.jsonify_table())
    return jsonify({
        "status": 200,
        "message": "球台获取成功",
        "tables": tables,
    })


# 预订球台
@bp.route('/reserve_table', methods=['POST'])
def reserve_table():
    data = request.json
    me = User.query.get(data['my_id'])
    table = Table.query.get(data['table_id'])
    if datetime.now() < table.release_time:
        return jsonify({
            "status": -1,
            "message": "未到该球台预订开始时间"
        })
    if datetime.now() > table.activity_time:
        return jsonify({
            "status": -1,
            "message": "已过活动开始时间，不可预订"
        })
    if len(table.players) >= table.max_members:
        return jsonify({
            "status": -1,
            "message": f"该球台已到最大预订名额：{len(table.players)}人，请选取其他球台"
        })
    me.table_id = data['table_id']
    action_log = ActionLog(action="预订球台", operator_id=data['my_id'])
    db.session.add(action_log)
    db.session.commit()
    return jsonify({
        "status": 200,
        "message": "球台预订成功"
    })


# 取消预订球台
@bp.route('/cancel_reserve_table', methods=['POST'])
def cancel_reserve_table():
    data = request.json
    me = User.query.get(data['my_id'])
    table = Table.query.get(data['table_id'])
    if datetime.now() > table.activity_time:
        return jsonify({
            "status": -1,
            "message": "已过活动开始时间，不可取消预订"
        })
    me.table_id = None
    action_log = ActionLog(action="取消预订球台", operator_id=data['my_id'])
    db.session.add(action_log)
    db.session.commit()
    return jsonify({
        "status": 200,
        "message": "球台取消预订成功"
    })


# 添加 / 修改球台备注
@bp.route('/modify_additional_info', methods=['POST'])
def modify_additional_info():
    data = request.json
    table = Table.query.get(data['table_id'])
    additional_info = data['additional_info']
    table.additional_info = additional_info
    action_log = ActionLog(action="添加 / 修改球台备注", operator_id=data['my_id'])
    db.session.add(action_log)
    db.session.commit()
    return jsonify({
        "status": 200,
        "message": "球台备注添加 / 修改成功"
    })


# （管理）添加球台预定者
@bp.route('/add_table_player', methods=['POST'])
def add_table_player():
    data = request.json
    me = User.query.get(data['my_id'])
    if me.usertype != "K9" and me.usertype != "K10" and me.usertype != "K11":
        return jsonify({
            "status": -1,
            "message": "权限不足"
        })
    if not data['player_name']:
        return jsonify({
            "status": -1,
            "message": "请输入预订者姓名"
        })
    player = User.query.filter_by(username=data['player_name']).first()
    if not player:
        return jsonify({
            "status": -1,
            "message": "预订者不存在"
        })
    table = Table.query.get(data['table_id'])
    if player in table.players:
        return jsonify({
            "status": -1,
            "message": "该预订者已存在"
        })
    player.table_id = data['table_id']
    action_log = ActionLog(action="（管理）添加球台预定者", operator_id=data['my_id'])
    db.session.add(action_log)
    db.session.commit()
    return jsonify({
        "status": 200,
        "message": "球台预订者添加成功"
    })


# （管理）移除球台预订者
@bp.route('/remove_table_player', methods=['POST'])
def remove_table_player():
    data = request.json
    me = User.query.get(data['my_id'])
    if me.usertype != "K9" and me.usertype != "K10" and me.usertype != "K11":
        return jsonify({
            "status": -1,
            "message": "权限不足"
        })
    player = User.query.get(data['player_id'])
    player.table_id = None
    action_log = ActionLog(action="（管理）移除球台预订者", operator_id=data['my_id'])
    db.session.add(action_log)
    db.session.commit()
    return jsonify({
        "status": 200,
        "message": "球台预订者移除成功"
    })


# 发起支付请求
@bp.route('/create_pay', methods=['POST'])
def create_pay():
    data = request.json
    pay_data = {
        'body': data['description'],  # 商品描述
        'attach': data['attach'],  # 附加数据
        'total_fee': int(data['amount'] * 100),  # 金额，单位为分
        'openid': data['openid'],
    }
    wxpay = WxPay(pay_data)
    pay_info = wxpay.get_pay_info()
    if pay_info:
        return jsonify(pay_info)
    return jsonify({
        "status": -1,
        "message": "支付请求发起失败"
    })


# 支付回调通知（暂时弃用）
@bp.route('/pay_notify', methods=['POST'])
def pay_notify():
    result_data = {
        'return_code': 'SUCCESS',
        'return_msg': 'OK'
    }
    return dict_to_order_xml(result_data), {'Content-Type': 'application/xml'}


# 发送测试邮件
@bp.route("/mail_test")
def mail_test():
    message = Message(subject="Test Message", recipients=["15947513567@163.com"], body="This is a test mail!")
    mail.send(message)
    return "成功"

# # 测试ip定位
# @bp.route("/ip_position")
# def ip_position():
#     get_location()
#     return get_location()
