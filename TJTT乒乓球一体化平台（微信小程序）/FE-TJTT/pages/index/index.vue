<template>
	<div id="app">
		<div class="head">
			<div class="headTitle">TJTT乒乓球一体化平台</div>
			<p v-if="hide_this" class="headTitle">b</p>
			<span v-if="username" class="welcome">你好，{{username}}</span>
			<span v-else class="welcome">你好，请登录</span>
			<div class="motto-container">
				<span class="motto">
				    “{{random_motto.content}}”
				    <span class="author">——{{random_motto.author}}</span>
				</span>
			</div>
		</div>
		<Nav />
		
		<section class="section">
			<div class="div" @click='img_show'>
				<img class="bgImg" src="https://tjtt-assets.oss-cn-shanghai.aliyuncs.com/pictures/decorations/homepage-img.png" alt="" />
			</div>
			<div class="flex cate">
				<div @click='all_matches' class="left">
					<image style="height: 340rpx" class="imgIcon" src="https://tjtt-assets.oss-cn-shanghai.aliyuncs.com/pictures/decorations/match.png" alt="" />
				</div>
				<div class="right">
					<div @click='enter_ranking'>
						<image style="height: 165rpx" class="imgIcon" src="https://tjtt-assets.oss-cn-shanghai.aliyuncs.com/pictures/decorations/rank.png"
							alt="" />
					</div>
					<div @click='enter_community'>
						<image style="height: 165rpx" class="imgIcon" src="https://tjtt-assets.oss-cn-shanghai.aliyuncs.com/pictures/decorations/friendship.png"
							alt="" />
					</div>
				</div>
			</div>
		</section>
		<div class="boxTwo">
			<div class="selectList">
				<div class="tab" style="display: flex; background-color: white;">
					<u-tabs :list="select_list" active-color="#F25C07" :is-scroll="true" :current="current"
						@change="change"></u-tabs>
					<button
						v-if="(usertype == 'K9' || usertype == 'K10' || usertype == 'K11') && current == 0&& !hide_this"
						class="cu-btn btn round line-cyan" style="margin: 10rpx 20rpx;"
						@click="issue_notice">发布通知公告</button>
					<button v-if="current == 1 && !hide_this" class="cu-btn btn round line-cyan" style="margin: 10rpx 20rpx;"
						@click="ask">提问</button>
				</div>
				<section v-if="!hide_this" class="shopList flex">
					<div v-if="current == 0" v-for="(notice, index) in display_content" :key="index"
						class="box">
						<div class="boxImg">
							<div class="text" style="font-weight: bold;">{{notice.title}}</div>
							<div class="divider"></div>
							<div class="text" style="font-weight: normal;">{{notice.content}}</div>
							<div class="text_time" style="font-weight: normal;">{{utils.format_time(notice.time)}}</div>
							<div class="text_time" style="font-weight: normal;">
								发布者：{{notice.announcer_name}}</div>
							<div v-if="usertype == 'K9' || usertype == 'K10' || usertype == 'K11'"
								class="divider"></div>
							<div v-if="usertype == 'K9' || usertype == 'K10' || usertype == 'K11'"
								style="display: flex;">
								<button class="btn round line-cyan" style="background-color: #FEF2DA;"
									@click="hide_notice(notice.id)">藏</button>
								<button class="btn round line-red" style="background-color: #FEF2DA;"
									@click="delete_notice(notice.id)">删</button>
							</div>
						</div>
					</div>
					<div v-else-if="current == 1" v-for="(QA, index) in display_content" :key="index"
						class="box">
						<div class="boxImg">
							<div class="text" style="font-weight: bold;">{{QA.question}}</div>
							<div class="divider"></div>
							<div class="text" style="font-weight: normal;">{{QA.answer}}</div>
							<div v-if="usertype == 'K9' || usertype == 'K10' || usertype == 'K11'"
								class="divider"></div>
							<div v-if="usertype == 'K9' || usertype == 'K10' || usertype == 'K11'"
								style="display: flex;">
								<button class="btn round line-cyan" style="background-color: #FEF2DA;"
									@click="modify_QA(QA)">改</button>
								<button class="btn round line-red" style="background-color: #FEF2DA;"
									@click="delete_QA(QA.id)">删</button>
							</div>
						</div>
					</div>
				</section>
			</div>
		</div>
		<tabbar :current-page="0"></tabbar>
	</div>
</template>

