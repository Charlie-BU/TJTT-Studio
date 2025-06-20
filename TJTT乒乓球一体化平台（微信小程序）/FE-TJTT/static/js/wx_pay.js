import { fetch_data } from '../../static/js/ajax_request.js'
import { login_check } from '../../static/js/login_check.js'
import * as utils from '../../static/js/utils.js'

function wx_pay(amount, description, attach=null, success=null) {
	amount = Number(amount);
	if (amount === NaN) {
		wx.showToast({
			title: "支付失败，请稍后重试",
			icon: "none",
			duration: 700,
		});
	}
	utils.get_openid((openid) => {
		if (openid) {
			let data = {
				"openid": openid,
				"amount": amount,
				"description": description,
				"attach": attach,
			}
			fetch_data("POST", "create_pay", data, "application", res => {
				if (res.data) {
					wx.requestPayment({
						timeStamp: res.data.timeStamp,
						nonceStr: res.data.nonceStr,
						package: res.data.package,
						signType: res.data.signType,
						paySign: res.data.paySign,
						success(r) {
							success(r);
						},
					})
				}
			});
			wx.hideToast();
		} else {
			wx.showToast({
				title: "支付失败，请稍后重试",
				icon: "none",
				duration: 700,
			});
		}
	});
}


export {
	wx_pay
}