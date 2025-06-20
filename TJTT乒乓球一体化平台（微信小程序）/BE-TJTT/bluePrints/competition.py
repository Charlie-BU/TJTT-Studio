import json, time, math, operator, datetime, sqlalchemy, random
from flask import Blueprint, request, redirect, url_for, session, render_template, g, jsonify, flash
from models import Competition, User, Organization, Team, Log, ActionLog, Season
from exts import db
from decorators import login_required
from sqlalchemy import and_, or_

bp = Blueprint("competition", __name__, url_prefix="/competition")


# 获取当前赛季
@bp.route("/get_this_season", methods=["POST"])
def get_this_season():
    now = datetime.datetime.now()
    this_season = Season.query.filter(
        and_(Season.start_time <= now, now <= Season.end_time)
    ).first()
    return jsonify({
        "status": 200,
        "message": "当前赛季获取成功",
        "this_season": this_season.jsonify_season(),
    })


# 获取积分变动日志
@bp.route("/get_score_logs", methods=["POST"])
def get_score_logs():
    # all_score_logs = Log.query.all()
    # if len(all_score_logs) > 300:
    #     for x in range(0, len(all_score_logs) - 300):
    #         db.session.delete(all_score_logs[x])
    #         db.session.commit()
    all_score_logs = Log.query.order_by(Log.time.desc()).all()
    score_logs = []
    for score_log in all_score_logs:
        score_logs.append(score_log.jsonify_score_log())
    return jsonify({
        "status": 200,
        "message": "积分变动日志获取成功",
        "score_logs": score_logs,
    })


# 单打积分更新（手动）
@bp.route("/score_update_single", methods=["POST"])
def score_update_single():
    data = request.json
    match_title = data["match_title"]
    match = Competition.query.filter_by(title=match_title).first()
    winner_name = data["winner1"]
    loser_name = data["loser1"]
    result = data["result"]
    my_id = data["my_id"]
    me = User.query.filter_by(id=my_id).first()

    if me.usertype == "K9" or me.usertype == "K10" or me.usertype == "K11":
        winner = User.query.filter_by(username=winner_name).first()
        loser = User.query.filter_by(username=loser_name).first()
        if not winner:
            return jsonify({
                "status": -1,
                "message": "胜者选手不存在"
            })
        if not loser:
            return jsonify({
                "status": -1,
                "message": "负者选手不存在"
            })
        if not result:
            return jsonify({
                "status": -1,
                "message": "请选择比分"
            })
        if winner == loser:
            return jsonify({
                "status": -1,
                "message": "比赛双方不能为同一人"
            })
        else:
            win_score_before_session = winner.score  # 这里是该场次前积分
            lose_score_before_session = loser.score
            if not match_title:
                win_score_before = win_score_before_session
                lose_score_before = lose_score_before_session
            else:
                if not match:
                    return jsonify({
                        "status": -1,
                        "message": "赛事不存在"
                    })
                if winner not in match.players or loser not in match.players:
                    return jsonify({
                        "status": -1,
                        "message": "存在未报名该赛事的选手"
                    })
                win_score_before = winner.fixed_score  # 这里是报名时积分
                lose_score_before = loser.fixed_score
            delta = math.fabs(win_score_before - lose_score_before)
            if win_score_before == 0 or lose_score_before == 0:
                return jsonify({
                    "status": -1,
                    "message": "0分选手需先定初始积分"
                })
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
                          loser_score_before=lose_score_before_session, loser_score_after=loser.score, result=result)
            else:
                log = Log(operator_id=my_id, winner_name=winner.username, winner_score_before=win_score_before_session, winner_score_after=winner.score, loser_name=loser.username,
                          loser_score_before=lose_score_before_session, loser_score_after=loser.score, match_id=match.id, result=result)
            db.session.add(log)
            db.session.commit()
            return jsonify({
                "status": 200,
                "message": "积分更新成功"
            })
    else:
        return jsonify({
            "status": -1,
            "message": "权限不足"
        })


