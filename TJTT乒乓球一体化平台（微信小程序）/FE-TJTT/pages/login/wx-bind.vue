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
					<view class="hint">微信绑定</view>
					<image class="images" src="https://tjtt-assets.oss-cn-shanghai.aliyuncs.com/pictures/logos/logo1.1.png" mode="" />
					<view class="form-group">
						<view class="input_section">
							<view class="title ipt">姓名：</view>
							<input placeholder="请输入姓名" maxlength="100" class="ipt tpyA"
								v-model="username" placeholder-class="phc ipt" />
						</view>
						<view class="input_section">
							<view class="title ipt">密码：</view>
							<input placeholder="请输入密码" maxlength="100" v-model="password" class="ipt tpyA"
								type="password" placeholder-class="phc ipt" />
						</view>
					</view>
					<button class="btn btn1 round" @click="confirm">确定</button>
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
				hide_this: magic(),
			}
		},
		onLoad() {
		},
		methods: {
			onInput(e){
			    this.username = e.target.value
			    this.password = e.target.value
			},
			
			backref() {
				uni.navigateBack({
				    delta: 1
				});
			},
			
			confirm(){
				wx.showToast({
					title: '请稍后...',
					icon: 'loading',
					duration: 100000,
				});
				const username = this.username;
				const password = this.password;
				wx.login({		// 这个里面this.xxx变undefined， 所以在外面用const重新定义
					success(r) {
						if (r.code) {
							fetch_data("POST", "fetch_openid", { "code": r.code }, "user", res => {
								if (res.data.openid) {
									let data = {"username": username, "password": password, "openid": res.data.openid};
									fetch_data("POST", "bind_wx", data, "user", res=>{
										wx.showToast({
											title: res.data.message,
											icon: "none",
											duration: 700,
										});
										if (res.data.status == 200){
											setTimeout(() => {
												uni.reLaunch({
													url: '/pages/login/login',
												})
											}, 700);
										}
									})
								}
							})
						} else {
							wx.showToast({
								title: "绑定失败，请联系TJTT Studio成员",
								icon: "none",
								duration: 700,
							});
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
		height: 1600rpx;
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
		width: 600rpx;
		background-color: #fff;
		height: 55%;
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