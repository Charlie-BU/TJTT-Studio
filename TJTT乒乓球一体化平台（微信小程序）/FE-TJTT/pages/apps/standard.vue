<template>
	<div class="app">
		<u-tabs style="position: relative; bottom: 4rpx;" :list="standard_list" bg-color=null
			active-color="#F25C07" font-size="20rpx" is-scroll="true" :current="current" @change="change">
		</u-tabs>
		<scroll-view v-if="current==0" class="scroll" scroll-y="auto">
			<div class="box">
				<div class="wrapper">
					<uni-table stripe emptyText="无数据">
						<uni-tr>
							<uni-th width="20rpx">
								<view class="table_head">选手间积分差</view>
							</uni-th>
							<uni-th width="20rpx">
								<view class="table_head">积分高者得胜所加积分<br/>积分低者战败所减积分</view>
							</uni-th>
							<uni-th width="20rpx">
								<view class="table_head">积分低者得胜所加积分<br/>积分高者战败所减积分</view>
							</uni-th>
						</uni-tr>
						<uni-tr v-for="(rule, index) in rules" :key="index">
							<uni-td>
								<view class="table_content" style="color: #f25c07;">{{ rule.difference }}</view>
							</uni-td>
							<uni-td>
								<view class="table_content">{{ rule.high_win_low }}</view>
							</uni-td>
							<uni-td>
								<view class="table_content">{{ rule.low_win_high }}</view>
							</uni-td>
						</uni-tr>
					</uni-table>
				</div>
				<p class="note">参考中国乒乓球水平积分制度“ChinaTT”</p>
			</div>
		</scroll-view>
		
		<scroll-view v-if="current==1" class="scroll" scroll-y="auto">
			<div class="box">
				<div class="wrapper">
					<uni-table stripe emptyText="无数据" style="z-index: -1;">
						<uni-tr>
							<uni-th>
								<view class="table_head">积分</view>
							</uni-th>
							<uni-th>
								<view class="table_head">标准</view>
							</uni-th>
						</uni-tr>
						<uni-tr v-for="(standard, index) in standards" :key="index">
							<uni-td>
								<view class="table_content font-weight-bold" style="color: #f25c07;">{{ standard.score }}</view>
							</uni-td>
							<uni-td>
								<view class="table_content font-weight-bold" style="text-align: justify;">{{ standard.description }}</view>
							</uni-td>
						</uni-tr>
					</uni-table>
				</div>
				<p class="note">参考中国乒乓球水平积分制度“ChinaTT”</p>
			</div>
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
				standard_list: [{
						name: "TJTT积分标准",
					},
					{
						name: "TJTT积分预估值参考",
					},
				],
				current: 0,
				rules: [{
						difference: '0-12',
						high_win_low: 8,
						low_win_high: 8
					},
					{
						difference: '13-37',
						high_win_low: 7,
						low_win_high: 10
					},
					{
						difference: '38-62',
						high_win_low: 6,
						low_win_high: 13
					},
					{
						difference: '63-87',
						high_win_low: 5,
						low_win_high: 16
					},
					{
						difference: '88-112',
						high_win_low: 4,
						low_win_high: 20
					},
					{
						difference: '113-137',
						high_win_low: 3,
						low_win_high: 25
					},
					{
						difference: '138-162',
						high_win_low: 2,
						low_win_high: 30
					},
					{
						difference: '163-187',
						high_win_low: 2,
						low_win_high: 35
					},
					{
						difference: '188-212',
						high_win_low: 1,
						low_win_high: 40
					},
					{
						difference: '213-237',
						high_win_low: 1,
						low_win_high: 45
					},
					{
						difference: '238以上',
						high_win_low: 0,
						low_win_high: 50
					},
				],
				standards: [
					{ score: '400', description: '刚开始打乒乓球。' },
					{ score: '600', description: '很有限的打球经验，主要练习能够打到球。' },
					{ score: '800', description: '需要打球经验，有明显的击球弱点，能打一些和平球，发一些和平球。' },
					{ score: '1000', description: '开始学习判断球的旋转，对球的控制能力弱，能打一些速度、力量一般的球。' },
					{ score: '1200', description: '能协调地回击中速球，能简单的使用搓、推、挡、攻等各种击球方法，但缺乏较好方向性、力度和旋转的控制，能发一些有力度和旋转球。' },
					{ score: '1400', description: '对来球的旋转性和方向性有一定的判断，球的控制能力有提高，能较熟练的使用搓、推、挡、攻等各种击球方法，发球有一些落点、旋转、速度的变化。' },
					{ score: '1600', description: '正反手击球较稳定，方向感较好。基本掌握前冲弧圈球、高吊弧圈球的区别，对不同打法有一定的了解，熟练掌握3套以上的发球方法，接发球判断较好。' },
					{ score: '1800', description: '熟练运用击球力量、速度、旋转的变化，开始注意步法；了解反胶、长胶、生胶、正胶的不同特点。针对不同的对手采用不同的战术打法，回球落点好，能连续进攻，已经形成自己的打法特点。利用发球为自己创造进攻机会或直接得分，在对手不易判断、用近乎相同的发球动作发出上下旋转变化的球。' },
					{ score: '2000', description: '有很好的球感、手感和判断力，经常能在比赛中打出精彩的对攻回合球来。经常使用摆、晃、切、挑、挤、弹、抹、快带等技术，能迅速洞悉对手的弱点，及时调整战术，发挥自己的特长和优势。' },
					{ score: '2200', description: '形成了以速度、技巧、力量和顽强作风作为取胜法宝的风格。在比赛中变化不同的战术，在有压力的情况下仍能稳定地发挥水平，曾接受过一定专业训练，参加过省级水平的比赛。' },
					{ score: '2400', description: '经过专业强化训练，参加国家级水平的比赛，并有国家定义的运动员级别。' },
					{ score: '2600', description: '参加规模较小的世界范围内的锦标赛，有合适的机会便会跃升到下一级。' },
					{ score: '2800', description: '世界级选手，经常参加国际级的比赛，主要收入来自于比赛的奖金。' },
					{ score: '3000', description: '奥运冠军、世乒赛单打冠军选手。' },
				],
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
		},
		methods: {			
			back() {
				uni.navigateBack({
					delta: 1
				});
			},
			
			change(index) {
				this.current = index; 
			},
		}
	}
</script>

<style lang="scss" scoped>
	.scroll {
		height: 90vh;
	}

	.wrapper {
		margin-top: -25rpx;
	}
	
	.note {
		margin-top: 20rpx;
		text-align: end;
		font-weight: bold;
		color: #cc01ff;
	}
	
	.box {
		box-sizing: border-box;
		padding: 40rpx 20rpx;
		background-color: white;
		margin-top: 8rpx;
		background: #ffffff;
		border-radius: 20rpx;

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
	
	.table_head {
		text-align: center;
		font-weight: normal;
		white-space: nowrap;
		text-overflow: ellipsis;
		color: black;
	}
	
	.table_content {
		text-align: center;
		font-weight: bold;
		text-overflow: ellipsis;
		color: black;
	}
</style>

