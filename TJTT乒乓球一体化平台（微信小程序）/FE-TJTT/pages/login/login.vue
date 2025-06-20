<template>
	<view class="main">
		<view class="main">
			<view class="pagenation">
				<view class="pagenation_back" @tap="backref()">
					<image class="back_arrow" src="..\..\static\tabbar\back.png" mode="" />
				</view>
			</view>
			<view class="login">
				<view class="kuang shadow">
					<view class="hint">用户登录</view>
					<image class="images" src="https://tjtt-assets.oss-cn-shanghai.aliyuncs.com/pictures/logos/logo1.1.png" mode="" />
					<view class="form-group flex ">
						<view class="title ipt">姓名：</view>
						<input placeholder="请输入姓名" maxlength="100" class="ipt tpyA" v-model="username"
							placeholder-class="phc ipt" />
					</view>
					<view class="form-group flex">
						<view class="title ipt">密码：</view>
						<input placeholder="请输入密码" maxlength="100" v-model="password" class="ipt tpyA"
							type="password" placeholder-class="phc ipt" />
					</view>
					<radio-group @change="whether_agree">
						<label class="radio" style="white-space: nowrap; display: flex;">
							<radio value="agreed" color="#FFCC33"
								style="transform:scale(0.7);" />同意小程序的<view @click="policy" style="color: blue;">协议与隐私政策</view>
						</label>
					</radio-group>
					<button class="btn btn1 round" @click="login">登录</button>
					<button v-if="!hide_this" class="btn btn2 round" style="background-color: #0bd618;" @click="wx_login">微信一键登录</button>
					<button v-if="!hide_this" class="btn btn2 round" @click="register_page">注册</button>
					<button v-if="!hide_this" class="btn btn2 round" @click="login_viaph_page">手机号登录</button>
					<button v-if="!hide_this" class="btn btn2 round" @click="forget_psw_page">忘记密码</button>
				</view>
			</view>
			<view class="bottom">
			</view>
		</view>
	</view>
</template>

<script>
	import { fetch_data } from '../../static/js/ajax_request.js'
	import { wx_login } from '../../static/js/wx_login.js'
	import { login_check } from '../../static/js/login_check.js'
	import { magic } from '../../static/js/magic_power.js'
	import * as utils from '../../static/js/utils.js'
	export default {
		data() {
			return {
				user: "",
				user_token: "",
				username: "",
				password: "",
				agree: "disagreed",
				hide_this: magic(),
			}
		},
		onLoad() {
		},
		methods: {
			onInput(e) {
				this.username = e.target.value
				this.password = e.target.value
			},
			whether_agree(e) {
				this.agree = e.detail.value
			},
			
			backref() {
				uni.reLaunch({
				    url: '/pages/index/index',
				});
			},
			
			policy() {
				wx.showModal({
					title: '用户服务协议与隐私政策',
					content: "1.在您注册、登录本平台之前，请仔细阅读以下用户服务协议。注册/登录本平台，即表示您同意遵守以下协议;2.我们将严格保护用户的个人隐私信息，不会将用户的个人信息透露给任何第三方。但在法律规定的情况下，我们可能会根据相关法律法规要求向有关部门提供用户的个人信息;3. 本平台不对用户因使用本平台服务而产生的任何直接或间接损失承担责任。用户在使用本平台服务时，需自行承担风险，并且同意在任何情况下不追究本平台的责任;4.本平台有权根据需要对用户服务协议进行修改，修改后的协议将在平台上公布。用户继续使用本平台服务即视为同意修改后的协议。",
					showCancel: false,
					confirmText: "同意",
				})
			},
			
			login() {
				wx.showToast({
					title: '登录中',
					icon: 'loading',
					duration: 100000,
				});
				let data = {
					"username": this.username,
					"password": this.password,
					"agree": this.agree,
				}
				fetch_data("POST", "login", data, "user", res => {
					this.user_token = res.data.user_token;
					wx.showToast({
						title: res.data.message,
						icon: "none",
						duration: 700,
					});
					// 登录成功
					if (this.user_token) {
						uni.setStorageSync('user_token', this.user_token);
						var user_token = this.user_token;
						// 异步获取用户信息
						function asyncTask(callback) {
							var user_id = utils.get_user_info(user_token)[0];
							utils.get_my_rank(user_id);
							callback();
						}
						asyncTask(() => {
							console.log('async task finished');
						})
						// -----异步进程结束-----
						
						setTimeout(() => {
							uni.reLaunch({
								url: '/pages/index/index',
							})
						}, 700);
					}
				})
			},
				
			wx_login() {
				if (this.agree != "agreed") {
					wx.showToast({
						title: '请阅读并同意小程序的协议与隐私政策',
						icon: 'none',
						duration: 700,
					});
					return;
				}
				wx.showToast({
					title: '登录中',
					icon: 'loading',
					duration: 100000,
				});
				wx_login();
			},
			
			register_page() {
				uni.navigateTo({
					url: '/pages/login/register',
				})
			},
			login_viaph_page() {
				uni.navigateTo({
					url: '/pages/login/login_viaph',
				})
			},
			forget_psw_page() {
				uni.navigateTo({
					url: '/pages/login/forget_psw',
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
		height: 1050rpx;
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

	.btn1 {
		background-color: #f05b05;
	}

	.btn2 {
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

	.form-group .title {
		font-weight: normal;
	}

	.flex {
		display: flex;
		flex-direction: row;
		justify-content: space-around;
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