import json, time, math, operator, datetime, sqlalchemy, random

from flask import Blueprint, request, redirect, url_for, session, render_template, g, jsonify, flash
from models import Competition, User, Organization, Team, Log, ActionLog, Couple
from exts import db
from bluePrints.form import UpdateScoreForm, MatchInsertForm, MatchDetailForm, MatchSignUpForm
from decorators import login_required

bp = Blueprint("competition", __name__, url_prefix="/competition")


# 积分标准
@bp.route("/score_standard")
@login_required
def score_standard():
    users = User.query.order_by(User.score.desc()).all()
    students = User.query.filter_by(role="学生").all()
    teachers = User.query.filter_by(role="教师").all()
    return render_template("info/score-standard.html", users=users, students=students, teachers=teachers)


def sort_id(users):
    ids = []
    flag_index = 0
    for i in range(len(users)):
        if i == 0:
            ids.append(i + 1)
        else:
            if users[i].score == users[flag_index].score:
                ids.append(flag_index + 1)
            else:
                flag_index = i
                ids.append(i + 1)
    return ids


# 进入个人积分排名
@bp.route("/score_rank")
@login_required
def score_rank():
    users = User.query.order_by(User.score.desc()).all()
    students = User.query.filter_by(role="学生").all()
    teachers = User.query.filter_by(role="教师").all()
    ids = sort_id(users)
    return render_template("info/score-rank.html", users=users, ids=ids, students=students, teachers=teachers)


# 进入代表队积分排名
@bp.route("/score_rank_team")
@login_required
def score_rank_team():
    teams = Team.query.order_by(Team.score.desc()).all()
    ids = sort_id(teams)
    return render_template("info/score-rank_team.html", teams=teams, ids=ids)


# 根据选手姓名查找选手（积分排名中）
@bp.route('/findUserByName2/<keywords>')
def findUserByName2(keywords):
    if keywords == '':
        users = User.query.all()
    else:
        users = User.query.filter(User.username.contains(keywords)).all()
        scores = operator.attrgetter('score')
        users.sort(key=scores, reverse=True)  # operator库，对users里的score属性逆序排序
        students = []
        teachers = []
        for x in range(len(users)):
            if users[x].role == "学生":
                students.append(users[x])
            else:
                teachers.append(users[x])
    ids = sort_id(users)
    return render_template("info/score-rank.html", users=users, ids=ids, students=students, teachers=teachers)


# 学校排名（积分排名中）
@bp.route('/schoolRank/<keywords>')
def schoolRank(keywords):
    if keywords == '':
        users = User.query.all()
    else:
        users = User.query.filter(User.school.contains(keywords)).all()  # users为列表形式
        scores = operator.attrgetter('score')
        users.sort(key=scores, reverse=True)  # operator库，对users里的score属性逆序排序
        students = []
        teachers = []
        for x in range(len(users)):
            if users[x].role == "学生":
                students.append(users[x])
            else:
                teachers.append(users[x])
    ids = sort_id(users)
    return render_template("info/score-rank.html", users=users, ids=ids, students=students, teachers=teachers)


# 地区排名（积分排名中）
@bp.route('/regionRank/<keywords>')
def regionRank(keywords):
    if keywords == '':
        users = User.query.all()
    else:
        users = User.query.filter(User.address.contains(keywords)).all()  # users为列表形式
        scores = operator.attrgetter('score')
        users.sort(key=scores, reverse=True)  # operator库，对users里的score属性逆序排序
        students = []
        teachers = []
        for x in range(len(users)):
            if users[x].role == "学生":
                students.append(users[x])
            else:
                teachers.append(users[x])
    ids = sort_id(users)
    return render_template("info/score-rank.html", users=users, ids=ids, students=students, teachers=teachers)


# 积分更新（手动）
@bp.route("/score_update", methods=["GET", "POST"])
@login_required
def score_update():
    if request.method == 'GET':
        matches = Competition.query.all()
        return render_template("info/score-update.html", matches=matches)
    else:
        match_title = request.form["match_title"]
        match = Competition.query.filter_by(title=match_title).first()
        winner_name = request.form["winner"]
        loser_name = request.form["loser"]
        result = request.form["result"]
        confirm = request.form["confirm"]

        my_id = request.form["user_id"]
        me = User.query.filter_by(id=my_id).first()
        usertype = me.usertype

        if usertype == "K9" or usertype == "K10" or usertype == "K11":
            winner = User.query.filter_by(username=winner_name).first()
            loser = User.query.filter_by(username=loser_name).first()
            if confirm != "确认":
                flash("请确保信息无误后输入“确认”！")
                return redirect(url_for("competition.score_update"))
            if not winner:
                flash("胜者选手不存在！")
                return redirect(url_for("competition.score_update"))
            if not loser:
                flash("负者选手不存在！")
                return redirect(url_for("competition.score_update"))
            if winner == loser:
                flash("比赛双方不能为同一人！")
                return redirect(url_for("competition.score_update"))
            else:
                win_score_before_session = winner.score     # 这里是该场次前积分
                lose_score_before_session = loser.score
                if not match:
                    win_score_before = win_score_before_session
                    lose_score_before = lose_score_before_session
                else:
                    if winner not in match.players or loser not in match.players:
                        flash("存在未报名该赛事的选手！")
                        return redirect(url_for("competition.score_update"))
                    win_score_before = winner.fixed_score     # 这里是报名时积分
                    lose_score_before = loser.fixed_score
                delta = math.fabs(win_score_before - lose_score_before)
                if win_score_before == 0 or lose_score_before == 0:
                    flash("0分选手需先定初始积分！")
                    return redirect(url_for("competition.score_update"))
                if win_score_before >= lose_score_before:  # 高分赢低分
                    if delta <= 12:
                        winner.score += 8
                        loser.score -= 8
                    elif 13 <= delta <= 37:
                        winner.score += 7
                        loser.score -= 7
                    elif 38 <= delta <= 62:
                        winner.score += 6
                        loser.score -= 6
                    elif 63 <= delta <= 87:
                        winner.score += 5
                        loser.score -= 5
                    elif 88 <= delta <= 112:
                        winner.score += 4
                        loser.score -= 4
                    elif 113 <= delta <= 137:
                        winner.score += 3
                        loser.score -= 3
                    elif 138 <= delta <= 187:
                        winner.score += 2
                        loser.score -= 2
                    elif 188 <= delta <= 237:
                        winner.score += 1
                        loser.score -= 1
                    elif delta >= 238:
                        pass
                else:  # 低分赢高分
                    if delta <= 12:
                        winner.score += 8
                        loser.score -= 8
                    elif 13 <= delta <= 37:
                        winner.score += 10
                        loser.score -= 10
                    elif 38 <= delta <= 62:
                        winner.score += 13
                        loser.score -= 13
                    elif 63 <= delta <= 87:
                        winner.score += 16
                        loser.score -= 16
                    elif 88 <= delta <= 112:
                        winner.score += 20
                        loser.score -= 20
                    elif 113 <= delta <= 137:
                        winner.score += 25
                        loser.score -= 25
                    elif 138 <= delta <= 162:
                        winner.score += 30
                        loser.score -= 30
                    elif 163 <= delta <= 187:
                        winner.score += 35
                        loser.score -= 35
                    elif 188 <= delta <= 212:
                        winner.score += 40
                        loser.score -= 40
                    elif 213 <= delta <= 237:
                        winner.score += 45
                        loser.score -= 45
                    elif delta >= 238:
                        winner.score += 50
                        loser.score -= 50

                # 写进积分变动日志
                if not match:
                    log = Log(operator_id=my_id, winner_name=winner.username, winner_score_before=win_score_before_session, winner_score_after=winner.score, loser_name=loser.username,
                              loser_score_before=lose_score_before_session, loser_score_after=loser.score)
                else:
                    log = Log(operator_id=my_id, winner_name=winner.username, winner_score_before=win_score_before_session, winner_score_after=winner.score, loser_name=loser.username,
                              loser_score_before=lose_score_before_session, loser_score_after=loser.score, match_id=match.id, result=result)
                db.session.add(log)
                db.session.commit()
                flash("积分更新成功！")
                return redirect(url_for("competition.score_update"))
        else:
            flash("权限不足！")
            return redirect(url_for("competition.score_update"))


