<template>
	<div class="app">
		<div class="bc flex">
			<div class="left">
				<img class="bcImg" src="https://tjtt-assets.oss-cn-shanghai.aliyuncs.com/pictures/logos/logo_new.png" alt="" />
			</div>
			<div class="right">
				<div class="wrapper">
					<div class="text1">{{match.title}}</div>
				</div>
				<div class="text1" style="color: #f25c07;">赛制：{{match.system}}</div>
			</div>
		</div>
		<div class="codeA code" style="margin-top: 20rpx">
			<div class="textDiv">
				<uni-table stripe emptyText="暂无比赛成绩">
					<uni-tr>
						<uni-th width="20rpx"><view class="table_content">场次</view></uni-th>
						<uni-th width="20rpx"><view class="table_content">胜者</view></uni-th>
						<uni-th width="20rpx"><view class="table_content">胜者原积分</view></uni-th>
						<uni-th width="20rpx"><view class="table_content">胜者结算积分</view></uni-th>
						<uni-th width="20rpx"><view class="table_content">负者</view></uni-th>
						<uni-th width="20rpx"><view class="table_content">负者原积分</view></uni-th>
						<uni-th width="20rpx"><view class="table_content">负者结算积分</view></uni-th>
						<uni-th width="20rpx"><view class="table_content">比分</view></uni-th>
					</uni-tr>
					<uni-tr v-for="(result, index) in results" :key="index">
						<uni-td><view class="table_content" style="font-weight: normal;">{{index+1}}</view></uni-td>
						<uni-td>
							<view v-if="result.winner_name == user.username" class="table_content" style="color: red;">{{result.winner_name}}</view>
							<view v-else class="table_content" style="color: black;">{{result.winner_name}}</view>
						</uni-td>
						<uni-td><view class="table_content" style="color: black;">{{result.winner_score_before}}</view></uni-td>
						<uni-td><view class="table_content" style="color: black;">{{result.winner_score_after}}</view></uni-td>
						<uni-td>
							<view v-if="result.loser_name == user.username" class="table_content" style="color: red;">{{result.loser_name}}</view>
							<view v-else class="table_content" style="color: black;">{{result.loser_name}}</view>
						</uni-td>
						<uni-td><view class="table_content" style="color: black;">{{result.loser_score_before}}</view></uni-td>
						<uni-td><view class="table_content" style="color: black;">{{result.loser_score_after}}</view></uni-td>
						<uni-td><view v-if="result.match_title" class="table_content" style="color: black;">{{result.result}}</view></uni-td>
					</uni-tr>
				</uni-table>
			</div>
		</div>
	</div>
</template>

<script>
	import { fetch_data } from '../../static/js/ajax_request.js'
	import { login_check } from '../../static/js/login_check.js'
	export default {
		data() {
			return {
				message: "",
				user: "",
				match: "",
				results: [],
			}
		},
		onLoad() {
			login_check(user => {
				this.user = user;
			});
			// 获取赛事
			wx.showToast({
				title: '加载中',
				icon: 'loading',
				duration: 100000,
			});
			let match_id = uni.getStorageSync('match_id');
			fetch_data("POST", "get_this_match", {"match_id": match_id}, "competition", res => {
				this.match = res.data.match;
			});
			fetch_data("POST", "match_result", {"match_id": match_id}, "competition", res => {
				this.results = res.data.results;
				wx.hideToast();
			});
		},
		methods: {
		}
	}
</script>

<style lang="scss" scoped>
	.wrapper {
		height: 60rpx;
	}
	
	.foot {
		.left {
			text-align: center;
			background-color: #ffffff;
			box-sizing: box-sizing;
			padding: 20rpx;
			padding-top: 36rpx;
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
			line-height: 28rpx;
		}

		.r {
			background-color: #f9d67a !important;
		}
	}

	.app {
		min-height: 100vh;
		background: linear-gradient(135deg, #FEF2DA, #FFD5A4);
		box-sizing: border-box;
		padding: 20rpx;
	}

	.textT {
		font-weight: 600;
		font-size: 32rpx;
		box-sizing: border-box;
		padding-top: 22rpx;
	}

	.codeA {
		text-align: left !important;
		padding: 30rpx !important;

		.divider {
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
			line-height: 38rpx;
			text-align: left;
			font-style: normal;
			text-transform: none;
		}

		.text2 {
			font-family: PingFang SC, PingFang SC;
			font-weight: 600;
			font-size: 26rpx;
			color: #f25c07;
			line-height: 60rpx;
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
				width: 60%;
				height: 100%;
				margin: 6rpx 50rpx;
			}
		}
	}

	.userList {
		position: relative;
		box-sizing: box-sizing;
		margin-top: 40rpx;
		background: #ffffff;
		border-radius: 20rpx 20rpx 20rpx 20rpx;

		.p {
			font-family: PingFang SC, PingFang SC;
			font-weight: 600;
			font-size: 36rpx;
			color: #282456;
			line-height: 40rpx;
			text-align: center;
			font-style: normal;
			text-transform: none;
		}

		.span {
			margin-top: 24rpx;
			font-family: PingFang SC, PingFang SC;
			font-weight: 400;
			font-size: 24rpx;
			color: #666666;
			line-height: 24rpx;
			text-align: center;
			font-style: normal;
			text-transform: none;
		}
	}

	.itemList {
		text-align: center;
		width: 24%;
	}
	
	.table_head {
		text-align: center;
		font-weight: normal;
		white-space: nowrap;
		text-overflow: ellipsis;
	}
	
	.table_content {
		text-align: center;
		font-weight: bold;
		white-space: nowrap;
		text-overflow: ellipsis;
	}
</style>