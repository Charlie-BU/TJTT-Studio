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
					<view class="hint">添加组织</view>
					<view class="form-group">
						<image class="images"
							src="https://tjtt-assets.oss-cn-shanghai.aliyuncs.com/pictures/logos/logo1.1.png"
							mode="" />
						<view class="input_section">
							<view class="title ipt">组织名：</view>
							<input placeholder="请输入组织名" maxlength="100" class="ipt tpyA"
								v-model="organname" placeholder-class="phc ipt" />
						</view>
						<view class="input_section">
							<view class="title ipt">简介：</view>
							<textarea maxlength="-1" style="height: 150rpx;" placeholder="请输入组织简介" class="ipt tpyA" v-model="description"
								placeholder-class="phc ipt" />
						</view>
					</view>
					<button class="btn round" style="background-color: #f05b05;" @click="add_user">确认添加</button>
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
				organname: "",
				description: "",
				hide_this: magic(),
			}
		},
		onLoad() {
			login_check(user => {
				this.user = user;
			});
			if (!this.user || (this.user.usertype != "K10" && this.user.usertype != "K11")) {
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
		},
		methods: {
			onInput(e) {
				this.organname = e.target.value
				this.description = e.target.value
			},

			backref() {
				uni.navigateBack({
					delta: 1
				});
			},

			add_user() {
				let data = {
					"my_id": this.user.id,
					"organname": this.organname,
					"description": this.description,
				}
				fetch_data("POST", "add_organ", data, "organization", res => {
					wx.showToast({
						title: res.data.message,
						icon: "none",
						duration: 700,
					});
					if (res.data.status == 200) {
						setTimeout(() => {
							uni.reLaunch({
								url: '/page_subjec/organization/organ-list',
							})
						}, 700);
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
		width: 620rpx;
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