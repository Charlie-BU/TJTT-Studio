<template>
	<div>
		<div class="head">
			<div class="headTitle">TJTT积分排名</div>
			<img class="topImg" src="../../static/tabbar/Groupbg.png" alt="" />
		</div>
		<div style="background-color: white; color: white; height: 10rpx;">space</div>
		<div style="display: flex; background-color: white;">
			<u-tabs style="margin-left: 15rpx;" :list="range_list" :show-bar="false" :duration="0" active-color="#2979FF" :is-scroll="true" :current="current" @change="change"></u-tabs>
			<picker class="school-picker" @change="pick_school" :value="school_index" :range="school_list">
				<view v-if="current>=0 && current<=2" style="margin: 21rpx; font-size: 30rpx;">{{school_list[school_index]}} <u-icon name="arrow-down" size="28" /></view>
				<view v-else style="margin: 21rpx; color: #2979FF; font-weight: bold; font-size: 30rpx;">{{school_list[school_index]}} <u-icon name="arrow-down" size="28" /></view>
			</picker>
		</div>
		<div style="display: flex;">
			<u-search class="search_bar" v-model="search_user" bg-color="#ffffff" :show-action="false"
				placeholder="输入选手姓名"></u-search>
			<button class="cu-btn btn round line-cyan" style="margin-top: 15rpx;" @click="search">查找</button>
		</div>
		<div v-if='user' class="userPm flex">
			<div class="left">
				<div class="l1L l1" style="margin: 20rpx 12rpx; font-weight: bold;">{{my_rank}}</div>
			</div>
			<div class="leftL">
				<img v-if="user.profile_img" class="userImg round"
					:src="user.profile_img"
					alt="" />
				<img v-else-if="user.gender == '男'" class="userImg round"
					src="https://tjtt-assets.oss-cn-shanghai.aliyuncs.com/pictures/avatars/male.jpg"
					alt="" />
				<img v-else-if="user.gender == '女'" class="userImg round"
					src="https://tjtt-assets.oss-cn-shanghai.aliyuncs.com/pictures/avatars/female.jpg"
					alt="" />
			</div>
			<div class="right">
				<p class="t1">{{user.username}}</p>
				<p class="t2">{{user.address}} | {{user.school}}</p>
			</div>
			<div class="rightL">{{user.score}}</div>
		</div>
		<section class="section">
			<div class="flex">
				<div class="box">
					<img class="pmBg" src="../../static/tabbar/Rectangle.png" alt="" />
					<div class="cont">
						<img v-if="user2_url" class="user round"
							:src="user2_url"
							alt="" />
						<img v-else class="user"
							src="https://tjtt-assets.oss-cn-shanghai.aliyuncs.com/pictures/avatars/player.png"
							alt="" />
						<div>
							<img class="pmBgc" src="/static/tabbar/second.png" alt="" />
						</div>
						<div v-if="users[1]" class="textT">
							<div v-if="users[1].privacy==1" class="tA">{{users[1].username[0]}} **</div>
							<div v-else class="tA">{{users[1].username}}</div>
							<div class="tB">{{users[1].address}}<br/>{{users[1].school}}</div>
							<div class="tC">{{users[1].score}}</div>
						</div>
					</div>
				</div>
				<div class="box pmBgA">
					<img class="pmBg" src="../../static/tabbar/Rectangle.png" alt="" />
					<div class="cont">
						<img v-if="user1_url" class="user round"
							:src="user1_url"
							alt="" />
						<img v-else class="user"
							src="https://tjtt-assets.oss-cn-shanghai.aliyuncs.com/pictures/avatars/player.png"
							alt="" />
						<div>
							<img class="pmBgc" src="../../static/tabbar/first.png" alt="" />
						</div>
						<div v-if="users[0]" class="textT">
							<div v-if="users[0].privacy==1" class="tA">{{users[0].username[0]}} **</div>
							<div v-else class="tA">{{users[0].username}}</div>
							<div class="tB">{{users[0].address}}<br/>{{users[0].school}}</div>
							<div class="tC">{{users[0].score}}</div>
						</div>
					</div>
				</div>
				<div class="box">
					<img class="pmBg" src="../../static/tabbar/Rectangle.png" alt="" />
					<div class="cont">
						<img v-if="user3_url" class="user round"
							:src="user3_url"
							alt="" />
						<img v-else class="user"
							src="https://tjtt-assets.oss-cn-shanghai.aliyuncs.com/pictures/avatars/player.png"
							alt="" />
						<div>
							<img class="pmBgc" src="/static/tabbar/third.png" alt="" />
						</div>
						<div v-if="users[2]" class="textT">
							<div v-if="users[2].privacy==1" class="tA">{{users[2].username[0]}} **</div>
							<div v-else class="tA">{{users[2].username}}</div>
							<div class="tB">{{users[2].address}}<br/>{{users[2].school}}</div>
							<div class="tC">{{users[2].score}}</div>
						</div>
					</div>
				</div>
			</div>
			<uni-table stripe emptyText="无数据">
				<uni-tr>
					<uni-th width="20rpx">
						<view class="table_head">排名</view>
					</uni-th>
					<uni-th width="20rpx">
						<view class="table_head">姓名</view>
					</uni-th>
					<uni-th width="20rpx">
						<view class="table_head">性别</view>
					</uni-th>
					<uni-th width="20rpx">
						<view class="table_head">赛季活跃度 <u-icon name="question-circle" color="#F25C07" size="27" @click="active_instruction" /></view>
					</uni-th>
					<uni-th width="20rpx">
						<view class="table_head">积分</view>
					</uni-th>
				</uni-tr>
				<uni-tr v-for="(user_x, index) in users" :key="index">
					<uni-td v-if="user_x.id==user.id">
						<view class="table_content" style="color: red;">{{ids[index]}}</view>
					</uni-td>
					<uni-td v-else>
						<view class="table_content">{{ids[index]}}</view>
					</uni-td>
					<uni-td v-if="user_x.id==user.id">
						<view class="table_content" style="color: red;">{{user_x.username}}</view>
					</uni-td>
					<uni-td v-else>
						<view v-if="user_x.privacy==1" class="table_content">{{user_x.username[0]}} **
						</view>
						<view v-else-if="user_x.username.length>=7" class="table_content">
							{{user_x.username.slice(0,7)}}...
						</view>
						<view v-else class="table_content">{{user_x.username}}</view>
					</uni-td>
					<uni-td v-if="user_x.id==user.id">
						<view class="table_content" style="color: red;">{{user_x.gender}}</view>
					</uni-td>
					<uni-td v-else>
						<view class="table_content">{{user_x.gender}}</view>
					</uni-td>
					<uni-td v-if="user_x.id==user.id">
						<view class="table_content" style="color: red;">{{user_x.active}}</view>
					</uni-td>
					<uni-td v-else>
						<view class="table_content">{{user_x.active}}</view>
					</uni-td>
					<uni-td v-if="user_x.score==0">
						<view class="table_content" style="color: #f25c07; white-space: nowrap;">未录入</view>
					</uni-td>
					<uni-td v-else>
						<view class="table_content" style="color: #f25c07; white-space: nowrap;">
							{{user_x.score}}
						</view>
					</uni-td>
				</uni-tr>
			</uni-table>
		</section>
		<div style="visibility: hidden;">————————</div>
		<div style="visibility: hidden;">————————</div>
		<div style="visibility: hidden;">————————</div>
		<tabbar :current-page="2"></tabbar>
	</div>
