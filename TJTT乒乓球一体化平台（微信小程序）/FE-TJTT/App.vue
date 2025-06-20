<script>
	export default {
		onLaunch: function() {
			console.log('App Launch')
		},
		onShow: function() {
			console.log('App Show')
		},
		onHide: function() {
			console.log('App Hide')
		}
	}
</script>

<style lang="scss">
	@import "@/components/colorui/main.css";
	@import "@/components/colorui/icon.css";
	@import "@/uni_modules/vk-uview-ui/index.scss";

	page {
		background: #f8f8f8;
	}
</style>