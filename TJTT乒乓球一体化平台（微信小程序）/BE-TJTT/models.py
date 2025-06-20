from exts import db
from datetime import datetime
from flask import jsonify

# 要实现多对多表，需要中间表
user_competition_table = db.Table("user_competition_table",
                                  db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                                  db.Column('competition_id', db.Integer, db.ForeignKey('competition.id'),
                                            primary_key=True))

user_team_table = db.Table("user_team_table",
                           db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                           db.Column('team_id', db.Integer, db.ForeignKey('team.id'), primary_key=True))

user_post_table = db.Table("user_post_table",
                           db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                           db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True))


class User(db.Model):
    # 数据库表名
    __tablename__ = 'user'
    # 用户id
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 微信openid
    openid = db.Column(db.String(255), nullable=True)
    # 姓名
    username = db.Column(db.String(100), nullable=False)
    # 密码
    password = db.Column(db.String(100), nullable=False)
    # 学校
    school = db.Column(db.String(255), nullable=True)
    # 手机号
    phone = db.Column(db.String(16), nullable=True)
    # 邮箱
    email = db.Column(db.String(100), nullable=True)
    # 学号
    stu_num = db.Column(db.String(16), nullable=True)
    # 用户类别
    usertype = db.Column(db.String(10), nullable=False)
    # 积分
    score = db.Column(db.Integer, nullable=True)
    # 活跃度
    active = db.Column(db.Float, nullable=True)
    # 注册时间
    join_time = db.Column(db.DateTime, default=datetime.now)
    # 性别
    gender = db.Column(db.String(10), nullable=True)
    # 身份（教师/学生）
    role = db.Column(db.String(20), nullable=True)
    # 执拍手
    hand = db.Column(db.String(20), nullable=True)
    # 握拍方式
    grip = db.Column(db.String(10), nullable=True)
    # 底板型号
    blade = db.Column(db.String(100), nullable=True)
    # 正手胶皮
    forehand = db.Column(db.String(100), nullable=True)
    # 反手胶皮
    backhand = db.Column(db.String(100), nullable=True)
    # 是否带颗粒：是、否
    particle = db.Column(db.String(10), nullable=True)
    # 地区
    address = db.Column(db.String(120), nullable=True)
    # 报名积分（报名时确定）
    fixed_score = db.Column(db.Integer, nullable=True)
    # 隐私设置
    privacy = db.Column(db.String(10), nullable=True)
    # 是否到场
    present = db.Column(db.Integer, nullable=True)
    # 是否为TJTT Studio成员
    is_TJTT = db.Column(db.Integer, nullable=True)
    # 头像
    profile_img = db.Column(db.Text, nullable=True)

    # 外键
    # 所在组织
    organ_id = db.Column(db.Integer, db.ForeignKey('organization.id'))
    organ = db.relationship('Organization', backref="users")  # backref会自动给Organization表加一个users的属性，来获取每个organ_id对应的所有users，返回的是列表
    # 所用球台
    table_id = db.Column(db.Integer, db.ForeignKey('table.id'))
    table = db.relationship('Table', backref="players")
    # 参加的所有比赛
    matches = db.relationship("Competition", secondary=user_competition_table, back_populates="players")
    # 团体比赛代表队
    teams = db.relationship("Team", secondary=user_team_table, back_populates="members")
    # 约球帖
    posts = db.relationship("Post", secondary=user_post_table, back_populates="couple")

    def jsonify_user(self):
        organ = {}
        if self.organ:
            organ['id'] = self.organ.id
            organ['organname'] = self.organ.organname
            organ['description'] = self.organ.description
        return {
            'id': self.id,
            'username': self.username,
            'school': self.school,
            'phone': self.phone,
            'email': self.email,
            'stu_num': self.stu_num,
            'usertype': self.usertype,
            'score': self.score,
            'active': self.active,
            'join_time': self.join_time,
            'gender': self.gender,
            'role': self.role,
            'hand': self.hand,
            'grip': self.grip,
            'blade': self.blade,
            'forehand': self.forehand,
            'backhand': self.backhand,
            'particle': self.particle,
            'address': self.address,
            'fixed_score': self.fixed_score,
            'privacy': self.privacy,
            'present': self.present,
            'is_TJTT': self.is_TJTT,
            'profile_img': self.profile_img,
            'organ_id': self.organ_id,
            'organ': organ,
            'openid': self.openid,
        }