<script>
	import { fetch_data } from '../../static/js/ajax_request.js'
	import { login_check } from '../../static/js/login_check.js'
	import * as utils from '../../static/js/utils.js'
	import { magic } from '../../static/js/magic_power.js'
	export default {
		data() {
			return {
				user_id: "",
				username: "",
				usertype: "",
				random_motto: "",
				display_content: [],
				select_list: [{
						name: "通知公告",
					},
					{
						name: "Q & A",
					},
				],
				current: 0,
				hide_this: magic(),
			}
		},
		onLoad() {
			uni.removeStorageSync('user_id');
			uni.removeStorageSync('match_id');
			
			const user_token = uni.getStorageSync("user_token");
			const decoded_user_token = utils.decode(user_token);
			const regex = /^(\d+)=/;
			const match = decoded_user_token.match(regex);
			const user_id = match ? match[1] : null;
			this.user_id = +user_id;
			
			if (this.user_id) {
				fetch_data("POST", "get_index_info", {'user_id': this.user_id}, "user", res => {
					this.username = res.data.username;
					this.usertype = res.data.usertype;
				});
			}

			fetch_data("POST", "get_random_motto", null, "application", res => {
				this.random_motto = res.data.random_motto;
			});
			fetch_data("POST", "get_notice", null, "application", res => {
				this.display_content = res.data.notices;
			});
		},
		methods: {
			all_matches() {
				uni.navigateTo({
					url: '/page_subjec/match/index',
				})
			},

			img_show() {
				let img_url = "https://tjtt-assets.oss-cn-shanghai.aliyuncs.com/pictures/decorations/studio-intro.png";
				wx.previewImage({
					urls: [img_url],
					current: img_url,
				});
			},

			enter_ranking() {
				uni.switchTab({
					url: '/pages/score-ranking/index',
				})
			},
			
			enter_community() {
				uni.switchTab({
					url: '/pages/community/index',
				})
			},

			change(index) {
				this.current = index; // 按钮切换状态
				if (index == 0) {
					fetch_data("POST", "get_notice", null, "application", res => {
						this.display_content = res.data.notices;
					});
				} else if (index == 1) {
					fetch_data("POST", "get_QAs", null, "application", res => {
						this.display_content = res.data.QAs;
					});
				};
			},
			issue_notice() {
				uni.navigateTo({
					url: '/pages/index/issue-notice',
				})
			},
			hide_notice(notice_id) {
				wx.showModal({
					title: '隐藏通知公告',
					content: '确定隐藏该通知公告？',
					success: res => {
						if (res.confirm) {
							let data = {
								"my_id": this.user_id,
								"notice_id": notice_id,
							}
							fetch_data("POST", "hide_notice", data, "application", res => {
								wx.showToast({
									title: res.data.message,
									icon: "none",
									duration: 1000,
								});
								if (res.data.status == 200) {
									fetch_data("POST", "get_notice", null, "application", res => {
										this.display_content = res.data.notices;
									});
								}
							})
						}
					}
				})
			},
			delete_notice(notice_id) {
				wx.showModal({
					title: '删除通知公告',
					content: '确定删除该通知公告',
					success: res => {
						if (res.confirm) {
							let data = {
								"my_id": this.user_id,
								"notice_id": notice_id,
							}
							fetch_data("POST", "delete_notice", data, "application", res => {
								wx.showToast({
									title: res.data.message,
									icon: "none",
									duration: 1000,
								});
								if (res.data.status == 200) {
									fetch_data("POST", "get_notice", null, "application", res => {
										this.display_content = res.data.notices;
									});
								}
							})
						}
					}
				})
			},

			ask() {
				if (!this.user_id) {
					wx.showToast({
						title: "请登录",
						icon: "none",
						duration: 1500,
					});
					setTimeout(() => {
						uni.navigateTo({
							url: '/pages/login/login',
						})
					}, 1000);
				} else {
					wx.showModal({
						title: '提问',
						placeholderText: '任何乒乓球相关问题',
						editable: true,
						confirmText: "提问",
						success: res => {
							if (res.confirm) {
								let data = {
									'my_id': this.user_id,
									'question': res.content,
								}
								fetch_data("POST", "ask_question", data, "application", res => {
									wx.showToast({
										title: res.data.message,
										icon: "none",
										duration: 1500,
									});
								})
							}
						}
					});
				}

			},
			modify_QA(QA) {
				wx.showModal({
					title: QA.question,
					content: QA.answer,
					editable: true,
					confirmText: "修改",
					success: res => {
						if (res.confirm) {
							let data = {
								"my_id": this.user_id,
								"QA_id": QA.id,
								"answer": res.content,
							}
							fetch_data("POST", "modify_QA", data, "application", res => {
								wx.showToast({
									title: res.data.message,
									icon: "none",
									duration: 1000,
								});
								if (res.data.status == 200) {
									fetch_data("POST", "get_QAs", null, "application", res => {
										this.display_content = res.data.QAs;
									});
								}
							})
						}
					}
				})
			},
			delete_QA(QA_id) {
				wx.showModal({
					title: '删除问题回答',
					content: '确定删除该问题与回答',
					success: res => {
						if (res.confirm) {
							let data = {
								"my_id": this.user_id,
								"QA_id": QA_id,
							}
							fetch_data("POST", "delete_QA", data, "application", res => {
								wx.showToast({
									title: res.data.message,
									icon: "none",
									duration: 1000,
								});
								if (res.data.status == 200) {
									fetch_data("POST", "get_QAs", null, "application", res => {
										this.display_content = res.data.QAs;
									});
								}
							})
						}
					}
				})
			},
		},

		onPullDownRefresh() {
			if (this.user_id) {
				let data = {
					"my_id": this.user_id,
				};
				fetch_data("POST", "refresh", data, "user", res => {
					// 异步获取用户排名
					var user_id = this.user_id
					function asyncTask(callback) {
						utils.get_my_rank(user_id);
						callback();
					}
					asyncTask(() => {
						console.log('async task finished');
					})
					uni.setStorageSync('user', res.data.user);
				});
			}
			uni.reLaunch({
				url: '/pages/index/index',
			});
			setTimeout(() => {
				uni.stopPullDownRefresh();
			}, 1000);
		}
	}
