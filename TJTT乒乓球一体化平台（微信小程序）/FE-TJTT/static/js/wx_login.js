import { fetch_data } from '../../static/js/ajax_request.js'
import { login_check } from '../../static/js/login_check.js'
import * as utils from '../../static/js/utils.js'

function wx_login() {
	utils.get_openid((openid) => {
		if (openid) {
			fetch_data("POST", "wx_login", { "open_id": openid }, "user", res => {
				// 登录成功
				if (res.data.status == 200) {
					wx.showToast({
						title: res.data.message,
						icon: "none",
						duration: 700,
					});
					uni.setStorageSync('user_token', res.data.user_token);
					var user_token = res.data.user_token;
					// 异步获取用户信息
					function asyncTask(callback) {
						var user_id = utils.get_user_info(user_token)[0];
						utils.get_my_rank(user_id);
						callback();
					}
					asyncTask(() => {
						console.log('async task finished');
					})
					// -----异步进程结束-----
					
					setTimeout(() => {
						uni.reLaunch({
							url: '/pages/index/index',
						})
					}, 700);
				}
				// 微信未被绑定
				else {
					wx.showModal({
						title: res.data.message,
						content: '是否前往绑定微信？',
						success: res => {
							if (res.confirm) {
								uni.navigateTo({
									url: '/pages/login/wx-bind',
								})
							}
						}
					})
				}
			});
		} else {
			wx.showToast({
				title: "登录失败，请换其他方式登录",
				icon: "none",
				duration: 700,
			});
		}
	});
}


export {
	wx_login
}