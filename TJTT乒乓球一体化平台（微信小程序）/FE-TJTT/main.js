import App from './App'
import Tabbar from '@/components/tabbar/index.vue';
import cuCustom from '@/components/colorui/components/cu-custom.vue';
import '@/static/base.css'
// #ifndef VUE3
import Vue from 'vue'
import './uni.promisify.adaptor'
Vue.config.productionTip = false
App.mpType = 'app'
const app = new Vue({
	...App
})
app.$mount()
// #endif
import uView from '@/uni_modules/vk-uview-ui';
// #ifdef VUE3

import {
	createSSRApp
} from 'vue'
export function createApp() {
	const app = createSSRApp(App)
	app.component('tabbar', Tabbar)
	app.component('cu-custom', cuCustom)
	app.use(uView)
	return {
		app
	}
}
// #endif