<template>
	<div class="app">
		<div class="phb flex">
			<div>
				<div>
					<span class="num">{{user_length}}</span>
					<span class="jf" style="margin-left: 20rpx">人</span>
				</div>
				<div style="color: #666666; margin-top: 20rpx" class="jf">
					用户总数
				</div>
			</div>
			<div>
				<div>
					<span class="num">{{student_length}}</span>
					<span class="jf" style="margin-left: 20rpx">人</span>
				</div>
				<div style="color: #666666; margin-top: 20rpx" class="jf">
					学生人数
				</div>
			</div>
			<div>
				<div>
					<span class="num">{{teacher_length}}</span>
					<span class="jf" style="margin-left: 20rpx">人</span>
				</div>
				<div style="color: #666666; margin-top: 20rpx" class="jf">
					教师人数
				</div>
			</div>
			<div>
				<div>
					<span class="num">{{admin_length}}</span>
					<span class="jf" style="margin-left: 20rpx">人</span>
				</div>
				<div style="color: #666666; margin-top: 20rpx" class="jf">
					管理员
				</div>
			</div>
		</div>

		<section class="section">
			<div style="display: flex;">
				<u-search v-model="search_user" bg-color="#ffffff" :show-action="false" placeholder="输入用户姓名"></u-search>
				<button class="cu-btn btn round line-cyan" style="margin: 8rpx 20rpx;" @click="search">查找</button>
				<button v-if="!hide_this" class="cu-btn btn round line-cyan" style="margin: 8rpx 20rpx;" @click="add_user">+ 添加用户</button>
			</div>
			<div v-for="(user, index) in users" :key="index" class="boxList flex">
				<div class="left">
					<img v-if="user.profile_img" class="lIcon"
						:src="user.profile_img"
						alt="" />
					<img v-else class="lIcon"
						src="https://tjtt-assets.oss-cn-shanghai.aliyuncs.com/pictures/avatars/player.png"
						alt="" />
				</div>
				<div class="right">
					<div class="text1" style="display: flex;"><p style="color: #d9d9d9;">{{index+1}}&nbsp;&nbsp;</p>{{user.username}}</div>
					<div class="text2">{{user.gender}} | {{user.school}} | {{user.role}}</div>
					<div class="text3 flex">
						<div class="l" style="font-size: 28rpx; color: #f25c07;">
							<div class="quan"></div>
							TJTT积分：{{user.score}}
						</div>
					</div>
					<div class="text3 flex" style="margin: 50rpx 0 -20rpx 0;">
						<div class="r">
							<button style="position: relative; bottom: 12px; margin-left: 190rpx;"
								class="cu-btn btn round line-orange" @click="modify_score(user.id)">
								积分变更
							</button>
						</div>
						<div class="r">
							<button style="position: relative; bottom: 12px;"
								class="cu-btn btn round line-cyan" @click="user_detail(user.id)">
								详情
							</button>
						</div>
					</div>
				</div>
			</div>
		</section>
	</div>
</template>

