<template>
	<div>
		<section v-if="!hide_this" class="section">
			<div style="margin-top: 18rpx; text-align: center;">
				<button @click='setAbtn(0)' :class="activeBtn == 0 ? 'bg-cyan cu-btn':' cu-btn line-cyan'"
					class="cu-btn">全部</button>
				<button @click='setAbtn(1)'
					:class="activeBtn == 1 ? 'cu-btn bg-purple':'cu-btn line-purple'">技术端</button>
				<button @click='setAbtn(2)'
					:class="activeBtn == 2 ? 'cu-btn bg-blue':'cu-btn line-blue'">组织端</button>
				<button @click='setAbtn(3)'
					:class="activeBtn == 3 ? 'cu-btn bg-orange':'cu-btn line-orange'">文化端</button>
			</div>
			<div v-for="(TJTTer, index) in this.TJTTers" :key="index" class="boxList flex">
				<div class="left" @click="avatar_operation(TJTTer)">
					<img v-if="TJTTer.avatar_url" class="lIcon" :src="TJTTer.avatar_url" alt="AVATAR" />
					<img v-else class="lIcon" src="https://tjtt-assets.oss-cn-shanghai.aliyuncs.com/pictures/avatars/unlogined.png" alt="" />
				</div>
				<div class="right" style="font-weight: bold;">
					<div v-if="TJTTer.gender=='男'" class="text1" style="color: #0081ff; display: flex; white-space: nowrap;">{{TJTTer.name}}&nbsp;&nbsp;&nbsp;&nbsp;<div v-if="TJTTer.email" class="text3">Email: {{TJTTer.email}}</div></div>
					<div v-else-if="TJTTer.gender=='女'" class="text1" style="color: #f37b1d; display: flex; white-space: nowrap;">{{TJTTer.name}}&nbsp;&nbsp;&nbsp;&nbsp;<div v-if="TJTTer.email" class="text3">Email: {{TJTTer.email}}</div></div>
					<div class="text2">{{TJTTer.department}} | {{TJTTer.job}}</div>
					<div class="text2">{{TJTTer.property}}</div>
					<div v-if="TJTTer.description" class="text3 flex" style="margin-top: 25rpx;">
						<div class="time">
							简介：{{TJTTer.description}}
						</div>
					</div>
				</div>
			</div>
		</section>
		<div style="visibility: hidden;">————————</div>
		<div style="visibility: hidden;">————————</div>
		<div style="visibility: hidden;">————————</div>
	</div>
</template>

