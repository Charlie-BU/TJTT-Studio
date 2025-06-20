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
					<view class="hint">添加用户</view>
					<view class="form-group">
						<image class="images"
							src="https://tjtt-assets.oss-cn-shanghai.aliyuncs.com/pictures/logos/logo1.1.png"
							mode="" />
						<view class="input_section">
							<view class="title ipt">* 姓名：</view>
							<input placeholder="请输入用户真实姓名" maxlength="100" class="ipt tpyA"
								v-model="username" placeholder-class="phc ipt" />
						</view>
						<view class="input_section">
							<view class="title ipt">* 性别：</view>
							<radio-group @change="which_gender">
								<label class="radio" style="margin-left: 15rpx; margin-right: 20rpx;">
									<radio value="男" color="#FFCC33" style="transform:scale(0.7)" />男
								</label>
								<label class="radio">
									<radio value="女" color="#FFCC33" style="transform:scale(0.7)" />女
								</label>
							</radio-group>
						</view>
						<view class="input_section">
							<view class="title ipt">手机号：</view>
							<input placeholder="请输入用户手机号" maxlength="100" class="ipt tpyA" v-model="phone"
								placeholder-class="phc ipt" />
						</view>
						<view class="input_section">
							<view class="title ipt">电子邮箱：</view>
							<input placeholder="请输入用户电子邮箱" maxlength="100" class="ipt tpyA" v-model="email"
								placeholder-class="phc ipt" />
						</view>
						<view class="input_section">
							<view class="title ipt">所在地区：</view>
							<picker mode="region" class="ipt tpyA" @change="pick_addr">
								<view style="color: #828182;">{{ address ? address : "请选择用户所在地区" }} <u-icon name="arrow-down" size="28" /></view>
							</picker>
						</view>
						<view class="input_section">
							<view class="title ipt">学校：</view>
							<input placeholder="请输入用户所在学校" maxlength="100" class="ipt tpyA" v-model="school"
								placeholder-class="phc ipt" />
						</view>
						<view class="input_section">
							<view class="title ipt">* 身份：</view>
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
							<view class="title ipt">学号 / 工号：</view>
							<input placeholder="请输入用户学号 / 工号" maxlength="100" class="ipt tpyA" v-model="stu_num"
								placeholder-class="phc ipt" />
						</view>
						<view class="input_section">
							<view class="title ipt">* 密码：</view>
							<input placeholder="请输入用户密码" maxlength="100" v-model="password" class="ipt tpyA"
								type="password" placeholder-class="phc ipt" />
						</view>
						<view class="input_section">
							<view class="title ipt">TJTT积分：</view>
							<input placeholder="请输入用户TJTT积分" maxlength="100" class="ipt tpyA" v-model="score"
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
				username: "",
				gender: "",
				phone: "",
				email: "",
				address: "",
				school: "",
				role: "",
				stu_num: "",
				password: "",
				score: "",
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
		},
		methods: {
			onInput(e) {
				this.username = e.target.value
				this.phone = e.target.value
				this.email = e.target.value
				this.school = e.target.value
				this.stu_num = e.target.value
				this.password = e.target.value
				this.score = e.target.value
			},
			
			pick_addr(event) {
			      const selected_addr = event.detail.value;
				this.address = selected_addr[1];
			},
			which_gender(e) {
				this.gender = e.detail.value
			},
			which_role(e) {
				this.role = e.detail.value
			},

			backref() {
				uni.navigateBack({
					delta: 1
				});
			},

			add_user() {
				wx.showToast({
					title: '添加中',
					icon: 'loading',
					duration: 100000,
				});
				let data = {
					"my_id": this.user.id,
					"username": this.username,
					"gender": this.gender,
					"phone": this.phone,
					"email": this.email,
					"address": this.address,
					"school": this.school,
					"role": this.role,
					"stu_num": this.stu_num,
					"password": this.password,
					"score": this.score,
				}
				fetch_data("POST", "add_user", data, "user", res => {
					wx.showToast({
						title: res.data.message,
						icon: "none",
						duration: 700,
					});
					if (res.data.status == 200) {
						setTimeout(() => {
							uni.reLaunch({
								url: '/page_subjec/user/user-list',
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