</template>

<script>
	import { fetch_data } from '../../static/js/ajax_request.js'
	import { login_check } from '../../static/js/login_check.js'
	import * as utils from '../../static/js/utils.js'
	export default {
		data() {
			return {
				user: "",
				school_list: [],
				school_index: 0,
				search_user: "",
				users: [],
				user1_url: "",
				user2_url: "",
				user3_url: "",
				ids: "",
				my_rank: "",
				range_list: [{
						name: "全国",
					},
					{
						name: "男子",
					},
					{
						name: "女子",
					},
				],
				current: 0,
			}
		},

		onLoad() {
			wx.showToast({
				title: '加载中',
				icon: 'loading',
				duration: 100000,
			});
			login_check(user => {
				this.user = user;
			});
			fetch_data('POST', 'get_users', null, 'user', res => {
				this.users = res.data.users;
				this.school_list = res.data.school_list;
				this.user1_url = res.data.users[0].profile_img;
				this.user2_url = res.data.users[1].profile_img;
				this.user3_url = res.data.users[2].profile_img;
				[this.ids, this.my_rank] = utils.get_rank(this.users, this.user.id);
				if (this.users) {
					wx.hideToast();
				}
			})
		},
		methods: {
			onInput(e) {
				this.search_user = e.target.value
			},

			back() {
				uni.navigateBack({
					delta: 1
				});
			},

			search() {
				wx.showToast({
					title: '加载中',
					icon: 'loading',
					duration: 100000,
				});
				this.current = 0;
				let data = {
					"search_user": this.search_user,
					"where": "score_rank"
				};
				fetch_data("POST", "findUserByName", data, "user", res => {
					this.user1_url = null;
					this.user2_url = null;
					this.user3_url = null;
					this.users = res.data.users;
					if (res.data.users.length > 0) {
						this.user1_url = res.data.users[0].profile_img;
					}
					if (res.data.users.length > 1) {
						this.user2_url = res.data.users[1].profile_img;
					}
					if (res.data.users.length > 2) {
						this.user3_url = res.data.users[2].profile_img;
					}
					[this.ids, this.my_rank] = utils.get_rank(this.users, this.user.id);
					wx.hideToast();
				});
			},

			change(index) {
				wx.showToast({
					title: '加载中',
					icon: 'loading',
					duration: 100000,
				});
				this.current = index;
				if (index == 0) {
					this.school_index = 0;
					fetch_data('POST', 'get_users', null, 'user', res => {
						this.user1_url = null;
						this.user2_url = null;
						this.user3_url = null;
						this.users = res.data.users;
						if (res.data.users.length > 0) {
							this.user1_url = res.data.users[0].profile_img;
						}
						if (res.data.users.length > 1) {
							this.user2_url = res.data.users[1].profile_img;
						}
						if (res.data.users.length > 2) {
							this.user3_url = res.data.users[2].profile_img;
						}
						[this.ids, this.my_rank] = utils.get_rank(this.users, this.user.id);
						wx.hideToast();
					})
				} else if (index == 1) {
					this.school_index = 0;
					fetch_data('POST', 'get_male_users', null, 'user', res => {
						this.user1_url = null;
						this.user2_url = null;
						this.user3_url = null;
						this.users = res.data.male_users;
						if (res.data.male_users.length > 0) {
							this.user1_url = res.data.male_users[0].profile_img;
						}
						if (res.data.male_users.length > 1) {
							this.user2_url = res.data.male_users[1].profile_img;
						}
						if (res.data.male_users.length > 2) {
							this.user3_url = res.data.male_users[2].profile_img;
						}
						[this.ids, this.my_rank] = utils.get_rank(this.users, this.user.id);
						wx.hideToast();
					})
				} else if (index == 2) {
					this.school_index = 0;
					fetch_data('POST', 'get_female_users', null, 'user', res => {
						this.user1_url = null;
						this.user2_url = null;
						this.user3_url = null;
						this.users = res.data.female_users;
						if (res.data.female_users.length > 0) {
							this.user1_url = res.data.female_users[0].profile_img;
						}
						if (res.data.female_users.length > 1) {
							this.user2_url = res.data.female_users[1].profile_img;
						}
						if (res.data.female_users.length > 2) {
							this.user3_url = res.data.female_users[2].profile_img;
						}
						[this.ids, this.my_rank] = utils.get_rank(this.users, this.user.id);
						wx.hideToast();
					})
				};
			},
			
			pick_school(e) {
				if (e.detail.value == 0) {
					wx.showToast({
						title: "请选择学校",
						icon: "none",
						duration: 1000,
					});
					return;
				}
				wx.showToast({
					title: "加载中",
					icon: "loading",
					duration: 100000,
				});
				this.school_index = e.detail.value;
				this.current = 3;
				let school = this.school_list[this.school_index];
				fetch_data('POST', 'get_users_by_school', {"school": school}, 'user', res => {
					this.user1_url = null;
					this.user2_url = null;
					this.user3_url = null;
					this.users = res.data.users;
					if (res.data.users.length > 0) {
						this.user1_url = res.data.users[0].profile_img;
					}
					if (res.data.users.length > 1) {
						this.user2_url = res.data.users[1].profile_img;
					}
					if (res.data.users.length > 2) {
						this.user3_url = res.data.users[2].profile_img;
					}
					[this.ids, this.my_rank] = utils.get_rank(this.users, this.user.id);
					wx.hideToast();
				})
			},

			active_instruction() {
				wx.showModal({
					title: '活跃度计算规则',
					content: "赛季活跃度反映用户在本赛季参加TJTT积分赛、参与约球、约教、提问等活动的频率。计算方式为：(本赛季完赛积分赛数 × 0.7 + 本赛季匹配成功约球帖数 × 0.1 + 本赛季被采纳提问问题数 × 0.1 + 本赛季约教成功次数 × 0.1) × 100。",
					showCancel: false,
					confirmText: '了解',
				})
			},

		},
		onPullDownRefresh() {
			if (this.user) {
				let data = {"my_id": this.user.id};
				fetch_data("POST", "refresh", data, "user", res => {
					// 异步获取用户排名
					var user_id = this.user.id
					function asyncTask(callback) {
						utils.get_my_rank(user_id);
						callback();
					}
					asyncTask(() => {
						console.log('async task finished');
					})
					uni.setStorageSync('user', res.data.user);
				});
			}
			wx.showToast({
				title: '加载中',
				icon: 'loading',
				duration: 100000,
			});
			login_check(user => {
				this.user = user;
			});
			fetch_data('POST', 'get_users', null, 'user', res => {
				this.users = res.data.users;
				[this.ids, this.my_rank] = utils.get_rank(this.users, this.user.id);
				if (this.users) {
					wx.hideToast();
				}
			})
			uni.reLaunch({
				url: '/pages/score-ranking/index',
			});
			setTimeout(() => {
				uni.stopPullDownRefresh();
			}, 1000);
		},
	}