# 双打积分更新（手动）
@bp.route("/score_update_double", methods=["POST"])
def score_update_double():
    data = request.json
    match_title = data["match_title"]
    match = Competition.query.filter_by(title=match_title).first()
    winner1_name = data["winner1"]
    winner2_name = data["winner2"]
    loser1_name = data["loser1"]
    loser2_name = data["loser2"]
    result = data["result"]
    my_id = data["my_id"]
    me = User.query.filter_by(id=my_id).first()

    if me.usertype == "K9" or me.usertype == "K10" or me.usertype == "K11":
        winner1 = User.query.filter_by(username=winner1_name).first()
        winner2 = User.query.filter_by(username=winner2_name).first()
        loser1 = User.query.filter_by(username=loser1_name).first()
        loser2 = User.query.filter_by(username=loser2_name).first()
        if not winner1:
            return jsonify({
                "status": -1,
                "message": "胜方选手1不存在"
            })
        if not winner2:
            return jsonify({
                "status": -1,
                "message": "胜方选手2不存在"
            })
        if not loser1:
            return jsonify({
                "status": -1,
                "message": "负方选手1不存在"
            })
        if not loser2:
            return jsonify({
                "status": -1,
                "message": "负方选手2不存在"
            })
        if not result:
            return jsonify({
                "status": -1,
                "message": "请选择比分"
            })
        if winner1 == winner2 or loser1 == loser2:
            return jsonify({
                "status": -1,
                "message": "双打选手不能为同一人"
            })
        if winner1 == loser1 or winner1 == loser2 or winner2 == loser1 or winner2 == loser2:
            return jsonify({
                "status": -1,
                "message": "比赛双方不能存在同一人"
            })
        else:
            winner1_score = winner1.score
            winner2_score = winner2.score
            loser1_score = loser1.score
            loser2_score = loser2.score
            if winner1_score == 0 or winner2_score == 0 or loser1_score == 0 or loser2_score == 0:
                return jsonify({
                    "status": -1,
                    "message": "0分选手需先定初始积分"
                })

            if not match_title:  # 没有绑定赛事的情况
                win_score_before = (winner1_score + winner2_score) / 2
                lose_score_before = (loser1_score + loser2_score) / 2
            else:  # 有绑定赛事的情况
                if not match:
                    return jsonify({
                        "status": -1,
                        "message": "赛事不存在"
                    })
                if winner1 not in match.players or winner2 not in match.players or loser1 not in match.players or loser2 not in match.players:
                    return jsonify({
                        "status": -1,
                        "message": "存在未报名该赛事的选手"
                    })
                win_score_before = (winner1.fixed_score + winner2.fixed_score) / 2
                lose_score_before = (loser1.fixed_score + loser2.fixed_score) / 2
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
            if not match:  # 没有绑定赛事的情况
                log = Log(operator_id=my_id, winner_name=f"{winner1_name}/{winner2_name}", winner_score_before=f"{winner1_score}/{winner2_score}",
                          winner_score_after=f"{winner1.score}/{winner2.score}",
                          loser_name=f"{loser1_name}/{loser2_name}", loser_score_before=f"{loser1_score}/{loser2_score}", loser_score_after=f"{loser1.score}/{loser2.score}", result=result)
            else:  # 有绑定赛事的情况
                log = Log(operator_id=my_id, winner_name=f"{winner1_name}/{winner2_name}", winner_score_before=f"{winner1_score}/{winner2_score}",
                          winner_score_after=f"{winner1.score}/{winner2.score}",
                          loser_name=f"{loser1_name}/{loser2_name}", loser_score_before=f"{loser1_score}/{loser2_score}", loser_score_after=f"{loser1.score}/{loser2.score}", match_id=match.id,
                          result=result)
            db.session.add(log)
            db.session.commit()
            return jsonify({
                "status": 200,
                "message": "积分更新成功"
            })
    else:
        return jsonify({
            "status": -1,
            "message": "权限不足"
        })


# 全部赛事
@bp.route("/match_list_all", methods=["POST"])
def match_list_all():
    matches = Competition.query.filter_by(visible=1).order_by(Competition.match_time.desc()).all()
    all_matches = []
    for match in matches:
        player_id_list = []
        for player in match.players:
            player_id_list.append(player.id)
        all_matches.append({
            "id": match.id,
            "title": match.title,
            "place": match.place,
            "match_time": match.match_time,
            "restriction": match.restriction,
            "description": match.description,
            "participant": match.participant,
            "players_id": player_id_list,
            "players_length": len(player_id_list),
            'match_type': match.match_type,
        })
    return jsonify({
        "status": 200,
        "message": "全部赛事获取成功",
        "matches": all_matches,
    })


# 当前赛事
@bp.route("/match_list_current", methods=["POST"])
def match_list_current():
    matches = Competition.query.filter_by(visible=1).order_by(Competition.match_time).all()
    c_matches = []
    now = datetime.datetime.now()
    for match in matches:
        if match.match_time + datetime.timedelta(hours=2) >= now:
            player_id_list = []
            for player in match.players:
                player_id_list.append(player.id)
            c_matches.append({
                "id": match.id,
                "title": match.title,
                "place": match.place,
                "match_time": match.match_time,
                "restriction": match.restriction,
                "description": match.description,
                "participant": match.participant,
                "players_id": player_id_list,
                "players_length": len(player_id_list),
                'match_type': match.match_type,
            })
    return jsonify({
        "status": 200,
        "message": "当前赛事获取成功",
        "matches": c_matches,
    })


# 历史赛事
@bp.route("/match_list_history", methods=["POST"])
def match_list_history():
    matches = Competition.query.filter_by(visible=1).order_by(Competition.match_time.desc()).all()
    h_matches = []
    now = datetime.datetime.now()
    for match in matches:
        if match.match_time + datetime.timedelta(hours=2) < now:
            player_id_list = []
            for player in match.players:
                player_id_list.append(player.id)
            h_matches.append({
                "id": match.id,
                "title": match.title,
                "place": match.place,
                "match_time": match.match_time,
                "restriction": match.restriction,
                "description": match.description,
                "participant": match.participant,
                "players_id": player_id_list,
                "players_length": len(player_id_list),
                'match_type': match.match_type,
            })
    return jsonify({
        "status": 200,
        "message": "历史赛事获取成功",
        "matches": h_matches,
    })


