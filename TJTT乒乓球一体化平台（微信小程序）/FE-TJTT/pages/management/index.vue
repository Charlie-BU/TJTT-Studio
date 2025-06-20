<template>
	<div class="app">
		<div v-if="user.usertype=='K9' || user.usertype=='K10' || user.usertype=='K11'" class="phb flex">
			<div>
				<div>
					<span v-if="user.id==1" class="num">{{user.username}} | {{user.usertype}} | TJTT负责人</span>
					<span v-else class="num">{{user.username}} | {{user.usertype}}</span>
				</div>
				<div style="color: #666666; margin-top: 20rpx" class="jf">
					<u-icon style="margin-right: 10rpx" name="integral" color="#F25C07"
						size="28" />管理员
				</div>
			</div>
			<u-icon style="margin-right: 10rpx" name="scan" color="#F25C07"
				size="50" @click="scan_qr" />
		</div>
		<div class="phb flex">
			<div>
				<div>
					<span class="num">{{user_length}}</span>
					<span class="jf" style="margin-left: 20rpx">人</span>
				</div>
				<div style="color: #666666; margin-top: 20rpx" class="jf">
					<u-icon style="margin-right: 10rpx" name="account-fill" color="#F25C07"
						size="28" />现有用户
				</div>
			</div>
			<div>
				<div>
					<span class="num">{{match_length}}</span>
					<span class="jf" style="margin-left: 20rpx">场</span>
				</div>
				<div style="color: #666666; margin-top: 20rpx" class="jf">
					<u-icon style="margin-right: 10rpx" name="coupon-fill" color="#F25C07"
						size="28" />近期赛事
				</div>
			</div>
			<div>
				<div>
					<span class="num">{{TJTTers_length}}</span>
					<span class="jf" style="margin-left: 20rpx">人</span>
				</div>
				<div style="color: #666666; margin-top: 20rpx" class="jf">
					<u-icon style="margin-right: 10rpx" name="integral-fill" color="#F25C07"
						size="28" />TJTT Studio
				</div>
			</div>
		</div>
		<div class="text"><u-icon style="margin-right: 10rpx" name="account" color="#F25C07" size="28" />用户</div>
		<div class="foot flex">
			<div class="left" @click="user_list">
				<uni-icons type="person-filled" color="#1f3347" size="50"></uni-icons>
				<p class="pt">用户管理</p>
			</div>
			<div class="left" @click="organ_list">
				<uni-icons type="staff-filled" color="#1f3347" size="50"></uni-icons>
				<p class="pt">组织管理</p>
			</div>
			<div class="left" @click="wx_bind">
				<uni-icons type="weixin" color="#1f3347" size="50"></uni-icons>
				<p class="pt">微信绑定</p>
			</div>
		</div>
		<div class="divider"></div>
		<div class="text"><u-icon style="margin-right: 10rpx" name="coupon" color="#F25C07" size="28" />赛事</div>
		<div class="foot flex">
			<div class="left" @click="score_update">
				<uni-icons type="cloud-upload" color="#1f3347" size="50"></uni-icons>
				<p class="pt">积分更新（手动）</p>
			</div>
			<div class="left" @click="team_list">
				<uni-icons type="staff" color="#1f3347" size="50"></uni-icons>
				<p class="pt">代表队管理</p>
			</div>
			<div class="left" @click="hold_match">
				<uni-icons type="plus" color="#1f3347" size="50"></uni-icons>
				<p class="pt">举办赛事</p>
			</div>
		</div>
		<div class="divider"></div>
		<div class="text"><u-icon style="margin-right: 10rpx" name="order" color="#F25C07" size="28" />日志</div>
		<div class="foot flex">
			<div class="left" @click="score_log">
				<uni-icons type="wallet" color="#1f3347" size="50"></uni-icons>
				<p class="pt">积分变动日志</p>
			</div>
			<div v-if="user.id == 1" class="left" @click="action_log">
				<uni-icons type="wallet-filled" color="#1f3347" size="50"></uni-icons>
				<p class="pt">用户操作日志</p>
			</div>
		</div>
		<div class="divider"></div>
		<div class="text"><u-icon style="margin-right: 10rpx" name="flag" color="#F25C07" size="28" />其他</div>
		<div class="foot flex">
			<div class="left" @click="agendas">
				<uni-icons type="home" color="#1f3347" size="50"></uni-icons>
				<p class="pt">库</p>
			</div>
			<div class="left" @click="add_motto">
				<uni-icons type="flag" color="#1f3347" size="50"></uni-icons>
				<p class="pt">添加乒乓语录</p>
			</div>
		</div>
	</div>
</template>

