<template>
    <view>
        <web-view :webview-styles="webviewStyles" :src="url" @message="getMessage"></web-view>
    </view>
</template>

<script>
    export default {
        data() {
            return {
                webviewStyles: {
                    progress: {
                        color: '#FF3333'
                    }
                },
                url: 'https://mp.weixin.qq.com/s/KeSkRYJ-3IP5wQNt5seO1g',
            }
        },
        onLoad() {
        },
        methods: {
        }
    }
</script>

<style>
</style>