<script>
	import { fetch_data } from '../../static/js/ajax_request.js'
	import { login_check } from '../../static/js/login_check.js'
	import { magic } from '../../static/js/magic_power.js'
	import * as utils from '../../static/js/utils.js'
	export default {
		data() {
			return {
				user: "",
				activeBtn: 0,
				current: 0,
				TJTTers: [],
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
			
			// 获取TJTT工作室成员
			wx.showToast({
				title: '加载中',
				icon: 'loading',
				duration: 100000,
			});
			fetch_data("POST", "update_TJTTers", null, "application", res => {
				console.log(res.data.message);
			});
			fetch_data("POST", "get_TJTTers", null, "application", res => {
				this.TJTTers = res.data.TJTTers;
				wx.hideToast();
			});
		},
		methods: {
			setAbtn(e) {
				this.activeBtn = e;
				if (e == 0) {
					wx.showToast({
						title: '加载中',
						icon: 'loading',
						duration: 100000,
					});
					fetch_data("POST", "get_TJTTers", null, "application", res => {
						this.TJTTers = res.data.TJTTers;
						wx.hideToast();
					});
				}
				else if (e == 1) {
					wx.showToast({
						title: '加载中',
						icon: 'loading',
						duration: 100000,
					});
					fetch_data("POST", "get_dept_technology_TJTTers", null, "application", res => {
						this.TJTTers = res.data.TJTTers;
						wx.hideToast();
					});
				}
				else if (e == 2) {
					wx.showToast({
						title: '加载中',
						icon: 'loading',
						duration: 100000,
					});
					fetch_data("POST", "get_dept_organizing_TJTTers", null, "application", res => {
						this.TJTTers = res.data.TJTTers;
						wx.hideToast();
					});
				}
				else if (e == 3) {
					wx.showToast({
						title: '加载中',
						icon: 'loading',
						duration: 100000,
					});
					fetch_data("POST", "get_dept_culture_TJTTers", null, "application", res => {
						this.TJTTers = res.data.TJTTers;
						wx.hideToast();
					});
				};
			},
			
			avatar_operation(TJTTer) {
				if (this.user.usertype != 'K11') {
					let avatarUrl = TJTTer.avatar_url;
					if (avatarUrl) {
						wx.previewImage({
							urls: [avatarUrl],
							current: avatarUrl,
						});
					};
				}
				else {
					wx.showActionSheet({
						itemList: ['查看头像', '修改信息'],
						success: (res) => {
							if (!res.cancel) {
								let avatarUrl = TJTTer.avatar_url;
								if (res.tapIndex == 0) {
									if (avatarUrl) {
										wx.previewImage({
											urls: [avatarUrl],
											current: avatarUrl,
										});
									}
									else {
										wx.showToast({
											title: "该成员暂未上传头像",
											icon: "none",
											duration: 1000,
										});
									};
								}
								else if (res.tapIndex == 1) {
									uni.setStorageSync("TJTTer_id", TJTTer.id);
									uni.navigateTo({
										url: '/pages/apps/modify-TJTTer-info',
									})
								}
								else if (res.tapIndex == 2) {
									if (!avatarUrl) {
										wx.showToast({
											title: "该用户还未上传头像",
											icon: "none",
											duration: 1000,
										});
										return;
									}
									wx.showModal({
										title: '删除头像',
										content: '确定删除该用户头像？',
										success: res => {
											if (res.confirm) {
												let data = {
													"my_id": this.user.id,
													"user_id": this.user_x.id,
												}
												fetch_data("POST", "delete_user_profile_img", data, "user", res => {
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
											}
										}
									})
								};
							}
						}
					});
				}
			},
		},				
	}
</script>


<style lang="scss" scoped>
	.head {
		position: relative;
		
		.headTitle {
			font-weight: 600;
			font-size: 35rpx;
			color: #212121;
			line-height: 36rpx;
			position: absolute;
			text-align: center;
			width: 100%;
			top: 100rpx;
			z-index: 999;
			position: fixed;
		}
	}
	
	.section {
		background: #ffffff;
		border-radius: 20rpx 20rpx 20rpx 20rpx;
		box-sizing: border-box;
		padding: 20rpx;

		.cu-btn {
			margin-right: 20rpx;
		}

		.boxList {
			margin-top: 6rpx;
			box-sizing: border-box;
			padding: 30rpx 20rpx;
			padding-top: 40rpx;
			border-bottom: 1px solid #f2f2f2;

			.left {
				width: 15%;
			}

			.right {
				.quan {
					margin-right: 4rpx;
					border-radius: 50%;
					background: #d9d9d9;
					width: 28rpx;
					height: 28rpx;
					display: inline-block;
					position: relative;
					top: 4rpx;

				}

				.text1 {
					font-weight: bold;
					font-size: 32rpx;
					color: #333333;
					line-height: 35rpx;
				}

				.text2 {
					margin-top: 28rpx;
					font-weight: bold;
					font-size: 28rpx;
					color: black;
					line-height: 22rpx;
				}

				.text3 {
					font-weight: 500;
					font-size: 26rpx;
					color: #999999;
					line-height: 38rpx;
					text-align: justify;
				}

				width: 83%;
			}

			.lIcon {
				width: 80rpx;
				height: 80rpx;
				border-radius: 50%;
			}
		}
	}

	.phb {
		.yjfk {
			font-size: 28rpx;
			color: #333333;
			line-height: 28rpx;
		}

		box-sizing: border-box;
		padding: 30rpx;
		background-color: white;
		margin-top: 35rpx;
		background: #FEF2DA;
		border-radius: 14rpx;

		.jf {
			font-family: PingFang SC, PingFang SC;
			font-weight: 400;
			font-size: 28rpx;
			color: #282456;
			line-height: 36rpx;
			text-align: left;
			font-style: normal;
			text-transform: none;
		}

		.num {
			font-family: PingFang SC, PingFang SC;
			font-weight: bold;
			font-size: 48rpx;
			color: #282456;
			line-height: 48rpx;
			text-align: center;
			font-style: normal;
			text-transform: none;
		}
	}
	
	.time {
		margin-top: 10rpx;
		box-sizing: box-sizing;
		padding: 20rpx;
		background: #f2c7ff;
		border-radius: 8rpx 8rpx 8rpx 8rpx;
		font-weight: 500;
		font-size: 24rpx;
		color: #000000;
		line-height: 30rpx;
		text-align: justify;
	}
	
	.headBox {
		background: linear-gradient(135deg, #FEF2DA, #FFD5A4);
		box-sizing: border-box;
		padding: 20rpx;
	}

	.topHead {
		margin-top: 50rpx;
	}

	.icon {
		margin-right: 30rpx;
		width: 37rpx;
		height: 37rpx;
	}
</style>