class Organization(db.Model):
    __tablename__ = 'organization'
    # 组织id
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 组织名称
    organname = db.Column(db.String(40), nullable=False)
    # 组织描述
    description = db.Column(db.Text, nullable=True)

    def jsonify_organization(self):
        user_list = []
        for user in self.users:
            user_list.append({
                "id": user.id,
                "username": user.username,
                "gender": user.gender,
                "role": user.role,
                "score": user.score})
        return {
            'id': self.id,
            'organname': self.organname,
            'description': self.description,
            'users': user_list,
        }


class Competition(db.Model):
    __tablename__ = 'competition'
    # 赛事id
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 赛事名称
    title = db.Column(db.String(100), nullable=False)
    # 赛事简介
    description = db.Column(db.Text, nullable=True)
    # 赛事类型
    match_type = db.Column(db.String(20), nullable=True)
    # 所在地区
    address = db.Column(db.String(120), nullable=True)
    # 比赛时间
    match_time = db.Column(db.DateTime, nullable=True)
    # 报名开始时间
    sign_start_time = db.Column(db.DateTime, nullable=True)
    # 报名截止时间
    sign_end_time = db.Column(db.DateTime, nullable=True)
    # 地点
    place = db.Column(db.String(100), nullable=False)
    # 最大参赛名额
    participant = db.Column(db.Integer, nullable=True)
    # 报名费
    fee = db.Column(db.Integer, nullable=True)
    # 赛制
    system = db.Column(db.String(30), nullable=False)
    # 冠军奖品
    prize_for_first = db.Column(db.String(30), nullable=True)
    # 亚军奖品
    prize_for_second = db.Column(db.String(30), nullable=True)
    # 季军奖品
    prize_for_third = db.Column(db.String(30), nullable=True)
    # 备注
    additional_info = db.Column(db.Text, nullable=True)
    # 选手报名限制
    restriction = db.Column(db.String(100), nullable=True)
    # 最低限制积分
    score_min = db.Column(db.Integer, nullable=True)
    # 最高限制积分
    score_max = db.Column(db.Integer, nullable=True)
    # 是否可见
    visible = db.Column(db.Integer, nullable=True)

    # 外键
    # 参赛选手（单元性）
    players = db.relationship("User", secondary="user_competition_table", back_populates="matches")
    # 主办方
    organ_id = db.Column(db.Integer, db.ForeignKey('organization.id'))
    organ = db.relationship('Organization',
                            backref="matches")  # backref会自动给Organization表加一个matches的属性，来获取每个organ_id对应的所有matches，返回的是列表
    # 赛季
    season_id = db.Column(db.Integer, db.ForeignKey('season.id'))
    season = db.relationship('Season', backref="matches")

    def jsonify_competition(self):
        player_list = []
        for player in self.players:
            player_list.append(player.jsonify_user())
        player_id_list = []
        for player in self.players:
            player_id_list.append(player.id)
        team_list = []
        for team in self.teams:
            team_list.append({
                "id": team.id,
                "teamname": team.teamname,
                "description": team.description,
                "member_max": team.member_max,
                "score": team.score})
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'match_type': self.match_type,
            'address': self.address,
            'match_time': self.match_time,
            'sign_start_time': self.sign_start_time,
            'sign_end_time': self.sign_end_time,
            'place': self.place,
            'participant': self.participant,
            'fee': self.fee,
            'system': self.system,
            'prize_for_first': self.prize_for_first,
            'prize_for_second': self.prize_for_second,
            'prize_for_third': self.prize_for_third,
            'additional_info': self.additional_info,
            'restriction': self.restriction,
            'score_min': self.score_min,
            'score_max': self.score_max,
            'visible': self.visible,
            'organ_id': self.organ_id,
            'season_id': self.season_id,
            'teams_length': len(team_list),
            'players_length': len(player_list),
            # 一对一外键
            'organ': self.organ.jsonify_organization(),
            'season': self.season.jsonify_season(),
            # 一对多外键
            'players': player_list,
            'players_id': player_id_list,
            'teams': team_list,
        }


