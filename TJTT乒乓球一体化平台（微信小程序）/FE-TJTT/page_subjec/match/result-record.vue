<template>
	<div v-if="!hide_this" class="app">
		<div class="bc flex">
			<div class="left">
				<img class="bcImg" src="https://tjtt-assets.oss-cn-shanghai.aliyuncs.com/pictures/decorations/5.png" alt="" />
			</div>
			<div class="right">
				<div class="wrapper">
					<div class="text1">{{match.title}}</div>
				</div>
				<div class="text1" style="color: #f25c07;">赛制：{{match.system}}</div>
			</div>
		</div>
		<div class="codeA code" style="margin-top: 20rpx">
			<div class="textDiv">
				<view class="input_section">
					<view class="title ipt">对阵双方：</view>
					<view class="title ipt">X {{player_x.username}}</view>&nbsp;&nbsp;&nbsp;&nbsp;
					<view class="title ipt">Y {{player_y.username}}</view>
				</view>
				<view class="input_section">
					<view class="title ipt">比分 (X:Y)：</view>
					<radio-group @change="what_result">
						<p>
							<label>三局两胜制</label>
						</p>
						<p>
							<label class="radio" style="margin-left: 15rpx; margin-right: 20rpx;">
								<radio value="2:0" color="#FFCC33" style="transform:scale(0.7)" />2:0
							</label>
							<label class="radio" style="margin-left: 15rpx; margin-right: 20rpx;">
								<radio value="2:1" color="#FFCC33" style="transform:scale(0.7)" />2:1
							</label>
							<label class="radio" style="margin-left: 15rpx; margin-right: 20rpx;">
								<radio value="0:2" color="#FFCC33" style="transform:scale(0.7)" />0:2
							</label>
							<label class="radio" style="margin-left: 15rpx; margin-right: 20rpx;">
								<radio value="1:2" color="#FFCC33" style="transform:scale(0.7)" />1:2
							</label>
						</p>
						<p>
							<label>五局三胜制</label>
						</p>
						<p>
							<label class="radio" style="margin-left: 15rpx; margin-right: 20rpx;">
								<radio value="3:0" color="#FFCC33" style="transform:scale(0.7)" />3:0
							</label>
							<label class="radio" style="margin-left: 15rpx; margin-right: 20rpx;">
								<radio value="3:1" color="#FFCC33" style="transform:scale(0.7)" />3:1
							</label>
							<label class="radio" style="margin-left: 15rpx; margin-right: 20rpx;">
								<radio value="3:2" color="#FFCC33" style="transform:scale(0.7)" />3:2
							</label>
						</p>
						<p>
							<label class="radio" style="margin-left: 15rpx; margin-right: 20rpx;">
								<radio value="0:3" color="#FFCC33" style="transform:scale(0.7)" />0:3
							</label>
							<label class="radio" style="margin-left: 15rpx; margin-right: 20rpx;">
								<radio value="1:3" color="#FFCC33" style="transform:scale(0.7)" />1:3
							</label>
							<label class="radio" style="margin-left: 15rpx; margin-right: 20rpx;">
								<radio value="2:3" color="#FFCC33" style="transform:scale(0.7)" />2:3
							</label>
						</p>
						<p>
							<label>七局四胜制</label>
						</p>
						<p>
							<label class="radio" style="margin-left: 15rpx; margin-right: 20rpx;">
								<radio value="4:x" color="#FFCC33" style="transform:scale(0.7)" />4:x（X胜）
							</label>
							<label class="radio" style="margin-left: 15rpx; margin-right: 20rpx;">
								<radio value="x:4" color="#FFCC33" style="transform:scale(0.7)" />x:4（Y胜）
							</label>
						</p>
					</radio-group>
				</view>
				<view class="input_section" style="color: red; white-space: normal;">
					注意：成绩录入后选手积分自动计算，该操作不可逆，请务必确认对阵双方及比分正确
				</view>
				<button class="btn round" style="background-color: #f05b05;" @click="confirm_record">确认录入</button>
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
				message: "",
				user: "",
				match: "",
				player_x: "",
				player_y: "",
				result: "",
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
			// 获取赛事
			wx.showToast({
				title: '加载中',
				icon: 'loading',
				duration: 100000,
			});
			let match_id = uni.getStorageSync('match_id');
			fetch_data("POST", "get_this_match", {"match_id": match_id}, "competition", res => {
				this.match = res.data.match;
				wx.hideToast();
			});
			
			
			// 获取对阵双方
			this.player_x = uni.getStorageSync('player_x')
			this.player_y = uni.getStorageSync('player_y')
			if (!this.player_x || !this.player_y) {
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
			uni.removeStorageSync('player_x');
			uni.removeStorageSync('player_y');
		},
		methods: {
			what_result(e) {
				this.result = e.detail.value
			},
			
			confirm_record() {
				if (!this.result) {
					wx.showToast({
						title: '请选择比分',
						icon: "none",
						duration: 1000,
					});
				}
				else {
					wx.showModal({
						title: '确认录入',
						content: '成绩录入后选手积分自动计算，该操作不可逆，请务必确认对阵双方及比分正确',
						success: res => {
							if (res.confirm) {
								wx.showToast({
									title: '计算中',
									icon: 'loading',
									duration: 100000,
								});
								let data = {
									"my_id": this.user.id,
									"match_id": this.match.id,
									"player_x_id": this.player_x.id,
									"player_y_id": this.player_y.id,
									"result": this.result,
								}
								fetch_data("POST", "result_record", data, "competition", res => {
									console.log(res.data.message);
									wx.showToast({
										title: res.data.message,
										icon: "none",
										duration: 1000,
									});
									if (res.data.status == 200){
										// 刷新个人信息
										fetch_data("POST", "refresh", {"my_id": this.user.id}, "user", res => {
											uni.setStorageSync('user', res.data.user);
											uni.setStorageSync('my_rank', res.data.my_rank);
										});
										setTimeout(() => {
											uni.navigateBack({
												delta: 1
											});
										}, 1000);
									}
								})
							}
						}
					})
				}
			}
		}
	}
