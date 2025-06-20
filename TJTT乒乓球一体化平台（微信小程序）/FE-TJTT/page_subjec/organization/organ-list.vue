<template>
	<div v-if="!hide_this" class="app">
		<div class="phb flex">
			<div>
				<div>
					<span class="num">{{organ_length}}</span>
					<span class="jf" style="margin-left: 20rpx">个</span>
				</div>
				<div style="color: #666666; margin-top: 20rpx" class="jf">
					全国组织
				</div>
			</div>
			<div>
				<div>
					<span class="num">{{tongji_length}}</span>
					<span class="jf" style="margin-left: 20rpx">个</span>
				</div>
				<div style="color: #666666; margin-top: 20rpx" class="jf">
					同济组织
				</div>
			</div>
			<div>
				<div>
					<span class="num">{{organ_length}}</span>
					<span class="jf" style="margin-left: 20rpx">个</span>
				</div>
				<div style="color: #666666; margin-top: 20rpx" class="jf">
					上海市组织
				</div>
			</div>
		</div>

		<section class="section">
			<div style="display: flex;">
				<u-search v-model="search_organ" bg-color="#ffffff" :show-action="false" placeholder="输入组织名"></u-search>
				<button class="cu-btn btn round line-cyan" style="margin: 8rpx 20rpx;" @click="search">查找</button>
				<button class="cu-btn btn round line-cyan" style="margin: 8rpx 20rpx;" @click="add_organ">+ 添加组织</button>
			</div>
			<div v-for="(organ, index) in organs" :key="index" class="boxList flex">
				<div class="left">
					<img class="lIcon"
						src="https://tjtt-assets.oss-cn-shanghai.aliyuncs.com/pictures/avatars/player.png"
						alt="" />
				</div>
				<div class="right">
					<div class="text1" style="display: flex;"><p style="color: #d9d9d9;">{{index+1}}&nbsp;&nbsp;</p>{{organ.organname}}</div>
					<div class="text2 flex">{{organ.description}}</div>
					<div class="text3 flex" style="margin: 50rpx 0 -20rpx 0; text-align: end;">
						<div class="r">
							<button style="position: relative; bottom: 12px;"
								class="cu-btn btn round line-blue">
								组织成员：{{organ.member_length}}人
							</button>
							<button style="position: relative; bottom: 12px;"
								class="cu-btn btn round line-red" @click="delete_organ(organ.id)">
								删除组织
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
				organ_length: "",
				tongji_length: "",
				search_organ: "",
				organs: [],
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
			fetch_data("POST", "get_info", null, "organization", res => {
				this.organ_length = res.data.organ_length;
				this.tongji_length = res.data.tongji_length;
			});
			// 获取组织
			fetch_data("POST", "get_organs", null, "organization", res => {
				this.organs = res.data.organs;
				wx.hideToast();
			});
			
		},
		methods: {
			onInput(e) {
				this.search_user = e.target.value
			},
			
			search() {
				let data = {"search_organ": this.search_organ};
				fetch_data("POST", "findOrganByName", data, "organization", res => {
					this.organs = res.data.organs;
				});
			},
			
			add_organ() {
				uni.navigateTo({
					url: '/page_subjec/organization/add-organ',
				})
			},
			
			delete_organ(organ_id) {
				wx.showModal({
					title: '删除组织',
					content: '删除组织后，该组织所有信息将被永久清除；该操作可能导致数据库混乱、系统崩溃，请上报K11级管理员后操作',
					success: res => {
						if (res.confirm) {
							let data = {
								"my_id": this.user.id,
								"organ_id": organ_id,
							}
							fetch_data("POST", "delete_organ", data, "organization", res => {
								wx.showToast({
									title: res.data.message,
									icon: "none",
									duration: 1000,
								});
								if (res.data.status == 200){
									setTimeout(() => {
										uni.reLaunch({
											url: '/page_subjec/organization/organ-list',
										})
									}, 1000);
								}
							})
						}
					}
				});
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
					line-height: 28rpx;
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
			line-height: 28rpx;
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