# 双打积分更新（手动）
@bp.route("/score_update_double", methods=["POST"])
@login_required
def score_update_double():
    match_title = request.form["match_title"]
    match = Competition.query.filter_by(title=match_title).first()
    winner1_name = request.form["winner1"]
    winner2_name = request.form["winner2"]
    loser1_name = request.form["loser1"]
    loser2_name = request.form["loser2"]
    result = request.form["result2"]     # 没法存进session表
    confirm = request.form["confirm"]

    my_id = request.form["user_id"]
    me = User.query.filter_by(id=my_id).first()
    usertype = me.usertype

    if usertype == "K9" or usertype == "K10" or usertype == "K11":
        winner1 = User.query.filter_by(username=winner1_name).first()
        winner2 = User.query.filter_by(username=winner2_name).first()
        loser1 = User.query.filter_by(username=loser1_name).first()
        loser2 = User.query.filter_by(username=loser2_name).first()
        if confirm != "确认":
            flash("请确保信息无误后输入“确认”！")
            return redirect(url_for("competition.score_update"))
        if not winner1:
            flash("胜方选手1不存在！")
            return redirect(url_for("competition.score_update"))
        if not winner2:
            flash("胜方选手2不存在！")
            return redirect(url_for("competition.score_update"))
        if not loser1:
            flash("负方选手1不存在！")
            return redirect(url_for("competition.score_update"))
        if not loser2:
            flash("负方选手2不存在！")
            return redirect(url_for("competition.score_update"))
        if winner1 == winner2 or loser1 == loser2:
            flash("双打选手不能为同一人！")
            return redirect(url_for("competition.score_update"))
        if winner1 == loser1 or winner1 == loser2 or winner2 == loser1 or winner2 == loser2:
            flash("比赛双方不能存在同一人！")
            return redirect(url_for("competition.score_update"))
        else:
            winner1_score = winner1.score
            winner2_score = winner2.score
            loser1_score = loser1.score
            loser2_score = loser2.score
            if winner1_score == 0 or winner2_score == 0 or loser1_score == 0 or loser2_score == 0:
                flash("0分选手需先定初始积分！")
                return redirect(url_for("competition.score_update"))

            if not match:     # 没有绑定赛事的情况
                win_score_before = (winner1_score + winner2_score)/2
                lose_score_before = (loser1_score + loser2_score)/2
            else:     # 有绑定赛事的情况
                if winner1 not in match.players or winner2 not in match.players or loser1 not in match.players or loser2 not in match.players:
                    flash("存在未报名该赛事的选手！")
                    return redirect(url_for("competition.score_update"))
                win_score_before = (winner1.fixed_score + winner2.fixed_score)/2
                lose_score_before = (loser1.fixed_score + loser2.fixed_score)/2
            delta = math.fabs(win_score_before - lose_score_before)
            if win_score_before >= lose_score_before:  # 高分赢低分
                if delta <= 12:
                    winner1.score += 8
                    winner2.score += 8
                    loser1.score -= 8
                    loser2.score -= 8
                elif 13 <= delta <= 37:
                    winner1.score += 7
                    winner2.score += 7
                    loser1.score -= 7
                    loser2.score -= 7
                elif 38 <= delta <= 62:
                    winner1.score += 6
                    winner2.score += 6
                    loser1.score -= 6
                    loser2.score -= 6
                elif 63 <= delta <= 87:
                    winner1.score += 5
                    winner2.score += 5
                    loser1.score -= 5
                    loser2.score -= 5
                elif 88 <= delta <= 112:
                    winner1.score += 4
                    winner2.score += 4
                    loser1.score -= 4
                    loser2.score -= 4
                elif 113 <= delta <= 137:
                    winner1.score += 3
                    winner2.score += 3
                    loser1.score -= 3
                    loser2.score -= 3
                elif 138 <= delta <= 187:
                    winner1.score += 2
                    winner2.score += 2
                    loser1.score -= 2
                    loser2.score -= 2
                elif 188 <= delta <= 237:
                    winner1.score += 1
                    winner2.score += 1
                    loser1.score -= 1
                    loser2.score -= 1
                elif delta >= 238:
                    pass
            else:  # 低分赢高分
                if delta <= 12:
                    winner1.score += 8
                    winner2.score += 8
                    loser1.score -= 8
                    loser2.score -= 8
                elif 13 <= delta <= 37:
                    winner1.score += 10
                    winner2.score += 10
                    loser1.score -= 10
                    loser2.score -= 10
                elif 38 <= delta <= 62:
                    winner1.score += 13
                    winner2.score += 13
                    loser1.score -= 13
                    loser2.score -= 13
                elif 63 <= delta <= 87:
                    winner1.score += 16
                    winner2.score += 16
                    loser1.score -= 16
                    loser2.score -= 16
                elif 88 <= delta <= 112:
                    winner1.score += 20
                    winner2.score += 20
                    loser1.score -= 20
                    loser2.score -= 20
                elif 113 <= delta <= 137:
                    winner1.score += 25
                    winner2.score += 25
                    loser1.score -= 25
                    loser2.score -= 25
                elif 138 <= delta <= 162:
                    winner1.score += 30
                    winner2.score += 30
                    loser1.score -= 30
                    loser2.score -= 30
                elif 163 <= delta <= 187:
                    winner1.score += 35
                    winner2.score += 35
                    loser1.score -= 35
                    loser2.score -= 35
                elif 188 <= delta <= 212:
                    winner1.score += 40
                    winner2.score += 40
                    loser1.score -= 40
                    loser2.score -= 40
                elif 213 <= delta <= 237:
                    winner1.score += 45
                    winner2.score += 45
                    loser1.score -= 45
                    loser2.score -= 45
                elif delta >= 238:
                    winner1.score += 50
                    winner2.score += 50
                    loser1.score -= 50
                    loser2.score -= 50
            # 写进积分变动日志
            if not match:     # 没有绑定赛事的情况
                log = Log(operator_id=my_id, winner_name=f"{winner1_name}/{winner2_name}", winner_score_before=f"{winner1_score}/{winner2_score}",
                          winner_score_after=f"{winner1.score}/{winner2.score}",
                          loser_name=f"{loser1_name}/{loser2_name}", loser_score_before=f"{loser1_score}/{loser2_score}", loser_score_after=f"{loser1.score}/{loser2.score}")
            else:     # 有绑定赛事的情况
                log = Log(operator_id=my_id, winner_name=f"{winner1_name}/{winner2_name}", winner_score_before=f"{winner1_score}/{winner2_score}",
                          winner_score_after=f"{winner1.score}/{winner2.score}",
                          loser_name=f"{loser1_name}/{loser2_name}", loser_score_before=f"{loser1_score}/{loser2_score}", loser_score_after=f"{loser1.score}/{loser2.score}", match_id=match.id, result=result)
            db.session.add(log)
            db.session.commit()
            flash("积分更新成功！")
            return redirect(url_for("competition.score_update"))
    else:
        flash("权限不足！")
        return redirect(url_for("competition.score_update"))