# 已报名赛事
@bp.route("/match_list_signed", methods=["POST"])
def match_list_signed():
    data = request.json
    my_id = data["my_id"]
    me = User.query.get(my_id)
    matches = Competition.query.filter_by(visible=1).order_by(Competition.match_time).all()
    my_matches = []
    now = datetime.datetime.now()
    for match in matches:
        if match.match_time + datetime.timedelta(hours=2) >= now:
            if me in match.players:
                player_id_list = []
                for player in match.players:
                    player_id_list.append(player.id)
                my_matches.append({
                    "id": match.id,
                    "title": match.title,
                    "place": match.place,
                    "match_time": match.match_time,
                    "restriction": match.restriction,
                    "description": match.description,
                    "participant": match.participant,
                    "players_id": player_id_list,
                    "players_length": len(player_id_list),
                    'match_type': match.match_type,
                })
    return jsonify({
        "status": 200,
        "message": "已报名赛事获取成功",
        "matches": my_matches,
    })


# 根据赛事名称查找赛事
@bp.route('/findMatchByName', methods=['POST'])
def findMatchByName():
    data = request.json
    search_match = data['search_match']
    matches = []
    if search_match == '':
        all_matches = Competition.query.order_by(Competition.match_time).all()
    else:
        all_matches = Competition.query.filter(Competition.title.contains(search_match)).all()
        match_time = operator.attrgetter('match_time')
        all_matches.sort(key=match_time)
    for match in all_matches:
        player_id_list = []
        for player in match.players:
            player_id_list.append(player.id)
        matches.append({
            "id": match.id,
            "title": match.title,
            "place": match.place,
            "match_time": match.match_time,
            "restriction": match.restriction,
            "description": match.description,
            "participant": match.participant,
            "players_id": player_id_list,
            "players_length": len(player_id_list),
            'match_type': match.match_type,
        })
    return jsonify({
        "status": 200,
        "message": "查找成功",
        "matches": matches,
    })


# 获取当前赛事
@bp.route("/get_this_match", methods=["POST"])
def get_this_match():
    data = request.json
    match_id = data['match_id']
    match = Competition.query.filter_by(id=match_id).first()
    return jsonify({
        "status": 200,
        "message": "获取该赛事成功",
        "match": match.jsonify_competition(),
    })


# 获取参赛选手
@bp.route("/get_match_players", methods=["POST"])
def get_match_players():
    data = request.json
    match = Competition.query.get(data['match_id'])
    all_players = match.players
    players = []
    for player in all_players:
        if player.organ:
            players.append({
                "id": player.id,
                "username": player.username,
                "gender": player.gender,
                "school": player.school,
                "role": player.role,
                "organname": player.organ.organname,
                "fixed_score": player.fixed_score,
                "present": player.present,
            })
        else:
            players.append({
                "id": player.id,
                "username": player.username,
                "gender": player.gender,
                "school": player.school,
                "role": player.role,
                "organname": None,
                "fixed_score": player.fixed_score,
                "present": player.present,
            })
    return jsonify({
        "status": 200,
        "message": "获取赛事选手成功",
        "players": players,
    })


# 添加参赛选手
@bp.route("/add_player", methods=["POST"])
def add_player():
    data = request.json
    my_id = data['my_id']
    me = User.query.filter_by(id=my_id).first()
    match_id = data['match_id']
    match1 = Competition.query.filter_by(id=match_id).first()
    player_username = data['player_username']
    player = User.query.filter_by(username=player_username).first()
    # team_id = data['team_id']
    # team1 = Team.query.filter_by(id=team_id).first()

    if me.usertype == "K9" or me.usertype == "K10" or me.usertype == "K11":
        if not player:
            return jsonify({
                "status": -1,
                "message": "选手不存在"
            })
        if player in match1.players:
            return jsonify({
                "status": -1,
                "message": "选手已报名该赛事"
            })
        # if match1.match_type == "男子团体" or match1.match_type == "女子团体" or match1.match_type == "混合团体":
        #     if not team1:
        #         return jsonify({
        #             "status": -1,
        #             "message": "请选择选手报名代表队"
        #         })
        #     team1.members.append(player)
        match1.players.append(player)
        player.fixed_score = player.score
        action_log = ActionLog(action=f"（管理）添加赛事『{match1.title}』参赛选手『{player_username}』", operator_id=my_id)
        db.session.add(action_log)
        db.session.commit()
        return jsonify({
            "status": 200,
            "message": "选手添加成功"
        })
    else:
        return jsonify({
            "status": -1,
            "message": "权限不足"
        })


# 移除选手（赛事选手中）
@bp.route('/remove_player', methods=['POST'])
def remove_player():
    data = request.json
    player = User.query.get(data['player_id'])
    match = Competition.query.get(data['match_id'])
    if player not in match.players:
        return jsonify({
            "status": -1,
            "message": "选手未报名该赛事"
        })
    match.players.remove(player)
    action_log = ActionLog(action=f"（管理）移除赛事『{match.title}』参赛选手『{player.username}』", operator_id=data['my_id'])
    db.session.add(action_log)
    db.session.commit()
    return jsonify({
        "status": 200,
        "message": "选手移除成功"
    })


