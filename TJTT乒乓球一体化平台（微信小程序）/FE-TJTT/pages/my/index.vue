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
			<div class="userDate flex">
				<button class="btn-outline-sm" @click="logout">退出登录</button>
				<div class="left" @click="avatar_operation">
					<img v-if="user.profile_img" class="user" style="border-radius: 50%;"
						:src="user.profile_img" alt="" />
					<img v-else-if="user.gender == '男'" class="user" style="border-radius: 50%;"
						src="https://tjtt-assets.oss-cn-shanghai.aliyuncs.com/pictures/avatars/male.jpg" alt="" />
					<img v-else-if="user.gender == '女'" class="user" style="border-radius: 50%;"
						src="https://tjtt-assets.oss-cn-shanghai.aliyuncs.com/pictures/avatars/female.jpg" alt="" />
				</div>
				<div class="right">
					<div class="nike">{{user.username}} - {{user.school}}</div>
					<div v-if="user.organ" class="model">{{user.organ.organname}}</div>
				</div>
			</div>
			<div class="userList flex">
				<div class="itemList">
					<p v-if="user.hand" class="p">{{user.hand}}</p>
					<p v-else class="p" style="color: red;" @click="modify_info">待完善</p>
					<div class="span">执拍手</div>
				</div>
				<div class="itemList">
					<p v-if="user.grip" class="p">{{user.grip}}</p>
					<p v-else class="p" style="color: red;" @click="modify_info">待完善</p>
					<div class="span">握拍方式</div>
				</div>
				<div class="itemList">
					<p v-if="user.particle" class="p">{{user.particle}}</p>
					<p v-else class="p" style="color: red;" @click="modify_info">待完善</p>
					<div class="span">颗粒</div>
				</div>
				<div class="itemList">
					<p v-if="user.address" class="p">{{user.address}}</p>
					<p v-else class="p" style="color: red;" @click="modify_info">待完善</p>
					<div class="span">所在地区</div>
				</div>
			</div>
		</div>
		<section style="margin-top: 20rpx;" class="section">
			<div class="box2 flex">
				<div class="boxT" @click="rank">
					<div class="top">
						<div class="tip"></div>
						<div class="myPm">积分排名</div>
						<u-icon class="fr" style="position: relative; top: 5rpx" name="arrow-right"
							color="#212121" size="28" />
					</div>
					<div style="margin-top: 30rpx">
						<div class="tipText">TJTT积分<span class="spanTip">{{user.score}}</span></div>
						<div class="tipText">全国排名<span class="spanTip">{{my_rank}}</span></div>
					</div>
				</div>
				<div class="boxT">
					<div class="top">
						<div class="tip"></div>
						<div class="myPm">赛季徽章</div>
						<div class="tp flex">
							<div class="LEFT">
								<img class="LEFTiCON round" :src="this_season.badge_url" alt="" @click="image_operation(this_season.badge_url)" />
							</div>
							<div class="righttP" style="font-weight: 600;">{{ this_season.season_name }}<div style="color: red;">活跃度：{{ user.active }}</div></div>
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
					<div class="span" style="white-space: nowrap;">{{ item.name }}</div>
				</div>
			</div>
			<div class="phBox">
				<div class="title">最近一场比赛</div>
				<div v-if="latest_match" class="bc flex" @click="match_detail_page(latest_match.id)">
					<div class="left">
						<img class="bcImg" src="https://tjtt-assets.oss-cn-shanghai.aliyuncs.com/pictures/decorations/5.png" alt="" />
					</div>
					<div class="right">
						<div class="wrapper">
							<div class="text1">{{latest_match.title}}</div>
						</div>
						<div class="text2">{{utils.format_time(latest_match.match_time)}}</div>
						<div class="text3">{{latest_match.place}}</div>
					</div>
				</div>
				<div v-else class="bc flex">
					<div class="left">
						<img class="bcImg" src="https://tjtt-assets.oss-cn-shanghai.aliyuncs.com/pictures/decorations/5.png" alt="" />
					</div>
					<div class="right">
						<div class="text1" style="margin: 50rpx 40rpx;">当前暂无赛事，敬请期待</div>
					</div>
				</div>
			</div>
			<div v-if="!hide_this" class="userList flex">
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
							<u-icon name="lock-fill" size="40" />
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
				
				<view v-if="user.usertype=='K9' || user.usertype=='K10' || user.usertype=='K11'" @click="management_page">
					<p class="p">
						<u-icon name="integral-fill" size="40" />
					</p>
					<div class="span">TJTT平台管理</div>
				</view>
				<view v-else @click="wx_bind">
					<p class="p">
						<u-icon name="weixin-fill" size="40" />
					</p>
					<div class="span">微信绑定</div>
				</view>
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
							<view v-if="user.organ" class="table_content">{{user.organ.organname}}</view>
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
				<button class="btn-outline-sm" style="left: 395rpx" @click="login_page">登录</button>
				<button v-if="!hide_this" class="btn-outline-sm" style="left: 570rpx" @click="register_page">注册</button>
				<div class="left">
					<img class="user" style="border-radius: 50%;"
						src="https://tjtt-assets.oss-cn-shanghai.aliyuncs.com/pictures/avatars/player.png" alt="" />
				</div>
				<div class="right">
					<div class="nike">请登录</div>
				</div>
			</div>
		</div>
		<tabbar :current-page="4"></tabbar>
	</div>