</script>

<script setup>
	import Nav from "./components/index.vue";
</script>

<style lang="scss" scoped>
	.head {
		position: relative;
		background: linear-gradient(180deg, #f9d5a5, #fef2da);

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
		}

		.welcome {
			font-weight: 600;
			font-size: 30rpx;
			color: #212121;
			line-height: 50rpx;
			position: absolute;
			text-align: start;
			width: 100%;
			left: 40rpx;
			top: 160rpx;
			z-index: 999;
		}
	}
	
	.motto-container {
		display: inline-block;
		padding: 20rpx;
		border-radius: 20rpx;
		background: linear-gradient(135deg, #f3ec78, #af4261);
		box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
		margin-top: 40rpx;
		width: auto;
		max-width: 90%;
		position: relative;
		left: 40rpx;
		top: 180rpx;
		z-index: 999;
		text-align: start;
	
		.motto {
			font-weight: bold;
			font-size: 30rpx;
			color: #212121;
			line-height: 50rpx;
			text-align: justify;
		}
	
		.author {
			display: inline-block;
			width: auto;
			float: right;
			text-align: end;
		}
	}
	
	.divider {
		background-color: #f2f2f2;
		margin: 15rpx 15rpx;
		height: 3rpx;
	}

	.box {
		width: 48%;
		background: linear-gradient(135deg, #FEF2DA, #FFD5A4);
		border-radius: 12rpx;
		margin-top: 24rpx;
		overflow: hidden;

		.boxImg {
			width: 100%;
			height: 300rpx;
			overflow: auto;
		}

		.time {
			margin-top: 20rpx;
			font-family: PingFang SC, PingFang SC;
			font-weight: 500;
			font-size: 24rpx;
			color: #666666;
			line-height: 24rpx;
			text-align: left;
			font-style: normal;
			text-transform: none;
		}

		.text {
			font-family: PingFang SC, PingFang SC;
			font-size: 28rpx;
			color: #282456;
			line-height: 44rpx;
			text-align: left;
			font-style: normal;
			text-transform: none;
			margin: 20rpx 20rpx;
		}

		.text_time {
			font-family: PingFang SC, PingFang SC;
			font-size: 19rpx;
			color: #282456;
			line-height: 10rpx;
			text-align: end;
			font-style: normal;
			text-transform: none;
			margin: 20rpx 20rpx;
		}

		.shopCont {
			box-sizing: border-box;
			padding: 14rpx;
			padding-bottom: 40rpx;
			height: 200rpx;
		}
	}

	.boxTwo {
		position: relative;
		bottom: 100rpx;
	}

	.selectList {
		border-radius: 20rpx 20rpx 20rpx 20rpx;
		background-color: white;
		box-sizing: border-box;
		padding: 20rpx 30rpx;
	}

	.divSelect {
		display: inline-block;
		margin-right: 30rpx;
	}

	.imgsA {
		width: 20rpx;
		height: 16rpx;
		margin-left: 13rpx;
	}

	#app {
		background-color: #f8f8f8;
		width: 100%;
		min-height: 100vh;
		height: 100%;
	}

	.section {
		box-sizing: border-box;
		padding: 0rpx 20rpx;
		position: relative;
		top: -110rpx;
	}

	.cate {
		box-sizing: border-box;
		padding: 15rpx 10rpx;
		text-align: center;

		.imgIcon {
			width: 100%;
		}

		.left {
			width: 48%;
		}

		.right {
			width: 49%;
			text-align: left;
		}
	}

	.div {
		position: relative;
		box-sizing: border-box;
		padding: 10rpx;
		height: 320rpx;
		margin-top: -95rpx;
		.bgImg {
			width: 100%;
			height: 100%;
		}
	}

	.tab {
		background-color: white;
	}
</style>