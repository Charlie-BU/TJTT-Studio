from exts import db
from datetime import datetime

# 要实现User-Competition多对多，需要中间表
user_competition_table = db.Table("user_competition_table",
                                  db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                                  db.Column('competition_id', db.Integer, db.ForeignKey('competition.id'), primary_key=True))

# user_session_table = db.Table("user_session_table",
#                               db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
#                               db.Column('session_id', db.Integer, db.ForeignKey('session.id'), primary_key=True))
#

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
    # 姓名
    username = db.Column(db.String(100), nullable=False)
    # 密码
    password = db.Column(db.String(16), nullable=False)
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
    gender = db.Column(db.String(1), nullable=True)
    # 身份（教师/学生）
    role = db.Column(db.String(2), nullable=True)
    # 执拍手
    hand = db.Column(db.String(2), nullable=True)
    # 握拍方式
    grip = db.Column(db.String(10), nullable=True)
    # 底板型号
    blade = db.Column(db.String(100), nullable=True)
    # 正手胶皮
    forehand = db.Column(db.String(100), nullable=True)
    # 反手胶皮
    backhand = db.Column(db.String(100), nullable=True)
    # 是否带颗粒：是、否
    particle = db.Column(db.String(1), nullable=True)
    # 地区
    address = db.Column(db.String(120), nullable=True)
    # 报名积分（报名时确定）
    fixed_score = db.Column(db.Integer, nullable=True)
    # 隐私设置
    privacy = db.Column(db.String(10), nullable=True)

    # 外键
    # 所在组织
    organ_id = db.Column(db.Integer, db.ForeignKey('organization.id'))
    organ = db.relationship('Organization', backref="users")  # backref会自动给Organization表加一个users的属性，来获取每个organ_id对应的所有users，返回的是列表
    # 参加的所有比赛
    matches = db.relationship("Competition", secondary=user_competition_table, back_populates="players")
    # 团体比赛代表队
    teams = db.relationship("Team", secondary=user_team_table, back_populates="members")
    # 约球帖
    posts = db.relationship("Post", secondary=user_post_table, back_populates="couple")


class Organization(db.Model):
    __tablename__ = 'organization'
    # 组织id
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 组织名称
    organname = db.Column(db.String(40), nullable=False)
    # 组织描述
    description = db.Column(db.Text, nullable=True)


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
    system = db.Column(db.String(16), nullable=False)
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
    # 参赛选手
    players = db.relationship("User", secondary="user_competition_table", back_populates="matches")
    # 主办方
    organ_id = db.Column(db.Integer, db.ForeignKey('organization.id'))
    organ = db.relationship('Organization', backref="matches")  # backref会自动给Organization表加一个matches的属性，来获取每个organ_id对应的所有matches，返回的是列表


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


# # 比赛场次（两个人）
# class Session(db.Model):
#     __tablename__ = 'session'
#     # 场次id
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     # 大比分
#     result = db.Column(db.String(10), nullable=False)
#     # 参赛双方
#     couple = db.relationship("User", secondary=user_session_table, back_populates="sessions")
#     # 外键：所属赛事id
#     match_id = db.Column(db.Integer, db.ForeignKey('competition.id'))
#     match = db.relationship("Competition", backref="sessions")


# 双打搭档
class Couple(db.Model):
    __tablename__ = 'couple'
    # id
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 两个选手的id
    user1_id = db.Column(db.Integer, nullable=False)
    user2_id = db.Column(db.Integer, nullable=False)


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
    winner_score_before = db.Column(db.Integer, nullable=True)
    # 胜者结算积分
    winner_score_after = db.Column(db.Integer, nullable=True)
    # 负者姓名（积分减）
    loser_name = db.Column(db.String(100), nullable=True)
    # 负者原积分
    loser_score_before = db.Column(db.Integer, nullable=True)
    # 负者结算积分
    loser_score_after = db.Column(db.Integer, nullable=True)


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


# 邮箱验证码
class EmailCaptcha(db.Model):
    __tablename__ = 'email_captcha'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False)
    captcha = db.Column(db.String(100), nullable=False)


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
    # 有无球台
    table_vacant = db.Column(db.String(50), nullable=True)
    # 发帖人和受帖人
    couple = db.relationship('User', secondary=user_post_table, back_populates="posts")