# 获取组织
@bp.route('/fetch_organs', methods=['POST'])
def fetch_organs():
    organs = []
    all_organs = Organization.query.all()
    for organ in all_organs:
        organs.append(organ.jsonify_organization())
    return jsonify({
        "status": 200,
        "message": "获取组织成功",
        "organs": organs,
    })


# # 获取二维码
# @bp.route('/get_qrcode', methods=['POST'])
# def get_qrcode():
#     data = request.json
#     qr_data = {'赛事id': data['match_id'], '赛事名称': data['match_title'], '选手id': data['user_id'], '选手姓名': data['user_username'], '选手报名积分': data['user_fixed_score']}
#     qr_img = qrcode.make(qr_data)
#     qr_img.save('na.png')
#     return jsonify({
#         "status": 200,
#         "message": "二维码获取成功",
#     })


# 修改赛事信息
@bp.route("/modify_match_info", methods=['POST'])
def modify_match_info():
    data = request.json
    match = Competition.query.get(data['match_id'])
    if not match:
        return jsonify({
            "status": -1,
            "message": "赛事不存在"
        })
    if data['title']:
        match.title = data['title']
    if data['description']:
        match.description = data['description']
    if data['match_type']:
        match.match_type = data['match_type']
    if data['system']:
        match.system = data['system']
    if data['address']:
        match.address = data['address']
    if data['organ_id']:
        match.organ_id = data['organ_id']
    if data['place']:
        match.place = data['place']
    if data['participant']:
        try:
            float(data['participant'])
        except ValueError:
            return jsonify({
                "status": -1,
                "message": "最大参赛名额格式错误"
            })
        match.participant = data['participant']
    if data['fee']:
        try:
            float(data['fee'])
        except ValueError:
            return jsonify({
                "status": -1,
                "message": "报名费格式错误"
            })
        match.fee = data['fee']
    if data['restriction']:
        match.restriction = data['restriction']
    if data['score_min']:
        match.score_min = data['score_min']
    if data['score_max']:
        match.score_max = data['score_max']
    if data['score_min'] or data['score_max']:
        try:
            float(score_min)
            float(score_max)
        except ValueError:
            return jsonify({
                "status": -1,
                "message": "积分限制格式错误"
            })
    if data['prize_for_first']:
        match.prize_for_first = data['prize_for_first']
    if data['prize_for_second']:
        match.prize_for_second = data['prize_for_second']
    if data['prize_for_third']:
        match.prize_for_third = data['prize_for_third']
    if data['additional_info']:
        match.additional_info = data['additional_info']

    if data['match_time']:
        try:
            match_time = datetime.datetime.strptime(data['match_time'], "%Y-%m-%d %H:%M:%S")
        except ValueError:
            return jsonify({
                "status": -1,
                "message": "时间格式错误",
            })
        match.match_time = match_time
    if data['sign_start_time']:
        try:
            sign_start_time = datetime.datetime.strptime(data['sign_start_time'], "%Y-%m-%d %H:%M:%S")
        except ValueError:
            return jsonify({
                "status": -1,
                "message": "时间格式错误",
            })
        match.sign_start_time = sign_start_time
    if data['sign_end_time']:
        try:
            sign_end_time = datetime.datetime.strptime(data['sign_end_time'], "%Y-%m-%d %H:%M:%S")
        except ValueError:
            return jsonify({
                "status": -1,
                "message": "时间格式错误",
            })
        match.sign_end_time = sign_end_time
    action_log = ActionLog(action=f"（管理）更新赛事『{match.title}』赛事信息", operator_id=data['my_id'])
    db.session.add(action_log)
    db.session.commit()
    return jsonify({
        "status": 200,
        "message": "修改成功",
        "match": match.jsonify_competition(),
    })


# 隐藏赛事
@bp.route('/hide_match', methods=['POST'])
def hide_match():
    data = request.json
    match = Competition.query.get(data['match_id'])
    match.visible = 0
    action_log = ActionLog(action=f"（管理）隐藏赛事『{match.title}』", operator_id=data['my_id'])
    db.session.add(action_log)
    db.session.commit()
    return jsonify({
        "status": 200,
        "message": "隐藏成功"
    })


# 取消隐藏赛事（待办中）
@bp.route('/unhide_match', methods=['POST'])
def unhide_match():
    data = request.json
    match = Competition.query.get(data['match_id'])
    match.visible = 1
    action_log = ActionLog(action=f"（管理）取消隐藏赛事『{match.title}』", operator_id=data["my_id"])
    db.session.add(action_log)
    db.session.commit()
    return jsonify({
        "status": 200,
        "message": "取消隐藏成功"
    })


# 删除赛事（赛事详情中）
@bp.route('/delete_match', methods=['POST'])
def delete_match():
    data = request.json
    me = User.query.get(data['my_id'])
    match = Competition.query.get(data['match_id'])
    if me.usertype != "K11":
        return jsonify({
            "status": -1,
            "message": "权限不足"
        })
    action_log = ActionLog(action=f"（管理）删除赛事『{match.title}』", operator_id=data["my_id"])
    db.session.add(action_log)
    db.session.delete(match)
    db.session.commit()
    return jsonify({
        "status": 200,
        "message": "删除成功"
    })


# 取消报名（赛事详情中）
@bp.route('/quit_match', methods=['POST'])
def quit_match():
    data = request.json
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
            "message": "取消报名成功"
        })


