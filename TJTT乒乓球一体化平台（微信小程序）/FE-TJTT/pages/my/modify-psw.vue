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
					<view class="hint">修改密码</view>
					<image class="images" src="https://tjtt-assets.oss-cn-shanghai.aliyuncs.com/pictures/logos/logo1.1.png" mode="" />
					<view class="form-group">
						<view class="input_section">
							<view class="title ipt">姓名：</view>
							<input maxlength="100" class="ipt tpyA" v-bind:value="user.username" disabled />
						</view>
						<view class="input_section">
							<view class="title ipt">原密码：</view>
							<input placeholder="请输入原密码" maxlength="100" v-model="old_psw" class="ipt tpyA"
								type="password" />
						</view>
						<view class="input_section">
							<view class="title ipt">新密码：</view>
							<input placeholder="请输入新密码" maxlength="100" v-model="new_psw" class="ipt tpyA"
								type="password" />
						</view>
						<view class="input_section">
							<view class="title ipt">确认新密码：</view>
							<input placeholder="请再次输入新密码" maxlength="100" v-model="new_psw2" class="ipt tpyA"
								type="password" />
						</view>
					</view>
					<button class="btn round" style="background-color: #f05b05;" @click="modify">确认修改</button>
				</view>
			</view>
			<view class="bottom">
			</view>
		</view>
	</view>
</template>

<script>
	import {fetch_data} from '../../static/js/ajax_request.js'
	import {login_check} from '../../static/js/login_check.js'
	import { magic } from '../../static/js/magic_power.js'
	export default {
		data() {
			return {
				message: "",
				user: "",
				old_psw: "",
				new_psw: "",
				new_psw2: "",
				hide_this: magic(),
			}
		},
		onLoad() {
			login_check(user=>{
				this.user = user;
			});
		},
		methods: {
			onInput(e) {
				this.old_psw = e.target.value
				this.new_psw = e.target.value
				this.new_psw2 = e.target.value
			},

			backref() {
				uni.navigateBack({
					delta: 1
				});
			},

			modify() {
				let data = {
					"my_id": this.user.id,
					"old_psw": this.old_psw,
					"new_psw": this.new_psw,
					"new_psw2": this.new_psw2,
				}
				fetch_data("POST", "modify_psw", data, "user", res => {
					console.log(res.data.message);
					wx.showToast({
						title: res.data.message,
						icon: "none",
						duration: 700,
					});
					if (res.data.status == 200){
						setTimeout(() => {
							uni.reLaunch({
								url: '/pages/my/index',
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
		height: 100vh;
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
		height: 65%;
		margin-top: 100rpx;
		border-radius: 20rpx;
		display: flex;
		flex-direction: column;
		justify-content: space-between;
		align-items: center;
		padding: 50rpx 20rpx;
	}

	.main .login .kuang button {
		width: 85%;
		color: #fff;
		font-size: 32rpx;
	}
	
	.btn1{
		background-color: #f05b05;
	}
	
	.btn2{
		background-color: #272555;
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
		height: 70rpx;
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