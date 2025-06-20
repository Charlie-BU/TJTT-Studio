<template>
	<div class="head">
		<div class="headTitle">TJTT乒乓球一体化平台</div>
	</div>
	<div>
		<div class="header">
			<div class="topIcon">
				<img class="icon" src="" alt="" />
				<img class="icon" src="" alt="" />
			</div>
			<div class="userDate flex">
				<div class="left" @click="img_operation">
					<img class="user" :src="this_season.badge_url" alt="" />
				</div>
				<div class="right">
					<div class="nike">{{ this_season.season_name }}</div>
					<div class="model">{{ formatted_time[0].split(' ')[0] }} — {{ formatted_time[1].split(' ')[0] }}</div>
				</div>
			</div>
			<div class="userList flex">
				<div class="itemList">
					<p class="p">{{ matches_length }}场</p>
					<div class="span">总参加赛事</div>
				</div>
				<div class="itemList">
					<p class="p">{{ win_length }} / {{ lose_length }}场</p>
					<div class="span">胜 / 负</div>
				</div>
				<div class="itemList">
					<p class="p">{{ (end_score - start_score) > 0 ? '+' : '' }}{{ end_score - start_score }}</p>
					<div class="span">积分净变更</div>
				</div>
				<div class="itemList" @click="active_instruction">
					<p class="p" style="color: red;">{{ user.active }}</p>
					<div class="span" style="color: red;">赛季活跃度</div>
				</div>
			</div>
			<div class="userList flex" style="margin-top: 20rpx;">
				<div class="itemList">
					<p class="p">{{ my_valid_posts_length }}次</p>
					<div class="span">有效约球</div>
				</div>
				<div class="itemList">
					<p class="p">{{ my_valid_train_length }}次</p>
					<div class="span">有效约教</div>
				</div>
				<div class="itemList">
					<p class="p">{{ my_valid_questions_length }}个</p>
					<div class="span">被采纳问题</div>
				</div>
			</div>
		</div>
		<section class="section">
			<div class="box2 flex" style="margin-top: 20rpx;">
				<div class="boxT" @click="standard_page">
					<div class="tp flex">
						<div class="LEFT">
							<img class="LEFTiCON round" src="https://tjtt-assets.oss-cn-shanghai.aliyuncs.com/pictures/logos/deco6.png" alt="" />
						</div>
						<div class="righttP">TJTT积分赛
							<div class="righttQ">积分标准</div>
						</div>
					</div>
				</div>
				<div class="boxT" @click="match_page">
					<div class="tp flex">
						<div class="LEFT">
							<img class="LEFTiCON round" src="https://tjtt-assets.oss-cn-shanghai.aliyuncs.com/pictures/logos/deco8.png" alt="" />
						</div>
						<div class="righttP">TJTT积分赛
							<div class="righttQ">赛事报名</div>
						</div>
					</div>
				</div>
			</div>
			<div class="box2 flex" style='margin-top: 30rpx;'>
				<div class="boxT" @click="community_page">
					<div class="tp flex">
						<div class="LEFT">
							<img class="LEFTiCON round" src="https://tjtt-assets.oss-cn-shanghai.aliyuncs.com/pictures/logos/deco5.png" alt="" />
						</div>
						<div class="righttP">以乒会友
							<div class="righttQ">约球约教</div>
						</div>
					</div>
				</div>
				<div class="boxT" @click="athlete_page">
					<div class="tp flex">
						<div class="LEFT">
							<img class="LEFTiCON round" src="https://tjtt-assets.oss-cn-shanghai.aliyuncs.com/pictures/logos/athlete.png" alt="" />
						</div>
						<div class="righttP">运动员
							<div class="righttQ">全方位介绍</div>
						</div>
					</div>
				</div>
			</div>
			<div class="box2 flex" style='margin-top: 30rpx;'>
				<div class="boxT" @click="match_forcast_page">
					<div class="tp flex">
						<div class="LEFT">
							<img class="LEFTiCON round" src="https://tjtt-assets.oss-cn-shanghai.aliyuncs.com/pictures/logos/paris-olympics-logo.png" alt="" />
						</div>
						<div class="righttP">重大赛事
							<div class="righttQ">观赛预告</div>
						</div>
					</div>
				</div>
				<div class="boxT" @click="store_page">
					<div class="tp flex">
						<div class="LEFT">
							<img class="LEFTiCON round" src="https://tjtt-assets.oss-cn-shanghai.aliyuncs.com/pictures/logos/deco3.png" alt="" />
						</div>
						<div class="righttP">乒乓闲鱼
							<div class="righttQ">正版器材</div>
						</div>
					</div>
				</div>
			</div>
			<div class="box2 flex" style='margin-top: 30rpx;'>
				<div class="boxT" @click="chat_room_page">
					<div class="tp flex">
						<div class="LEFT">
							<img class="LEFTiCON round" src="https://tjtt-assets.oss-cn-shanghai.aliyuncs.com/pictures/logos/deco10.png" alt="" />
						</div>
						<div class="righttP">乒乓贴吧
							<div class="righttQ">聊天分享</div>
						</div>
					</div>
				</div>
				<div class="boxT" @click="athlete_auth_page">
					<div class="tp flex">
						<div class="LEFT">
							<img class="LEFTiCON round" src="https://tjtt-assets.oss-cn-shanghai.aliyuncs.com/pictures/logos/deco9.png" alt="" />
						</div>
						<div class="righttP">运动员认证
							<div class="righttQ">专属徽章</div>
						</div>
					</div>
				</div>
			</div>
			<div class="box2 flex" style='margin-top: 30rpx;'>
				<div class="boxT" @click="TJTTers_page">
					<div class="tp flex">
						<div class="LEFT">
							<img class="LEFTiCON round" src="https://tjtt-assets.oss-cn-shanghai.aliyuncs.com/pictures/logos/logo1.1.png" alt="" />
						</div>
						<div class="righttP">TJTT工作室
							<div class="righttQ">成员介绍</div>
						</div>
					</div>
				</div>
				<div class="boxT" @click="send_feedback">
					<div class="tp flex">
						<div class="LEFT">
							<img class="LEFTiCON round" src="https://tjtt-assets.oss-cn-shanghai.aliyuncs.com/pictures/decorations/feedback.png" alt="" />
						</div>
						<div class="righttP">意见反馈
							<div class="righttQ">投诉建议</div>
						</div>
					</div>
				</div>
			</div>
		</section>
	</div>
	<div style="visibility: hidden;">————————</div>
	<div style="visibility: hidden;">————————</div>
	<div style="visibility: hidden;">————————</div>
	<tabbar :current-page="1"></tabbar>
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
				this_season: "",
				matches_length: "",
				win_length: "",
				lose_length: "",
				start_score: "",
				end_score: "",
				my_valid_posts_length: "",
				my_valid_train_length: 0,
				my_valid_questions_length: "",
				hide_this: magic(),
			}
		},
		computed: {
		    formatted_time() {
		        if (this.this_season && this.this_season.start_time && this.this_season.end_time) {
		            return [utils.format_time(this.this_season.start_time), utils.format_time(this.this_season.end_time)];
		        } else {
		            return ["", ""];
		        };
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
			// 获取赛季信息
			fetch_data("POST", "get_this_season", null, "competition", res => {
				this.this_season = res.data.this_season;
				const data = {
					'my_id': this.user.id,
					'season_id': this.this_season.id,
				};
				fetch_data("POST", "get_user_season_recording", data, "user", res => {
					this.matches_length = res.data.matches_length
					this.win_length = res.data.win_length
					this.lose_length = res.data.lose_length
					this.start_score = res.data.start_score
					this.end_score = res.data.end_score
				});
				fetch_data('POST', 'cal_active', { 'user_id': this.user.id }, 'user', res => {
					this.my_valid_posts_length = res.data.my_valid_posts_length;
					this.my_valid_questions_length = res.data.my_valid_questions_length;
				});
			});
		},
		methods: {
			img_operation() {
				let avatarUrl = this.this_season.badge_url;
				if (avatarUrl) {
					wx.previewImage({
						urls: [avatarUrl],
						current: avatarUrl,
					});
				};
			},
			
			active_instruction() {
				wx.showModal({
					title: '活跃度计算规则',
					content: "赛季活跃度反映用户在本赛季参加TJTT积分赛、参与约球、约教、提问等活动的频率。计算方式为：(本赛季完赛积分赛数 × 0.7 + 本赛季匹配成功约球帖数 × 0.1 + 本赛季被采纳提问问题数 × 0.1 + 本赛季约教成功次数 × 0.1) × 100。",
					showCancel: false,
					confirmText: '了解',
				})
			},
			
			standard_page() {
				if (this.hide_this) {
					return;
				}
				uni.navigateTo({
					url: '/pages/apps/standard',
				});
			},
			
			match_page() {
				if (this.hide_this) {
					return;
				}
				uni.navigateTo({
					url: '/page_subjec/match/index',
				});
			},
			
			community_page() {
				if (this.hide_this) {
					return;
				}
				uni.switchTab({
					url: '/pages/community/index',
				});
			},
			
			store_page() {
				if (this.hide_this) {
					return;
				}
				wx.showToast({
					title: "该功能暂未上线，敬请期待",
					icon: "none",
					duration: 1000,
				});
			},
			
			athlete_page() {
				if (this.hide_this) {
					return;
				}
				// wx.showToast({
				// 	title: "该功能暂未上线，敬请期待",
				// 	icon: "none",
				// 	duration: 1000,
				// });
				uni.navigateTo({
					url: '/pages/apps/athlete',
				})
			},
			
			match_forcast_page() {
				if (this.hide_this) {
					return;
				}
				wx.showToast({
					title: "该功能暂未上线，敬请期待",
					icon: "none",
					duration: 1000,
				});
			},
			
			chat_room_page() {
				if (this.hide_this) {
					return;
				}
				wx.showToast({
					title: "该功能暂未上线，敬请期待",
					icon: "none",
					duration: 1000,
				});
			},
			
			athlete_auth_page() {
				if (this.hide_this) {
					return;
				}
				wx.showToast({
					title: "该功能暂未上线，敬请期待",
					icon: "none",
					duration: 1000,
				});
			},
			
			
			TJTTers_page() {
				if (this.hide_this) {
					return;
				}
				uni.navigateTo({
					url: '/pages/apps/TJTTers',
				})
			},
			
			send_feedback() {
				if (this.hide_this) {
					return;
				}
				wx.showModal({
					title: "用户反馈",
					placeholderText: "提交后反馈内容将自动发送至TJTT邮箱",
					editable: true,
					confirmText: "提交",
					success: res => {
						if (res.confirm) {
							let data = {
								"my_id": this.user.id,
								"feedback": res.content,
							}
							fetch_data("POST", "send_feedback", data, "user", res => {
								wx.showToast({
									title: res.data.message,
									icon: "none",
									duration: 1200,
								});
							})
						}
					}
				})
			},
		},
		onPullDownRefresh() {
			uni.reLaunch({
				url: '/pages/apps/index',
			});
			setTimeout(() => {
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
		}
	}

	.topIcon {
		margin-top: 30rpx;
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

	.section {
		box-sizing: border-box;
		padding: 20rpx 32rpx;
		padding-top: 90rpx;
		margin-top: 160rpx;
	}

	.box2 {
		display: flex;
		flex-wrap: wrap;
		justify-content: space-between;

		.boxT {
			box-sizing: border-box;
			padding: 20rpx;
			background: linear-gradient(180deg, #fef2da, #f9d5a5);
			width: 48%;
			border-radius: 20rpx;
			display: flex;
			align-items: center;
			justify-content: center;

			.tp {
				display: flex;
				align-items: center;
				justify-content: center;
				text-align: center;
			}

			.LEFT {
				display: flex;
				align-items: center;
				justify-content: center;
				margin-right: 20rpx;
			}

			.LEFTiCON {
				width: 85rpx;
				height: 85rpx;
			}

			.righttP {
				font-family: PingFang SC, PingFang SC;
				font-weight: 500;
				font-size: 28rpx;
				font-weight: bold;
				color: #212121;
				text-align: center;

				.righttQ {
					color: red;
					margin-top: 10rpx;
				}
			}
		}
	}

	.userList {
		position: relative;
		top: 30rpx;
		box-sizing: border-box;
		padding: 28rpx 20rpx;
		background: #ffffff;
		border-radius: 20rpx;

		.p {
			font-family: PingFang SC, PingFang SC;
			font-weight: 600;
			font-size: 36rpx;
			color: #282456;
			line-height: 40rpx;
			text-align: center;
		}
	}

	.itemList {
		text-align: center;
		width: 24%;
	}

	.user {
		width: 120rpx;
		height: 120rpx;
		border-radius: 50%;
	}

	.span {
		margin-top: 24rpx;
		font-family: PingFang SC, PingFang SC;
		font-weight: 400;
		font-size: 24rpx;
		color: #666666;
		line-height: 24rpx;
		text-align: center;
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
		}
	}
</style>
