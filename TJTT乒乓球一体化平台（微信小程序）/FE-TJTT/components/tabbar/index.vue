<template>
	<!-- 底部操作条：背景颜色、对应图标、字体颜色，可自定义 -->
	<view class="cu-bar tabbar bg-white foot">
		<view class="action" :class="currentPage == 0 ? 'text-blue  ' : 'text-gray'" data-cur="home"
			@click="NavChange('/pages/index/index')">
			<div>
				<image class="tabbImg" v-show="currentPage == 0" src="@/static/tabbar/Ahome.png"></image>
				<image class="tabbImg" v-show="currentPage != 0" src="@/static/tabbar/home.png"></image>
			 </div>
			 <div class="text" >首页</div>
		</view>
		<view class="action" :class="currentPage == 3 ? 'text-blue' : 'text-gray'" data-cur="cart"
			@click="NavChange('/pages/community/index')">
			<div>
				<image class="tabbImg" v-show="currentPage == 3" src="@/static/tabbar/list.png"></image>
				<image class="tabbImg" v-show="currentPage != 3" src="@/static/tabbar/lis.png"></image>
			 </div>
			 <div class="text">交流</div>
			
		</view>
		<view class="action add-action" :class="currentPage == 2 ? 'text-blue' : 'text-gray'" data-cur="sub"
			@click="NavChange('/pages/score-ranking/index')">
			<button class="cu-btn Zhong shadow tabbImgA" style="background-color: transparent;" >
				<image  class="tabbImg tabbImgA" src="@/static/tabbar/g.png"></image>
			</button>
		</view>
		<view class="action" :class="currentPage == 1 ? 'text-blue' : 'text-gray'" data-cur="similar"
			@click="NavChange('/pages/apps/index')">
			<div style="position: relative;" >
				<view v-if="flagShow" class="hbTag cu-tag badge">{{ shopNum }}</view>			
				<image class="tabbImg" v-show="currentPage == 1" src="@/static/tabbar/Ashop.png"></image>
				<image class="tabbImg" v-show="currentPage != 1" src="@/static/tabbar/shop.png"></image>
			 </div>
			<div class="text" >应用</div>
		</view>
		<view class="action" :class="currentPage == 4 ? 'text-blue' : 'text-gray'" data-cur="mine"
			@click="NavChange('/pages/my/index')">
			<div>
				<image class="tabbImg" v-show="currentPage == 4" src="@/static/tabbar/Amy.png"></image>
				<image class="tabbImg" v-show="currentPage != 4" src="@/static/tabbar/my.png"></image>
			 </div>
			<div class="text">我的</div>
		</view>
	</view>
</template>
<script>


export default {
	props: {
		currentPage: {
			type: Number,
			default: 0,
			show:false
		}	
	},
	data() {
		return {
			currentItem: 0,
			tabbarList: [{
				id: 0,
				path: '/pages/index/index',
				icon: '/static/tabbar/home.png',
				selectIcon: '/static/tabbar/Ahome.png',
				text: '',
				centerItem: false
			},
			{
				id: 1,
				path: '/pages/apps/index',
				icon: '/static/tabbar/shop.png',
				selectIcon: '/static/tabbar/Ashop.png',
				text: '',
				centerItem: false
			},
			{
				id: 2,
				path: '/pages/score-ranking/index',
				icon: '/static/tabbar/g.png',
				selectIcon: '/static/tabbar/g.png',
				text: '',
				centerItem: true
			},
			{
				id: 3,
				path: '/pages/community/index',
				icon: '/static/tabbar/lis.png',
				selectIcon: '/static/tabbar/list.png',
				text: '',
				centerItem: false
			},
			{
				id: 4,
				path: '/pages/my/index',
				icon: '/static/tabbar/my.png',
				selectIcon: '/static/tabbar/Amy.png',
				text: '',
				centerItem: false
			}
			]
		};
	},
	mounted() {
		this.currentItem = this.currentPage;
		// uni.hideTabBar()
	},
	computed: {
		shopNum(){
			
		},
		flagShow(){
			return false
		}

	},
	methods: {
		NavChange(e) {
			let _this = this;
			uni.switchTab({
				url: e
			});
		}
	}
};
</script>
<style lang="scss"  scoped >
.text-blue {
	color: #F25C07 !important;
}
.tabbImgA{
	width: 178rpx !important;
	height: 178rpx !important;
	position: relative;
	bottom: 0rpx;
	left: -10rpx;
}
.hbTag{
	position: absolute;
	width: 36rpx;
	top: 0rpx;
	right: 10rpx !important;
}
.Zhong{
	position: absolute;
    width: 70rpx;
    z-index: 2;
    height: 70rpx;
    border-radius: 50%;
    line-height: 70rpx;
    font-size: 50rpx;
    top: -35rpx;
    left: 0;
    right: 0;
    margin: auto;
    padding: 0;
}
.text{
	margin-top: 10rpx;
	
}
.tabbImg{
	width: 40rpx;
	height: 40rpx;
}
.TsImage {
	width: 50% !important;
	height: 50% !important;
	position: relative;


}

view {
	padding: 0;
	margin: 0;
	box-sizing: border-box;
}

.tabbar-container {
	position: fixed;
	bottom: 0;
	left: 0;
	width: 100%;
	height: 110rpx;
	box-shadow: 0 0 5px #999;
	display: flex;
	align-items: center;
	padding: 5rpx 0;
	color: #999999;
}

.tabbar-container .tabbar-item {
	width: 20%;
	height: 100rpx;
	display: flex;
	flex-direction: column;
	justify-content: center;
	align-items: center;
	text-align: center;
}

.tabbar-container .item-active {
	color: #F25C07;
}

.tabbar-container .center-item {
	display: block;
	position: relative;
}

.tabbar-container .tabbar-item .item-top {
	width: 70rpx;
	height: 70rpx;
	padding: 10rpx;
}

.tabbar-container .center-item .item-top {
	flex-shrink: 0;
	width: 100rpx;
	height: 100rpx;
	position: absolute;
	top: -50rpx;
	left: calc(50% - 50rpx);
	border-radius: 50%;
	box-shadow: 0 0 5px #999;
	background-color: #F25C07;
}

.tabbar-container .tabbar-item .item-top image {
	width: 80%;
	height: 80%;

}

.tabbar-container .tabbar-item .item-bottom {
	font-size: 28rpx;
	width: 100%;
}

.tabbar-container .center-item .item-bottom {
	position: absolute;
	bottom: 5rpx;
}

.item-bottom {
	font-size: 22rpx !important;
	position: relative;
	bottom: 8rpx;
}

.TsText {
	position: relative;
	bottom: 58rpx;
	color: white !important;
}</style>
