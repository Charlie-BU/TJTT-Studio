<template>
	<div class="head">
		<div class="headTitle">TJTT乒乓球一体化平台</div>
	</div>
	<div>
		<u-sticky offset-top="0">
			<div class="headBox">
				<div class="topHead">
					<img class="icon" src="" alt="" />
					<img class="icon" src="" alt="" />
				</div>
				<div class="phb flex" style="margin: 50rpx 0 -30rpx 0">
					<div>
						<div>
							<span class="num">{{user_length}}</span>
							<span class="jf" style="margin-left: 20rpx">人</span>
						</div>
						<div style="color: black; margin-top: 20rpx" class="jf">
							<u-icon style="margin-right: 10rpx" name="account-fill" color="#F25C07"
								size="28" />现有用户
						</div>
					</div>
					<div>
						<div>
							<span class="num">{{male_length}} / {{female_length}}</span>
							<span class="jf" style="margin-left: 20rpx">人</span>
						</div>
						<div style="color: black; margin-top: 20rpx; margin-left: 15rpx;" class="jf">
							<u-icon style="margin-right: 10rpx" name="man-add" color="#F25C07" size="28" />
							<u-icon name="man" size="28" />男 /
							<u-icon name="woman" size="28" />女
						</div>
					</div>
					<div>
						<div>
							<span class="num">{{student_length}} / {{teacher_length}}</span>
							<span class="jf" style="margin-left: 20rpx">人</span>
						</div>
						<div style="color: black; margin-top: 20rpx" class="jf">
							<u-icon style="margin-right: 10rpx" name="account" color="#F25C07" size="28" />学生 /
							教师
						</div>
					</div>
				</div>
				<div @click="talk_room_page" class="phb flex">
					<div>
						<u-icon style="margin-right: 20rpx;" name="chat" color="#F25C07" size="28" />
						<span class="yjfk">乒乓贴吧</span>
					</div>
					<div class="jf" style="color: #666666">
						进来聊天
						<u-icon class="fr" style="margin-left: 14rpx; margin-top: 5rpx" name="arrow-right"
							color="#656565" size="28" />
					</div>
				</div>
			</div>
		</u-sticky>
		<section v-if="!hide_this" class="section">
			<div v-if="user && (user.school=='同济大学')" style="background-color: #f8f8f8; display: flex;">
				<u-tabs :list="pick_list" bg-color="#f8f8f8" active-color="#F25C07" :is-scroll="true" :current="current"
					@change="change"></u-tabs>
				<u-icon v-if="current==2" name="question-circle" color="#F25C07" size="30" @click="reserve_role" />
			</div>
			<div v-else style="background-color: #f8f8f8; display: flex;">
				<u-tabs :list="pick_list.slice(0, 2)" bg-color="#f8f8f8" active-color="#F25C07" :is-scroll="true" :current="current"
					@change="change"></u-tabs>
			</div>
			<div class="date" v-if="this.current<=1">
				<div style="margin-top: 18rpx; display: flex;">
					<button @click='setAbtn(0)' :class="activeBtn == 0 ? 'bg-cyan cu-btn':' cu-btn line-cyan'"
						class="cu-btn">全部</button>
					<button @click='setAbtn(1)' :class="activeBtn == 1 ? 'cu-btn bg-blue':'cu-btn line-blue'"><u-icon name="man" size="28" /> 发帖</button>
					<button @click='setAbtn(2)' :class="activeBtn == 2 ? 'cu-btn bg-orange':'cu-btn line-orange'"><u-icon name="woman" size="28" /> 发帖</button>
					<div style="text-align: end;">
						<button v-if="current == 0" class="cu-btn btn round line-cyan"
							@click="send_play_post">发布约球帖</button>
					</div>
				</div>
				<div v-if="this.play_posts.length == 0" class="boxList" style="text-align: center; color: #999999;">
					暂无约球帖</div>
				<div v-for="(play_post, index) in this.play_posts" :key="index" class="boxList flex">
					<div class="left">
						<img class="lIcon"
							src="https://tjtt-assets.oss-cn-shanghai.aliyuncs.com/pictures/decorations/post.jpg"
							alt="" />
					</div>
					<div class="right">
						<div class="text1">约球帖 {{index + 1}}</div>
						<div v-if="play_post.playerA_gender=='男'" class="text2" style="color: #0081ff;">A:
							{{play_post.playerA_name}} | {{play_post.playerA_gender}} |
							TJTT积分：{{play_post.playerA_score}}</div>
						<div v-else-if="play_post.playerA_gender=='女'" class="text2" style="color: #f37b1d;">A:
							{{play_post.playerA_name}} | {{play_post.playerA_gender}} |
							TJTT积分：{{play_post.playerA_score}}</div>
						<div v-if="play_post.playerA_gender=='男' && ((play_post.playerB_name) && (play_post.playerA_name == this.user.username || play_post.playerB_name == this.user.username))" class="text2" style="color: #0081ff;">
							&nbsp;&nbsp;&nbsp;&nbsp;手机号：{{play_post.playerA_phone}}
						</div>
						<div v-else-if="play_post.playerA_gender=='女' && ((play_post.playerB_name) && (play_post.playerA_name == this.user.username || play_post.playerB_name == this.user.username))" class="text2" style="color: #f37b1d;">
							&nbsp;&nbsp;&nbsp;&nbsp;手机号：{{play_post.playerA_phone}}
						</div>
						
						<div v-if="play_post.playerB_name && play_post.playerB_gender=='男'" class="text2"
							style="color: #0081ff;">B: {{play_post.playerB_name}} | {{play_post.playerB_gender}} |
							TJTT积分：{{play_post.playerB_score}}</div>
						<div v-else-if="play_post.playerB_name && play_post.playerB_gender=='女'" class="text2"
							style="color: #f37b1d;">B: {{play_post.playerB_name}} | {{play_post.playerB_gender}} |
							TJTT积分：{{play_post.playerB_score}}</div>
						<div v-if="play_post.playerB_gender=='男' && ((play_post.playerB_name) && (play_post.playerA_name == this.user.username || play_post.playerB_name == this.user.username))" class="text2" style="color: #0081ff;">
							&nbsp;&nbsp;&nbsp;&nbsp;手机号：{{play_post.playerB_phone}}
						</div>
						<div v-else-if="play_post.playerB_gender=='女' && ((play_post.playerB_name) && (play_post.playerA_name == this.user.username || play_post.playerB_name == this.user.username))" class="text2" style="color: #f37b1d;">
							&nbsp;&nbsp;&nbsp;&nbsp;手机号：{{play_post.playerB_phone}}
						</div>
						<div class="text2">约球时间：{{play_post.play_time}}</div>
						<div class="text2">地点：{{play_post.place}}</div>
						<div v-if="play_post.table_vacant" class="text2">球台：{{play_post.table_vacant}}</div>
						<div class="text3 flex">
							<div v-if="play_post.description" style="line-height: 30rpx;">
								备注：{{play_post.description}}
							</div>
						</div>
						<div class="text3" style="text-align: end; white-space: nowrap;">
							<button v-if="(!play_post.playerB_name)" style="place: relative; bottom: 8rpx"
								class="cu-btn round line-green" @click="accpet_play_post(play_post.id)">
								受邀
							</button>
							<button
								v-else-if="(play_post.playerB_name) && (play_post.playerA_name == this.user.username || play_post.playerB_name == this.user.username)"
								style="place: relative; bottom: 8rpx" class="cu-btn round line-green"
								@click="cancel_post(play_post.id)">
								取消受邀
							</button>
							<button
								v-else-if="(play_post.playerB_name) && (play_post.playerA_name != this.user.username && play_post.playerB_name != this.user.username)"
								style="place: relative; bottom: 8rpx" class="cu-btn round line-grey"
								@click="warning">
								已受邀
							</button>
							<button
								v-if="(play_post.playerA_name == this.user.username) || (play_post.playerB_name == this.user.username) || (this.user.usertype == 'K10' || this.user.usertype == 'K11')"
								style="place: relative; bottom: 8rpx" class="cu-btn round line-red"
								@click="delete_play_post(play_post.id)">
								删除
							</button>
						</div>
					</div>
				</div>
			</div>
			
			<div v-if="this.current>=2" class="weeklyActivity">
				<div style="margin-top: 18rpx;"></div>
				<view class="picker">
					<label class="txt">当前选择：</label>
					<picker class="p-left" @change="change_place"
						:value="place_index" :range="place_list">
						<view v-if="place_index==0" class="uni-input">{{place_list[place_index]}}</view>
						<view v-else class="uni-input">{{place_list[place_index].slice(0,2)}}</view>
					</picker>
					<picker class="p-right" @change="change_time"
						:value="time_index" :range="time_list">
						<view v-if="time_index==0" class="uni-input">{{time_list[time_index]}}</view>
						<view v-else class="uni-input">{{time_list[time_index].match(/\d{2}:\d{2}:\d{2}/)[0]}}</view>
					</picker>
				</view>
				<div v-for="(table, index) in this.tables" :key="index" class="boxList flex">
					<div class="left">
						<img class="lIcon"
							src="https://tjtt-assets.oss-cn-shanghai.aliyuncs.com/pictures/decorations/table.jpg"
							alt="" />
					</div>
					<div class="right">
						<div class="text1">{{table.number}}号球台 <u-icon v-if="user.usertype == 'K9' || user.usertype == 'K10' || user.usertype == 'K11'" name="man-add" color="#1cbbb4" size="27" @click="add_table_player(table.id)" /></div>
						<div v-for="(player, index) in table.players" :key="index">
							<div v-if="player && player.gender=='男'" class="text2" style="color: #0081ff;">
								{{player.username}} | {{player.gender}} | TJTT积分：{{player.score}} <u-icon v-if="user.usertype == 'K9' || user.usertype == 'K10' || user.usertype == 'K11'" name="man-delete" color="#ff0000" size="27" @click="remove_table_player(table.id, player.id, player.username)" />
							</div>
							<div v-else-if="player && player.gender=='女'" class="text2" style="color: #f37b1d;">
								{{player.username}} | {{player.gender}} | TJTT积分：{{player.score}} <u-icon v-if="user.usertype == 'K9' || user.usertype == 'K10' || user.usertype == 'K11'" name="man-delete" color="#ff0000" size="27" @click="remove_table_player(table.id, player.id, player.username)" />
							</div>
							<div v-if="player && player.gender=='男' && table.players_id.includes(user.id)" class="text2" style="color: #0081ff;">
								手机号：{{player.phone}}
							</div>
							<div v-else-if="player && player.gender=='女' && table.players_id.includes(user.id)" class="text2" style="color: #f37b1d;">
								手机号：{{player.phone}}
							</div>
						</div>
						<div class="text2">活动时间：{{table.activity_time}}</div>
						<div class="text2">地点：{{table.place}}</div>
						<div class="text2" style="color: red;">预订开始时间：{{table.release_time}}</div>
						<div class="text2" style="color: red;">最大预订人数：{{(table.max_members > table.players_id.length) ? table.max_members : table.players_id.length}}</div>
						<div v-if="table.additional_info" class="text3 flex">
							<div style="line-height: 30rpx;">
								备注：{{table.additional_info}}
							</div>
						</div>
						<div class="text3" style="margin-top: 50rpx; text-align: end; white-space: nowrap;">
							<button v-if="!table.players_id.includes(user.id)"
								style="place: relative; bottom: 8rpx"
								class="cu-btn round line-green" @click="reserve(table.id)">
								预订
							</button>
							<button v-else style="place: relative; bottom: 8rpx"
								class="cu-btn round line-red" @click="cancel_reserve(table.id)">
								取消预订
							</button>
							<button v-if="(table.players_id.includes(user.id)) || (user.usertype == 'K9' || user.usertype == 'K10' || user.usertype == 'K11')"
								style="place: relative; bottom: 8rpx" class="cu-btn round line-cyan"
								@click="modify_additional_info(table.id, table.additional_info)">
								添加 / 修改备注
							</button>
						</div>
					</div>
				</div>
			</div>
		</section>
		<div v-else style="text-align: center;">
			<image src='https://tjtt-assets.oss-cn-shanghai.aliyuncs.com/pictures/decorations/details-modal.jpg' alt="">
			</image>
			<image src='https://tjtt-assets.oss-cn-shanghai.aliyuncs.com/pictures/decorations/QA.jpg' alt=""></image>
		</div>
		<div style="visibility: hidden;">————————</div>
		<div style="visibility: hidden;">————————</div>
		<div style="visibility: hidden;">————————</div>
		<tabbar :current-page="3"></tabbar>
	</div>