# 报名赛事
@bp.route("/match_sign_up", methods=["POST"])
def match_sign_up():
    data = request.json
    match_id = data['match_id']
    match1 = Competition.query.filter_by(id=match_id).first()
    teams = Team.query.filter_by(match_id=match_id).all()
    user_id = data['user_id']
    user1 = User.query.filter_by(id=user_id).first()
    team_id = data['team_id']
    team1 = Team.query.filter_by(id=team_id).first()
    agree = data['agree']

    if match1.sign_end_time < datetime.datetime.now():
        return jsonify({
            "status": -1,
            "message": "该赛事已截止报名"
        })
    if match1.sign_start_time > datetime.datetime.now():
        return jsonify({
            "status": -1,
            "message": "该赛事尚未开始报名"
        })
    if match1.match_type == "男子单打" or match1.match_type == "女子单打" or match1.match_type == "混合单打":
        if len(match1.players) >= match1.participant:
            return jsonify({
                "status": -1,
                "message": "该赛事参赛名额已满"
            })
    if match1.match_type == "男子团体" or match1.match_type == "女子团体" or match1.match_type == "混合团体":
        if not team1:
            return jsonify({
                "status": -1,
                "message": "请选择报名代表队"
            })
        elif team1.member_max - len(team1.members) <= 0:
            return jsonify({
                "status": -1,
                "message": "该赛事参赛名额已满"
            })
        elif user1 not in team1.members:
            for team_x in teams:
                if team_x.match_id == match1.id:
                    if user1 in team_x.members:
                        team_x.members.remove(user1)
            team1.members.append(user1)
    if match1.restriction == "限制（仅）男子" and user1.gender != "男":
        return jsonify({
            "status": -1,
            "message": "该赛事报名限制：仅男子"
        })
    elif match1.restriction == "限制（仅）女子" and user1.gender != "女":
        return jsonify({
            "status": -1,
            "message": "该赛事报名限制：仅女子"
        })
    elif match1.restriction == "限制（仅）学生" and user1.role != "学生":
        return jsonify({
            "status": -1,
            "message": "该赛事报名限制：仅学生"
        })
    elif match1.restriction == "限制（仅）教师" and user1.role != "教师":
        return jsonify({
            "status": -1,
            "message": "该赛事报名限制：仅教师"
        })
    elif match1.restriction == "积分限制" and (user1.score < match1.score_min or user1.score > match1.score_max):
        return jsonify({
            "status": -1,
            "message": "您不符合该赛事积分限制"
        })
    else:
        # 报名成功
        if agree == "agreed":
            try:
                match1.players.append(user1)
                user1.fixed_score = user1.score
                action_log = ActionLog(action=f"报名赛事『{match1.title}』", operator_id=user_id)
                db.session.add(action_log)
                db.session.commit()
            except sqlalchemy.exc.IntegrityError:
                return jsonify({
                    "status": -1,
                    "message": "您已成功报名，无需重复操作"
                })
            else:
                return jsonify({
                    "status": 200,
                    "message": "报名成功"
                })
        else:
            return jsonify({
                "status": -1,
                "message": "请阅读并同意承诺书"
            })


# 赛事成绩录入
@bp.route("/result_record", methods=["POST"])
def result_record():
    data = request.json
    match_id = data["match_id"]
    play_x_id = data["player_x_id"]
    player_x = User.query.filter_by(id=play_x_id).first()
    play_y_id = data["player_y_id"]
    player_y = User.query.filter_by(id=play_y_id).first()
    result = data["result"]
    my_id = data["my_id"]
    me = User.query.filter_by(id=my_id).first()

    if me.usertype == "K9" or me.usertype == "K10" or me.usertype == "K11":
        if not result:
            return jsonify({
                "status": -1,
                "message": "请选择比分"
            })
        if result == "2:0" or result == "2:1" or result == "3:0" or result == "3:1" or result == "3:2" or result == "4:x":  # 注意每个or后面都要加result==
            winner = player_x
            loser = player_y
        else:
            winner = player_y
            loser = player_x
        # 计算积分
        win_score_before = winner.fixed_score  # 这里是赛前报名积分
        lose_score_before = loser.fixed_score
        win_score_before_session = winner.score  # 这里是该场次计算前的积分
        lose_score_before_session = loser.score
        delta = math.fabs(win_score_before - lose_score_before)
        if win_score_before == 0 or lose_score_before == 0:
            return jsonify({
                "status": -1,
                "message": "0分选手需先定初始积分"
            })
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
        try:
            if int(result[0]) < int(result[-1]):
                result = result[::-1]
        except ValueError:
            if result == "x:4":
                result = "4:x"
        log = Log(operator_id=my_id, match_id=match_id, winner_name=winner.username, winner_score_before=win_score_before_session, winner_score_after=winner.score,
                  loser_name=loser.username, loser_score_before=lose_score_before_session, loser_score_after=loser.score, result=result)
        db.session.add(log)
        db.session.commit()
        return jsonify({
            "user": me.jsonify_user(),
            "status": 200,
            "message": "积分计算完成 成绩录入成功"
        })
    else:
        return jsonify({
            "status": -1,
            "message": "权限不足"
        })