</script>

<style lang="scss" scoped>
	.school-picker {
	    margin-top: -3rpx;
	    height: 87rpx;
	}
	
	.tabbarList {
		box-sizing: border-box;
		padding: 0rpx 10rpx;
		margin-top: 20rpx;
		font-weight: 400;
		font-size: 25rpx;
		color: #666666;
		line-height: 24rpx;

		.l3L {
			font-weight: 500 !important;
			font-size: 28rpx !important;
			color: #f25c07 !important;
			line-height: 28rpx !important;
		}

		.userSpan {
			margin-left: 20rpx;
			font-weight: 500;
			font-size: 28rpx;
			color: #000000;

			position: relative;
			bottom: 46rpx;
		}

		.userA {
			width: 72rpx;
			height: 72rpx;
			position: relative;
			bottom: 20rpx;
		}

		.headTabA {
			margin-top: 50rpx !important;
		}

		.headTab {
			margin-top: 20rpx;
		}

		.l1L {
			text-align: center !important;
			font-weight: 600;
			font-size: 32rpx;
			color: #666666;
			line-height: 32rpx;
		}

		.l3 {
			text-align: left;
		}

		.l1 {
			text-align: left;
			width: 8%;
		}

		.l2 {
			width: 70%;
		}
	}

	.table_head {
		text-align: center;
		font-weight: normal;
		white-space: nowrap;
		text-overflow: ellipsis;
	}

	.table_content {
		text-align: center;
		font-weight: bold;
		white-space: nowrap;
		text-overflow: ellipsis;
	}

	.search_bar {
		width: 550rpx;
		margin: 15rpx 30rpx;
	}

	.section {
		box-sizing: border-box;
		padding: 20rpx;
		background-color: white;
		margin-top: 16rpx;
		padding-top: 160rpx;

		.pmBgA {
			position: relative;
			top: -90rpx;
		}

		.box {
			.cont {
				text-align: center;
				position: relative;
				bottom: 40rpx;

				.textT {
					position: relative;
					bottom: 40rpx;
					z-index: 99999;
				}

				.tA {
					font-weight: 600;
					font-size: 32rpx;
					color: #000000;
					line-height: 25rpx;
				}

				.tB {
					margin-top: 36rpx;
					font-weight: 400;
					font-size: 24rpx;
					color: #666666;
					line-height: 30rpx;
				}

				.tC {
					margin-top: 36rpx;
					font-weight: 600;
					font-size: 32rpx;
					color: #f25c07;
					line-height: 0rpx;
				}

				.pmBgc {
					position: relative;
					bottom: 40rpx;
					width: 60rpx;
					height: 60rpx;
				}
			}

			.user {
				width: 100rpx;
				height: 100rpx;
			}

			height: 340rpx;
			width: 30%;
			position: relative;

			.pmBg {
				position: absolute;
				width: 100%;
				top: 0%;
				left: 0%;
				height: 310rpx;
			}
		}
	}

	.userPm {
		background-color: white;
		box-sizing: border-box;
		padding: 10rpx 30rpx;

		.left {
			line-height: 100rpx;
			width: 10%;
		}

		.rightL {
			padding-top: 34rpx;
			font-weight: 600;
			font-size: 32rpx;
			color: #f25c07;
			line-height: 32rpx;
			margin-top: 20rpx;
			text-align: center;
		}

		.t1 {
			font-weight: 600;
			font-size: 32rpx;
			color: #000000;
		}

		.t2 {
			margin-top: 8rpx;
			font-weight: 400;
			font-size: 24rpx;
			color: #666666;
		}

		.leftL {
			text-align: center;
			width: 16%;
		}

		.right {
			width: 50%;
			box-sizing: border-box;
			padding-top: 26rpx;
			padding-left: 14rpx;
		}

		.rightL {
			width: 22%;
		}

		.userImg {
			margin-top: 16rpx;
			width: 100rpx;
			height: 100rpx;
		}

		.iconP {
			margin-top: 40rpx;
			width: 60rpx;
			height: 60rpx;
		}
	}

	.head {
		position: relative;

		.topImg {
			width: 100%;
			height: 364rpx;
		}

		.icons {
			position: absolute;
			top: 86rpx;
			left: 50rpx;
			z-index: 999;
		}

		.headTitle {
			font-weight: 600;
			font-size: 36rpx;
			color: #212121;
			line-height: 36rpx;
			position: absolute;
			text-align: center;
			width: 100%;
			top: 86rpx;
			z-index: 999;
		}
	}
</style>