</template>

<script>
	import { fetch_data, fetch_data_wxLogin} from '../../static/js/ajax_request.js'
	import { login_check } from '../../static/js/login_check.js'
	import { magic } from '../../static/js/magic_power.js'
	import * as utils from '../../static/js/utils.js'
	export default {
		data() {
			return {
				user: "",
				user_length: "",
				male_length: "",
				female_length: "",
				student_length: "",
				teacher_length: "",
				TJTTers_length: "",
				pick_list: [{
						name: "约球帖",
					},
					{
						name: "约教帖",
					},
					{
						name: "球台预订",
					},
				],
				activeBtn: 0,
				current: 0,
				all_play_posts: [],
				male_play_posts: [],
				female_play_posts: [],
				play_posts: [],
				
				time_list: [],
				place_list: [],
				time_index: "",
				place_index: "",
				tables: [],
				hide_this: magic(),
			}
		},
		onLoad() {
			login_check(user => {
				this.user = user;
			});
			if (!this.user) {
				wx.showToast({
					title: "请登录",
					icon: "none",
					duration: 1500,
				});
				setTimeout(() => {
					uni.reLaunch({
						url: '/pages/login/login',
					})
				}, 1000);
			};

			fetch_data("POST", "get_info", null, "user", res => {
				this.user_length = res.data.user_length;
				this.male_length = res.data.male_length;
				this.female_length = res.data.female_length;
				this.student_length = res.data.student_length;
				this.teacher_length = res.data.teacher_length;
				this.TJTTers_length = res.data.TJTTers_length;
			});
			
			fetch_data("POST", "get_play_posts", null, "application", res => {
				// 修改play_time属性
				this.all_play_posts = res.data.all_play_posts.map(play_post => ({
					...play_post,
					play_time: utils.format_time(play_post.play_time)
				}));
				this.male_play_posts = res.data.male_play_posts.map(play_post => ({
					...play_post,
					play_time: utils.format_time(play_post.play_time)
				}));
				this.female_play_posts = res.data.female_play_posts.map(play_post => ({
					...play_post,
					play_time: utils.format_time(play_post.play_time)
				}));
				this.play_posts = this.all_play_posts;
			});
		},
		
		methods: {
			// 约球帖、约教贴、预订球台切换
			change(index) {
				this.current = index;
				if (index == 0) {
					wx.showToast({
						title: "加载中",
						icon: "loading",
						duration: 100000,
					});
					fetch_data("POST", "get_play_posts", null, "application", res => {
						// 修改play_time属性
						this.all_play_posts = res.data.all_play_posts.map(play_post => ({
							...play_post,
							play_time: utils.format_time(play_post.play_time)
						}));
						this.male_play_posts = res.data.male_play_posts.map(play_post => ({
							...play_post,
							play_time: utils.format_time(play_post.play_time)
						}));
						this.female_play_posts = res.data.female_play_posts.map(play_post => ({
							...play_post,
							play_time: utils.format_time(play_post.play_time)
						}));
						this.play_posts = this.all_play_posts;
						wx.hideToast();
					});
				} else if (index == 1) {
					wx.showToast({
						title: "TJTT教练库正在建立中，敬请期待",
						icon: "none",
						duration: 1200,
					});
					setTimeout(() => this.current = 0, 700);
				} else if (index == 2) {
					wx.showToast({
						title: "加载中",
						icon: "loading",
						duration: 100000,
					});
					this.time_index = 0;
					this.place_index = 0;
					fetch_data("POST", "get_all_tables", null, "application", res => {
						this.time_list = [
							res.data.time_list[0],
							...res.data.time_list.slice(1).map(time => utils.format_time(time))
						];
						this.place_list = res.data.place_list;
						this.tables = res.data.tables.map(table => ({
							...table,
							activity_time: utils.format_time(table.activity_time),
							release_time: utils.format_time(table.release_time),
						}));
						wx.hideToast();
					});
				};
			},
			// ♂发帖、♀发帖切换
			setAbtn(e) {
				this.activeBtn = e;
				if (e == 0) {
					this.play_posts = this.all_play_posts;
				} else if (e == 1) {
					this.play_posts = this.male_play_posts;
				} else if (e == 2) {
					this.play_posts = this.female_play_posts;
				};
			},
			// 预订球台时间、地点切换
			change_time(e) {
				wx.showToast({
					title: "加载中",
					icon: "loading",
					duration: 100000,
				});
				this.time_index = e.detail.value;
				if (this.time_index == 0 && this.place_index == 0) {
					fetch_data("POST", "get_all_tables", null, "application", res => {
						this.tables = res.data.tables.map(table => ({
							...table,
							activity_time: utils.format_time(table.activity_time),
							release_time: utils.format_time(table.release_time),
						}));
						wx.hideToast();
					});
				}
				let time_condition = this.time_list[this.time_index];
				let place_condition = this.place_list[this.place_index];
				let data = {
					"time_condition": time_condition,
					"place_condition": place_condition,
				};
				fetch_data("POST", "get_tables_by_condition", data, "application", res => {
					this.tables = res.data.tables.map(table => ({
						...table,
						activity_time: utils.format_time(table.activity_time),
						release_time: utils.format_time(table.release_time),
					}));
					wx.hideToast();
				});
			},
			
			change_place(e) {
				wx.showToast({
					title: "加载中",
					icon: "loading",
					duration: 100000,
				});
				this.place_index = e.detail.value;
				if (this.time_index == 0 && this.place_index == 0) {
					fetch_data("POST", "get_all_tables", null, "application", res => {
						this.tables = res.data.tables.map(table => ({
							...table,
							activity_time: utils.format_time(table.activity_time),
							release_time: utils.format_time(table.release_time),
						}));
						wx.hideToast();
					});
				}
				let time_condition = this.time_list[this.time_index];
				let place_condition = this.place_list[this.place_index];
				let data = {
					"time_condition": time_condition,
					"place_condition": place_condition,
				};
				fetch_data("POST", "get_tables_by_condition", data, "application", res => {
					this.tables = res.data.tables.map(table => ({
						...table,
						activity_time: utils.format_time(table.activity_time),
						release_time: utils.format_time(table.release_time),
					}));
					wx.hideToast();
				});
			},

			send_play_post() {
				uni.navigateTo({
					url: '/pages/community/send-play-post',
				})
			},
			accpet_play_post(post_id) {
				wx.showModal({
					title: '受邀约球帖',
					content: '确定受邀该约球帖？',
					success: res => {
						if (res.confirm) {
							fetch_data_wxLogin("POST", "store_openid", { "my_id": this.user.id }, "user",);
							subscirbe_message(['pSBm6ewDwG2_kTS3K2_n9kniQsDamkIUeSwjw1F381g'], () => {
								let data = {
									"my_id": this.user.id,
									"post_id": post_id,
								}
								fetch_data("POST", "accept_play_post", data, "application", res => {
									wx.showToast({
										title: res.data.message,
										icon: "none",
										duration: 1000,
									});
									if (res.data.status == 200) {
										setTimeout(() => {
											uni.reLaunch({
												url: '/pages/community/index',
											})
										}, 1000);
									}
								})
								fetch_data("POST", "answer_post", data, "application", res => {
									if (res.data.status == 200) {
										console.log("微信通知发送成功");
									} else {
										console.log("微信通知存在一方发送失败");
									}
								})
							})
						}
					}
				})
			},
			cancel_post(post_id) {
				wx.showModal({
					title: '取消约球',
					content: '确定取消约球？',
					success: res => {
						if (res.confirm) {
							let data = {
								"my_id": this.user.id,
								"post_id": post_id,
							}
							fetch_data("POST", "cancel_post", data, "application", res => {
								wx.showToast({
									title: res.data.message,
									icon: "none",
									duration: 1000,
								});
								if (res.data.status == 200) {
									setTimeout(() => {
										uni.reLaunch({
											url: '/pages/community/index',
										})
									}, 1000);
								}
							})
						}
					}
				})
			},
			delete_play_post(post_id) {
				wx.showModal({
					title: '删除约球帖',
					content: '确定删除约球帖？',
					success: res => {
						if (res.confirm) {
							let data = {
								"my_id": this.user.id,
								"post_id": post_id,
							}
							fetch_data("POST", "delete_play_post", data, "application", res => {
								wx.showToast({
									title: res.data.message,
									icon: "none",
									duration: 1000,
								});
								if (res.data.status == 200) {
									setTimeout(() => {
										uni.reLaunch({
											url: '/pages/community/index',
										})
									}, 1000);
								}
							})
						}
					}
				})
			},
			warning() {
				wx.showToast({
					title: "该约球帖已受邀，请选取其他约球帖",
					icon: "none",
					duration: 1000,
				});
			},
			
			reserve_role() {
				wx.showModal({
					title: '球台预订规则',
					content: "本功能当前应用于同济大学乒乓球协会周常活动球台预订，请务必确认所预订球台的地点、时间正确。每人在一次活动周期内只能预订一个地点一个时间的一张球台，若已预订后再次预订其他球台，第一次预订记录将被覆盖，以最后一次预订球台为准。",
					showCancel: false,
					confirmText: '我已知晓',
				})
			},
			reserve(table_id) {
				wx.showModal({
					title: '预订球台',
					content: '确定预订该球台？',
					success: res => {
						if (res.confirm) {
							wx.showToast({
								title: "预订中",
								icon: "loading",
								duration: 100000,
							});
							let data = {
								"my_id": this.user.id,
								"table_id": table_id,
							}
							fetch_data("POST", "reserve_table", data, "application", res => {
								wx.showToast({
									title: res.data.message,
									icon: "none",
									duration: 1000,
								});
								if (res.data.status == 200) {
									setTimeout(() => {
										uni.reLaunch({
											url: '/pages/community/index',
										})
									}, 1000);
								}
							})
						}
					}
				})
			},
			cancel_reserve(table_id) {
				wx.showModal({
					title: '取消预订球台',
					content: '确定取消预订该球台？',
					success: res => {
						if (res.confirm) {
							wx.showToast({
								title: "预订中",
								icon: "loading",
								duration: 100000,
							});
							let data = {
								"my_id": this.user.id,
								"table_id": table_id,
							}
							fetch_data("POST", "cancel_reserve_table", data, "application", res => {
								wx.showToast({
									title: res.data.message,
									icon: "none",
									duration: 1000,
								});
								if (res.data.status == 200) {
									setTimeout(() => {
										uni.reLaunch({
											url: '/pages/community/index',
										})
									}, 1000);
								}
							})
						}
					}
				})
			},
			modify_additional_info(table_id, additional_info) {
				wx.showModal({
					title: "添加 / 修改球台备注",
					content: additional_info,
					editable: true,
					success: res => {
						if (res.confirm) {
							let data = {
								"my_id": this.user.id,
								"table_id": table_id,
								"additional_info": res.content,
							}
							fetch_data("POST", "modify_additional_info", data, "application", res => {
								wx.showToast({
									title: res.data.message,
									icon: "none",
									duration: 1000,
								});
								if (res.data.status == 200) {
									setTimeout(() => {
										uni.reLaunch({
											url: '/pages/community/index',
										})
									}, 1000);
								}
							})
						}
					}
				});
			},
			
			add_table_player(table_id) {
				wx.showModal({
					title: "添加球台预订者",
					editable: true,
					placeholderText: "请输入预订者姓名",
					success: res => {
						if (res.confirm) {
							let data = {
								"my_id": this.user.id,
								"table_id": table_id,
								"player_name": res.content,
							}
							fetch_data("POST", "add_table_player", data, "application", res => {
								wx.showToast({
									title: res.data.message,
									icon: "none",
									duration: 1000,
								});
								if (res.data.status == 200) {
									setTimeout(() => {
										uni.reLaunch({
											url: '/pages/community/index',
										})
									}, 1000);
								}
							})
						}
					}
				});
			},
			
			remove_table_player(table_id, player_id, player_name) {
				wx.showModal({
					title: '移除球台预订者',
					content: '确定移除该球台预订者'+player_name+'？',
					success: res => {
						if (res.confirm) {
							wx.showToast({
								title: "移除中",
								icon: "loading",
								duration: 100000,
							});
							let data = {
								"my_id": this.user.id,
								"table_id": table_id,
								"player_id": player_id,
							}
							fetch_data("POST", "remove_table_player", data, "application", res => {
								wx.showToast({
									title: res.data.message,
									icon: "none",
									duration: 1000,
								});
								if (res.data.status == 200) {
									setTimeout(() => {
										uni.reLaunch({
											url: '/pages/community/index',
										})
									}, 1000);
								}
							})
						}
					}
				})
			},
			
			talk_room_page() {
				if (this.hide_this) {
					return;
				}
				wx.showToast({
					title: "该功能暂未上线，敬请期待",
					icon: "none",
					duration: 1000,
				});
			}
		},
		onPullDownRefresh() {
			uni.reLaunch({
				url: '/pages/community/index',
			});
			setTimeout(function() {
				uni.stopPullDownRefresh();
			}, 1000);
		}
	}
