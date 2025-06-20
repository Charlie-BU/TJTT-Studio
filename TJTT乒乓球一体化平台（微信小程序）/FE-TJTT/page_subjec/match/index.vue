<template>
	<div class="app">
		<u-tabs style="position: relative; bottom: 4rpx;" :list="match_list" bg-color=null
			active-color="#F25C07" font-size="20rpx" is-scroll="true" :current="current" @change="change">
		</u-tabs>
		<div style="display: flex;">
			<u-search class="search_bar" v-model="search_match" bg-color="#ffffff" :show-action="false" placeholder="输入赛事名称"></u-search>
			<button class="cu-btn btn round line-cyan" style="margin-top: 15rpx;" @click="search">查找</button>
		</div>
		<scroll-view class="scroll" scroll-y="auto">
			<div v-if="matches.length != 0" class="box" v-for='(match, index) in matches' :key='index'>
				<div class="flex top">
					<div class="l">赛事 {{index + 1}}</div>
					<div class="r">{{match.match_type}}</div>
				</div>
				<div class="bc flex">
					<div class="left">
						<img class="bcImg" src="https://tjtt-assets.oss-cn-shanghai.aliyuncs.com/pictures/decorations/5.png" alt="" />
					</div>
					<div class="right">
						<div class="text1">{{match.title}}</div>
						<div class="text3">{{ utils.format_time(match.match_time) }}</div>
						<div class="text3">{{match.place}}</div>
						<div class="text2">报名限制：{{match.restriction}}</div>
					</div>
				</div>
				<div class="time">{{match.description}}</div>

				<div v-if="isNaN(match.participant - match.players_length)" class="mon">剩余参赛名额：见各队名额</div>
				<div v-else class="mon">剩余参赛名额：
					<span class="q">{{match.participant - match.players_length}}</span>
				</div>
				<div v-if="!hide_this" style="text-align: right; margin-top: 20rpx;">
					<!-- 样式问题，所以要分情况 -->
					<button v-if="(user.usertype == 'K9' || user.usertype == 'K10' || user.usertype == 'K11') && (match.players_id.includes(user.id))" class="cu-btn btn round line-orange" style="left: -205rpx;" @click="hide_match(match.id)">藏</button>
					<button v-else-if="(user.usertype == 'K9' || user.usertype == 'K10' || user.usertype == 'K11') && (!match.players_id.includes(user.id))" class="cu-btn btn round line-orange" style="left: -260rpx;" @click="hide_match(match.id)">藏</button>
					<button v-if="(match.players_id.includes(user.id))" class="cu-btn btn round line-orange"
						@click="quit(match.id)">取消报名</button>
					<button v-else class="cu-btn btn round line-orange" @click="sign_up_page(match.id)">报名</button>
					<button class="cu-btn btn round line-cyan" @click="match_detail_page(match.id)">赛事详情</button>
				</div>
			</div>
			<div v-else style="text-align: center; margin-top: 40rpx;">无赛事信息</div>
		</scroll-view>
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
				search_match: "",
				matches: [],
				match_list: [{
						name: "当前赛事",
					},
					{
						name: "已报名赛事",
					},
					{
						name: "历史赛事",
					},
					{
						name: "全部赛事",
					},
				],
				current: 0,
				hide_this: magic(),
			}
		},
		onLoad() {
			uni.removeStorageSync('user_id');
			uni.removeStorageSync('match_id');
			
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
			// 获取比赛
			wx.showToast({
				title: '加载中',
				icon: 'loading',
				duration: 100000,
			});
			fetch_data("POST", "match_list_current", null, "competition", res => {
				this.message = res.data.message;
				this.matches = res.data.matches;
				wx.hideToast();
			});
		},
		methods: {
			onInput(e) {
				this.search_match = e.target.value
			},
			
			back() {
				uni.navigateBack({
					delta: 1
				});
			},

			search() {
				this.current = 3;
				wx.showToast({
					title: '加载中',
					icon: 'loading',
					duration: 100000,
				});
				let data = {"search_match": this.search_match};
				fetch_data("POST", "findMatchByName", data, "competition", res => {
					this.matches = res.data.matches;
					wx.hideToast();
				});
			},
			
			change(index) {
				this.current = index; 			// 按钮切换状态
				if (index == 0) {
					wx.showToast({
						title: '加载中',
						icon: 'loading',
						duration: 100000,
					});
					fetch_data("POST", "match_list_current", null, "competition", res => {
						this.matches = res.data.matches;
						wx.hideToast();
					});
				} else if (index == 1) {
					wx.showToast({
						title: '加载中',
						icon: 'loading',
						duration: 100000,
					});
					fetch_data("POST", "match_list_signed", {"my_id": this.user.id}, "competition", res => {
						this.matches = res.data.matches;
						wx.hideToast();
					});
				} else if (index == 2) {
					wx.showToast({
						title: '加载中',
						icon: 'loading',
						duration: 100000,
					});
					fetch_data("POST", "match_list_history", null, "competition", res => {
						this.matches = res.data.matches;
						wx.hideToast();
					});
				} else if (index == 3) {
					wx.showToast({
						title: '加载中',
						icon: 'loading',
						duration: 100000,
					});
					fetch_data("POST", "match_list_all", null, "competition", res => {
						this.matches = res.data.matches;
						wx.hideToast();
					});
				};
			},

			sign_up_page(match_id) {
				uni.setStorageSync('match_id', match_id)
				uni.navigateTo({
					url: '/page_subjec/match/sign_up',
				});
			},

			quit(match_id) {
				wx.showModal({
					title: '取消报名',
					content: '确认放弃参加该赛事？',
					success: res => {
						if (res.confirm) {
							let data = {
								"my_id": this.user.id,
								"match_id": match_id,
							}
							fetch_data("POST", "quit_match", data, "competition", res => {
								wx.showToast({
									title: res.data.message,
									icon: "none",
									duration: 1000,
								});
								if (res.data.status == 200) {
									setTimeout(() => {
										uni.reLaunch({
											url: '/page_subjec/match/index',
										})
									}, 1000);
								}
							})
						}
					}
				})
			},
			
			hide_match(match_id) {
				wx.showModal({
					title: '隐藏赛事',
					content: '确定隐藏该赛事？',
					success: res => {
						if (res.confirm) {
							let data = {
								"my_id": this.user.id,
								"match_id": match_id,
							}
							fetch_data("POST", "hide_match", data, "competition", res => {
								wx.showToast({
									title: res.data.message,
									icon: "none",
									duration: 1000,
								});
								if (res.data.status == 200){
									this.current = 0;
									fetch_data("POST", "match_list_current", null, "competition", res => {
										this.matches = res.data.matches;
									});
								}
							})
						}
					}
				})
			},
			
			match_detail_page(match_id) {
				uni.setStorageSync('match_id', match_id)
				uni.navigateTo({
					url: '/page_subjec/match/detail',
				});
			},
		}
	}
