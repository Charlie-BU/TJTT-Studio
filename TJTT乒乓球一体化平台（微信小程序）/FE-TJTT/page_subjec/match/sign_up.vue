<template>
	<view class="main">
		<view class="main">
			<view v-if="!hide_this" class="login">
				<view class="kuang shadow">
					<view class="hint">赛事报名</view>
					<view class="sub">请确认相关信息，阅读并同意承诺书</view>
					<view class="form-group">
						<image class="images" src="https://tjtt-assets.oss-cn-shanghai.aliyuncs.com/pictures/logos/logo1.1.png" mode="" />
						<view class="input_section">
							<view class="title ipt">选手姓名：</view>
							<input maxlength="100" class="ipt tpyA" v-bind:value="user.username"
								disabled />
						</view>
						<view class="input_section">
							<view class="title ipt">手机号：</view>
							<input maxlength="100" class="ipt tpyA" v-bind:value="user.phone" disabled />
						</view>
						<view class="input_section">
							<view class="title ipt">身份：</view>
							<input maxlength="100" class="ipt tpyA" v-bind:value="user.role" disabled />
						</view>
						<view class="input_section">
							<view class="title ipt">积分：</view>
							<input maxlength="100" class="ipt tpyA" v-bind:value="user.score" disabled />
						</view>
						<view class="divider" />
						<view class="input_section">
							<view class="title ipt">报名赛事：</view>
							<input v-if="match" maxlength="100" class="ipt tpyA" v-bind:value="match.title"
								disabled />
						</view>
						<view class="input_section">
							<view class="title ipt">报名限制：</view>
							<input v-if="match" maxlength="100" class="ipt tpyA"
								v-bind:value="match.restriction" disabled />
						</view>
						<view class="input_section">
							<view class="title ipt">剩余参赛名额：</view>
							<input v-if="isNaN(match.participant - match.players_length)" maxlength="100"
								class="ipt tpyA" value="见各队名额" disabled />
							<input v-else maxlength="100" class="ipt tpyA"
								v-bind:value="match.participant - match.players_length" disabled />
						</view>
						<view v-if="match.teams_length != 0" class="input_section">
							<view class="title ipt">报名代表队：</view>
							<radio-group style="width: 100000000rpx;" @change="which_team">
								<label v-for="(team_x, index) in match.teams" :key="index" class="radio"
									style="margin-left: 15rpx; margin-right: 20rpx;">
									<radio v-bind:value="team_x.id" color="#FFCC33" v-html="message"
										style="transform:scale(0.7)" />{{team_x.teamname}}<br />
								</label>
							</radio-group>
						</view>
						<view class="input_section" style="color: red;">
							<view class="title ipt">报名费：\t{{match.fee}} 元</view>
						</view>
						<view class="input_section" style="color: #f05b05;">
							<view>承诺书：<br/>本人真实姓名{{user.username}}，不打假球，不消极比赛，不另注册账号参加积分赛，不找人替打、帮人替打积分赛，营造公平、公正的比赛环境。若违反上述承诺，本人自愿接受“永久取消TJTT积分、禁止参加TJTT积分赛”的处罚。</view>
						</view>
						<radio-group @change="whether_agree">
							<label class="radio">
								<radio value="agreed" color="#FFCC33" style="transform:scale(0.7)" />已阅读并同意承诺书
							</label>
						</radio-group>
					</view>
					<button class="btn round" style="background-color: #f05b05;"
						@click="sign_up">确认报名</button>
					<button class="btn round" style="background-color: #bebebe;" @click="backref">取消</button>
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
	import { wx_pay } from '../../static/js/wx_pay.js'
	import { magic } from '../../static/js/magic_power.js'
	export default {
		data() {
			return {
				message: "",
				user: "",
				match: "",
				team_id: "",
				agree: "",
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
		},
		methods: {
			which_team(e) {
				this.team_id = e.detail.value
			},
			whether_agree(e) {
				this.agree = e.detail.value
			},

			backref() {
				uni.navigateBack({
					delta: 1
				});
			},

			sign_up() {
				if (this.agree !== "agreed") {
					wx.showToast({
						title: "请阅读并同意承诺书",
						icon: "none",
						duration: 1000,
					});
					return;
				}
				if (this.match.fee > 0) {
					this.initiate_payment();
				} else {
					this.confirm_sign_up();
				}
			},
			
			
			initiate_payment() {
				wx.showToast({
					title: '请稍后',
					icon: 'loading',
					duration: 100000,
				});
				wx_pay(this.match.fee, this.user.username+"赛事报名", null,  (res) => {
					if (res) {
						this.confirm_sign_up();
					} else {
						wx.showToast({
							title: "支付失败，请重试",
							icon: "none",
							duration: 1000,
						});
					}
				});
			},
			
			// 确认报名流程
			confirm_sign_up() {
				wx.showToast({
					title: '报名中',
					icon: 'loading',
					duration: 100000,
				});
			
				// 构建报名数据
				const data = {
					match_id: this.match.id,
					user_id: this.user.id,
					team_id: parseInt(this.team_id),
					agree: this.agree,
				};
			
				// 调用报名接口
				fetch_data("POST", "match_sign_up", data, "competition", (res) => {
					wx.showToast({
						title: res.data.message,
						icon: "none",
						duration: 1000,
					});
			
					// 报名成功的处理
					if (res.data.status === 200) {
						setTimeout(() => {
							uni.reLaunch({
								url: '/page_subjec/match/index',
							});
						}, 1000);
					}
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
		width: 600rpx;
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

	.main .login .kuang .sub {
		width: 100%;
		font-size: 30rpx;
		line-height: 60rpx;
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

	.divider {
		background: #e0e2da;
		width: 100%;
		height: 3rpx;
	}
</style>