</script>

<style lang="scss" scoped>
	.wrapper {
		height: 60rpx;
	}
	
	.foot {
		.left {
			text-align: center;
			background-color: #ffffff;
			box-sizing: box-sizing;
			padding: 20rpx;
			padding-top: 36rpx;
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
			line-height: 28rpx;
		}

		.r {
			background-color: #f9d67a !important;
		}
	}

	.app {
		min-height: 100vh;
		background: linear-gradient(135deg, #FEF2DA, #FFD5A4);
		box-sizing: border-box;
		padding: 20rpx;
	}

	.textT {
		font-weight: 600;
		font-size: 32rpx;
		box-sizing: border-box;
		padding-top: 22rpx;
	}

	.codeA {
		text-align: left !important;
		padding: 30rpx !important;

		.divider {
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
			// margin-top: 70rpx;
			font-family: PingFang SC, PingFang SC;
			font-weight: 600;
			font-size: 26rpx;
			color: #f25c07;
			line-height: 60rpx;
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

	.userList {
		position: relative;
		box-sizing: box-sizing;
		margin-top: 40rpx;
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
	}

	.itemList {
		text-align: center;
		width: 24%;
	}
	
	.input_section {
		margin: 40rpx;
		display: flex;
		flex-direction: row;
		font-weight: bold;
		text-align: justify;
		white-space: nowrap;
	}
	
	.title {
		line-height: 42rpx !important;
	}
	
	.tpyA {
		padding: 0px 20rpx;
	}
	
	.ipt {
		font-size: 26rpx;
	}
	
	.btn {
		width: 85%;
		color: #fff;
		font-size: 32rpx;
		margin: 40rpx;
	}
</style>