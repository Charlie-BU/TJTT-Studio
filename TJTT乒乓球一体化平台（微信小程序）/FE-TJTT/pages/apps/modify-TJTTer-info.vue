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
					<view class="hint">修改TJTT工作室成员信息</view>
					<view class="form-group">
						<image class="images" src="https://tjtt-assets.oss-cn-shanghai.aliyuncs.com/pictures/logos/logo1.1.png" mode="" />
						<view class="input_section">
							<view class="title ipt">姓名：</view>
							<input maxlength="100" class="ipt tpyA" v-bind:value="TJTTer.name" disabled />
						</view>
						<view class="input_section">
							<view class="title ipt">职能部：</view>
							<radio-group @change="which_department">
								<label v-for="department in ['技术端', '组织端', '文化端']" :key="department"
									class="radio" style="margin-left: 15rpx; margin-right: 20rpx; display: block;">
									<radio :value="department" color="#FFCC33"
										style="transform:scale(0.7)"
										:checked="TJTTer.department === department" />
									{{ department }}
								</label>
							</radio-group>
						</view>
						
						<view class="input_section">
							<view class="title ipt">职务：</view>
							<radio-group @change="which_job">
								<view v-for="job in ['负责人', '顾问', '组长', '成员']" :key="job">
									<label class="radio"
										style="margin-left: 15rpx; margin-right: 20rpx; display: block;">
										<radio :value="job" color="#FFCC33"
											style="transform:scale(0.7)"
											:checked="TJTTer.job === job" />
										{{ job }}
									</label>
								</view>
							</radio-group>
						</view>
						
						<view class="input_section">
							<view class="title ipt">成员属性：</view>
							<radio-group @change="which_property">
								<view v-for="property in ['0期创始成员', '1期成员', '2期成员']" :key="property">
									<label class="radio"
										style="margin-left: 15rpx; margin-right: 20rpx; display: block;">
										<radio :value="property" color="#FFCC33"
											style="transform:scale(0.7)"
											:checked="TJTTer.property === property" />
										{{ property }}
									</label>
								</view>
							</radio-group>
						</view>
						
						<view class="input_section">
							<view class="title ipt">个人简介：</view>
							<textarea maxlength="-1" class="ipt tpyA" style="height: 200rpx;" v-model="description" v-bind:placeholder="TJTTer.description" />
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
				TJTTer: "",
				department: "",
				job: "",
				property: "",
				description: "",
				hide_this: magic(),
			}
		},
		onLoad() {
			login_check(user => {
				this.user = user;
			});
			if (!this.user || (this.user.usertype != "K11")) {
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
			
			let TJTTer_id = uni.getStorageSync("TJTTer_id");
			if (!TJTTer_id) {
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
				fetch_data("POST", "get_this_TJTTer", {"TJTTer_id": TJTTer_id}, "user", res => {
					this.TJTTer = res.data.TJTTer;
				});
			};
		},
		methods: {
			onInput(e) {
				this.description = e.target.value
			},
			
			which_department(e) {
				this.department = e.detail.value
			},
			which_job(e) {
				this.job = e.detail.value
			},
			which_property(e) {
				this.property = e.detail.value
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
					"TJTTer_id": this.TJTTer.id,
					"department": this.department,
					"job": this.job,
					"property": this.property,
					"description": this.description,
				};
				fetch_data("POST", "modify_TJTTer_info", data, "user", res => {
					wx.showToast({
						title: res.data.message,
						icon: "none",
						duration: 1000,
					});
					if (res.data.status == 200){
						setTimeout(() => {
							uni.reLaunch({
								url: '/pages/apps/TJTTers',
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