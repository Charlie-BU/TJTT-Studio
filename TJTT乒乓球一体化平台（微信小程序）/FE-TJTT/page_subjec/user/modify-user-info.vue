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
					<view class="hint">修改用户信息</view>
					<view class="form-group">
						<image class="images" src="https://tjtt-assets.oss-cn-shanghai.aliyuncs.com/pictures/logos/logo1.1.png" mode="" />
						<view class="input_section">
							<view class="title ipt">姓名：</view>
							<input maxlength="100" class="ipt tpyA" v-bind:value="user_x.username" disabled />
						</view>
						<view class="input_section">
							<view class="title ipt">性别：</view>
							<radio-group @change="which_gender">
								<label v-if="user_x.gender=='男'" class="radio" style="margin-left: 15rpx; margin-right: 20rpx;">
									<radio value="男" color="#FFCC33" style="transform:scale(0.7)" checked />
									男
								</label>
								<label v-else class="radio" style="margin-left: 15rpx; margin-right: 20rpx;">
									<radio value="男" color="#FFCC33" style="transform:scale(0.7)" />
									男
								</label>
								<label v-if="user_x.gender=='女'" class="radio" style="margin-left: 15rpx; margin-right: 20rpx;">
									<radio value="女" color="#FFCC33" style="transform:scale(0.7)" checked />
									女
								</label>
								<label v-else class="radio" style="margin-left: 15rpx; margin-right: 20rpx;">
									<radio value="女" color="#FFCC33" style="transform:scale(0.7)" />
									女
								</label>
							</radio-group>
						</view>
						<view class="input_section">
							<view class="title ipt">所在地区：</view>
							<picker mode="region" class="ipt tpyA" @change="pick_addr">
								<view style="color: #828182;">{{ address ? address : user_x.address }} <u-icon name="arrow-down" size="28" /></view>
							</picker>
						</view>
						<view class="input_section">
							<view class="title ipt">手机号：</view>
							<input maxlength="100" class="ipt tpyA" v-model="phone" v-bind:placeholder="user_x.phone" />
						</view>
						<view class="input_section">
							<view class="title ipt">邮箱：</view>
							<input maxlength="100" class="ipt tpyA" v-model="email" v-bind:placeholder="user_x.email" />
						</view>
						<view class="input_section">
							<view class="title ipt">学校：</view>
							<input maxlength="100" class="ipt tpyA" v-model="school" v-bind:placeholder="user_x.school" />
						</view>
						<view class="input_section">
							<view class="title ipt">身份：</view>
							<radio-group @change="which_role">
								<label v-if="user_x.role=='学生'" class="radio" style="margin-left: 15rpx; margin-right: 20rpx;">
									<radio value="学生" color="#FFCC33" style="transform:scale(0.7)" checked />
									学生
								</label>
								<label v-else class="radio" style="margin-left: 15rpx; margin-right: 20rpx;">
									<radio value="学生" color="#FFCC33" style="transform:scale(0.7)" />
									学生
								</label>
								<label v-if="user_x.role=='教师'" class="radio" style="margin-left: 15rpx; margin-right: 20rpx;">
									<radio value="教师" color="#FFCC33" style="transform:scale(0.7)" checked />
									教师
								</label>
								<label v-else class="radio" style="margin-left: 15rpx; margin-right: 20rpx;">
									<radio value="教师" color="#FFCC33" style="transform:scale(0.7)" />
									教师
								</label>
								<label v-if="user_x.role=='校友及校外人士'" class="radio" style="white-space: pre-wrap;">\n&nbsp;
									<radio value="校友及校外人士" color="#FFCC33" style="transform:scale(0.7)" checked />
									校友及校外人士
								</label>
								<label v-else class="radio" style="white-space: pre-wrap;">\n&nbsp;
									<radio value="校友及校外人士" color="#FFCC33" style="transform:scale(0.7)" />
									校友及校外人士
								</label>
							</radio-group>
						</view>
						<view class="input_section">
							<view class="title ipt">学号 / 工号：</view>
							<input maxlength="100" class="ipt tpyA" v-model="stu_num" v-bind:placeholder="user_x.stu_num" />
						</view>
						<view class="input_section">
							<view class="title ipt">所属组织：</view>
							<radio-group @change="which_organ_id">
								<view v-for="(organ, index) in this.organs" :key="index">
									<label v-if="user_x.organ_id==organ.id" class="radio" style="margin-left: 15rpx;">
										<radio v-bind:value="organ.id" color="#FFCC33" style="transform:scale(0.7)" checked />{{organ.organname}}
									</label>
									<label v-else class="radio" style="margin-left: 15rpx;">
										<radio v-bind:value="organ.id" color="#FFCC33" style="transform:scale(0.7)" />{{organ.organname}}
									</label>
								</view>
							</radio-group>
						</view>
						<view class="input_section">
							<view class="title ipt">执拍手：</view>
							<radio-group @change="which_hand">
								<label v-if="user_x.hand=='右手'" class="radio" style="margin-left: 15rpx; margin-right: 20rpx;">
									<radio value="右手" color="#FFCC33" style="transform:scale(0.7)" checked />
									右手
								</label>
								<label v-else class="radio" style="margin-left: 15rpx; margin-right: 20rpx;">
									<radio value="右手" color="#FFCC33" style="transform:scale(0.7)" />
									右手
								</label>
								<label v-if="user_x.hand=='左手'" class="radio" style="margin-left: 15rpx; margin-right: 20rpx;">
									<radio value="左手" color="#FFCC33" style="transform:scale(0.7)" checked />
									左手
								</label>
								<label v-else class="radio" style="margin-left: 15rpx; margin-right: 20rpx;">
									<radio value="左手" color="#FFCC33" style="transform:scale(0.7)" />
									左手
								</label>
							</radio-group>
						</view>
						<view class="input_section">
							<view class="title ipt">握拍方式：</view>
							<radio-group @change="which_grip">
								<label v-if="user_x.grip=='横拍'" class="radio" style="margin-left: 15rpx; margin-right: 20rpx;">
									<radio value="横拍" color="#FFCC33" style="transform:scale(0.7)" checked />
									横拍
								</label>
								<label v-else class="radio" style="margin-left: 15rpx; margin-right: 20rpx;">
									<radio value="横拍" color="#FFCC33" style="transform:scale(0.7)" />
									横拍
								</label>
								<label v-if="user_x.grip=='直拍'" class="radio" style="margin-left: 15rpx; margin-right: 20rpx;">
									<radio value="直拍" color="#FFCC33" style="transform:scale(0.7)" checked />
									直拍
								</label>
								<label v-else class="radio" style="margin-left: 15rpx; margin-right: 20rpx;">
									<radio value="直拍" color="#FFCC33" style="transform:scale(0.7)" />
									直拍
								</label>
							</radio-group>
						</view>
						<view class="input_section">
							<view class="title ipt">底板型号：</view>
							<input maxlength="100" class="ipt tpyA" v-model="blade" v-bind:placeholder="user_x.blade" />
						</view>
						<view class="input_section">
							<view class="title ipt">正手胶皮：</view>
							<input maxlength="100" class="ipt tpyA" v-model="forehand" v-bind:placeholder="user_x.forehand" />
						</view>
						<view class="input_section">
							<view class="title ipt">反手胶皮：</view>
							<input maxlength="100" class="ipt tpyA" v-model="backhand" v-bind:placeholder="user_x.backhand" />
						</view>
						<view class="input_section">
							<view class="title ipt">是否带颗粒：</view>
							<radio-group @change="which_particle">
								<label v-if="user_x.particle=='是'" class="radio" style="margin-left: 15rpx; margin-right: 20rpx;">
									<radio value="是" color="#FFCC33" style="transform:scale(0.7)" checked />
									是
								</label>
								<label v-else class="radio" style="margin-left: 15rpx; margin-right: 20rpx;">
									<radio value="是" color="#FFCC33" style="transform:scale(0.7)" />
									是
								</label>
								<label v-if="user_x.particle=='否'" class="radio" style="margin-left: 15rpx; margin-right: 20rpx;">
									<radio value="否" color="#FFCC33" style="transform:scale(0.7)" checked />
									否
								</label>
								<label v-else class="radio" style="margin-left: 15rpx; margin-right: 20rpx;">
									<radio value="否" color="#FFCC33" style="transform:scale(0.7)" />
									否
								</label>
							</radio-group>
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
	import { fetch_data } from '../../static/js/ajax_request.js'
	import { login_check } from '../../static/js/login_check.js'
	import { magic } from '../../static/js/magic_power.js'
	export default {
		data() {
			return {
				message: "",
				user: "",
				user_x: "",
				organs: [],
				gender: "",
				address: "",
				phone: "",
				email: "",
				school: "",
				role: "",
				organ_id: "",
				stu_num: "",
				hand: "",
				grip: "",
				blade: "",
				forehand: "",
				backhand: "",
				particle: "",
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
			// 获取用户信息
			let user_id = uni.getStorageSync("user_id");
			if (!user_id) {
				wx.showToast({
					title: "服务器繁忙，请稍后再试",
					icon: "none",
					duration: 1500,
				});
				setTimeout(() => {
					uni.reLaunch({
						url: '/pages/index/index',
					})
				}, 1000);
			}
			else {
				fetch_data("POST", "get_this_user", {"user_id": user_id}, "user", res => {
					this.user_x = res.data.user;
				});
			};
			// 获取组织
			fetch_data("POST", "fetch_organs", null, "competition", res => {
				this.organs = res.data.organs;
			});
		},
		methods: {
			onInput(e) {
				this.phone = e.target.value
				this.email = e.target.value
				this.school = e.target.value
				this.stu_num = e.target.value
				this.blade = e.target.value
				this.forehand = e.target.value
				this.backhand = e.target.value
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
			which_organ_id(e) {
				this.organ_id = parseInt(e.detail.value)
			},
			which_hand(e) {
				this.hand = e.detail.value
			},
			which_grip(e) {
				this.grip = e.detail.value
			},
			which_particle(e) {
				this.particle = e.detail.value
			},

			backref() {
				uni.navigateBack({
					delta: 1
				});
			},

			modify() {
				wx.showToast({
					title: '修改中',
					icon: 'loading',
					duration: 100000,
				});
				let data = {
					"my_id": this.user.id,
					"user_id": this.user_x.id,
					"gender": this.gender,
					"address": this.address,
					"phone": this.phone,
					"email": this.email,
					"school": this.school,
					"role": this.role,
					"organ_id": this.organ_id,
					"stu_num": this.stu_num,
					"hand": this.hand,
					"grip": this.grip,
					"blade": this.blade,
					"forehand": this.forehand,
					"backhand": this.backhand,
					"particle": this.particle,
				}
				fetch_data("POST", "modify_user", data, "user", res => {
					wx.showToast({
						title: res.data.message,
						icon: "none",
						duration: 1000,
					});
					if (res.data.status == 200){
						setTimeout(() => {
							uni.reLaunch({
								url: '/page_subjec/user/user-detail',
							})
						}, 1000);
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