</script>

<style lang="scss" scoped>
	.head {
		position: relative;

		.headTitle {
			font-weight: 600;
			font-size: 35rpx;
			color: #212121;
			line-height: 36rpx;
			position: absolute;
			text-align: center;
			width: 100%;
			top: 100rpx;
			z-index: 999;
			position: fixed;
		}
	}

	.section {
		background: #ffffff;
		border-radius: 20rpx 20rpx 20rpx 20rpx;
		box-sizing: border-box;
		padding: 20rpx;

		.cu-btn {
			margin-right: 20rpx;
		}

		.boxList {
			margin-top: 6rpx;
			box-sizing: border-box;
			padding: 30rpx 20rpx;
			padding-top: 40rpx;
			border-bottom: 1px solid #f2f2f2;

			.left {
				width: 15%;
			}

			.right {
				.quan {
					margin-right: 4rpx;
					border-radius: 50%;
					background: #d9d9d9;
					width: 28rpx;
					height: 28rpx;
					display: inline-block;
					position: relative;
					top: 4rpx;

				}

				.text1 {
					font-weight: 500;
					font-size: 32rpx;
					color: #999999;
					line-height: 32rpx;
				}

				.text2 {
					margin-top: 28rpx;
					font-weight: 500;
					font-size: 28rpx;
					color: black;
					line-height: 20rpx;
				}

				.text3 {
					margin-top: 28rpx;
					font-weight: 500;
					font-size: 24rpx;
					color: #999999;
					line-height: 24rpx;
				}

				width: 83%;
			}

			.lIcon {
				width: 80rpx;
				height: 80rpx;

				border-radius: 12rpx 12rpx 12rpx 12rpx;
			}
		}
	}

	.phb {
		.yjfk {
			font-size: 28rpx;
			color: #333333;
			line-height: 28rpx;
		}

		box-sizing: border-box;
		padding: 30rpx;
		background-color: white;
		margin-top: 50rpx;
		background: linear-gradient(135deg, #f3ec78, #ec668a);
		border-radius: 20rpx;

		.jf {
			font-family: PingFang SC, PingFang SC;
			font-weight: 400;
			font-size: 28rpx;
			color: #282456;
			line-height: 36rpx;
			text-align: left;
			font-style: normal;
			text-transform: none;
		}

		.num {
			font-family: PingFang SC, PingFang SC;
			font-weight: bold;
			font-size: 40rpx;
			color: #282456;
			line-height: 48rpx;
			text-align: center;
			font-style: normal;
			text-transform: none;
		}
	}

	.headBox {
		background: linear-gradient(180deg, #f9d5a5, #fef2da);
		box-sizing: border-box;
		padding: 20rpx;
	}

	.topHead {
		margin-top: 50rpx;
	}

	.icon {
		margin-right: 30rpx;
		width: 37rpx;
		height: 37rpx;
	}

	.picker {
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: 10px;
		border-radius: 8px;
		background-color: #f9f9f9;
	}

	.picker .txt {
		margin-right: 10px;
		font-size: 16px;
		color: #333;
	}

	.picker .p-left,
	.picker .p-right {
		flex: 1;
		margin: 0 5px;
	}

	.uni-input {
		border: 1px solid #ccc;
		border-radius: 40rpx;
		padding: 8px;
		color: #333;
		text-align: center;
		transition: all 0.3s ease;
	}

	.uni-input:hover {
		border-color: #007AFF;
	}
</style>