@bp.route("/match_result", methods=["POST"])
def match_result():
    data = request.json
    match_id = data["match_id"]
    all_results = Log.query.filter_by(match_id=match_id).all()
    results = []
    for result in all_results:
        results.append(result.jsonify_score_log())
    return jsonify({
        "status": 200,
        "message": "赛事成绩获取成功",
        "results": results,
    })


# 进入代表队管理
@bp.route("/get_teams", methods=["POST"])
def get_teams():
    teams = Team.query.order_by(Team.score.desc()).all()
    team_length = len(teams)
    all_teams = []
    for team in teams:
        all_teams.append(team.jsonify_team())
        # 计算每队的代表队积分
        team_members = team.members
        member_score = operator.attrgetter("score")
        team_members.sort(key=member_score, reverse=True)
        if len(team_members) == 0:
            team.score = 0
            db.session.commit()
        elif len(team_members) >= 4:
            ave_score1 = (team_members[0].score + team_members[1].score + team_members[2].score) / 3
            score2 = 0
            for i in range(3, len(team_members)):
                score2 += team_members[i].score
            ave_score2 = score2 / (len(team_members) - 3)
            team.score = format(ave_score1 * 0.6 + ave_score2 * 0.4, '.1f')
            db.session.commit()
        else:
            score1 = 0
            for i in range(len(team_members)):
                score1 += team_members[i].score
            team.score = format(score1 / (len(team_members)), ".1f")
            db.session.commit()
    return jsonify({
        "status": 200,
        "message": "代表队获取成功",
        "team_length": team_length,
        "teams": all_teams,
    })


# 查找代表队
@bp.route('/findTeamByName', methods=['POST'])
def findTeamByName():
    data = request.json
    search_team = data['search_team']
    teams = []
    if search_team == '':
        all_teams = Team.query.order_by(Team.score.desc()).all()
    else:
        all_teams = Team.query.filter(Team.teamname.contains(search_team)).all()
        scores = operator.attrgetter('score')
        all_teams.sort(key=scores, reverse=True)  # operator库，对teams里的score属性逆序排序
    for team in all_teams:
        teams.append(team.jsonify_team())
    return jsonify({
        "status": 200,
        "message": "查找成功",
        "teams": teams,
        "team_length": len(teams),
    })


# 添加参赛代表队
@bp.route("/add_team", methods=["POST"])
def add_team():
    data = request.json
    my_id = data["my_id"]
    me = User.query.get(my_id)
    teamname = data["teamname"]
    description = data["description"]
    member_max = data["member_max"]
    match = Competition.query.filter_by(title=data["match_title"]).first()
    team_exist = Team.query.filter_by(teamname=teamname).first()
    if me.usertype == "K9" or me.usertype == "K10" or me.usertype == "K11":
        if not teamname:
            return jsonify({
                "status": -1,
                "message": "请输入队名",
            })
        try:
            int(member_max)
        except ValueError:
            return jsonify({
                "status": -1,
                "message": "队员人数上限输入有误",
            })
        if int(member_max) < 0:
            return jsonify({
                "status": -1,
                "message": "队员人数上限输入有误",
            })
        if data["match_title"] and not match:
            return jsonify({
                "status": -1,
                "message": "绑定赛事不存在",
            })
        if match and (match.match_type != "男子团体" and match.match_type != "女子团体" and match.match_type != "混合团体"):
            return jsonify({
                "status": -1,
                "message": "绑定赛事不是团体比赛",
            })
        if team_exist:
            return jsonify({
                "status": -1,
                "message": "该代表队已存在",
            })
        if match:
            team = Team(teamname=teamname, description=description, member_max=int(member_max), match_id=match.id)
        else:
            team = Team(teamname=teamname, description=description, member_max=int(member_max))
        db.session.add(team)
        action_log = ActionLog(action=f"（管理）添加代表队『{teamname}』", operator_id=my_id)
        db.session.add(action_log)
        db.session.commit()
        return jsonify({
            "status": 200,
            "message": "代表队添加成功",
        })
    else:
        return jsonify({
            "status": -1,
            "message": "权限不足",
        })


# 变更代表队人数上限
@bp.route("/modify_member_max", methods=['POST'])
def modify_member_max():
    data = request.json
    team = Team.query.get(data['team_id'])
    try:
        int(data["member_max"])
    except ValueError:
        return jsonify({
            "status": -1,
            "message": "人数上限输入有误"
        })
    if int(data["member_max"]) < 0:
        return jsonify({
            "status": -1,
            "message": "人数上限输入有误"
        })
    team.member_max = int(data["member_max"])
    action_log = ActionLog(action=f"（管理）变更代表队『{team.teamname}』人数上限", operator_id=data["my_id"])
    db.session.add(action_log)
    db.session.commit()
    return jsonify({
        "status": 200,
        "message": "变更成功"
    })


