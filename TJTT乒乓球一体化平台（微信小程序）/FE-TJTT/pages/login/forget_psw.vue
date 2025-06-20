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
					<view class="hint">忘记密码</view>
					<image class="images" src="https://tjtt-assets.oss-cn-shanghai.aliyuncs.com/pictures/logos/logo1.1.png" mode="" />
					<view class="form-group">
						<view class="input_section">
							<view class="title ipt">姓名：</view>
							<input placeholder="请输入姓名" maxlength="100" class="ipt tpyA"
								v-model="username" placeholder-class="phc ipt" />
							<view style="white-space: nowrap;" @click.stop="getCode()">
								{{getCodeText}}</view>
						</view>
						<view class="input_section">
							<view class="title ipt">邮箱验证码：</view>
							<input placeholder="请输入邮箱验证码" maxlength="100" v-model="captcha" class="ipt tpyA"
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
				message: "",
				user: "",
				getCodeText: "获取验证码",
				getCodeisWaiting: false,
				username: "",
				captcha: "",
				hide_this: magic(),
			}
		},
		onLoad() {
		},
		methods: {
			onInput(e){
			    this.username = e.target.value
			    this.captcha = e.target.value
			},
			
			backref() {
				uni.navigateBack({
				    delta: 1
				});
			},
			
			Timer() {},
			
			getCode() {
				let data = {
					"username": this.username,
				};
				fetch_data("POST", "send_captcha", data, "user", res => {
					if (res.data.status == 200){
						if (this.getCodeisWaiting) {
							return;
						};
						this.getCodeText = "发送中"; //发送验证码
						this.getCodeisWaiting = true;
						//示例用定时器模拟请求效果
						//setTimeout(()用于在指定的毫秒数后调用函数或计算表达式
						setTimeout(() => {
							uni.showToast({
								title: res.data.message,
								icon: "none",
								duration: 1500,
							});
							this.setTimer(); //调用定时器方法
						}, 1000);
					}
					else {
						wx.showToast({
							title: res.data.message,
							icon: "none",
							duration: 700,
						});
					};
				});
			},
			//setTimer： 需要每隔一段时间执行一件事的的时候就需要使用SetTimer函数
			setTimer() {
				let holdTime = 60; //定义变量并赋值
				this.getCodeText = "60秒"
				//setInterval（）是一个实现定时调用的函数，可按照指定的周期（以毫秒计）来调用函数或计算表达式。
				//setInterval方法会不停地调用函数，直到 clearInterval被调用或窗口被关闭。
				this.Timer = setInterval(() => {
					if (holdTime <= 0) {
						this.getCodeisWaiting = false;
						this.getCodeText = "获取验证码";
						clearInterval(this.Timer); //清除该函数
						return; //返回前面
					}
					this.getCodeText = holdTime + "秒"
					holdTime--;
				}, 1000)
			},
			
			confirm(){
				wx.showToast({
					title: '请稍后...',
					icon: 'loading',
					duration: 100000,
				});
				let data = {"username": this.username, "captcha": this.captcha}
				fetch_data("POST", "forget_psw", data, "user", res=>{
					console.log(res.data.message);
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