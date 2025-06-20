<template>
	<div class="head">
		<div class="headTitle">TJTT乒乓球一体化平台</div>
	</div>
	<div v-if="user">
		<div class="header">
			<div class="topIcon">
				<img class="icon" src="" alt="" />
				<img class="icon" src="" alt="" />
			</div>
			<div v-if="user" class="userDate flex">
				<button class="btn-outline-sm" @click="logout">退出登录</button>
				<div class="left">
					<img v-if="user.id == 1" class="user" style="border-radius: 50%;"
						src="https://tjtt-assets.oss-cn-shanghai.aliyuncs.com/pictures/admins/bt2.jpg"
						alt="" />
					<img v-else-if="user.gender == '男'" class="user" style="border-radius: 50%;"
						src="https://tjtt-assets.oss-cn-shanghai.aliyuncs.com/pictures/avatars/male.jpg"
						alt="" />
					<img v-else-if="user.gender == '女'" class="user" style="border-radius: 50%;"
						src="https://tjtt-assets.oss-cn-shanghai.aliyuncs.com/pictures/avatars/female.jpg"
						alt="" />
				</div>
				<div class="right">
					<div class="nike">{{user.username}} - {{user.school}}</div>
					<div class="model">{{user.organ.organname}}</div>
				</div>
			</div>
			<div v-else class="userDate flex">
				<button class="btn-outline-sm" style="left: 410rpx" @click="login_page">登录</button>
				<button class="btn-outline-sm" style="left: 570rpx" @click="register_page">注册</button>
				<div class="left">
					<img class="user" style="border-radius: 50%;"
						src="https://tjtt-assets.oss-cn-shanghai.aliyuncs.com/pictures/avatars/player.png"
						alt="" />
				</div>
				<div class="right">
					<div class="nike">请登录</div>
				</div>
			</div>
			<div class="userList flex">
				<div class="itemList">
					<p class="p">{{user.hand}}</p>
					<div class="span">执拍手</div>
				</div>
				<div class="itemList">
					<p class="p">{{user.grip}}</p>
					<div class="span">握拍方式</div>
				</div>
				<div class="itemList">
					<p class="p">{{user.particle}}</p>
					<div class="span">颗粒</div>
				</div>
				<div class="itemList">
					<p class="p">{{user.address}}</p>
					<div class="span">所在地区</div>
				</div>
			</div>
		</div>
		<section style="margin-top: 20rpx;" class="section">
			<div class="box2 flex">
				<div class="boxT">
					<div class="top" @click="rank">
						<div class="tip"></div>
						<div class="myPm">积分排名</div>
						<u-icon class="fr" style="position: relative; top: 5rpx" name="arrow-right"
							color="#212121" size="28" />
					</div>
					<div style="margin-top: 30rpx">
						<div class="tipText">TJTT积分<span class="spanTip"
								style="margin-left: 70rpx;">{{user.score}}</span></div>
						<div class="tipText">排名<span class="spanTip"
								style="margin-left: 130rpx;">{{my_rank}}</span></div>
					</div>
				</div>
				<div class="boxT">
					<div class="top">
						<div class="tip"></div>
						<div class="myPm">赛季徽章</div>
						<u-icon class="fr" style="position: relative; top: 5rpx" name="arrow-right"
							color="#212121" size="28" />
						<div class="tp flex">
							<div class="LEFT">
								<img class="LEFTiCON round"
									src="https://tjtt-assets.oss-cn-shanghai.aliyuncs.com/pictures/logos/badge-S1.jpg"
									alt="" />
							</div>
							<div class="righttP" style="font-weight: 600;">第一赛季<div style="color: red;">
									活跃度：{{user.active}}</div>
							</div>
						</div>
					</div>
				</div>
			</div>
			<div class="userList flex">
				<div class="itemList" style="width: 18%" @click='goAdd' v-for="(item, i) in userListA" :key="i">
					<p class="p">
						<img class="piCon" :src="`../../static/tabbar/Frame (${item.content}).png`"
							alt="" />
					</p>
					<div class="span">{{ item.name }}</div>
				</div>
			</div>
			<div class="phBox">
				<div class="title">最近一场比赛</div>
				<div class="bc flex" @click="match_detail_page(latest_match.id)">
					<div class="left">
						<img class="bcImg" src="https://tjtt-assets.oss-cn-shanghai.aliyuncs.com/pictures/decorations/5.png" alt="" />
					</div>
					<div class="right">
						<div class="text1">{{latest_match.title}}</div>
						<div class="text2">{{latest_match.match_time}}</div>
						<div class="text3">{{latest_match.place}}</div>
					</div>
				</div>
			</div>
			<div class="userList flex">
				<div class="itemList" style="width: 25%; white-space: nowrap;"
					v-for="(item, index) in actionList" :key="index">
					<view v-if="index==0" @click="modify_info">
						<p class="p">
							<u-icon name="setting-fill" size="40" />
						</p>
						<div class="span">{{ item.name }}</div>
					</view>
					<view v-else-if="index==1" @click="modify_psw">
						<p class="p">
							<u-icon name="lock" size="40" />
						</p>
						<div class="span">{{ item.name }}</div>
					</view>
					<view v-else-if="index==2">
						<view v-if="user.privacy==0" @click="set_private">
							<p class="p">
								<u-icon name="account-fill" size="40" />
							</p>
							<div class="span">{{ item.name }}</div>
						</view>
						<view v-else @click="set_public">
							<p class="p">
								<u-icon name="account" size="40" />
							</p>
							<div class="span">设为公开用户</div>
						</view>
					</view>
				</div>
			</div>
			<div class="tipTitle">个人信息</div>
			<div style="margin: 30rpx;">
				<uni-table stripe emptyText="无数据" style="z-index: -1;">
					<uni-tr>
						<uni-td>
							<view class="table_head">性别</view>
						</uni-td>
						<uni-td>
							<view class="table_content">{{user.gender}}</view>
						</uni-td>
					</uni-tr>
					<uni-tr>
						<uni-td>
							<view class="table_head">所在地区</view>
						</uni-td>
						<uni-td>
							<view class="table_content">{{user.address}}</view>
						</uni-td>
					</uni-tr>
					<uni-tr>
						<uni-td>
							<view class="table_head">手机号</view>
						</uni-td>
						<uni-td>
							<view class="table_content">{{user.phone}}</view>
						</uni-td>
					</uni-tr>
					<uni-tr>
						<uni-td>
							<view class="table_head">邮箱</view>
						</uni-td>
						<uni-td>
							<view class="table_content">{{user.email}}</view>
						</uni-td>
					</uni-tr>
					<uni-tr>
						<uni-td>
							<view class="table_head">学校</view>
						</uni-td>
						<uni-td>
							<view class="table_content">{{user.school}}</view>
						</uni-td>
					</uni-tr>
					<uni-tr>
						<uni-td>
							<view class="table_head">身份</view>
						</uni-td>
						<uni-td>
							<view class="table_content">{{user.role}}</view>
						</uni-td>
					</uni-tr>
					<uni-tr>
						<uni-td>
							<view class="table_head">学号 / 工号</view>
						</uni-td>
						<uni-td>
							<view class="table_content">{{user.stu_num}}</view>
						</uni-td>
					</uni-tr>
					<uni-tr>
						<uni-td>
							<view class="table_head">所属组织</view>
						</uni-td>
						<uni-td>
							<view class="table_content">{{user.organ.organname}}</view>
						</uni-td>
					</uni-tr>
					<uni-tr>
						<uni-td>
							<view class="table_head">执拍手</view>
						</uni-td>
						<uni-td>
							<view class="table_content">{{user.hand}}</view>
						</uni-td>
					</uni-tr>
					<uni-tr>
						<uni-td>
							<view class="table_head">握拍方式</view>
						</uni-td>
						<uni-td>
							<view class="table_content">{{user.grip}}</view>
						</uni-td>
					</uni-tr>
					<uni-tr>
						<uni-td>
							<view class="table_head">底板型号</view>
						</uni-td>
						<uni-td>
							<view class="table_content">{{user.blade}}</view>
						</uni-td>
					</uni-tr>
					<uni-tr>
						<uni-td>
							<view class="table_head">正手胶皮</view>
						</uni-td>
						<uni-td>
							<view class="table_content">{{user.forehand}}</view>
						</uni-td>
					</uni-tr>
					<uni-tr>
						<uni-td>
							<view class="table_head">反手胶皮</view>
						</uni-td>
						<uni-td>
							<view class="table_content">{{user.backhand}}</view>
						</uni-td>
					</uni-tr>
					<uni-tr>
						<uni-td>
							<view class="table_head">是否带颗粒</view>
						</uni-td>
						<uni-td>
							<view class="table_content">{{user.particle}}</view>
						</uni-td>
					</uni-tr>
					<uni-tr>
						<uni-td>
							<view class="table_head">是否为私密用户</view>
						</uni-td>
						<uni-td v-if="user.privacy==1">
							<view class="table_content" style="color: red;">是</view>
						</uni-td>
						<uni-td v-else>
							<view class="table_content" style="color: red;">否</view>
						</uni-td>
					</uni-tr>
				</uni-table>
			</div>
		</section>
		<div style="height: 150rpx;"></div>
		<tabbar :current-page="4"></tabbar>
	</div>

	<div v-else>
		<div class="header">
			<div class="topIcon">
				<img class="icon" src="" alt="" />
				<img class="icon" src="" alt="" />
			</div>
			<div class="userDate flex">
				<button class="btn-outline-sm" style="left: 250rpx" open-type="getUserInfo" @getuserinfo="wx_login">微信一键登录</button>
				<button class="btn-outline-sm" style="left: 410rpx" @click="login_page">登录</button>
				<button class="btn-outline-sm" style="left: 570rpx" @click="register_page">注册</button>
				<div class="left">
					<img class="user" style="border-radius: 50%;"
						src="https://tjtt-assets.oss-cn-shanghai.aliyuncs.com/pictures/avatars/player.png"
						alt="" />
				</div>
				<div class="right">
					<div class="nike">请登录</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
	import {
		fetch_data
	} from '../../static/js/ajax_request.js'
	import {
		login_check
	} from '../../static/js/login_check.js'

	export default {
		data() {
			return {
				user: "",
				my_rank: "",
				latest_match: "",
				userList: [{
						name: "执拍手",
					},
					{
						name: "握拍方式",
					},
					{
						name: "颗粒",
					},
					{
						name: "所在地区",
					},
				],
				actionList: [{
						name: "修改个人信息",
					},
					{
						name: "修改密码",
					},
					{
						name: "设为私密用户",
					},
				],
			}
		},
		onLoad() {
			login_check(user => {
				this.user = user;
			});
			this.my_rank = wx.getStorageSync('my_rank');

			fetch_data("POST", "match_list", {
				"range": "c_matches",
				"my_id": this.user.id
			}, "competition", res => {
				this.latest_match = res.data.matches[0];
			});
		},
		methods: {
			modify_info() {
				uni.navigateTo({
					url: '/pages/my/modify-info',
				})
			},

			modify_psw() {
				uni.navigateTo({
					url: '/pages/my/modify-psw',
				})
			},

			match_detail_page(match_id) {
				uni.setStorageSync('match_id', match_id)
				uni.navigateTo({
					url: '/page_subjec/match/detail',
				});
			},

			set_private() {
				wx.showModal({
					title: '设为私密用户',
					content: '设为私密用户后，您在“积分排名”中将以“' + this.user.username[0] + '** ”显示。',
					success: res => {
						if (res.confirm) {
							let data = {
								"my_id": this.user.id,
								"user_id": "",
								"set": "private",
							}
							fetch_data("POST", "set_privacy", data, "user", res => {
								console.log(res.data.message);
								wx.showToast({
									title: res.data.message,
									icon: "none",
									duration: 1000,
								});
								if (res.data.status == 200) {
									uni.setStorageSync('user', res.data
										.user); // 存到本地缓存
									this.user = res.data.user;
									setTimeout(() => {
										uni.reLaunch({
											url: '/pages/my/index',
										})
									}, 1000);
								}
							})
						}
					}
				})
			},

			set_public() {
				wx.showModal({
					title: '设为公开用户',
					content: '设为公开用户后，您在“积分排名”中将以全名显示。',
					success: res => {
						if (res.confirm) {
							let data = {
								"my_id": this.user.id,
								"user_id": "",
								"set": "public",
							}
							fetch_data("POST", "set_privacy", data, "user", res => {
								console.log(res.data.message);
								wx.showToast({
									title: res.data.message,
									icon: "none",
									duration: 1000,
								});
								if (res.data.status == 200) {
									uni.setStorageSync('user', res.data
										.user); // 存到本地缓存
									this.user = res.data.user;
									setTimeout(() => {
										uni.reLaunch({
											url: '/pages/my/index',
										})
									}, 1000);
								}
							})
						}
					}
				})
			},

			logout() {
				uni.clearStorageSync();
				uni.reLaunch({
					url: '/pages/my/index',
				})
				console.log("已退出登录")
			},

			login_page() {
				uni.navigateTo({
					url: '/pages/login/login',
				})
			},

			register_page() {
				uni.navigateTo({
					url: '/pages/login/register',
				})
			},

			wx_login(e) {
				console.log(e)
				wx.login({
					success: res => {
						if (res.code) {
							let URL =
								'https://api.weixin.qq.com/sns/jscode2session?appid=wxb0c7089038505d64&secret=2db7b2e7689d6bf2dd57eddd5c67f7e8&js_code=' +
								res.code + '&grant_type=authorization_code'
							wx.request({
								url: URL,
								success: function(res) {
									console.log(res.data)
								},
								fail: function(err) {
									console.log("登录失败" + err.errMsg)
								}
							})
						}
					}
				})
				// wx.getUserProfile({
				// 	desc: '用于完善会员资料',
				// 	success: (res) => {
				// 		if (res.errMsg === "getUserProfile:ok") {
				// 			wx.login({
				// 				success: res => {
				// 					if (res.code) {
				// 						let URL =
				// 							'https://api.weixin.qq.com/sns/jscode2session?appid=wxb0c7089038505d64&secret=2db7b2e7689d6bf2dd57eddd5c67f7e8&js_code=' +
				// 							res.code + '&grant_type=authorization_code'
				// 						wx.request({
				// 							url: URL,
				// 							success: function(res) {
				// 								console.log(res.data)
				// 							},
				// 							fail: function(err) {
				// 								console.log("登录失败" + err.errMsg)
				// 							}
				// 						})
				// 					}
				// 				}
				// 			})
				// 		}
				// 	}
				// })
			},
		},
	}