# 变更代表队绑定赛事
@bp.route("/modify_match", methods=['POST'])
def modify_match():
    data = request.json
    team = Team.query.get(data['team_id'])
    match = Competition.query.filter_by(title=data["match_title"]).first()
    if data["match_title"] and not match:
        return jsonify({
            "status": -1,
            "message": "绑定赛事不存在",
        })
    if match and (match.match_type != "男子团体" and match.match_type != "女子团体" and match.match_type != "混合团体"):
        return jsonify({
            "status": -1,
            "message": "绑定赛事不是团体比赛",
        })
    if match:
        team.match_id = match.id
    else:
        team.match_id = None
    action_log = ActionLog(action=f"（管理）变更代表队『{team.teamname}』绑定赛事", operator_id=data["my_id"])
    db.session.add(action_log)
    db.session.commit()
    return jsonify({
        "status": 200,
        "message": "变更成功"
    })


# 删除代表队
@bp.route('/delete_team', methods=['POST'])
def delete_team():
    data = request.json
    me = User.query.get(data["my_id"])
    team = Team.query.get(data['team_id'])
    if me.usertype != "K11":
        return jsonify({
            "status": -1,
            "message": "权限不足"
        })
    action_log = ActionLog(action=f"（管理）删除代表队『{team.teamname}』", operator_id=data['my_id'])
    db.session.add(action_log)
    db.session.delete(team)
    db.session.commit()
    return jsonify({
        "status": 200,
        "message": "删除成功"
    })


# 获取当前代表队
@bp.route("/get_this_team", methods=["POST"])
def get_this_team():
    data = request.json
    team_id = data['team_id']
    team = Team.query.get(team_id)
    return jsonify({
        "status": 200,
        "message": "代表队获取成功",
        "team": team.jsonify_team(),
    })


# 添加代表队队员
@bp.route("/add_member", methods=["POST"])
def add_member():
    data = request.json
    me = User.query.get(data['my_id'])
    team = Team.query.get(data['team_id'])
    member = User.query.filter_by(username=data['member_name']).first()
    if me.usertype == "K9" or me.usertype == "K10" or me.usertype == "K11":
        if not member:
            return jsonify({
                "status": -1,
                "message": "该队员不存在",
            })
        if member in team.members:
            return jsonify({
                "status": -1,
                "message": "该队员已在队内",
            })
        # other_teams = Team.query.filter_by(match_id=team.match_id).all()
        # for other_team in other_teams:
        #     if member in other_team.members:
        #         other_team.members.remove(member)
        #         flash("该队员原在其他代表队，已移入该代表队")
        team.members.append(member)
        action_log = ActionLog(action=f"（管理）添加代表队『{team.teamname}』队员『{member.username}』", operator_id=me.id)
        db.session.add(action_log)
        db.session.commit()
        return jsonify({
            "status": 200,
            "message": "队员添加成功",
        })
    else:
        return jsonify({
            "status": -1,
            "message": "权限不足",
        })


# 移除代表队队员
@bp.route('/remove_member', methods=['POST'])
def remove_member():
    data = request.json
    member = User.query.get(data['member_id'])
    team = Team.query.get(data['team_id'])
    action_log = ActionLog(action=f"（管理）移除代表队『{team.teamname}』队员『{member.username}』", operator_id=data['my_id'])
    db.session.add(action_log)
    team.members.remove(member)
    db.session.commit()
    return jsonify({
        "status": 200,
        "message": "移除成功"
    })


# 根据绑定赛事查找代表队（代表队管理中）
@bp.route("/filter_team")
# @login_required
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
            matches.append(match)  # matches为现在之后全部团体赛
    return render_template("info/team-management.html", teams=teams, all_matches=all_matches, matches=matches)


