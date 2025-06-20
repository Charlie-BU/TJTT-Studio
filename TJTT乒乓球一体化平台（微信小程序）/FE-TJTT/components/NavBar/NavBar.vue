<template>
	<view  >
		
	</view>
</template>

<script setup>
	import { defineEmits } from 'vue'
	const emit = defineEmits(['back'])
	const leftClick = ()=>{
		emit('back')
		
	}
	
</script>

<style lang="scss" scoped >

</style>