# 进入查看赛事
@bp.route("/match_list")
@login_required
def match_list():
    matches = Competition.query.order_by(Competition.match_time).all()
    SH_matches = Competition.query.filter_by(address="上海市").all()
    c_matches = []
    h_matches = []
    now = datetime.datetime.now()
    for match in matches:
        if match.match_time >= now:
            c_matches.append(match)
        else:
            h_matches.append(match)
    return render_template("info/match-list.html", matches=matches, SH_matches=SH_matches, c_matches=c_matches, h_matches=h_matches)


# 根据赛事名称查找赛事（查看赛事中）
@bp.route('/findMatchByName/<keywords>')
def findMatchByName(keywords):
    matches = Competition.query.order_by(Competition.match_time).all()
    SH_matches = Competition.query.filter_by(address="上海市").all()
    if keywords == '':
        c_matches = Competition.query.all()
    else:
        c_matches = Competition.query.filter(Competition.title.contains(keywords)).all()
    return render_template("info/match-list.html", matches=matches, SH_matches=SH_matches, c_matches=c_matches)


# 查看全部赛事（查看赛事中）
@bp.route('/allMatches')
def allMatches():
    matches = Competition.query.order_by(Competition.match_time).all()
    SH_matches = Competition.query.filter_by(address="上海市").all()
    c_matches = Competition.query.order_by(Competition.match_time).all()
    return render_template("info/match-list.html", matches=matches, SH_matches=SH_matches, c_matches=c_matches)


# 查看历史赛事（查看赛事中）
@bp.route('/historyMatches')
def historyMatches():
    matches = Competition.query.order_by(Competition.match_time).all()
    SH_matches = Competition.query.filter_by(address="上海市").all()
    c_matches = []
    now = datetime.datetime.now()
    for match in matches:
        if match.match_time < now:  # 现在之前的所有赛事
            c_matches.append(match)
    return render_template("info/match-list.html", matches=matches, SH_matches=SH_matches, c_matches=c_matches)


# 查看已报名赛事（查看赛事中）
@bp.route('/myMatches', methods=['POST', "GET"])
def myMatches():
    if request.method == "GET":
        matches = Competition.query.order_by(Competition.match_time).all()
        SH_matches = Competition.query.filter_by(address="上海市").all()
        my_id = request.args.get("my_id")
        me = User.query.filter_by(id=my_id).first()
        my_matches = me.matches  # 反向引用（back_populates）
        c_matches = []
        now = datetime.datetime.now()
        for match in my_matches:
            if match.match_time >= now:
                c_matches.append(match)
        return render_template("info/match-list.html", matches=matches, SH_matches=SH_matches, c_matches=c_matches)
    else:
        return render_template("info/match-list.html")


# 进入赛事详情页面
@bp.route("/match_detail", methods=['GET', "POST"])
@login_required
def match_detail():
    if request.method == 'GET':
        return render_template("info/match-detail.html")  # 无法到达
    else:
        organs = Organization.query.all()
        form = MatchDetailForm(request.form)
        id = form.id.data
        match1 = Competition.query.filter_by(id=id).first()
        return render_template("info/match-detail.html", organs=organs, match1=match1)


# 添加参赛代表队
@bp.route("/add_team", methods=['GET', "POST"])
@login_required
def add_team():
    if request.method == 'GET':
        return render_template("info/match-players.html")  # 无法到达
    else:
        organs = Organization.query.all()
        my_id = request.form.get("my_id")
        me = User.query.filter_by(id=my_id).first()
        match_id = request.form.get("match_id")
        match1 = Competition.query.filter_by(id=match_id).first()
        teamname = request.form.get("teamname")
        description = request.form.get("description")
        member_max = request.form.get("member_max")
        teams = Team.query.all()
        team_x = Team.query.filter_by(teamname=teamname).first()
        if me.usertype == "K9" or me.usertype == "K10" or me.usertype == "K11":
            if not teamname:
                flash("请输入队名！")
                return render_template("info/match-detail.html", organs=organs, match1=match1)
            if not member_max:
                flash("请输入队员人数上限！")
                return render_template("info/match-detail.html", organs=organs, match1=match1)
            if team_x in teams:
                flash("该代表队已存在！")
                return render_template("info/match-detail.html", organs=organs, match1=match1)
            team = Team(teamname=teamname, description=description, member_max=member_max, match_id=match_id)
            db.session.add(team)
            action_log = ActionLog(action=f"（管理）添加赛事『{match1.title}』参赛代表队『{teamname}』", operator_id=my_id)
            db.session.add(action_log)
            db.session.commit()
            flash("添加成功！")
            return render_template("info/match-detail.html", organs=organs, match1=match1)
        else:
            flash("权限不足！")
            return render_template("info/match-detail.html", organs=organs, match1=match1)