# 举办赛事
@bp.route("/hold_match", methods=['POST'])
def hold_match():
    data = request.json
    my_id = data['my_id']
    title = data['title']
    description = data['description']
    match_type = data['match_type']
    system = data['system']
    address = data['address']
    organ_id = data['organ_id']
    match_time = data['match_time']
    place = data['place']
    sign_start_time = data['sign_start_time']
    sign_end_time = data['sign_end_time']
    participant = data['participant']
    fee = data['fee']
    restriction = data['restriction']
    prize_for_first = data['prize_for_first']
    prize_for_second = data['prize_for_second']
    prize_for_third = data['prize_for_third']
    additional_info = data['additional_info']
    score_min = data['score_min']
    score_max = data['score_max']

    me = User.query.get(data['my_id'])
    if me.usertype == "K9" or me.usertype == "K10" or me.usertype == "K11":
        if not title or not address or not place or not participant or not fee or not match_type or not system or not organ_id or not sign_start_time or not sign_end_time or not match_time:
            return jsonify({
                "status": -1,
                "message": "信息输入不完整"
            })
        if participant:
            try:
                float(participant)
            except ValueError:
                return jsonify({
                    "status": -1,
                    "message": "最大参赛名额格式错误"
                })
        if fee:
            try:
                float(fee)
            except ValueError:
                return jsonify({
                    "status": -1,
                    "message": "报名费格式错误"
                })
        if score_min or score_max:
            try:
                float(score_min)
                float(score_max)
            except ValueError:
                return jsonify({
                    "status": -1,
                    "message": "积分限制格式错误"
                })
        try:
            match_time = datetime.datetime.strptime(match_time, "%Y-%m-%d %H:%M:%S")
            sign_start_time = datetime.datetime.strptime(sign_start_time, "%Y-%m-%d %H:%M:%S")
            sign_end_time = datetime.datetime.strptime(sign_end_time, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            return jsonify({
                "status": -1,
                "message": "时间格式错误"
            })
        if sign_start_time > sign_end_time:
            return jsonify({
                "status": -1,
                "message": "报名开始时间早于报名截止时间"
            })
        if match_time < sign_end_time:
            return jsonify({
                "status": -1,
                "message": "比赛时间晚于报名截止时间"
            })
        else:
            seasons = Season.query.all()
            season_id = None
            for season in seasons:
                if season.start_time <= match_time <= season.end_time:
                    season_id = season.id
                    break
            if not season_id:
                return jsonify({
                    "status": -1,
                    "message": "比赛须在本赛季进行"
                })

            if restriction == "积分限制":
                if score_max <= score_min:
                    return jsonify({
                        "status": -1,
                        "message": "最高限制积分需大于最低限制积分"
                    })
                match = Competition(title=title, description=description, match_type=match_type, address=address, organ_id=organ_id, match_time=match_time, sign_start_time=sign_start_time,
                                    sign_end_time=sign_end_time, place=place,
                                    participant=participant, fee=fee, system=system, season_id=season_id,
                                    prize_for_first=prize_for_first, prize_for_second=prize_for_second, prize_for_third=prize_for_third, additional_info=additional_info,
                                    restriction=restriction, score_min=score_min, score_max=score_max, visible=1)
            else:
                match = Competition(title=title, description=description, match_type=match_type, address=address, organ_id=organ_id, match_time=match_time, sign_start_time=sign_start_time,
                                    sign_end_time=sign_end_time, place=place, participant=participant, season_id=season_id,
                                    prize_for_first=prize_for_first, prize_for_second=prize_for_second, prize_for_third=prize_for_third, additional_info=additional_info,
                                    fee=fee, system=system, restriction=restriction, visible=1)
            db.session.add(match)
            action_log = ActionLog(action=f"（管理）举办赛事『{title}』", operator_id=my_id)
            db.session.add(action_log)
            db.session.commit()
            return jsonify({
                "status": 200,
                "message": "赛事举办成功"
            })
    else:
        return jsonify({
            "status": -1,
            "message": "权限不足"
        })


# 选手签到
@bp.route('/player_sign_in', methods=['POST'])
def player_sign_in():
    data = request.json
    qr_content = data['qr_content']
    content_lines = qr_content.splitlines()
    if content_lines[0] == "Player's QRcode":
        try:
            int(content_lines[1])
            int(content_lines[2])
            int(content_lines[3])
        except ValueError:
            return jsonify({
                "status": -1,
                "message": "选手身份无效"
            })
        match = Competition.query.get(int(content_lines[1]))
        player = User.query.get(int(content_lines[2]))
        if (match.match_time - datetime.datetime.now() > datetime.timedelta(minutes=15)) or (datetime.datetime.now() - match.match_time > datetime.timedelta(hours=2)):
            return jsonify({
                "status": -1,
                "message": "本场比赛在该时间段无法签到，请在赛前15分钟至比赛开始后2小时内进行签到"
            })
        if player in match.players and player.fixed_score == int(content_lines[3]):
            player.present = 1
            action_log = ActionLog(action=f"（管理）选手『{player.username}』签到赛事『{match.title}』", operator_id=data['my_id'])
            db.session.add(action_log)
            db.session.commit()
            return jsonify({
                "status": 200,
                "message": "选手签到成功"
            })
        else:
            return jsonify({
                "status": -1,
                "message": "选手身份无效"
            })
    else:
        return jsonify({
            "status": -1,
            "message": "二维码无效"
        })


# 全体退签
@bp.route('/reset_present', methods=['POST'])
def reset_present():
    data = request.json
    me = User.query.get(data['my_id'])
    match = Competition.query.get(data['match_id'])
    if me.usertype == "K9" or me.usertype == "K10" or me.usertype == "K11":
        for player in match.players:
            player.present = 0
        action_log = ActionLog(action=f"（管理）退签赛事『{match.title}』选手", operator_id=data['my_id'])
        db.session.add(action_log)
        db.session.commit()
        return jsonify({
            "status": 200,
            "message": "全体退签成功"
        })
    else:
        return jsonify({
            "status": -1,
            "message": "权限不足"
        })


# 选手签到/退签
@bp.route('/player_sign_or_unsign', methods=['POST'])
def player_sign_or_unsign():
    data = request.json
    me = User.query.get(data['my_id'])
    player = User.query.get(data['player_id'])
    if me.usertype == "K9" or me.usertype == "K10" or me.usertype == "K11":
        if player.present == 0:
            player.present = 1
            action_log = ActionLog(action=f"（管理）选手『{player.username}』签到赛事『{data['match_title']}』", operator_id=data['my_id'])
            db.session.add(action_log)
            db.session.commit()
            return jsonify({
                "status": 200,
                "message": "签到成功"
            })
        else:
            player.present = 0
            action_log = ActionLog(action=f"（管理）选手『{player.username}』退签赛事『{data['match_title']}』", operator_id=data['my_id'])
            db.session.add(action_log)
            db.session.commit()
            return jsonify({
                "status": 200,
                "message": "退签成功"
            })
    else:
        return jsonify({
            "status": -1,
            "message": "权限不足"
        })