# 团体比赛代表队
class Team(db.Model):
    __tablename__ = 'team'
    # 代表队id
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 队名
    teamname = db.Column(db.String(100), nullable=False)
    # 简介
    description = db.Column(db.Text, nullable=True)
    # 队员
    members = db.relationship("User", secondary="user_team_table", back_populates="teams")
    # 队员人数上限
    member_max = db.Column(db.Integer, nullable=True)
    # 关联比赛
    match_id = db.Column(db.Integer, db.ForeignKey('competition.id'))
    match = db.relationship("Competition", backref="teams")
    # 代表队积分
    score = db.Column(db.Integer, nullable=True)

    def jsonify_team(self):
        member_list = []
        for member in self.members:
            member_list.append(member.jsonify_user())
        if not self.match:
            return {
                'id': self.id,
                'teamname': self.teamname,
                'description': self.description,
                'members': member_list,
                'member_max': self.member_max,
                'match_id': self.match_id,
                'match_title': None,
                'score': self.score,
            }
        return {
            'id': self.id,
            'teamname': self.teamname,
            'description': self.description,
            'members': member_list,
            'member_max': self.member_max,
            'match_id': self.match_id,
            'match_title': self.match.title,
            'score': self.score,
        }


# 通知公告
class Notice(db.Model):
    __tablename__ = 'notice'
    # id
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 标题
    title = db.Column(db.String(100), nullable=True)
    # 内容
    content = db.Column(db.Text, nullable=True)
    # 发布时间
    time = db.Column(db.DateTime, default=datetime.now)
    # 是否显示
    released = db.Column(db.Integer, nullable=True)
    # 发布人
    announcer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    announcer = db.relationship("User", backref="notices")

    def jsonify_notice(self):
        if not self.announcer:
            return {
                'id': self.id,
                'title': self.title,
                'content': self.content,
                'time': self.time,
                'released': self.released,
                'announcer_id': self.announcer_id,
                'announcer': None,
            }
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'time': self.time,
            'released': self.released,
            'announcer_id': self.announcer_id,
            'announcer_name': self.announcer.username,
        }


# 积分变动日志
class Log(db.Model):
    __tablename__ = 'log'
    # 日志id
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 变动时间
    time = db.Column(db.DateTime, default=datetime.now)
    # 外键：操作者
    operator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    operator = db.relationship('User', backref="logs")
    # 外键：关联赛事
    match_id = db.Column(db.Integer, db.ForeignKey('competition.id'))
    match = db.relationship("Competition", backref="logs")
    # 比分
    result = db.Column(db.String(100), nullable=True)
    # 胜者姓名（积分加）
    winner_name = db.Column(db.String(100), nullable=True)
    # 胜者原积分
    winner_score_before = db.Column(db.String(20), nullable=True)
    # 胜者结算积分
    winner_score_after = db.Column(db.String(20), nullable=True)
    # 负者姓名（积分减）
    loser_name = db.Column(db.String(100), nullable=True)
    # 负者原积分
    loser_score_before = db.Column(db.String(20), nullable=True)
    # 负者结算积分
    loser_score_after = db.Column(db.String(20), nullable=True)

    def jsonify_score_log(self):
        if not self.match:
            return {
                'id': self.id,
                'time': self.time,
                'operator_id': self.operator_id,
                'operator_name': self.operator.username,
                'match_id': self.match_id,
                'match_title': None,
                'winner_name': self.winner_name,
                'winner_score_before': self.winner_score_before,
                'winner_score_after': self.winner_score_after,
                'loser_name': self.loser_name,
                'loser_score_before': self.loser_score_before,
                'loser_score_after': self.loser_score_after,
            }
        return {
            'id': self.id,
            'time': self.time,
            'operator_id': self.operator_id,
            'operator_name': self.operator.username,
            'match_id': self.match_id,
            'match_title': self.match.title,
            'result': self.result,
            'winner_name': self.winner_name,
            'winner_score_before': self.winner_score_before,
            'winner_score_after': self.winner_score_after,
            'loser_name': self.loser_name,
            'loser_score_before': self.loser_score_before,
            'loser_score_after': self.loser_score_after,
        }


