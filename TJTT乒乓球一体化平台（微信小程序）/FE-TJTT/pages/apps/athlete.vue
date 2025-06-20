<template>
	<div v-if="!hide_this" class="app">
		<u-tabs style="position: relative; bottom: 4rpx;" :list="athlete_list" bg-color=null
			active-color="#F25C07" font-size="20rpx" is-scroll="true" :current="current" @change="change">
		</u-tabs>
		<div style="display: flex;">
			<u-search class="search_bar" v-model="search_athlete" bg-color="#ffffff" :show-action="false" placeholder="输入运动员姓名"></u-search>
			<button class="cu-btn btn round line-cyan" style="margin-top: 15rpx;" @click="search">查找</button>
		</div>
		<scroll-view class="scroll" scroll-y="auto">
			<div v-if="athletes.length != 0" class="box" v-for='(athlete, index) in athletes' :key='index'>
				<div class="flex top">
					<div class="l">运动员 {{index + 1}}</div>
					<div class="r" v-if="athlete.nationality">{{athlete.nationality}}</div>
				</div>
				<div class="bc flex">
					<div class="left">
						<img class="bcImg" v-if="athlete.image_url" :src="athlete.image_url" alt="" @click="image_operation(athlete.image_url)" />
						<div class="time" v-if="athlete.glory">
							<div style="text-align: center; font-weight: bold;">所获荣誉</div>{{athlete.glory}}
						</div>
					</div>
					<div class="right">
						<div v-if="athlete.name && athlete.gender=='男'" class="text1"
							style="color: #0081ff;">{{athlete.name}}</div>
						<div v-else-if="athlete.name && athlete.gender=='女'" class="text1"
							style="color: #f37b1d;">{{athlete.name}}</div>
						<div v-if="athlete.hand && athlete.grip && athlete.particle=='否'" class="text2"
							style="color: #f25c07;">
							{{athlete.hand}} | {{athlete.grip}} | 无颗粒
						</div>
						<div v-else-if="athlete.hand && athlete.grip && athlete.particle=='是'" class="text2"
							style="color: #f25c07;">
							{{athlete.hand}} | {{athlete.grip}} | 有颗粒
						</div>
						<div class="text2" style="margin-top: 40rpx;" v-if="athlete.blade">底板：{{athlete.blade}}</div>
						<div class="text2" v-if="athlete.forehand">正手胶皮：{{athlete.forehand}}</div>
						<div class="text2" v-if="athlete.backhand">反手胶皮：{{athlete.backhand}}</div>
						<div class="time2" style="margin-top: 35rpx;" v-if="athlete.description">
							<div style="text-align: center; font-weight: bold;">个人简介</div>{{athlete.description}}
						</div>
						<div class="time3" v-if="athlete.personal_style">
							<div style="text-align: center; font-weight: bold;">技术特点</div>{{athlete.personal_style}}
						</div>
					</div>
				</div>
				<div style="text-align: right; margin-top: 20rpx;">
					<button class="cu-btn btn round line-cyan" @click="anecdote(athlete)">轶闻趣事</button>
					<button class="cu-btn btn round line-cyan" @click="comment(athlete)">人物评价</button>
				</div>
			</div>

			<div v-else style="text-align: center; margin-top: 40rpx;">无运动员信息</div>
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
				search_athlete: "",
				athletes: [],
				athlete_list: [{
						name: "中国运动员",
					},
					{
						name: "外国运动员",
					},
					{
						name: "男子运动员",
					},
					{
						name: "女子运动员",
					},
					{
						name: "全部",
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
			fetch_data("POST", "get_Chinese_athletes", null, "application", res => {
				this.athletes = res.data.athletes;
				wx.hideToast();
			});
		},
		methods: {
			onInput(e) {
				this.search_athlete = e.target.value
			},
			
			back() {
				uni.navigateBack({
					delta: 1
				});
			},

			search() {
				this.current = 4;
				wx.showToast({
					title: '加载中',
					icon: 'loading',
					duration: 100000,
				});
				let data = {"search_athlete": this.search_athlete};
				fetch_data("POST", "find_athlete_by_name", data, "application", res => {
					this.athletes = res.data.athletes;
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
					fetch_data("POST", "get_Chinese_athletes", null, "application", res => {
						this.athletes = res.data.athletes;
						wx.hideToast();
					});
				} else if (index == 1) {
					wx.showToast({
						title: '加载中',
						icon: 'loading',
						duration: 100000,
					});
					fetch_data("POST", "get_foreign_athletes", null, "application", res => {
						this.athletes = res.data.athletes;
						wx.hideToast();
					});
				} else if (index == 2) {
					wx.showToast({
						title: '加载中',
						icon: 'loading',
						duration: 100000,
					});
					fetch_data("POST", "get_male_athletes", null, "application", res => {
						this.athletes = res.data.athletes;
						wx.hideToast();
					});
				} else if (index == 3) {
					wx.showToast({
						title: '加载中',
						icon: 'loading',
						duration: 100000,
					});
					fetch_data("POST", "get_female_athletes", null, "application", res => {
						this.athletes = res.data.athletes;
						wx.hideToast();
					});
				} else if (index == 4) {
					wx.showToast({
						title: '加载中',
						icon: 'loading',
						duration: 100000,
					});
					fetch_data("POST", "get_athletes", null, "application", res => {
						this.athletes = res.data.athletes;
						wx.hideToast();
					});
				};
			},
			
			image_operation(image_url) {
				wx.previewImage({
					urls: [image_url],
					current: image_url,
				});
			},
			
			anecdote(athlete) {
				if (!athlete.anecdote) {
					wx.showToast({
						title: "该运动员暂未完善轶闻趣事",
						icon: "none",
						duration: 1000,
					});
					return;
				}
				wx.showModal({
					title: athlete.name + '的轶闻趣事',
					content: athlete.anecdote,
					showCancel: false,
					confirmText: "退出",
				})
			},
			
			comment(athlete) {
				if (!athlete.comment) {
					wx.showToast({
						title: "该运动员暂未完善人物评价",
						icon: "none",
						duration: 1000,
					});
					return;
				}
				wx.showModal({
					title: athlete.name + '的人物评价',
					content: athlete.comment,
					showCancel: false,
					confirmText: "退出",
				})
			}
		}
	}
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
			margin-top: 20rpx;
			box-sizing: box-sizing;
			padding: 20rpx;
			background: #fff3eb;
			border-radius: 8rpx 8rpx 8rpx 8rpx;
			font-weight: 500;
			font-size: 24rpx;
			color: #000000;
			line-height: 30rpx;
			text-align: justify;
		}
		
		.time2 {
			margin-top: 20rpx;
			box-sizing: box-sizing;
			padding: 20rpx;
			background: #ebebeb;
			border-radius: 8rpx 8rpx 8rpx 8rpx;
			font-weight: 500;
			font-size: 24rpx;
			color: #000000;
			line-height: 30rpx;
			text-align: justify;
		}
		
		.time3 {
			margin-top: 20rpx;
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
				color: black;
				line-height: 10rpx;
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
				line-height: 15rpx;
				text-align: left;
				font-style: normal;
				text-transform: none;
			}

			.right {
				width: 54%;
			}

			.left {
				width: 42%;

				.bcImg {
				    border-radius: 20rpx;
				    width: 100%;
				    height: 116.67px;
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