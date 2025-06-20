import * as utils from '../../static/js/utils.js'

function login_check(success=null){
	const user_token = uni.getStorageSync('user_token');
	if (user_token) {
		const user = utils.get_user_info(user_token)[1];
		if (!user) {
			console.log("登录失效");
		}
		success(user);
		console.log("用户已登录");
	}
	else{
		console.log("未登录");
	}
}


export {
	login_check
}