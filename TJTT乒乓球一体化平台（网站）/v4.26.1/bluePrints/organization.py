from flask import Blueprint, request, redirect, url_for, session, render_template, g, jsonify
from models import Organization, ActionLog
from exts import db
from bluePrints.form import Registration, LoginForm, Login_viaphForm
from decorators import login_required

bp = Blueprint("organization", __name__, url_prefix="/organization")


# 进入组织管理
@bp.route("/organ_list")
@login_required
def organ_list():
    organs = Organization.query.order_by(-Organization.id.desc()).all()
    return render_template("info/organ-list.html", organs=organs)


# 删除组织
@bp.route('/delete_organ', methods=['GET', 'POST'])
def delete_organ():
    if request.method == 'GET':
        return jsonify({
            "status": -1,
            "message": "请求方式错误！"
        })
    else:
        data = request.get_json()
        organ = Organization.query.get(data['id'])
        if not organ:
            return jsonify({
                "status": -1,
                "message": "组织不存在!"
            })
        else:
            action_log = ActionLog(action=f"（管理）删除组织『{organ.organname}』", operator_id=data['my_id'])
            db.session.add(action_log)
            db.session.delete(organ)
            db.session.commit()
            return jsonify({
                "status": 200,
                "message": "删除成功！"
            })


# 添加组织（从系统内）
@bp.route("/insert_organ", methods=['GET', 'POST'])
def insert_organ():
    if request.method == 'GET':
        return render_template("info/organ-insert.html")
    else:
        data = request.get_json()
        organname = data['organname']
        description = data['description']
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
    data = request.get_json()
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


# 根据组织名查找组织
@bp.route('/findOrganByName/<keywords>')
def findOrganByName(keywords):
    if keywords == '':
        organs = Organization.query.all()
    else:
        organs = Organization.query.filter(Organization.organname.contains(keywords)).all()
    return render_template("info/organ-list.html", organs=organs)


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


@login_required
@bp.route("/icon_simple_lineicon")
@login_required
def icon_simple_lineicon():
    return render_template("info/icon-simple-lineicon.html")
