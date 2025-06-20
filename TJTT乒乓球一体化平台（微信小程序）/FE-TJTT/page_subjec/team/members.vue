<template>
	<div>
		<section v-if="!hide_this" class="section">
			<div class='title'>{{team.teamname}}队员</div>
			<div style="text-align: center;">
				<button class="cu-btn btn round line-cyan" @click="add_member">+ 添加队员</button>
			</div>
			<div v-for="(member, index) in team.members" :key="index" class="boxList flex">
				<div class="left">
					<img class="lIcon"
						src="https://tjtt-assets.oss-cn-shanghai.aliyuncs.com/pictures/avatars/player.png"
						alt="" />
				</div>
				<div class="right">
					<div class="text1">{{member.username}}</div>
					<div class="text2">{{member.gender}} | {{member.school}} | {{member.role}}</div>
					<div v-if="member.organ" class="text2">{{member.organ.organname}}</div>
					<div class="text3 flex">
						<div class="l" style="font-size: 28rpx; color: #f25c07;">
							<div class="quan"></div>
							TJTT积分：{{member.score}}
						</div>
						<div class="r">
							<button style="position: relative; bottom: 12px;"
								class="cu-btn btn round line-red" @click="remove_member(member.id)">
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
	import { magic } from '../../static/js/magic_power.js'
	export default {
		data() {
			return {
				message: "",
				user: "",
				team: "",
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
			

			// 获取代表队
			this.team = uni.getStorageSync('team');
			if (!this.team) {
				wx.showToast({
					title: "服务器繁忙，请稍后再试",
					icon: "none",
					duration: 1500,
				});
				setTimeout(() => {
					uni.navigateBack({
						delta: 1
					});
				}, 1000);
			};
			uni.removeStorageSync('team');
		},
		methods: {
			add_member() {
				wx.showModal({
					title: '添加队员',
					placeholderText: '请输入队员姓名',
					editable: true,
					success: res => {
						if (res.confirm) {
							let data = {
								'my_id': this.user.id,
								'team_id': this.team.id,
								'member_name': res.content,
							}
							fetch_data("POST", "add_member", data, "competition", res => {
								wx.showToast({
									title: res.data.message,
									icon: "none",
									duration: 1000,
								});
								if (res.data.status == 200) {
									fetch_data("POST", "get_this_team", {team_id: this.team.id}, "competition", res => {
										this.team = res.data.team
									})
									uni.setStorageSync('team', this.team);
								}
							})
						}
					}
				})
			},
			remove_member(member_id) {
				wx.showModal({
					title: '移除队员',
					content: '确认移除该队员？',
					success: res => {
						if (res.confirm) {
							let data = {
								'my_id': this.user.id,
								'member_id': member_id,
								'team_id': this.team.id,
							}
							fetch_data("POST", "remove_member", data, "competition", res => {
								wx.showToast({
									title: res.data.message,
									icon: "none",
									duration: 1000,
								});
								if (res.data.status == 200) {
									this.team.members.forEach(function(item,
										index, arr) {
										if (item.id ==
											member_id) {
											arr.splice(index,
												1);
										}
									}); // 把该选手从this.team.members删掉
									uni.setStorageSync('team', this.team);
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