</script>

// 直接挂载到template中使用
<script setup>
	import * as utils from '../../static/js/utils.js'
</script>

<style lang="scss" scoped>
	.scroll {
		height: 90vh;
	}

	.search_bar {
		width: 540rpx;
		margin: 15rpx 20rpx;
	}
	
	.box {
		box-sizing: border-box;
		padding: 40rpx 20rpx;
		background-color: white;
		margin-top: 8rpx;
		background: #ffffff;
		border-radius: 20rpx 20rpx 20rpx 20rpx;

		.btn {
			margin-left: 20rpx;
		}

		.mon {
			margin-top: 20rpx;
			text-align: right;
			font-weight: 600;
			font-size: 28rpx;
			color: #333333;
			line-height: 40rpx;

			.q {
				font-size: 38rpx;
			}
		}

		.time {
			box-sizing: box-sizing;
			padding: 20rpx;
			background: #fff3eb;
			border-radius: 8rpx 8rpx 8rpx 8rpx;

			font-weight: 500;
			font-size: 24rpx;
			color: #f25c07;
			line-height: 24rpx;
		}

		.l {
			font-weight: 400;
			font-size: 28rpx;
			color: #666666;
			line-height: 24rpx;
			margin-left: 10rpx;
		}

		.r {
			font-weight: 600;
			font-size: 28rpx;
			color: #f25c07;
			line-height: 28rpx;
			margin-right: 20rpx;
		}

		.bc {
			border-radius: 12rpx 12rpx 12rpx 12rpx;

			.text1 {
				margin-top: 4rpx;
				font-family: PingFang SC, PingFang SC;
				font-weight: bold;
				font-size: 28rpx;
				color: #282456;
				text-align: left;
				font-style: normal;
				text-transform: none;
			}

			.text2 {
				margin-top: 34rpx;
				font-family: PingFang SC, PingFang SC;
				font-weight: 600;
				font-size: 26rpx;
				color: #f25c07;
				line-height: 28rpx;
				text-align: left;
				font-style: normal;
				text-transform: none;
			}

			.text3 {
				margin-top: 34rpx;
				font-family: PingFang SC, PingFang SC;
				font-weight: 400;
				font-size: 24rpx;
				color: #666666;
				line-height: 5rpx;
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

			margin-top: 30rpx;
			background-color: white;
			box-sizing: box-sizing;
			padding: 18rpx 0rpx;
		}
	}

	.app {
		box-sizing: border-box;
		padding: 20rpx;
		background: linear-gradient(135deg, #FEF2DA, #FFD5A4);
	}

	.tabA {
		background-color: #f25c07 !important;
		color: white !important;
	}

	.tabs {
		width: 16%;
		text-align: center;
		font-weight: 400;
		font-size: 24rpx !important;
		color: #999999;
		background-color: red;
		box-sizing: border-box;
		padding: 5rpx 20rpx;
		background: #ffffff;
		border-radius: 40rpx 40rpx 40rpx 40rpx;
	}
</style>