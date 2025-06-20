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
					<view class="hint">用户注册</view>
					<view class="form-group">
						<image class="images"
							src="https://tjtt-assets.oss-cn-shanghai.aliyuncs.com/pictures/logos/logo1.1.png"
							mode="" />
						<view class="input_section">
							<view class="title ipt">姓名：</view>
							<input placeholder="请输入真实姓名" maxlength="100" class="ipt tpyA"
								v-model="username" placeholder-class="phc ipt" />
						</view>
						<view class="input_section">
							<view class="title ipt">性别：</view>
							<radio-group @change="which_gender">
								<label class="radio" style="margin-left: 15rpx; margin-right: 20rpx;">
									<radio value="男" color="#FFCC33" style="transform:scale(0.7)" />
									男
								</label>
								<label class="radio">
									<radio value="女" color="#FFCC33" style="transform:scale(0.7)" />
									女
								</label>
							</radio-group>
						</view>
						<view class="input_section">
							<view class="title ipt">手机号：</view>
							<input placeholder="请输入手机号" maxlength="100" class="ipt tpyA" v-model="phone"
								placeholder-class="phc ipt" />
						</view>
						<view class="input_section">
							<view class="title ipt">电子邮箱：</view>
							<input placeholder="请输入电子邮箱" maxlength="100" class="ipt tpyA" v-model="email"
								placeholder-class="phc ipt" />
						</view>
						<view class="input_section">
							<view class="title ipt">学校：</view>
							<input placeholder="请输入所在学校" maxlength="100" class="ipt tpyA" v-model="school"
								placeholder-class="phc ipt" />
						</view>
						<view class="input_section">
							<view class="title ipt">身份：</view>
							<radio-group @change="which_role">
								<label class="radio" style="margin-left: 15rpx; margin-right: 20rpx;">
									<radio value="学生" color="#FFCC33" style="transform:scale(0.7)" />
									学生
								</label>
								<label class="radio">
									<radio value="教师" color="#FFCC33" style="transform:scale(0.7)" />
									教师
								</label>
								<label class="radio" style="white-space: pre-wrap;">\n&nbsp;
									<radio value="校友及校外人士" color="#FFCC33" style="transform:scale(0.7)" />
									校友及校外人士
								</label>
							</radio-group>
						</view>
						<view class="input_section">
							<view class="title ipt">密码：</view>
							<input placeholder="请输入密码" maxlength="100" v-model="password" class="ipt tpyA"
								type="password" placeholder-class="phc ipt" />
						</view>
						<view class="input_section">
							<view class="title ipt">确认密码：</view>
							<input placeholder="请再次输入密码" maxlength="100" v-model="password2"
								class="ipt tpyA" type="password" placeholder-class="phc ipt" />
						</view>
						<view class="input_section">
							<radio-group @change="whether_agree">
								<label class="radio" style="white-space: nowrap; display: flex; margin-left: 20rpx;">
									<radio value="agreed" color="#FFCC33"
										style="transform:scale(0.7);" />同意小程序的<view @click="policy" style="color: blue;">协议与隐私政策</view>
								</label>
							</radio-group>
						</view>
					</view>
					<button class="btn round" style="background-color: #f05b05;" @click="register">注册</button>
					<button class="btn round" style="background-color: #272555;"
						@click="login_page">登录</button>
				</view>
			</view>
			<view class="bottom">
			</view>
		</view>
	</view>
</template>

<script>
	import { fetch_data } from '../../static/js/ajax_request.js'
	import { magic } from '../../static/js/magic_power.js'
	export default {
		data() {
			return {
				message: "",
				user: "",
				username: "",
				gender: "",
				phone: "",
				email: "",
				school: "",
				role: "",
				password: "",
				password2: "",
				agree: "disagreed",
				hide_this: magic(),
			}
		},
		onLoad() {
		},
		methods: {
			onInput(e) {
				this.username = e.target.value
				this.phone = e.target.value
				this.email = e.target.value
				this.school = e.target.value
				this.password = e.target.value
				this.password2 = e.target.value
			},

			which_gender(e) {
				this.gender = e.detail.value
			},
			which_role(e) {
				this.role = e.detail.value
			},
			whether_agree(e) {
				this.agree = e.detail.value
			},

			backref() {
				uni.navigateBack({
					delta: 1
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
			
			register() {
				wx.showToast({
					title: '注册中',
					icon: 'loading',
					duration: 100000,
				});
				let data = {
					"username": this.username,
					"gender": this.gender,
					"phone": this.phone,
					"email": this.email,
					"school": this.school,
					"role": this.role,
					"password": this.password,
					"password2": this.password2,
					"agree": this.agree,
				}
				fetch_data("POST", "register", data, "user", res => {
					wx.showToast({
						title: res.data.message,
						icon: "none",
						duration: 700,
					});
					if (res.data.status == 200) {
						setTimeout(() => {
							uni.reLaunch({
								url: '/pages/login/wx-bind',
							})
						}, 700);
					}
				})
			},
			login_page() {
				uni.navigateTo({
					url: '/pages/login/login',
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
	/* packageA/supplierLogin/index.wxss */

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
		width: 650rpx;
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