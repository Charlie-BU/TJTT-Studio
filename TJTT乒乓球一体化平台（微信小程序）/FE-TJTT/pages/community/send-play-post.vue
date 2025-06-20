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
					<view class="hint">发布约球帖</view>
					<view class="form-group">
						<image class="images" src="https://tjtt-assets.oss-cn-shanghai.aliyuncs.com/pictures/logos/logo1.1.png" mode="" />
						<view class="input_section">
							<view class="title ipt">发帖人：</view>
							<input maxlength="100" class="ipt tpyA" v-bind:value="user.username" disabled />
						</view>
						<view class="input_section">
							<view class="title ipt">约球时间：</view>
							<input maxlength="100" class="ipt tpyA" v-model="play_time" placeholder="YYYY-MM-DD H:M" />
						</view>
						<view class="input_section">
							<view class="title ipt">地点：</view>
							<input maxlength="100" class="ipt tpyA" v-model="place" placeholder="请填写约球地点" />
						</view>
						<view class="input_section">
							<view class="title ipt">球台：</view>
							<input maxlength="100" class="ipt tpyA" v-model="table_vacant" placeholder="请填写球台" />
						</view>
						<view class="input_section">
							<view class="title ipt">备注：</view>
							<textarea maxlength="-1" class="ipt tpyA" style="height: 150rpx;" v-model="description" placeholder="请输入备注内容" />
						</view>
					</view>
					<button class="btn round" style="background-color: #f05b05;" @click="issue">确认发布</button>
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
				play_time: "",
				table_vacant: "",
				description: "",
				place: "",
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
		},
		methods: {
			onInput(e) {
				this.play_time = e.target.value
				this.table_vacant = e.target.value
				this.description = e.target.value
				this.place = e.target.value
			},

			backref() {
				uni.navigateBack({
					delta: 1
				});
			},

			issue() {
				fetch_data_wxLogin("POST", "store_openid", { "my_id": this.user.id }, "user",);
				subscirbe_message(['pSBm6ewDwG2_kTS3K2_n9kniQsDamkIUeSwjw1F381g'], () => {
					wx.showToast({
						title: '发布中',
						icon: 'loading',
						duration: 100000,
					});
					let data = {
						"my_id": this.user.id,
						"play_time": this.play_time,
						"table_vacant": this.table_vacant,
						"description": this.description,
						"place": this.place,
					}
					fetch_data("POST", "send_play_post", data, "application", res => {
						wx.showToast({
							title: res.data.message,
							icon: "none",
							duration: 1000,
						});		
						if (res.data.status == 200) {
							setTimeout(() => {
								uni.reLaunch({
									url: '/pages/community/index',
								});
							}, 1000);
						}
					})
				});
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
		height: 600rpx;
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