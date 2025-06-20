<template>
	<view class="main">
		<view class="main">
			<view class="pagenation">
				<view class="pagenation_back" @tap="backref()">
					<image class="back_arrow" src="..\..\static\tabbar\back.png" mode="" />
				</view>
			</view>
			<view v-if="!hide_this" class="login">
				<view class="kuang shadow">
					<view class="hint">积分更新（手动）</view>
					<view class="form-group">
						<image class="images" src="https://tjtt-assets.oss-cn-shanghai.aliyuncs.com/pictures/logos/logo1.1.png" mode="" />
						<view v-if="update_match_type=='single'" class="input_section">
							<view class="title ipt">胜者姓名：</view>
							<input maxlength="100" class="ipt tpyA" v-model="winner1" placeholder="请输入胜者姓名" />
						</view>
						<view v-if="update_match_type=='single'" class="input_section">
							<view class="title ipt">负者姓名：</view>
							<input maxlength="100" class="ipt tpyA" v-model="loser1" placeholder="请输入负者姓名" />
						</view>
						<view v-if="update_match_type=='double'" class="input_section">
							<view class="title ipt">胜方选手姓名：</view>
							<input maxlength="100" class="ipt tpyA" v-model="winner1" placeholder="选手1" />
						</view>
						<view v-if="update_match_type=='double'" class="input_section">
							<view class="title ipt" style="visibility: hidden;">胜方选手姓名：</view>
							<input maxlength="100" class="ipt tpyA" v-model="winner2" placeholder="选手2" />
						</view>
						<view v-if="update_match_type=='double'" class="input_section">
							<view class="title ipt">负方选手姓名：</view>
							<input maxlength="100" class="ipt tpyA" v-model="loser1" placeholder="选手1" />
						</view>
						<view v-if="update_match_type=='double'" class="input_section">
							<view class="title ipt" style="visibility: hidden;">负方选手姓名：</view>
							<input maxlength="100" class="ipt tpyA" v-model="loser2" placeholder="选手2" />
						</view>
						
						<view class="input_section">
							<view class="title ipt">比分：</view>
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
								</p>
								<p>
									<label>五局三胜制</label>
								</p>
								<p style="white-space: nowrap;">
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
									<label>七局四胜制</label>
								</p>
								<p>
									<label class="radio" style="margin-left: 15rpx; margin-right: 20rpx;">
										<radio value="4:x" color="#FFCC33" style="transform:scale(0.7)" />4:x
									</label>
								</p>
							</radio-group>
						</view>
						<view class="input_section">
							<view class="title ipt">关联赛事名：</view>
							<input maxlength="100" class="ipt tpyA" v-model="match_title" placeholder="请准确输入,若无请留空" />
						</view>
						<view class="input_section" style="color: red; white-space: normal;">
							注意：比分录入后选手积分自动计算，该操作不可逆，请务必确认对阵双方及比分正确
						</view>
					</view>
					<button v-if="update_match_type=='single'" class="btn round" style="background-color: #f05b05;" @click="confirm_single">确定</button>
					<button v-if="update_match_type=='double'" class="btn round" style="background-color: #f05b05;" @click="confirm_double">确定</button>
				</view>
			</view>
			<view class="bottom">
			</view>
		</view>
	</view>
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
				update_match_type: "",
				match_title: "",
				winner1: "",
				winner2: "",
				loser1: "",
				loser2: "",
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
			this.update_match_type = uni.getStorageSync("update_match_type");
			uni.removeStorageSync("update_match_type");
		},
		methods: {
			onInput(e) {
				this.match_title = e.target.value
				this.winner1 = e.target.value
				this.loser1 = e.target.value
				this.winner2 = e.target.value
				this.loser2 = e.target.value
			},
			what_result(e) {
				this.result = e.detail.value
			},

			backref() {
				uni.navigateBack({
					delta: 1
				});
			},

			confirm_single() {
				wx.showModal({
					title: '确认更新',
					content: '比分录入后选手积分自动计算，该操作不可逆，请务必确认对阵双方及比分正确',
					success: res => {
						if (res.confirm) {
							wx.showToast({
								title: '计算中',
								icon: 'loading',
								duration: 100000,
							});
							let data = {
								"my_id": this.user.id,
								"match_title": this.match_title,
								"winner1": this.winner1,
								"loser1": this.loser1,
								"result": this.result,
							}
							fetch_data("POST", "score_update_single", data, "competition", res => {
								console.log(res.data.message);
								wx.showToast({
									title: res.data.message,
									icon: "none",
									duration: 700,
								});
							})
						}
					}
				})
			},
			
			confirm_double() {
				wx.showModal({
					title: '确认更新',
					content: '比分录入后选手积分自动计算，该操作不可逆，请务必确认对阵双方及比分正确',
					success: res => {
						if (res.confirm) {
							wx.showToast({
								title: '计算中',
								icon: 'loading',
								duration: 100000,
							});
							let data = {
								"my_id": this.user.id,
								"match_title": this.match_title,
								"winner1": this.winner1,
								"loser1": this.loser1,
								"winner2": this.winner2,
								"loser2": this.loser2,
								"result": this.result,
							}
							fetch_data("POST", "score_update_double", data, "competition", res => {
								console.log(res.data.message);
								wx.showToast({
									title: res.data.message,
									icon: "none",
									duration: 700,
								});
							})
						}
					}
				})
			},
		}
	}
