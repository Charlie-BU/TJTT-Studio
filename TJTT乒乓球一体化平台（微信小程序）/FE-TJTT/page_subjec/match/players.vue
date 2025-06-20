<template>
	<div>
		<section class="section">
			<div class='title'>{{match.title}}</div>
			<div style="text-align: center;">
				<button class="cu-btn btn round line-cyan" @click="add_player">+ 添加选手</button>
				<button class="cu-btn btn round line-orange" @click="reset_present">全体退签</button>
			</div>
			<div v-for="(player, index) in this.players" :key="index" class="boxList flex">
				<div class="left">
					<img class="lIcon"
						src="https://tjtt-assets.oss-cn-shanghai.aliyuncs.com/pictures/avatars/player.png"
						alt="" />
				</div>
				<div class="right">
					<div class="text1">{{player.username}}</div>
					<div class="text2">{{player.gender}} | {{player.school}} | {{player.role}}</div>
					<div v-if="player.organ" class="text2">{{player.organ.organname}}</div>
					<div class="text3 flex">
						<div class="l" style="font-size: 28rpx; color: #f25c07;">
							<div class="quan"></div>
							报名积分：{{player.fixed_score}}
						</div>
						<div class="r">
							<button v-if="player.present==0" style="position: relative; bottom: 12px;"
								class="cu-btn btn round line-cyan" @click="sign_or_unsign(player.id, player.present)">
								签到
							</button>
							<button v-else style="position: relative; bottom: 12px;"
								class="cu-btn btn round line-orange" @click="sign_or_unsign(player.id, player.present)">
								退签
							</button>
							<button style="position: relative; bottom: 12px;"
								class="cu-btn btn round line-red" @click="remove_player(player.id)">
								移除
							</button>
						</div>
					</div>
				</div>
			</div>
		</section>
	</div>
</template>

<script>
	import { fetch_data } from '../../static/js/ajax_request.js'
	import { login_check } from '../../static/js/login_check.js'
	export default {
		data() {
			return {
				message: "",
				user: "",
				match: "",
				players: "",
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
			
			// 获取赛事
			wx.showToast({
				title: '加载中',
				icon: 'loading',
				duration: 100000,
			});
			let match_id = uni.getStorageSync('match_id');
			fetch_data("POST", "get_this_match", {"match_id": match_id}, "competition", res => {
				this.match = res.data.match;
			});
			
			// 获取参赛选手
			fetch_data("POST", "get_match_players", {"match_id": match_id}, "competition", res => {
				this.players = res.data.players;
				wx.hideToast();
			});
			
		},
		methods: {
			add_player() {
				wx.showModal({
					title: '添加参赛选手',
					placeholderText: '请输入选手姓名',
					editable: true,
					success: res => {
						if (res.confirm) {
							wx.showToast({
								title: '添加中',
								icon: 'loading',
								duration: 100000,
							});
							let data = {
								'my_id': this.user.id,
								'match_id': this.match.id,
								'player_username': res.content,
							}
							fetch_data("POST", "add_player", data, "competition", res => {
								wx.showToast({
									title: res.data.message,
									icon: "none",
									duration: 1000,
								});
								if (res.data.status == 200) {
									fetch_data("POST", "get_match_players", {"match_id": this.match.id}, "competition", res => {
										this.players = res.data.players;
									});
								}
							})
						}
					}
				})
			},
			reset_present() {
				wx.showModal({
					title: '退签',
					content: '比赛已结束，确认将所有选手置为未签到状态？',
					success: res => {
						if (res.confirm) {
							wx.showToast({
								title: '退签中',
								icon: 'loading',
								duration: 100000,
							});
							let data = {
								'my_id': this.user.id,
								'match_id': this.match.id,
							}
							fetch_data("POST", "reset_present", data, "competition", res => {
								wx.showToast({
									title: res.data.message,
									icon: "none",
									duration: 1000,
								});
								if (res.data.status == 200) {
									fetch_data("POST", "get_match_players", {"match_id": this.match.id}, "competition", res => {
										this.players = res.data.players;
									});
								}
							})
						}
					}
				})
			},
			sign_or_unsign(player_id, player_present) {
				if (player_present==0) {
					wx.showModal({
						title: '选手签到',
						content: '确认签到该选手？',
						success: res => {
							if (res.confirm) {
								wx.showToast({
									title: '签到中',
									icon: 'loading',
									duration: 100000,
								});
								let data = {
									'my_id': this.user.id,
									'match_title': this.match.title,
									'player_id': player_id,
								}
								fetch_data("POST", "player_sign_or_unsign", data, "competition", res => {
									wx.showToast({
										title: res.data.message,
										icon: "none",
										duration: 1000,
									});
									if (res.data.status == 200) {
										fetch_data("POST", "get_match_players", {"match_id": this.match.id}, "competition", res => {
											this.players = res.data.players;
										});
									}
								})
							}
						}
					})
				}
				else {
					wx.showModal({
						title: '选手退签',
						content: '确认退签该选手？',
						success: res => {
							if (res.confirm) {
								wx.showToast({
									title: '退签中',
									icon: 'loading',
									duration: 100000,
								});
								let data = {
									'my_id': this.user.id,
									'match_title': this.match.title,
									'player_id': player_id,
								}
								fetch_data("POST", "player_sign_or_unsign", data, "competition", res => {
									wx.showToast({
										title: res.data.message,
										icon: "none",
										duration: 1000,
									});
									if (res.data.status == 200) {
										fetch_data("POST", "get_match_players", {"match_id": this.match.id}, "competition", res => {
											this.players = res.data.players;
										});
									}
								})
							}
						}
					})
				}
				
			},
			remove_player(player_id) {
				wx.showModal({
					title: '移除参赛选手',
					content: '确认移除该选手？',
					success: res => {
						if (res.confirm) {
							wx.showToast({
								title: '移除中',
								icon: 'loading',
								duration: 100000,
							});
							let data = {
								'my_id': this.user.id,
								'player_id': player_id,
								'match_id': this.match.id,
							}
							fetch_data("POST", "remove_player", data, "competition", res => {
								wx.showToast({
									title: res.data.message,
									icon: "none",
									duration: 1000,
								});
								if (res.data.status == 200) {
									this.players.forEach(function(item, index, arr) {
										if (item.id == player_id) {
											arr.splice(index, 1);
										}
									}); // 把该选手从this.players删掉
								}
							})
						}
					}
				})
			},
		}
	}
</script>


<style lang="scss" scoped>
	.section {
		background: #ffffff;
		border-radius: 20rpx 20rpx 20rpx 20rpx;
		box-sizing: border-box;
		padding: 20rpx;

		.title {
			text-align: center;
			font-weight: bold;
			font-size: 32rpx;
			line-height: 70rpx;
		}

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
					font-weight: bold;
					font-size: 32rpx;
					color: #333333;
					line-height: 32rpx;
				}

				.text2 {
					margin-top: 28rpx;
					font-weight: 500;
					font-size: 28rpx;
					color: #999999;
					line-height: 14rpx;
				}

				.text3 {
					margin-top: 28rpx;
					font-weight: 500;
					font-size: 24rpx;
					color: #999999;
					line-height: 28rpx;
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
		margin-top: 20rpx;
		background: #ffffff;
		border-radius: 14rpx;

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
			font-size: 48rpx;
			color: #282456;
			line-height: 48rpx;
			text-align: center;
			font-style: normal;
			text-transform: none;
		}
	}

	.headBox {
		background-color: white;
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
</style>