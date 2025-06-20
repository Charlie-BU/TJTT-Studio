from flask import Blueprint, request, redirect, url_for, session, render_template, g, jsonify
from models import Organization, ActionLog, User
from exts import db
from decorators import login_required

bp = Blueprint("organization", __name__, url_prefix="/organization")


# 获取组织信息
@bp.route("/get_info", methods=["POST"])
def get_info():
    all_organs = Organization.query.all()
    TTTA = Organization.query.filter_by(organname="同济大学乒乓球协会").first()
    organ_length = len(all_organs)
    tongji_organs = []
    for organ in all_organs:
        if "同济" in organ.organname:
            tongji_organs.append(organ)
    tongji_length = len(tongji_organs)
    return jsonify({
        "status": 200,
        "message": "信息获取成功！",
        "organ_length": organ_length,
        "tongji_length": tongji_length,
        "TTTA_members": len(TTTA.users)
    })


# 获取所有组织
@bp.route("/get_organs", methods=["POST"])
def get_organs():
    all_organs = Organization.query.all()
    organs = []
    for organ in all_organs:
        organs.append({
            "id": organ.id,
            "organname": organ.organname,
            "description": organ.description,
            "member_length": len(organ.users),
        })
    return jsonify({
        "status": 200,
        "message": "组织获取成功！",
        "organs": organs,
    })


# 删除组织
@bp.route('/delete_organ', methods=['POST'])
def delete_organ():
    data = request.json
    organ = Organization.query.get(data['organ_id'])
    me = User.query.get(data['my_id'])
    if me.usertype != "K11":
        return jsonify({
            "status": -1,
            "message": "权限不足!"
        })
    if not organ:
        return jsonify({
            "status": -1,
            "message": "组织不存在!"
        })
    action_log = ActionLog(action=f"（管理）删除组织『{organ.organname}』", operator_id=data['my_id'])
    db.session.add(action_log)
    db.session.delete(organ)
    db.session.commit()
    return jsonify({
        "status": 200,
        "message": "删除成功！"
    })


# 根据组织名查找组织
@bp.route('/findOrganByName', methods=['POST'])
def findOrganByName():
    data = request.json
    search_organ = data['search_organ']
    organs = []
    if search_organ == '':
        all_organs = Organization.query.all()
    else:
        all_organs = Organization.query.filter(Organization.organname.contains(search_organ)).all()
    for organ in all_organs:
        organs.append({
            "id": organ.id,
            "organname": organ.organname,
            "description": organ.description,
        })
    return jsonify({
        "status": 200,
        "message": "查找成功！",
        "organs": organs,
    })


# 添加组织
@bp.route("/add_organ", methods=['POST'])
def add_organ():
    data = request.json
    organname = data['organname']
    description = data['description']
    if not organname or not description:
        return jsonify({
            "status": -1,
            "message": "信息输入不完整！"
        })
    organ = Organization(organname=organname, description=description)
    db.session.add(organ)
    action_log = ActionLog(action=f"（管理）添加组织『{organname}』", operator_id=data["my_id"])
    db.session.add(action_log)
    db.session.commit()
    return jsonify({
        "status": 200,
        "message": "添加成功！"
    })


# 更新组织
@bp.route("/update_organ", methods=['POST'])
def update_organ():
    data = request.json
    organ_id = data['id']
    organ = Organization.query.get(organ_id)
    if not organ:
        return jsonify({
            "status": -1,
            "message": "组织不存在！"
        })
    organ.organname = data['organname']
    organ.description = data['description']
    action_log = ActionLog(action=f"（管理）更新组织『{data['organname']}』组织信息", operator_id=data['my_id'])
    db.session.add(action_log)
    db.session.commit()
    return jsonify({
        "status": 200,
        "message": "修改成功！"
    })