<script>
	import { fetch_data } from '../../static/js/ajax_request.js'
	import { login_check } from '../../static/js/login_check.js'
	import { magic } from '../../static/js/magic_power.js'
	export default {
		data() {
			return {
				user: "",
				message: "",
				user_length: "",
				match_length: "",
				TJTTers_length: "",
				foreign_admins: "",
				hide_this: magic(),
			}
		},
		onLoad() {
			login_check(user => {
				this.user = user;
			});
			if (!this.user || (this.user.usertype != "K9" && this.user.usertype != "K10" && this.user.usertype != "K11")) {
				wx.showToast({
					title: "权限不足",
					icon: "none",
					duration: 1500,
				});
				setTimeout(() => {
					uni.reLaunch({
						url: '/pages/index/index',
					})
				}, 1000);
			};
			// 获取信息
			fetch_data("POST", "get_info", null, "user", res => {
				this.user_length = res.data.user_length;
				this.match_length = res.data.match_length;
				this.TJTTers_length = res.data.TJTTers_length;
				this.foreign_admins = res.data.foreign_admins;
			});
		},
		methods: {
			scan_qr() {
				if (this.hide_this) {
					return;
				}
				uni.scanCode({
					success: res => {
						// 若是选手参赛二维码
						if (res.result.includes("Player's QRcode")) {
							let data = {
								"my_id": this.user.id,
								"qr_content": res.result,
							}
							fetch_data("POST", "player_sign_in", data, "competition", res => {
								wx.showToast({
									title: res.data.message,
									icon: "none",
									duration: 1200,
								});
							});
						}
						else {
							wx.showToast({
								title: "二维码无效",
								icon: "none",
								duration: 1200,
							});
						}
					}
					
				});
			},
			
			user_list() {
				if (this.hide_this) {
					return;
				}
				uni.navigateTo({
					url: '/page_subjec/user/user-list',
				})
			},
			organ_list() {
				if (this.hide_this) {
					return;
				}
				uni.navigateTo({
					url: '/page_subjec/organization/organ-list',
				})
			},
			wx_bind() {
				if (this.hide_this) {
					return;
				}
				uni.navigateTo({
					url: '/pages/login/wx-bind',
				})
			},
			score_update() {
				if (this.hide_this) {
					return;
				}
				wx.showActionSheet({
					itemList: ['单打', '双打'],
					success: function(res) {
						if (!res.cancel) {
							if (res.tapIndex == 0) {
								uni.setStorageSync("update_match_type", "single")
							}
							else if (res.tapIndex == 1) {
								uni.setStorageSync("update_match_type", "double")
							}
							uni.navigateTo({
								url: '/page_subjec/match/score-update',
							});
						}
					}
				})
			},
			team_list() {
				if (this.hide_this) {
					return;
				}
				uni.navigateTo({
					url: '/page_subjec/team/team-list',
				})
			},
			hold_match() {
				if (this.hide_this) {
					return;
				}
				uni.navigateTo({
					url: '/page_subjec/match/hold-match',
				})
			},
			agendas() {
				if (this.hide_this) {
					return;
				}
				uni.navigateTo({
					url: '/page_subjec/agendas/index',
				})
			},
			score_log() {
				if (this.hide_this) {
					return;
				}
				uni.navigateTo({
					url: '/page_subjec/log/score-log',
				})
			},
			action_log() {
				if (this.hide_this) {
					return;
				}
				uni.navigateTo({
					url: '/page_subjec/log/action-log',
				})
			},
			add_motto() {
				if (this.hide_this) {
					return;
				}
				uni.navigateTo({
					url: '/page_subjec/motto/add-motto',
				})
			},
		},
	}
</script>

<style lang="scss" scoped>
	.foot {
		.left {
			text-align: center;
			box-sizing: box-sizing;
			padding: 20rpx;
			padding-top: 36rpx;
			margin-top: 25rpx;
			width: 47%;
			height: 208rpx;
			border-radius: 20rpx 20rpx 20rpx 20rpx;
		}

		.lIcons {
			width: 104rpx;
			height: 104rpx;
			border-radius: 50%;
		}

		.pt {
			font-weight: 500;
			font-size: 28rpx;
			color: #212121;
			margin-top: 14rpx;
			line-height: 30rpx;
		}

		.r {
			background-color: #f9d67a !important;
		}
	}

	.app {
		background: linear-gradient(180deg, #fef2da, #f9d5a5);
		box-sizing: border-box;
		padding: 20rpx;
	}

	.text {
		font-weight: 600;
		font-size: 32rpx;
		box-sizing: border-box;
		padding-top: 22rpx;
		margin-left: 30rpx;
	}

	.divider {
		background-color: #f2f2f2;
		margin: 28rpx 0rpx;
		height: 1rpx;
	}

	.codeA {
		text-align: left !important;
		padding: 30rpx !important;

		.xian {
			background-color: #f2f2f2;
			margin: 28rpx 0rpx;
			height: 1rpx;
		}

		.tipTit {
			font-weight: 600;
			font-size: 32rpx;
			color: #333333;
			line-height: 32rpx;
		}

		.textDiv {
			margin-top: 20rpx;
			font-weight: 400;
			font-size: 24rpx;
			color: #333333;
			line-height: 44rpx;
		}
	}

	.code {
		box-sizing: border-box;
		padding: 50rpx;
		background-color: white;
		position: relative;
		top: -70rpx;
		border-radius: 28rpx;
		text-align: center;

		.codeImg {
			width: 320rpx;
			height: 320rpx;
		}

		.tis {
			margin: 36rpx 0rpx;
			font-weight: 400;
			font-size: 24rpx;
			color: #666666;
			line-height: 24rpx;
		}

		.title {
			margin-top: 22rpx;
			font-weight: 600;
			font-size: 40rpx;
			color: #000000;
			line-height: 40rpx;
		}
	}

	.bc {
		margin-top: 30rpx;
		background-color: #eed4bd;
		box-sizing: box-sizing;
		padding: 18rpx 20rpx;
		border-radius: 20rpx;
		padding-bottom: 90rpx;

		.text1 {
			margin-top: 14rpx;
			font-family: PingFang SC, PingFang SC;
			font-weight: bold;
			font-size: 28rpx;
			color: #333333;
			line-height: 40rpx;
			text-align: left;
			font-style: normal;
			text-transform: none;
		}

		.text2 {
			margin-top: 70rpx;
			font-family: PingFang SC, PingFang SC;
			font-weight: 600;
			font-size: 28rpx;
			color: #f25c07;
			line-height: 28rpx;
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
				border-radius: 12rpx;
				width: 100%;
				height: 144rpx;
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
		margin-top: 20rpx;
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
</style>