# 进入赛事选手页面
@bp.route("/match_players", methods=['GET', "POST"])
@login_required
def match_players():
    if request.method == 'GET':
        id = request.args.get('id')
        match1 = Competition.query.filter_by(id=id).first()
        teams = Team.query.filter_by(match_id=id).all()
        players = match1.players
        scores = operator.attrgetter('score')
        players.sort(key=scores, reverse=True)  # 按积分排列
        return render_template("info/match-players.html", match1=match1, players=players, teams=teams)
    else:
        return "请求方式错误！"


# 添加参赛选手（赛事选手中）
@bp.route("/add_player", methods=['GET', "POST"])
@login_required
def add_player():
    if request.method == 'GET':
        return render_template("info/match-players.html")  # 无法到达
    else:
        form = MatchSignUpForm(request.form)
        user_id = form.user_id.data
        me = User.query.filter_by(id=user_id).first()
        match_id = form.match_id.data
        match1 = Competition.query.filter_by(id=match_id).first()
        teams = Team.query.filter_by(match_id=match_id).all()
        player_username = form.player_username.data
        player = User.query.filter_by(username=player_username).first()
        team_id = form.team_id.data
        team1 = Team.query.filter_by(id=team_id).first()

        players = match1.players  # 为了添加后回到赛事选手界面，需要把其需要的几个变量定义一下
        scores = operator.attrgetter('score')
        players.sort(key=scores, reverse=True)  # 按积分排列

        if me.usertype == "K9" or me.usertype == "K10" or me.usertype == "K11":
            if not player:
                flash("该选手不存在！")
                return render_template("info/match-players.html", match1=match1, players=players, teams=teams)
            if player in match1.players:
                flash("该选手已报名该赛事！")
                return render_template("info/match-players.html", match1=match1, players=players, teams=teams)
            if match1.match_type == "男子团体" or match1.match_type == "女子团体" or match1.match_type == "混合团体":
                if not team1:
                    flash("请选择选手报名代表队！")
                    return render_template("info/match-players.html", match1=match1, players=players, teams=teams)
                team1.members.append(player)
            match1.players.append(player)
            player.fixed_score = player.score
            action_log = ActionLog(action=f"（管理）添加赛事『{match1.title}』参赛选手『{player_username}』", operator_id=user_id)
            db.session.add(action_log)
            db.session.commit()
            flash("选手添加成功！")
            return render_template("info/match-players.html", match1=match1, players=players, teams=teams)
        else:
            flash("权限不足！")
            return redirect(url_for("competition.match_list"))


# 移除选手（赛事选手中）
@bp.route('/delete_player', methods=['GET', 'POST'])
def delete_player():
    if request.method == 'GET':
        return jsonify({
            "status": -1,
            "message": "请求方式错误！"
        })
    else:
        data = request.get_json()
        player = User.query.get(data['player_id'])
        match1 = Competition.query.get(data['match1_id'])
        action_log = ActionLog(action=f"（管理）移除赛事『{match1.title}』参赛选手『{player.username}』", operator_id=data['my_id'])
        db.session.add(action_log)
        match1.players.remove(player)
        db.session.commit()
        return jsonify({
            "status": 200,
            "message": "移除成功！"
        })


# 更新赛事（赛事详情中）
@bp.route("/update_match", methods=['POST'])
def update_match():
    data = request.get_json()
    match_id = data['id']
    match = Competition.query.get(match_id)
    if not match:
        return jsonify({
            "status": -1,
            "message": "赛事不存在！"
        })
    match.title = data['title']
    match.description = data['description']
    match.match_type = data['match_type']
    match.address = data['address']
    match.system = data['system']
    match.place = data['place']
    match.participant = data['participant']
    match.fee = data['fee']
    match.prize_for_first = data['prize_for_first']
    match.prize_for_second = data['prize_for_second']
    match.prize_for_third = data['prize_for_third']
    match.additional_info = data['additional_info']

    match_time = datetime.datetime.strptime(data['match_time'], "%Y-%m-%d %H:%M:%S")
    match.match_time = match_time
    sign_start_time = datetime.datetime.strptime(data['sign_start_time'], "%Y-%m-%d %H:%M:%S")
    match.sign_start_time = sign_start_time
    sign_end_time = datetime.datetime.strptime(data['sign_end_time'], "%Y-%m-%d %H:%M:%S")
    match.sign_end_time = sign_end_time
    action_log = ActionLog(action=f"（管理）更新赛事『{data['title']}』赛事信息", operator_id=data['my_id'])
    db.session.add(action_log)
    db.session.commit()
    return jsonify({
        "status": 200,
        "message": "修改成功！"
    })


# 变更报名限制（赛事详情中）
@bp.route("/restriction_change", methods=["GET", "POST"])
def restriction_change():
    if request.method == 'GET':
        return "请求方式错误！"
    else:
        organs = Organization.query.all()
        my_id = request.form.get('my_id')
        me = User.query.filter_by(id=my_id).first()
        match_id = request.form.get('match_id')
        match1 = Competition.query.filter_by(id=match_id).first()
        restriction = request.form.get('restriction')
        if me.usertype == "K9" or me.usertype == "K10" or me.usertype == "K11":
            if restriction == "积分限制":
                score_min = form.score_min.data
                score_max = form.score_max.data
                match1.score_min = score_min
                match1.score_max = score_max
            match1.restriction = restriction
            action_log = ActionLog(action=f"（管理）变更赛事『{match1.title}』报名限制", operator_id=my_id)
            db.session.add(action_log)
            db.session.commit()
            flash("变更成功！")
            return render_template("info/match-detail.html", organs=organs, match1=match1)
        else:
            flash("权限不足！")
            return render_template("info/match-detail.html", organs=organs, match1=match1)


# 变更主办方（赛事详情中）
@bp.route("/organ_change", methods=["GET", "POST"])
def organ_change():
    if request.method == 'GET':
        return render_template("match-detail.html")
    else:
        organs = Organization.query.all()
        my_id = request.form.get('my_id')
        me = User.query.filter_by(id=my_id).first()
        match_id = request.form.get('match_id')
        match1 = Competition.query.filter_by(id=match_id).first()
        organ_id = request.form.get('organ_id')
        if me.usertype == "K10" or me.usertype == "K11":
            match1.organ_id = organ_id
            action_log = ActionLog(action=f"（管理）变更赛事『{match1.title}』主办方", operator_id=my_id)
            db.session.add(action_log)
            db.session.commit()
            flash("变更成功！")
            return render_template("info/match-detail.html", organs=organs, match1=match1)
        else:
            flash("权限不足！")
            return render_template("info/match-detail.html", organs=organs, match1=match1)


# 删除赛事（赛事详情中）
@bp.route('/delete_match', methods=['GET', 'POST'])
def delete_match():
    if request.method == 'GET':
        return jsonify({
            "status": -1,
            "message": "请求方式错误！"
        })
    else:
        data = request.get_json()
        match = Competition.query.get(data['id'])
        if not match:
            return jsonify({
                "status": -1,
                "message": "赛事不存在!"
            })
        else:
            action_log = ActionLog(action=f"（管理）删除赛事『{match.title}』", operator_id=data["my_id"])
            db.session.add(action_log)
            db.session.delete(match)
            db.session.commit()
            return jsonify({
                "status": 200,
                "message": "删除成功！"
            })