<script>
	import { fetch_data } from '../../static/js/ajax_request.js'
	import { login_check } from '../../static/js/login_check.js'
	import { magic } from '../../static/js/magic_power.js'
	export default {
		data() {
			return {
				user: "",
				message: "",
				user_length: "",
				student_length: "",
				teacher_length: "",
				admin_length: "",
				search_user: "",
				users: [],
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
			// 获取信息
			wx.showToast({
				title: '加载中',
				icon: 'loading',
				duration: 100000,
			});
			fetch_data("POST", "get_info", null, "user", res => {
				this.user_length = res.data.user_length;
				this.student_length = res.data.student_length;
				this.teacher_length = res.data.teacher_length;
				this.admin_length = res.data.admin_length;
			});
			// 获取用户
			fetch_data("POST", "get_users_by_join_time", null, "user", res => {
				this.users = res.data.users;
				wx.hideToast();
			});
			
		},
		methods: {
			onInput(e) {
				this.search_user = e.target.value
			},
			
			search() {
				let data = {"search_user": this.search_user, "where": "user_list"};
				fetch_data("POST", "findUserByName", data, "user", res => {
					this.users = res.data.users;
				});
			},
			
			add_user() {
				uni.navigateTo({
					url: '/page_subjec/user/add-user',
				})
			},
			
			modify_score(user_id) {
				wx.showModal({
					title: '变更用户积分',
					placeholderText: '请输入变更后积分',
					editable: true,
					confirmText: "确认变更",
					success: res => {
						if (res.confirm) {
							let data = {
								"my_id": this.user.id,
								"user_id": user_id,
								"score": res.content,
							}
							fetch_data("POST", "modify_score", data, "user", res => {
								wx.showToast({
									title: res.data.message,
									icon: "none",
									duration: 1000,
								});
								if (res.data.status == 200){
									fetch_data("POST", "get_users", null, "user", res => {
										this.users = res.data.users;
										if (res.data.status == 200) {
											wx.showToast({
												title: res.data.message,
												icon: "none",
												duration: 1000,
											});
										}
									});
								}
							})
						}
					}
				})
			},
			
			user_detail(user_id) {
				uni.setStorageSync("user_id", user_id);
				uni.navigateTo({
					url: '/page_subjec/user/user-detail',
				})
			},
		},
	}
</script>

<style lang="scss" scoped>
	.foot {

		.left {
			text-align: center;
			background-color: #ffffff;
			box-sizing: box-sizing;
			padding: 20rpx;
			padding-top: 36rpx;
			margin-top: 25rpx;
			width: 47%;
			height: 208rpx;

			border-radius: 20rpx 20rpx 20rpx 20rpx;
		}

		.lIcons {
			width: 104rpx;
			height: 104rpx;
			border-radius: 50%;
		}

		.pt {
			font-weight: 500;
			font-size: 28rpx;
			color: #212121;
			margin-top: 14rpx;
			line-height: 30rpx;
		}

		.r {
			background-color: #f9d67a !important;
		}
	}

	.app {
		height: 1800rpx;
		background: linear-gradient(135deg, #FEF2DA, #FFD5A4);
		box-sizing: border-box;
		padding: 20rpx;
	}

	.section {
		background: #ffffff;
		border-radius: 20rpx 20rpx 20rpx 20rpx;
		box-sizing: border-box;
		padding: 20rpx;
	
		.cu-btn {
			margin-right: 20rpx;
			white-space: nowrap;
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
					font-weight: 500;
					font-size: 32rpx;
					color: #333333;
					line-height: 32rpx;
				}
	
				.text2 {
					margin-top: 28rpx;
					font-weight: 500;
					font-size: 28rpx;
					color: #999999;
					line-height: 40rpx;
				}
	
				.text3 {
					margin-top: 28rpx;
					font-weight: 500;
					font-size: 24rpx;
					color: #999999;
					line-height: 24rpx;
				}
	
				width: 83%;
			}
	
			.lIcon {
				width: 80rpx;
				height: 80rpx;
	
				border-radius: 12rpx 12rpx 12rpx 12rpx;
			}
		}
	}
	
	.text {
		font-weight: 600;
		font-size: 32rpx;
		box-sizing: border-box;
		padding-top: 22rpx;
	}
	
	.divider {
		background-color: #f2f2f2;
		margin: 28rpx 0rpx;
		height: 1rpx;
	}

	.codeA {
		text-align: left !important;
		padding: 30rpx !important;

		.xian {
			background-color: #f2f2f2;
			margin: 28rpx 0rpx;
			height: 1rpx;
		}

		.tipTit {
			font-weight: 600;
			font-size: 32rpx;
			color: #333333;
			line-height: 32rpx;
		}

		.textDiv {
			margin-top: 20rpx;
			font-weight: 400;
			font-size: 24rpx;
			color: #333333;
			line-height: 44rpx;
		}
	}

	.code {
		box-sizing: border-box;
		padding: 50rpx;
		background-color: white;
		position: relative;
		top: -70rpx;
		border-radius: 28rpx;
		text-align: center;

		.codeImg {
			width: 320rpx;
			height: 320rpx;
		}

		.tis {
			margin: 36rpx 0rpx;
			font-weight: 400;
			font-size: 24rpx;
			color: #666666;
			line-height: 24rpx;
		}

		.title {
			margin-top: 22rpx;
			font-weight: 600;
			font-size: 40rpx;
			color: #000000;
			line-height: 40rpx;
		}
	}

	.bc {
		margin-top: 30rpx;
		background-color: #eed4bd;
		box-sizing: box-sizing;
		padding: 18rpx 20rpx;
		border-radius: 20rpx;
		padding-bottom: 90rpx;

		.text1 {
			margin-top: 14rpx;
			font-family: PingFang SC, PingFang SC;
			font-weight: bold;
			font-size: 28rpx;
			color: #333333;
			line-height: 40rpx;
			text-align: left;
			font-style: normal;
			text-transform: none;
		}

		.text2 {
			margin-top: 70rpx;
			font-family: PingFang SC, PingFang SC;
			font-weight: 600;
			font-size: 28rpx;
			color: #f25c07;
			line-height: 40rpx;
			text-align: left;
			font-style: normal;
			text-transform: none;
		}

		.right {
			width: 62%;
		}

		.left {
			width: 34%;

			.bcImg {
				border-radius: 12rpx;
				width: 100%;
				height: 144rpx;
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
		margin-top: 20rpx;
		background: #ffffff;
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
</style>