# Q&A
class Ques_and_answer(db.Model):
    __tablename__ = 'ques_and_answer'
    # id
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 问题
    question = db.Column(db.Text, nullable=False)
    # 回答
    answer = db.Column(db.Text, nullable=True)
    # 提问时间
    time = db.Column(db.DateTime, default=datetime.now)
    # 外键：提问者
    person_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    person = db.relationship('User', backref="questions")

    def jsonify_QA(self):
        if not self.person:
            return {
                'id': self.id,
                'question': self.question,
                'answer': self.answer,
                'time': self.time,
                'person_id': self.person_id,
                'person': None,
            }
        return {
            'id': self.id,
            'question': self.question,
            'answer': self.answer,
            'time': self.time,
            'person_id': self.person_id,
            'person_name': self.person.username,
        }


# 邮箱验证码
class EmailCaptcha(db.Model):
    __tablename__ = 'email_captcha'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False)
    captcha = db.Column(db.String(100), nullable=False)

    def jsonify_email_captcha(self):
        return {
            'id': self.id,
            'email': self.email,
            'captcha': self.captcha,
        }


# 约球帖
class Post(db.Model):
    __tablename__ = 'post'
    # id
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 发帖时间
    post_time = db.Column(db.DateTime, default=datetime.now)
    # 约球时间
    play_time = db.Column(db.DateTime, nullable=True)
    # 介绍
    description = db.Column(db.Text, nullable=True)
    # 地点
    place = db.Column(db.Text, nullable=True)
    # 球台
    table_vacant = db.Column(db.String(50), nullable=True)
    # 发帖人和受帖人
    couple = db.relationship('User', secondary=user_post_table, back_populates="posts")

    def jsonify_post(self):
        couple_list = []
        for single in self.couple:
            couple_list.append(single.jsonify_user())
        return {
            'id': self.id,
            'post_time': self.post_time,
            'play_time': self.play_time,
            'description': self.description,
            'place': self.place,
            'table_vacant': self.table_vacant,
            'couple': couple_list,
        }


# 赛季
class Season(db.Model):
    __tablename__ = 'season'
    # 赛季id
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 赛季名
    season_name = db.Column(db.String(20), nullable=False)
    # 徽章
    badge_url = db.Column(db.Text, nullable=True)
    # 赛季介绍
    description = db.Column(db.Text, nullable=True)
    # 赛季开始时间
    start_time = db.Column(db.DateTime, nullable=True)
    # 赛季结束时间
    end_time = db.Column(db.DateTime, nullable=True)

    def jsonify_season(self):
        return {
            'id': self.id,
            'season_name': self.season_name,
            'badge_url': self.badge_url,
            'description': self.description,
            'start_time': self.start_time,
            'end_time': self.end_time,
        }


# TJTT Studio成员
class TJTTer(db.Model):
    __tablename__ = 'TJTTer'
    # 成员id（与user_id保持一致）
    id = db.Column(db.Integer, primary_key=True)
    # 姓名
    name = db.Column(db.String(100), nullable=False)
    # 职能部
    department = db.Column(db.String(20), nullable=True)
    # 职务
    job = db.Column(db.String(20), nullable=True)
    # 成员属性
    property = db.Column(db.String(20), nullable=True)
    # 简介
    description = db.Column(db.Text, nullable=True)
    # 头像url
    avatar_url = db.Column(db.Text, nullable=True)

    def jsonify_TJTTer(self):
        return {
            'id': self.id,
            'name': self.name,
            'department': self.department,
            'job': self.job,
            'property': self.property,
            'description': self.description,
            'avatar_url': self.avatar_url,
        }


# 名言金句
class Motto(db.Model):
    __tablename__ = 'motto'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100), nullable=True)

    def jsonify_motto(self):
        return {
            'id': self.id,
            'content': self.content,
            'author': self.author,
        }