# 取消报名（赛事详情中）
@bp.route('/quit_match', methods=['GET', 'POST'])
def quit_match():
    if request.method == 'GET':
        return jsonify({
            "status": -1,
            "message": "请求方式错误！"
        })
    else:
        data = request.get_json()
        me = User.query.get(data['my_id'])
        match = Competition.query.get(data['match_id'])
        now = datetime.datetime.now()
        if not match:
            return jsonify({
                "status": -1,
                "message": "赛事不存在!"
            })
        if match not in me.matches:
            return jsonify({
                "status": -1,
                "message": "您还未报名该赛事!"
            })
        if match.sign_end_time < now:
            return jsonify({
                "status": -1,
                "message": "已过报名截止时间，无法取消报名!"
            })
        else:
            me.matches.remove(match)
            action_log = ActionLog(action=f"取消报名赛事『{match.title}』", operator_id=me.id)
            db.session.add(action_log)
            db.session.commit()
            return jsonify({
                "status": 200,
                "message": "取消报名成功！"
            })


# 赛事报名
@bp.route("/match_sign_up", methods=["GET", "POST"])
@login_required
def match_sign_up():
    if request.method == "GET":
        match_id = request.args.get("match_id")  # GET表单获取数据的方式
        match1 = Competition.query.filter_by(id=match_id).first()
        teams = Team.query.filter_by(match_id=match_id).all()
        return render_template("info/match-sign_up.html", match1=match1, teams=teams)
    else:
        form = MatchSignUpForm(request.form)
        match_id = form.match_id.data
        match1 = Competition.query.filter_by(id=match_id).first()
        teams = Team.query.filter_by(match_id=match_id).all()
        user_id = form.user_id.data
        user1 = User.query.filter_by(id=user_id).first()
        team_id = form.team_id.data
        team1 = Team.query.filter_by(id=team_id).first()
        agree = form.agree.data

        if match1.sign_end_time < datetime.datetime.now():
            flash("该赛事已截止报名！")
            return render_template("info/match-sign_up.html", match1=match1, teams=teams)  # render_template函数返回的是生成的HTML页面代码；redirect函数返回的是一个新的URL，用户的浏览器将会跳转到该URL。
        if match1.sign_start_time > datetime.datetime.now():
            flash("该赛事尚未开始报名！")
            return render_template("info/match-sign_up.html", match1=match1, teams=teams)
        if match1.match_type == "男子单打" or match1.match_type == "女子单打" or match1.match_type == "混合单打":
            if len(match1.players) >= match1.participant:
                flash("该赛事参赛名额已满！")
                return render_template("info/match-sign_up.html", match1=match1, teams=teams)
        if match1.match_type == "男子团体" or match1.match_type == "女子团体" or match1.match_type == "混合团体":
            if not team1:
                flash("请选择报名代表队！")
                return render_template("info/match-sign_up.html", match1=match1, teams=teams)
            elif team1.member_max - len(team1.members) <= 0:
                flash("该赛事参赛名额已满！")
                return render_template("info/match-sign_up.html", match1=match1, teams=teams)
            elif user1 not in team1.members:
                for team_x in teams:
                    if team_x.match_id == match1.id:
                        if user1 in team_x.members:
                            team_x.members.remove(user1)
                team1.members.append(user1)
        if match1.restriction == "限制（仅）男子" and user1.gender != "男":
            flash("该赛事报名限制：仅男子！")
            return render_template("info/match-sign_up.html", match1=match1, teams=teams)
        elif match1.restriction == "限制（仅）女子" and user1.gender != "女":
            flash("该赛事报名限制：仅女子！")
            return render_template("info/match-sign_up.html", match1=match1, teams=teams)
        elif match1.restriction == "限制（仅）女子" and user1.gender != "女":
            flash("该赛事报名限制：仅女子！")
            return render_template("info/match-sign_up.html", match1=match1, teams=teams)
        elif match1.restriction == "限制（仅）学生" and user1.role != "学生":
            flash("该赛事报名限制：仅学生！")
            return render_template("info/match-sign_up.html", match1=match1, teams=teams)
        elif match1.restriction == "限制（仅）教师" and user1.role != "教师":
            flash("该赛事报名限制：仅教师！")
            return render_template("info/match-sign_up.html", match1=match1, teams=teams)
        elif match1.restriction == "积分限制" and (user1.score < match1.score_min or user1.score > match1.score_max):
            flash("您不符合该赛事积分限制！")
            return render_template("info/match-sign_up.html", match1=match1, teams=teams)
        else:
            if agree == "disagreed":
                flash("请阅读并同意承诺书！")
                return render_template("info/match-sign_up.html", match1=match1, teams=teams)
            # 报名成功
            elif agree == "agreed":
                try:
                    match1.players.append(user1)
                    user1.fixed_score = user1.score
                    action_log = ActionLog(action=f"报名赛事『{match1.title}』", operator_id=user_id)
                    db.session.add(action_log)
                    db.session.commit()
                except sqlalchemy.exc.IntegrityError:
                    flash("您已成功报名，无需重复操作！")
                    return redirect(url_for("competition.match_list"))
                else:
                    flash("报名成功！")
                    return redirect(url_for("competition.match_list"))


# 进入赛事成绩管理页面
@bp.route("/tea_stu_page", methods=['GET'])
@login_required
def tea_stu_page():
    couples = Couple.query.all()
    for couple in couples:
        user1 = User.query.get(couple.user1_id)
        user2 = User.query.get(couple.user2_id)
        print(user1.username, user1.gender, user1.role, user2.username, user2.gender, user2.role)
    return render_template("info/tea_stu-players.html")

# 师生混双报名
@bp.route("/tea_stu_sign", methods=['POST'])
@login_required
def tea_stu_sign():
    user1_id = request.form["user1_id"]
    user2_username = request.form["user2_username"]
    user2 = User.query.filter_by(username=user2_username).first()
    if not user2:
        flash("选手2不存在！")
        return redirect(url_for("competition.match_list"))
    couple = Couple(user1_id=user1_id, user2_id=user2.id)
    couple_exist1 = (Couple.query.filter_by(user1_id=user1_id).first()) or (Couple.query.filter_by(user2_id=user1_id).first())
    couple_exist2 = (Couple.query.filter_by(user1_id=user2.id).first()) or (Couple.query.filter_by(user2_id=user2.id).first())
    if couple_exist1 or couple_exist2:
        flash("已成功报名，无需重复操作！")
        return redirect(url_for("competition.match_list"))
    db.session.add(couple)
    db.session.commit()
    flash("报名成功")
    return redirect(url_for("competition.match_list"))


