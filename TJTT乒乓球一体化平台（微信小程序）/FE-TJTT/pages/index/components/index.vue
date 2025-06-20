<template>	
	<div class="box">
		<!-- <div>
			<img class="imgs" src="../../../static/tabbar/Frame.png" alt="">
			<span class="imgs">上海</span>
			<img class="imgsA" src="../../../static/tabbar/Polygon.png" alt="">
		</div> -->
		<div class="search">
			<!-- <u-search bg-color="#ffffff" :show-action="false" placeholder="搜索比赛关键词"></u-search> -->
		</div>
	</div>
</template>

<script>
	
</script>

<style lang="scss" scoped>
	.box {
		width: 100%;
		height: 400rpx;
		background: #FEF2DA;
		box-sizing: border-box;
		padding: 20rpx 26rpx;
		padding-top: 102rpx;
	}

	.imgs {
		width: 42rpx;
		height: 42rpx;
		position: relative;
		top: 50rpx;
	}
	
	.welcome {
		margin: 40rpx 12rpx;
		font-weight: bold;
		font-size: 30rpx;
		position: relative;
		top: 60rpx;
	}

	.search {
		margin-top: 115rpx;
	}

	.span {
		margin: 40rpx 12rpx;
		color: #282456;
		font-size: 30rpx;
	}

	.imgsA {
		width: 22rpx;
		height: 17rpx;
	}
</style>