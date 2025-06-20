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
                url: 'https://docs.qq.com/aio/DZHd6Y2pBR3JQemV4',
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