# 进入赛事成绩管理页面
@bp.route("/match_order", methods=['GET', "POST"])
@login_required
def match_order():
    if request.method == 'GET':
        match_id = request.args.get('match_id')
        match1 = Competition.query.filter_by(id=match_id).first()
        players = match1.players
        # random.shuffle(players)
        return render_template("info/match-order.html", match1=match1, players=players)
    else:  # 点击录成绩进成绩录入
        match1_id = request.form.get("match1_id")
        match1 = Competition.query.filter_by(id=match1_id).first()
        player_x_id = request.form.get("player_x_id")
        player_x = User.query.filter_by(id=player_x_id).first()
        player_y_id = request.form.get("player_y_id")
        player_y = User.query.filter_by(id=player_y_id).first()
        return render_template("info/match-result-record.html", match1=match1, player_x=player_x, player_y=player_y)


# 进入成绩录入页面（赛事成绩管理中）
@bp.route("/result_record", methods=['GET', "POST"])
@login_required
def result_record():
    if request.method == 'GET':  # 过不来
        return render_template("info/match-result-record.html")
    else:  # 确认录入成绩
        match1_id = request.form.get("match1_id")
        match1 = Competition.query.filter_by(id=match1_id).first()
        player_x_id = request.form.get("player_x_id")
        player_x = User.query.filter_by(id=player_x_id).first()
        player_y_id = request.form.get("player_y_id")
        player_y = User.query.filter_by(id=player_y_id).first()
        result = request.form.get("result")

        my_id = request.form.get("user_id")
        me = User.query.filter_by(id=my_id).first()
        usertype = me.usertype

        if usertype == "K9" or usertype == "K10" or usertype == "K11":
            if not result:
                flash("请录入比分！")
                return render_template("info/match-result-record.html", match1=match1, player_x=player_x, player_y=player_y)
            if result == "2:0" or result == "2:1" or result == "3:0" or result == "3:1" or result == "3:2" or result == "4:x":  # 注意每个or后面都要加result==
                winner = player_x
                loser = player_y
            else:
                winner = player_y
                loser = player_x
            # 计算积分
            win_score_before = winner.fixed_score     # 这里是赛前报名积分
            lose_score_before = loser.fixed_score
            win_score_before_session = winner.score     # 这里是该场次计算前的积分
            lose_score_before_session = loser.score
            delta = math.fabs(win_score_before - lose_score_before)
            if win_score_before == 0 or lose_score_before == 0:
                flash("0分选手需先定初始积分！")
                return render_template("info/match-result-record.html", match1=match1, player_x=player_x, player_y=player_y)
            if win_score_before >= lose_score_before:  # 高分赢低分
                if delta <= 12:
                    winner.score += 8
                    loser.score -= 8
                elif 13 <= delta <= 37:
                    winner.score += 7
                    loser.score -= 7
                elif 38 <= delta <= 62:
                    winner.score += 6
                    loser.score -= 6
                elif 63 <= delta <= 87:
                    winner.score += 5
                    loser.score -= 5
                elif 88 <= delta <= 112:
                    winner.score += 4
                    loser.score -= 4
                elif 113 <= delta <= 137:
                    winner.score += 3
                    loser.score -= 3
                elif 138 <= delta <= 187:
                    winner.score += 2
                    loser.score -= 2
                elif 188 <= delta <= 237:
                    winner.score += 1
                    loser.score -= 1
                elif delta >= 238:
                    pass
            else:  # 低分赢高分
                if delta <= 12:
                    winner.score += 8
                    loser.score -= 8
                elif 13 <= delta <= 37:
                    winner.score += 10
                    loser.score -= 10
                elif 38 <= delta <= 62:
                    winner.score += 13
                    loser.score -= 13
                elif 63 <= delta <= 87:
                    winner.score += 16
                    loser.score -= 16
                elif 88 <= delta <= 112:
                    winner.score += 20
                    loser.score -= 20
                elif 113 <= delta <= 137:
                    winner.score += 25
                    loser.score -= 25
                elif 138 <= delta <= 162:
                    winner.score += 30
                    loser.score -= 30
                elif 163 <= delta <= 187:
                    winner.score += 35
                    loser.score -= 35
                elif 188 <= delta <= 212:
                    winner.score += 40
                    loser.score -= 40
                elif 213 <= delta <= 237:
                    winner.score += 45
                    loser.score -= 45
                elif delta >= 238:
                    winner.score += 50
                    loser.score -= 50
            flash("积分计算完成！")
            # 写进积分变动日志
            if int(result[0]) < int(result[-1]):
                result = result[::-1]
            log = Log(operator_id=my_id, match_id=match1_id, winner_name=winner.username, winner_score_before=win_score_before_session, winner_score_after=winner.score,
                      loser_name=loser.username, loser_score_before=lose_score_before_session, loser_score_after=loser.score, result=result)
            db.session.add(log)
            db.session.commit()
            flash("成绩录入成功！")
            return render_template("info/match-result-record.html", match1=match1, player_x=player_x, player_y=player_y)
        else:
            flash("权限不足！")
            return render_template("info/match-result-record.html", match1=match1, player_x=player_x, player_y=player_y)


# 进入赛事成绩（公开）页面
@bp.route("/match_result", methods=['GET', "POST"])
@login_required
def match_result():
    if request.method == 'GET':
        match_id = request.args.get('match_id')
        match1 = Competition.query.filter_by(id=match_id).first()
        players = match1.players
        logs = Log.query.filter_by(match_id=match_id).all()
        for log in logs:
            if int(log.result[0]) < int(log.result[-1]):
                log.result = log.result[::-1]
        return render_template("info/match-result.html", match1=match1, players=players, logs=logs)
    else:  # 还没设置
        return render_template("info/match-result.html")


# 进入代表队管理
@bp.route("/team_management")
@login_required
def team_management():
    teams = Team.query.order_by(Team.score.desc()).all()
    all_matches1 = Competition.query.filter_by(match_type="男子团体").all()
    all_matches2 = Competition.query.filter_by(match_type="女子团体").all()
    all_matches3 = Competition.query.filter_by(match_type="混合团体").all()
    all_matches = all_matches1 + all_matches2 + all_matches3
    matches = []
    now = datetime.datetime.now()
    for match in all_matches:
        if match.match_time >= now:
            matches.append(match)     # matches为现在之后全部团体赛

    for team in teams:     # 计算每队的代表队积分
        team_members = team.members
        member_score = operator.attrgetter("score")
        team_members.sort(key=member_score, reverse=True)
        if len(team_members) == 0:
            team.score = 0
            db.session.commit()
        elif len(team_members) >= 4:
            ave_score1 = (team_members[0].score + team_members[1].score + team_members[2].score)/3
            score2 = 0
            for i in range(3, len(team_members)):
                score2 += team_members[i].score
            ave_score2 = score2/(len(team_members)-3)
            team.score = format(ave_score1*0.6 + ave_score2*0.4, '.1f')
            db.session.commit()
        else:
            score1 = 0
            for i in range(len(team_members)):
                score1 += team_members[i].score
            team.score = format(score1/(len(team_members)), ".1f")
            db.session.commit()
    return render_template("info/team-management.html", teams=teams, all_matches=all_matches, matches=matches)


