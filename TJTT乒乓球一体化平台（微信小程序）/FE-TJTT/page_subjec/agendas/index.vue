<template>
	<div v-if="!hide_this" class="app">
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
			<u-tabs style="position: relative; bottom: 4rpx;" :list="agenda_list" bg-color="#ffffff"
				active-color="#F25C07" f font-size="20rpx" is-scroll="true" :current="current"
				@change="change"></u-tabs>
			<div v-for="(item, index) in items" :key="index" class="boxList flex">
				<div class="left">
					<img class="lIcon"
						src="https://tjtt-assets.oss-cn-shanghai.aliyuncs.com/pictures/logos/logo1.1.png"
						alt="" />
				</div>
				<div v-if="current==0" class="right">
					<div class="text1" style="display: flex;"><p style="color: #d9d9d9;">{{index+1}}&nbsp;&nbsp;</p>{{item.question}}</div>
					<div class="text3 flex">
						<div class="l" style="font-size: 28rpx; color: #f25c07;">
							<div class="quan"></div>
							提问者：{{item.person_name}}
						</div>
					</div>
					<div class="text3 flex">
						<div class="r">
							<button style="position: relative; bottom: 12px; margin-left: 250rpx;"
								class="cu-btn btn round line-cyan" @click="answer(item)">
								回答
							</button>
						</div>
						<div class="r">
							<button style="position: relative; bottom: 12px;"
								class="cu-btn btn round line-red" @click="delete_question(item.id)">
								删除
							</button>
						</div>
					</div>
				</div>
				
				<div v-else-if="current==1" class="right">
					<div class="text1" style="display: flex;"><p style="color: #d9d9d9;">{{index+1}}&nbsp;&nbsp;</p>{{item.title}}</div>
					<div class="text2">{{item.content}}</div>
					<div class="text3 flex">
						<div class="l" style="font-size: 28rpx; color: #f25c07;">
							<div class="quan"></div>
							发布者：{{item.announcer_name}}
						</div>
					</div>
					<div class="text3 flex">
						<div class="r">
							<button style="position: relative; bottom: 12px; margin-left: 190rpx;"
								class="cu-btn btn round line-cyan" @click="unhide_notice(item.id)">
								取消隐藏
							</button>
						</div>
						<div class="r">
							<button style="position: relative; bottom: 12px;"
								class="cu-btn btn round line-red" @click="delete_notice(item.id)">
								删除
							</button>
						</div>
					</div>
				</div>
				
				<div v-else-if="current==2" class="right">
					<div class="text1" style="display: flex; line-height: 40rpx;"><p style="color: #d9d9d9;">{{index+1}}&nbsp;&nbsp;</p>{{item.title}}</div>
					<div class="text2" style="line-height: 20rpx;">{{item.place}}</div>
					<div class="text3 flex">
						<div class="l" style="font-size: 28rpx; color: #f25c07;">
							<div class="quan"></div>
							比赛时间：{{utils.format_time(item.match_time)}}
						</div>
					</div>
					<div class="text3 flex">
						<div class="r">
							<button style="position: relative; margin-left: 190rpx;"
								class="cu-btn btn round line-cyan" @click="unhide_match(item.id)">
								取消隐藏
							</button>
						</div>
						<div class="r">
							<button style="position: relative;"
								class="cu-btn btn round line-red" @click="delete_match(item.id)">
								删除
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
				user_length: "",
				student_length: "",
				teacher_length: "",
				admin_length: "",
				items: [],
				agenda_list: [{
						name: "待回答问题",
					},
					{
						name: "隐藏通知",
					},
					{
						name: "隐藏赛事",
					},
				],
				current: 0,
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
			// 获取待回答问题
			fetch_data("POST", "get_unanswered_Qs", null, "application", res => {
				this.items = res.data.unanswered_Qs;
				wx.hideToast();
			});
		},
		methods: {
			change(index) {
				this.current = index; // 按钮切换状态
				if (index == 0) {
					wx.showToast({
						title: '加载中',
						icon: 'loading',
						duration: 100000,
					});
					fetch_data("POST", "get_unanswered_Qs", null, "application", res => {
						this.items = res.data.unanswered_Qs;
						wx.hideToast();
					});
				} else if (index == 1) {
					wx.showToast({
						title: '加载中',
						icon: 'loading',
						duration: 100000,
					});
					fetch_data("POST", "get_hidden_notices", null, "application", res => {
						this.items = res.data.hidden_notices;
						wx.hideToast();
					});
				} else if (index == 2) {
					wx.showToast({
						title: '加载中',
						icon: 'loading',
						duration: 100000,
					});
					fetch_data("POST", "get_hidden_matches", null, "application", res => {
						this.items = res.data.hidden_matches;
						wx.hideToast();
					});
				};
			},
			
			answer(question) {
				wx.showModal({
					title: question.question,
					placeholderText: '请输入回答',
					editable: true,
					success: res => {
						if (res.confirm) {
							let data = {
								'my_id': this.user.id,
								'question_id': question.id,
								'answer': res.content,
							}
							fetch_data("POST", "answer_question", data, "application", res => {
								wx.showToast({
									title: res.data.message,
									icon: "none",
									duration: 1500,
								});
								fetch_data("POST", "get_unanswered_Qs", null, "application", res => {
									this.items = res.data.unanswered_Qs;
								});
							})
						}
					}
				});
			},
			delete_question(question_id) {
				wx.showModal({
					title: '删除问题',
					content: '确定删除该问题？',
					success: res => {
						if (res.confirm) {
							let data = {
								"my_id": this.user.id,
								"QA_id": question_id,
							}
							fetch_data("POST", "delete_QA", data, "user", res => {
								wx.showToast({
									title: res.data.message,
									icon: "none",
									duration: 1000,
								});
								if (res.data.status == 200){
									fetch_data("POST", "get_unanswered_Qs", null, "application", res => {
										this.items = res.data.unanswered_Qs;
									});
								}
							})
						}
					}
				})
			},
			
			unhide_notice(notice_id) {
				wx.showModal({
					title: '取消隐藏',
					content: '确定取消隐藏该通知公告？',
					success: res => {
						if (res.confirm) {
							let data = {
								"my_id": this.user.id,
								"notice_id": notice_id,
							};
							fetch_data("POST", "unhide_notice", data, "application", res => {
								wx.showToast({
									title: res.data.message,
									icon: "none",
									duration: 1000,
								});
								if (res.data.status == 200) {
									fetch_data("POST", "get_hidden_notices", null, "application", res => {
										this.items = res.data.hidden_notices;
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
					content: '确定删除该通知公告？',
					success: res => {
						if (res.confirm) {
							let data = {
								"my_id": this.user.id,
								"notice_id": notice_id,
							}
							fetch_data("POST", "delete_notice", data, "application", res => {
								wx.showToast({
									title: res.data.message,
									icon: "none",
									duration: 1000,
								});
								if (res.data.status == 200){
									fetch_data("POST", "get_hidden_notices", null, "application", res => {
										this.items = res.data.hidden_notices;
									});
								}
							})
						}
					}
				})
			},
			
			unhide_match(match_id) {
				wx.showModal({
					title: '取消隐藏',
					content: '确定取消隐藏该赛事？',
					success: res => {
						if (res.confirm) {
							let data = {
								"my_id": this.user.id,
								"match_id": match_id,
							};
							fetch_data("POST", "unhide_match", data, "competition", res => {
								wx.showToast({
									title: res.data.message,
									icon: "none",
									duration: 1000,
								});
								if (res.data.status == 200) {
									fetch_data("POST", "get_hidden_matches", null, "application", res => {
										this.items = res.data.hidden_matches;
									});
								}
							})
						}
					}
				})
			},
			delete_match(match_id) {
				wx.showModal({
					title: '删除赛事',
					content: '删除赛事后，选手信息、赛事成绩等将一并删除。确认删除该赛事？',
					success: res => {
						if (res.confirm) {
							let data = {
								"my_id": this.user.id,
								"match_id": match_id,
							};
							fetch_data("POST", "delete_match", data, "competition", res => {
								wx.showToast({
									title: res.data.message,
									icon: "none",
									duration: 1000,
								});
								if (res.data.status == 200) {
									fetch_data("POST", "get_hidden_matches", null, "application", res => {
										this.items = res.data.hidden_matches;
									});
								}
							})
						}
					}
				})
			},
		},
	}
</script>

// 直接挂载到template中使用
<script setup>
	import * as utils from '../../static/js/utils.js'
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
					line-height: 40rpx;
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