</script>

<script setup>
	import {
		ref
	} from "vue";
	let userListA = ref([{
			name: "待付款",
			content: 3,
		},
		{
			name: "待开始",
			content: 4,
		},
		{
			name: "进行中",
			content: 5,
		},
		{
			name: "已完成",
			content: 6,
		},
		{
			name: "赛事报名",
			content: 7,
		},
	]);
	const goAdd = () => {
		uni.navigateTo({
			url: '/page_subjec/match/index?id=',
		})
	}
	const rank = () => {
		uni.navigateTo({
			url: '/pages/score-ranking/index?id=',
		})
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
		}
	}

	.btn-outline-sm {
		position: absolute;
		display: inline-block;
		padding: 1rem 1.5rem 1rem 1.5rem;
		border: 1px solid #f25c05;
		border-radius: 30px;
		background-color: transparent;
		color: #f25c05;
		font-weight: 600;
		font-size: 0.875rem;
		line-height: 0;
		text-decoration: none;
		transition: all 0.2s;
		top: 210rpx;
		left: 520rpx;
	}

	.btn-modify {
		position: relative;
		display: inline-block;
		padding: 1rem 1.5rem 1rem 1.5rem;
		border: 1px solid #00ffff;
		border-radius: 30px;
		background-color: transparent;
		color: #00ffff;
		font-weight: 600;
		font-size: 0.875rem;
		line-height: 0;
		text-decoration: none;
		transition: all 0.2s;
		top: 18rpx;
		left: 15rpx;
	}

	.dropdown1 {
		position: absolute;
		width: 300rpx;
		top: 1180rpx;
		z-index: 999;
	}

	.topIcon {
		margin-top: 30rpx;
	}

	.imgs {
		margin-top: 20rpx;
		width: 48%;
		border-radius: 12rpx;
		height: 190rpx;
	}

	.tipTitle {
		position: relative;
		margin-top: 55rpx;
		font-family: PingFang SC, PingFang SC;
		font-weight: 600;
		font-size: 32rpx;
		color: #212121;
		line-height: 36rpx;
		text-align: left;
		font-style: normal;
		text-transform: none;
	}

	.phBox {
		background: linear-gradient(320deg, #f7eddd 0%, #edd3bc 100%);
		border-radius: 0rpx 0rpx 20rpx 20rpx;
		box-sizing: border-box;
		padding: 26rpx 16rpx;
		padding-top: 40rpx;

		.bc {
			border-radius: 12rpx 12rpx 12rpx 12rpx;

			.text1 {
				margin-top: 4rpx;
				font-family: PingFang SC, PingFang SC;
				font-weight: bold;
				font-size: 28rpx;
				color: #282456;
				line-height: 30rpx;
				text-align: left;
				font-style: normal;
				text-transform: none;
			}

			.text2 {
				margin-top: 19rpx;
				font-family: PingFang SC, PingFang SC;
				font-weight: 600;
				font-size: 24rpx;
				color: #f25c07;
				line-height: 10rpx;
				text-align: left;
				font-style: normal;
				text-transform: none;
			}

			.text3 {
				margin-top: 27rpx;
				font-family: PingFang SC, PingFang SC;
				font-weight: 400;
				font-size: 24rpx;
				color: #666666;
				line-height: 0rpx;
				text-align: left;
				font-style: normal;
				text-transform: none;
			}

			.right {
				width: 62%;
			}

			.left {
				width: 34%;

				.bcImg {
					border-radius: 6rpx 6rpx 6rpx 6rpx;
					width: 100%;
					height: 130rpx;
				}
			}

			margin-top: 30rpx;
			background-color: white;
			box-sizing: box-sizing;
			padding: 18rpx 14rpx;
		}

		.title {
			font-family: PingFang SC, PingFang SC;
			font-weight: 600;
			font-size: 28rpx;
			color: #212121;
			line-height: 24rpx;
			text-align: left;
			font-style: normal;
			text-transform: none;
			margin-top: 20rpx;
		}
	}

	.piCon {
		width: 44rpx;
		height: 44rpx;
	}

	.table_head {
		width: 200rpx;
		text-align: center;
		font-weight: normal;
		white-space: nowrap;
		text-overflow: ellipsis;
	}

	.table_content {
		width: 400rpx;
		text-align: center;
		font-weight: bold;
		white-space: nowrap;
		text-overflow: ellipsis;
	}

	.section {
		box-sizing: border-box;
		padding: 20rpx 32rpx;
		box-sizing: border-box;
		padding-top: 90rpx;
	}

	.box2 {
		.tp {
			box-sizing: box-sizing;
			padding: 0rpx 18rpx;
			margin-top: 40rpx;
		}

		.boxT {
			box-sizing: box-sizing;
			padding: 20rpx;
			background-color: #ffffff;
			width: 48%;

			border-radius: 20rpx 20rpx 20rpx 20rpx;

			.LEFTiCON {
				width: 85rpx;
				height: 85rpx;
			}

			.myPm {
				margin-left: 14rpx;
				display: inline-block;
				font-family: PingFang SC, PingFang SC;
				font-weight: 600;
				font-size: 32rpx;
				color: #212121;
				line-height: 40rpx;
				text-align: left;
				font-style: normal;
				text-transform: none;
			}

			.righttP {
				width: 60%;
				font-family: PingFang SC, PingFang SC;
				font-weight: 500;
				font-size: 28rpx;
				color: #212121;
				line-height: 28rpx;
				text-align: center;
				line-height: 40rpx;
				font-style: normal;
				text-transform: none;
			}

			.tipText {
				font-size: 28rpx;
				color: #666666;
				margin-top: 12rpx;
				margin-left: 20rpx;
			}

			.spanTip {
				color: #f25c07;
				font-weight: bold;
			}

			.tip {
				display: inline-block;
				width: 6rpx;
				height: 20rpx;
				background: #f25c07;
				border-radius: 12rpx 12rpx 12rpx 12r;
			}
		}
	}

	.userList {
		position: relative;
		top: 30rpx;
		box-sizing: box-sizing;
		padding: 28rpx 20rpx;
		background: #ffffff;
		border-radius: 20rpx 20rpx 20rpx 20rpx;

		.p {
			font-family: PingFang SC, PingFang SC;
			font-weight: 600;
			font-size: 36rpx;
			color: #282456;
			line-height: 40rpx;
			text-align: center;
			font-style: normal;
			text-transform: none;
		}
	}

	.itemList {
		text-align: center;
		width: 24%;
	}

	.user {
		width: 120rpx;
		height: 120rpx;
		border-radius: 0rpx 0rpx 0rpx 0rpx;
	}

	.span {
		margin-top: 24rpx;
		font-family: PingFang SC, PingFang SC;
		font-weight: 400;
		font-size: 24rpx;
		color: #666666;
		line-height: 24rpx;
		text-align: center;
		font-style: normal;
		text-transform: none;
	}

	.header {
		background: linear-gradient(135deg, #FEF2DA, #FFD5A4);
		width: 100%;
		height: 400rpx;
		box-sizing: border-box;
		padding: 30rpx;
		padding-top: 60rpx;

		.icon {
			margin-right: 20rpx;
			width: 37rpx;
			height: 37rpx;
		}

		.userDate {
			margin-top: 50rpx;
		}

		.nike {
			font-family: PingFang SC, PingFang SC;
			font-weight: 600;
			font-size: 36rpx;
			color: #282456;
			line-height: 36rpx;
			text-align: left;
			font-style: normal;
			text-transform: none;
		}

		.left {
			width: 20%;
		}

		.right {
			width: 80%;
			box-sizing: border-box;
			padding-top: 20rpx;
		}

		.model {
			font-family: PingFang SC, PingFang SC;
			font-weight: 400;
			font-size: 24rpx;
			color: #666666;
			line-height: 24rpx;
			margin-top: 20rpx;
			margin-left: 8rpx;
			font-style: normal;
			text-transform: none;
		}
	}
</style>