# 进入代表队队员（代表队管理中）
@bp.route("/team_members", methods=['GET', "POST"])
@login_required
def team_members():
    if request.method == 'GET':
        team_id = request.args.get('team_id')
        team1 = Team.query.filter_by(id=team_id).first()
        members = team1.members
        scores = operator.attrgetter('score')
        members.sort(key=scores, reverse=True)  # 按积分排列
        return render_template("info/team-members.html", team1=team1, members=members)
    else:
        return "请求方式错误！"


# 添加队员（代表队队员中）
@bp.route("/add_member", methods=["POST"])
@login_required
def add_member():
    user_id = request.form.get("user_id")
    me = User.query.filter_by(id=user_id).first()
    team_id = request.form.get("team_id")
    team1 = Team.query.filter_by(id=team_id).first()
    member_username = request.form.get("member_username")
    member = User.query.filter_by(username=member_username).first()

    members = team1.members    # 为了添加后回到代表队队员界面，需要把其需要的几个变量定义一下
    scores = operator.attrgetter('score')
    members.sort(key=scores, reverse=True)  # 按积分排列

    if me.usertype == "K9" or me.usertype == "K10" or me.usertype == "K11":
        if not member:
            flash("该队员不存在！")
            return render_template("info/team-members.html", team1=team1, members=members)
        if member in team1.members:
            flash("该队员已在队内！")
            return render_template("info/team-members.html", team1=team1, members=members)

        other_teams = Team.query.filter_by(match_id=team1.match_id).all()
        for other_team in other_teams:
            if member in other_team.members:
                other_team.members.remove(member)
                flash("该队员原在其他代表队，已移入该代表队！")
        team1.members.append(member)
        match = Competition.query.get(team1.match_id)
        if member not in match.players:
            match.players.append(member)
        action_log = ActionLog(action=f"（管理）添加代表队『{team1.teamname}』队员『{member.username}』", operator_id=user_id)
        db.session.add(action_log)
        db.session.commit()
        flash("队员添加成功！")
        return render_template("info/team-members.html", team1=team1, members=members)
    else:
        flash("权限不足！")
        return redirect(url_for("competition.match_list"))


# 移除队员（代表队队员中）
@bp.route('/delete_member', methods=['GET', 'POST'])
def delete_member():
    if request.method == 'GET':
        return jsonify({
            "status": -1,
            "message": "请求方式错误！"
        })
    else:
        if g.user.usertype != "K9" and g.user.usertype != "K10" and g.user.usertype != "K11":
            return jsonify({
                "status": -1,
                "message": "权限不足！"
            })
        data = request.get_json()
        member = User.query.get(data['member_id'])
        team1 = Team.query.get(data['team1_id'])
        action_log = ActionLog(action=f"（管理）移除代表队『{team1.teamname}』队员『{member.username}』", operator_id=data['my_id'])
        db.session.add(action_log)
        team1.members.remove(member)
        match = Competition.query.get(team1.match_id)
        if member in match.players:
            match.players.remove(member)
        db.session.commit()
        return jsonify({
            "status": 200,
            "message": "移除成功！"
        })


# 变更绑定赛事（代表队管理中）
@bp.route("/match_change", methods=["GET", "POST"])
def match_change():
    if request.method == 'GET':
        return "请求方式错误！"
    else:
        teams = Team.query.order_by(Team.score.desc()).all()
        all_matches1 = Competition.query.filter_by(match_type="男子团体").all()
        all_matches2 = Competition.query.filter_by(match_type="女子团体").all()
        all_matches3 = Competition.query.filter_by(match_type="混合团体").all()
        all_matches = all_matches1 + all_matches2 + all_matches3
        matches = []
        now = datetime.datetime.now()
        for match in all_matches:
            if match.match_time >= now:
                matches.append(match)

        my_id = request.form.get('my_id')
        me = User.query.filter_by(id=my_id).first()
        if me.usertype == "K10" or me.usertype == "K11":
            team_id = request.form.get('team_id')
            team = Team.query.get(team_id)
            match_id = request.form.get('match_id')
            if not team or not match_id:
                flash("绑定赛事不能为空！")
                return render_template("info/team-management.html", teams=teams, all_matches=all_matches, matches=matches)
            team.match_id = match_id
            action_log = ActionLog(action=f"（管理）变更代表队『{team.teamname}』绑定赛事", operator_id=my_id)
            db.session.add(action_log)
            db.session.commit()
            flash("变更成功！")
            return render_template("info/team-management.html", teams=teams, all_matches=all_matches, matches=matches)
        else:
            flash("权限不足！")
            return render_template("info/team-management.html", teams=teams, all_matches=all_matches, matches=matches)


# 修改人数上限（代表队管理中）
@bp.route("/modify_max", methods=['POST'])
def modify_max():
    data = request.get_json()
    team_id = data['id']
    team = Team.query.get(team_id)
    if not team:
        return jsonify({
            "status": -1,
            "message": "代表队不存在！"
        })
    team.member_max = data['member_max']
    action_log = ActionLog(action=f"（管理）修改代表队『{team.teamname}』人数上限", operator_id=data['my_id'])
    db.session.add(action_log)
    db.session.commit()
    return jsonify({
        "status": 200,
        "message": "修改成功！"
    })


# 删除代表队（代表队管理中）
@bp.route('/delete_team', methods=['GET', 'POST'])
def delete_team():
    if request.method == 'GET':
        return jsonify({
            "status": -1,
            "message": "请求方式错误！"
        })
    else:
        data = request.get_json()
        team = Team.query.get(data['id'])
        if not team:
            return jsonify({
                "status": -1,
                "message": "代表队不存在!"
            })
        else:
            action_log = ActionLog(action=f"（管理）删除代表队『{team.teamname}』", operator_id=data['my_id'])
            db.session.add(action_log)
            db.session.delete(team)
            db.session.commit()
            return jsonify({
                "status": 200,
                "message": "删除成功！"
            })