</script>


<style lang="scss">
	.pagenation {
		.pagenation_back {
			position: absolute;
			display: flex;
			justify-content: center;
			align-items: center;
			width: 76rpx;
			height: 76rpx;
			border-radius: 50%;
			border: 1rpx solid #bcbcbc;
			margin: 75rpx 40rpx;

			.back_arrow {
				width: 50rpx;
				height: 50rpx;
			}
		}
	}
</style>

<style>
	.main {
		width: 100%;
		height: 100%;
		background: linear-gradient(135deg, #FEF2DA, #FFD5A4);
		display: flex;
		flex-direction: column;
		justify-content: flex-start;
	}

	.main .login {
		margin-top: 150rpx;
		display: flex;
		flex-direction: column;
		justify-content: flex-start;
		align-items: center;
		flex: 1;
	}

	.main .login .kuang {
		width: 660rpx;
		background-color: #fff;
		height: 100%;
		margin-top: 85rpx;
		border-radius: 20rpx;
		/* display: flex; */
		flex-direction: column;
		justify-content: space-between;
		align-items: center;
		padding: 50rpx 20rpx;
	}

	.main .login .kuang .btn {
		width: 85%;
		color: #fff;
		font-size: 32rpx;
		margin: 40rpx;
	}

	.main .login .kuang .hint {
		width: 100%;
		color: black;
		font-size: 50rpx;
		font-weight: bold;
		text-align: center;
	}

	.main .login .kuang .return {
		width: 100%;
		color: #fef2da;
		font-size: 30rpx;
		text-align: center;
		font-size: 26rpx;
	}

	.main .avatar-open {
		width: 180rpx;
		height: 180rpx;
		clip-path: circle(90rpx at center);
	}

	.main .bottom {
		width: 100%;
		align-self: flex-end;
		font-size: 26rpx;
		height: 120rpx;
		text-align: center;
		color: #fff;
		display: flex;
		flex-direction: column;
	}

	.form-group {
		margin: 40rpx;
		text-align: center;
	}

	.form-group .title {
		white-space: nowrap;
		font-weight: normal;
	}

	.form-group .input_section {
		margin: 40rpx;
		display: flex;
		flex-direction: row;
		text-align: justify;
	}

	.title {
		line-height: 42rpx !important;
	}

	.images {
		width: 160rpx;
		height: 160rpx;
		border-radius: 50%;
	}

	.tpyA {
		padding: 0px 20rpx;
	}

	.ipt {
		font-size: 26rpx;
	}
</style>