</template>

<script>
	import { fetch_data } from '../../static/js/ajax_request.js'
	import { login_check } from '../../static/js/login_check.js'
	import { magic } from '../../static/js/magic_power.js'
	import * as utils from '../../static/js/utils.js'

	export default {
		data() {
			return {
				user: "",
				my_rank: "",
				this_season: "",
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
				hide_this: magic(),
			}
		},
		onLoad() {
			login_check(user => {
				this.user = user;
			});
			this.my_rank = wx.getStorageSync('my_rank');
			
			fetch_data("POST", "match_list_current", null, "competition", res => {
				this.latest_match = res.data.matches[0];
			});
			// 获取赛季信息
			fetch_data("POST", "get_this_season", null, "competition", res => {
				this.this_season = res.data.this_season;
			});
		},
		
		methods: {
			avatar_operation() {
				wx.showActionSheet({
					itemList: ['查看头像', '更换头像'],
					success: (res) => {
						if (!res.cancel) {
							if (res.tapIndex == 0) {
								let avatarUrl = this.user.profile_img;
								if (avatarUrl) {
									wx.previewImage({
										urls: [avatarUrl],
										current: avatarUrl,
									});
								}
								else {
									wx.showToast({
										title: "您还未上传头像",
										icon: "none",
										duration: 1000,
									});
									return;
								}
								
							}
							else if (res.tapIndex == 1) {
								wx.showToast({
									title: "请联系TJTT工作室成员",
									icon: "none",
									duration: 1000,
								});
								return;
							};
						}
					}
				})
			},
			
			image_operation(image_url) {
				wx.previewImage({
					urls: [image_url],
					current: image_url,
				});
			},
			
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
				if (this.hide_this) {
					return;
				}
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
								wx.showToast({
									title: res.data.message,
									icon: "none",
									duration: 1000,
								});
								if (res.data.status == 200){
									fetch_data("POST", "refresh", {"my_id": this.user.id}, "user", res => {
										uni.setStorageSync('user', res.data.user);
									});
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
								wx.showToast({
									title: res.data.message,
									icon: "none",
									duration: 1000,
								});
								if (res.data.status == 200){
									fetch_data("POST", "refresh", {"my_id": this.user.id}, "user", res => {
										uni.setStorageSync('user', res.data.user);
									});
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
			wx_bind() {
				uni.navigateTo({
					url: '/pages/login/wx-bind',
				})
			},
			
			management_page() {
				uni.navigateTo({
					url: '/pages/management/index',
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
			uni.reLaunch({
				url: '/pages/my/index',
			});
			setTimeout(() => {
				uni.stopPullDownRefresh();
			}, 1000);
		}
	}
</script>

<script setup>
	import {
		ref
	} from "vue";
	let userListA = ref([
		{
			name: "当前赛事",
			content: 4,
		},
		{
			name: "已报名赛事",
			content: 6,
		},
		{
			name: "历史赛事",
			content: 5,
		},
		{
			name: "全部赛事",
			content: 7,
		},
	]);
	const goAdd = () => {
		uni.navigateTo({
			url: '/page_subjec/match/index?id=',
		})
	}
	const rank = () => {
		uni.reLaunch({
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

	.topIcon {
		margin-top: 30rpx;
	}

	.wrapper {
		margin-top: 7rpx;
		height: 55rpx;
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
					border-radius: 10%;
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
			    display: flex;
			    justify-content: space-between;
			    align-items: center;
			    margin-bottom: 10rpx;
			}
			
			.spanTip {
			    color: #f25c07;
			    font-weight: bold;
			    margin-right: 20rpx;
			    text-align: right;
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
		background: linear-gradient(180deg, #f9d5a5, #fef2da);
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
	
	::v-deep .uni-table {
		background-color: #f8f8f8;
	}
</style>