# 根据绑定赛事查找代表队（代表队管理中）
@bp.route("/filter_team")
@login_required
def filter_team():
    match_id = request.args.get('match_id')
    teams = Team.query.filter_by(match_id=match_id).order_by(Team.score.desc()).all()
    all_matches1 = Competition.query.filter_by(match_type="男子团体").all()
    all_matches2 = Competition.query.filter_by(match_type="女子团体").all()
    all_matches3 = Competition.query.filter_by(match_type="混合团体").all()
    all_matches = all_matches1 + all_matches2 + all_matches3
    matches = []
    now = datetime.datetime.now()
    for match in all_matches:
        if match.match_time >= now:
            matches.append(match)     # matches为现在之后全部团体赛
    return render_template("info/team-management.html", teams=teams, all_matches=all_matches, matches=matches)


# 举办赛事（单打）
@bp.route("/match_insert", methods=['GET', 'POST'])
@login_required
def match_insert():
    if request.method == 'GET':
        return render_template("info/match-insert_single.html")
    else:
        form = MatchInsertForm(request.form)
        title = form.title.data
        description = form.description.data
        match_type = form.match_type.data
        address = form.address.data
        organ_id = form.organ_id.data
        organ = Organization.query.get(organ_id)

        match_time = form.match_time.data
        sign_start_time = form.sign_start_time.data
        sign_end_time = form.sign_end_time.data
        if not sign_start_time or not sign_end_time or not match_time:
            flash("时间不能为空！")
            return redirect(url_for("competition.match_insert"))
        match_time = datetime.datetime.strptime(match_time, "%Y-%m-%dT%H:%M")
        sign_start_time = datetime.datetime.strptime(sign_start_time, "%Y-%m-%dT%H:%M")
        sign_end_time = datetime.datetime.strptime(sign_end_time, "%Y-%m-%dT%H:%M")

        place = form.place.data
        participant = form.participant.data
        if not participant:
            flash("最大参赛名额不能为空！")
            return redirect(url_for("competition.match_insert"))
        fee = form.fee.data
        system = form.system.data
        restriction = form.restriction.data
        my_id = request.form.get("my_id")
        me = User.query.get(my_id)

        if me.usertype == "K9" or me.usertype == "K10" or me.usertype == "K11":
            if not system:
                flash("赛制不能为空！")
                return redirect(url_for("competition.match_insert"))
            if not match_type:
                flash("赛事类型不能为空！")
                return redirect(url_for("competition.match_insert"))
            if sign_start_time > sign_end_time:
                flash("报名开始时间早于报名截止时间！")
                return redirect(url_for("competition.match_insert"))
            if match_time < sign_end_time:
                flash("比赛时间晚于报名截止时间！")
                return redirect(url_for("competition.match_insert"))
            else:
                if restriction == "积分限制":
                    score_min = form.score_min.data
                    score_max = form.score_max.data
                    if score_max <= score_min:
                        flash("最高限制积分需大于最低限制积分！")
                        return redirect(url_for("competition.match_insert"))
                    match = Competition(title=title, description=description, match_type=match_type, address=address, organ=organ, match_time=match_time, sign_start_time=sign_start_time,
                                        sign_end_time=sign_end_time, place=place,
                                        participant=participant, fee=fee, system=system,
                                        restriction=restriction, score_min=score_min, score_max=score_max, visiable=1)
                else:
                    match = Competition(title=title, description=description, match_type=match_type, address=address, organ=organ, match_time=match_time, sign_start_time=sign_start_time,
                                        sign_end_time=sign_end_time, place=place, participant=participant,
                                        fee=fee, system=system, restriction=restriction, visiable=1)
                db.session.add(match)
                action_log = ActionLog(action=f"（管理）举办赛事『{title}』", operator_id=my_id)
                db.session.add(action_log)
                db.session.commit()
                flash("赛事创建成功！")
                return redirect(url_for("competition.match_list"))
        else:
            flash("权限不足！")
            return redirect(url_for("competition.match_insert"))


# 举办赛事（团体）
@bp.route("/match_insert_team", methods=['GET', 'POST'])
@login_required
def match_insert_team():
    if request.method == 'GET':
        return render_template("info/match-insert_team.html")
    else:
        form = MatchInsertForm(request.form)
        title = form.title.data
        description = form.description.data
        match_type = form.match_type.data
        address = form.address.data
        organ_id = form.organ_id.data
        organ = Organization.query.get(organ_id)

        match_time = form.match_time.data
        sign_start_time = form.sign_start_time.data
        sign_end_time = form.sign_end_time.data
        if not sign_start_time or not sign_end_time or not match_time:
            flash("时间不能为空！")
            return redirect(url_for("competition.match_insert_team"))
        match_time = datetime.datetime.strptime(match_time, "%Y-%m-%dT%H:%M")
        sign_start_time = datetime.datetime.strptime(sign_start_time, "%Y-%m-%dT%H:%M")
        sign_end_time = datetime.datetime.strptime(sign_end_time, "%Y-%m-%dT%H:%M")

        place = form.place.data
        fee = form.fee.data
        system = form.system.data
        restriction = form.restriction.data
        my_id = request.form.get("my_id")
        me = User.query.get(my_id)

        if me.usertype == "K9" or me.usertype == "K10" or me.usertype == "K11":
            if not system:
                flash("赛制不能为空！")
                return redirect(url_for("competition.match_insert_team"))
            if not match_type:
                flash("赛事类型不能为空！")
                return redirect(url_for("competition.match_insert_team"))
            if sign_start_time > sign_end_time:
                flash("报名开始时间早于报名截止时间！")
                return redirect(url_for("competition.match_insert_team"))
            if match_time < sign_end_time:
                flash("比赛时间晚于报名截止时间！")
                return redirect(url_for("competition.match_insert_team"))
            else:
                if restriction == "积分限制":
                    score_min = form.score_min.data
                    score_max = form.score_max.data
                    if score_max <= score_min:
                        flash("最高限制积分需大于最低限制积分！")
                        return redirect(url_for("competition.match_insert_team"))
                    match = Competition(title=title, description=description, match_type=match_type, address=address, organ=organ, match_time=match_time, sign_start_time=sign_start_time,
                                        sign_end_time=sign_end_time, place=place,
                                        fee=fee, system=system,
                                        restriction=restriction, score_min=score_min, score_max=score_max, visiable=1)
                else:
                    match = Competition(title=title, description=description, match_type=match_type, address=address, organ=organ, match_time=match_time, sign_start_time=sign_start_time,
                                        sign_end_time=sign_end_time, place=place,
                                        fee=fee, system=system, restriction=restriction, visiable=1)
                db.session.add(match)
                action_log = ActionLog(action=f"（管理）举办赛事『{title}』", operator_id=my_id)
                db.session.add(action_log)
                db.session.commit()
                flash("赛事创建成功！")
                return redirect(url_for("competition.match_list"))
        else:
            flash("权限不足！")
            return redirect(url_for("competition.match_insert_team"))