# 乒乓球运动员
class Athlete(db.Model):
    __tablename__ = 'athlete'
    # id
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 姓名
    name = db.Column(db.String(20), nullable=False)
    # 性别
    gender = db.Column(db.String(10), nullable=True)
    # 个人介绍
    description = db.Column(db.Text, nullable=True)
    # 照片url
    image_url = db.Column(db.Text, nullable=True)
    # 国籍
    nationality = db.Column(db.String(10), nullable=True)
    # 执拍手
    hand = db.Column(db.String(20), nullable=True)
    # 握拍方式
    grip = db.Column(db.String(10), nullable=True)
    # 底板型号
    blade = db.Column(db.String(100), nullable=True)
    # 正手胶皮
    forehand = db.Column(db.String(100), nullable=True)
    # 反手胶皮
    backhand = db.Column(db.String(100), nullable=True)
    # 是否带颗粒：是、否
    particle = db.Column(db.String(10), nullable=True)
    # 打法风格
    personal_style = db.Column(db.Text, nullable=True)
    # 所获成绩
    glory = db.Column(db.Text, nullable=True)
    # 轶闻趣事
    anecdote = db.Column(db.Text, nullable=True)
    # 世界排名
    rank = db.Column(db.Integer, nullable=True)
    # 人物评价
    comment = db.Column(db.Text, nullable=True)

    def jsonify_athlete(self):
        return {
            'id': self.id,
            'name': self.name,
            'gender': self.gender,
            'description': self.description,
            'image_url': self.image_url,
            'nationality': self.nationality,
            'hand': self.hand,
            'grip': self.grip,
            'blade': self.blade,
            'forehand': self.forehand,
            'backhand': self.backhand,
            'particle': self.particle,
            'personal_style': self.personal_style,
            'glory': self.glory,
            'anecdote': self.anecdote,
            'rank': self.rank,
            'comment': self.comment,
        }


# 球台
class Table(db.Model):
    __tablename__ = 'table'
    # id
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 球台号
    number = db.Column(db.Integer, nullable=False)
    # 活动时间
    activity_time = db.Column(db.DateTime, nullable=True)
    # 活动地点
    place = db.Column(db.String(100), nullable=True)
    # 备注
    additional_info = db.Column(db.Text, nullable=True)
    # 最大限制人数
    max_members = db.Column(db.Integer, nullable=True)
    # 开抢时间
    release_time = db.Column(db.DateTime, nullable=True)

    def jsonify_table(self):
        player_list = []
        players_id_list = []
        for player in self.players:
            players_id_list.append(player.id)
            player_list.append({
                "id": player.id,
                "username": player.username,
                "gender": player.gender,
                "role": player.role,
                "school": player.school,
                "phone": player.phone,
                "score": player.score})
        return {
            'id': self.id,
            'number': self.number,
            'activity_time': self.activity_time,
            'place': self.place,
            'additional_info': self.additional_info,
            'max_members': self.max_members,
            'release_time': self.release_time,
            'players': player_list,
            'players_id': players_id_list,
        }


# 用户操作日志
class ActionLog(db.Model):
    __tablename__ = 'action_log'
    # 日志id
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 操作行为
    action = db.Column(db.String(100), nullable=True)
    # 操作时间
    time = db.Column(db.DateTime, default=datetime.now)
    # 操作者
    operator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    operator = db.relationship('User', backref="action_logs")

    def jsonify_action_log(self):
        if not self.operator:
            return {
                'id': self.id,
                'action': self.action,
                'time': self.time,
                'operator_id': self.operator_id,
                'operator_name': None,
            }
        return {
            'id': self.id,
            'action': self.action,
            'time': self.time,
            'operator_id': self.operator_id,
            'operator_name': self.operator.username,
        }


class AccessToken(db.Model):
    __tablename__ = 'access_token'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    access_token = db.Column(db.String(200), nullable=False)  # Todo 官方提示不小于512，但目前在136个字符空间
    update_time = db.Column(db.DateTime, default=datetime.now)
    expires_in = db.Column(db.Integer, nullable=False)

    def jsonify_access_token(self):
        return {
            'access_token': self.access_token,
            'update_time': self.update_time,
            'expires_in_seconds': self.expires_in_seconds,
        }
