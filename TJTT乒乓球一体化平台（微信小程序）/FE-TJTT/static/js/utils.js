import { fetch_data } from '../../static/js/ajax_request.js'

function get_openid(success=null) {
	wx.login({
		success(r) {
			if (r.code) {
				// 由于微信官方要求，获取用户openid的接口调用必须在后端实现，此处把r.code发给后端，换取openid
				fetch_data("POST", "fetch_openid", { "code": r.code }, "user", res => {
					if (res.data.openid) {
						success(res.data.openid);
					} else {
						console.log("openid获取失败");
					}
				});
			} else {
				console.log("openid获取失败");
			}
		}
	})
}

function get_rank(users, currentUserId) {
	let ids = [];
	let flagIndex = 0;
	let my_rank = '—';

	for (let i = 0; i < users.length; i++) {
		if (i === 0) {
			ids.push(i + 1);
		} else {
			if (users[i].score === users[flagIndex].score) {
				ids.push(flagIndex + 1);
			} else {
				flagIndex = i;
				ids.push(i + 1);
			}
		}
		// 检查当前用户的排名
		if (users[i].id === currentUserId) {
			my_rank = ids[ids.length - 1];
		}
	}
	return [ids, my_rank];
}

function get_my_rank(currentUserId) {
	var my_rank = null;
	fetch_data('POST', 'get_users', null, 'user', res => {
		my_rank = get_rank(res.data.users, currentUserId)[1];
		uni.setStorageSync('my_rank', my_rank);
	})
}

function decodeBase64(encodedString) {
	const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=';
	let str = String(encodedString).replace(/=+$/, '');
	if (str.length % 4 === 1) {
		throw new Error("'decodeBase64' failed: The string to be decoded is not correctly encoded.");
	}
	let output = '';
	for (let bc = 0, bs, buffer, idx = 0;
		(buffer = str.charAt(idx++)); ~buffer && (bs = bc % 4 ? bs * 64 + buffer : buffer, bc++ % 4) ? output +=
		String.fromCharCode(255 & bs >> (-2 * bc & 6)) : 0) {
		buffer = chars.indexOf(buffer);
	}
	return output;
}

function decode(encodedString) {
	let byteString = decodeBase64(encodedString);
	let decodedString = decodeURIComponent(escape(byteString));
	return decodedString;
}

function token_operation(user_token) {
	// 从user_token中拿到user_id和timestamp
	const decoded_user_token = decode(user_token);
	const regex = /(.*?)=(.*)=([\d.]+)$/;
	const match = decoded_user_token.match(regex);
	const user_id = match ? match[1] : null;
	const token_check = match ? match[2] : null;
	const timestamp = +(match ? match[3] : null);
	// 设置token过期时间
	const login_time = new Date(timestamp * 1000);
	const valid_time_end = new Date(login_time.getTime() + 24 * 60 * 60 * 1000);
	const now = new Date();
	if (!match || token_check !== 'logined_user_id[ATTENTION]timestamp') {
		console.log('用户token无效');
		wx.clearStorageSync();
		return null;
	}
	if (now > valid_time_end) {
		console.log('登录过期');
		wx.clearStorageSync();
		return null;
	}
	return user_id;
}

function get_user_info(user_token) {
	const user_id = token_operation(user_token);
	if (!user_id) {
		return [null, null];
	}
	fetch_data('POST', 'get_this_user', { 'user_id': user_id }, 'user', res => {
		uni.setStorageSync("user", res.data.user);
	})
	// 计算活跃度
	fetch_data('POST', 'cal_active', { 'user_id': user_id }, 'user')
	return [+user_id, uni.getStorageSync("user")];
}

function format_time(datetime) {
	const date = new Date(datetime);
	if (isNaN(date.getTime())) {
		console.log('Invalid datetime:', datetime);
		return null;
	}
	const year = date.getUTCFullYear().toString();
	const month = (date.getUTCMonth() + 1).toString().padStart(2, '0');
	const day = date.getUTCDate().toString().padStart(2, '0');
	const hours = date.getUTCHours().toString().padStart(2, '0');
	const minutes = date.getUTCMinutes().toString().padStart(2, '0');
	const seconds = date.getUTCSeconds().toString().padStart(2, '0');
	return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
}

function subscirbe_message(template_Ids, callback = null) {
	//template_Ids为列表，对应的消息模板
	wx.requestSubscribeMessage({
		tmplIds: template_Ids,
		success(res) {
			//用户授权后，无论同意与否
			if (res.errMsg == 'requestSubscribeMessage:ok') {
				callback();
			} 
		},
		fail(e) {
			console.log(e)
		},
	});
}

export {
	get_openid,
	get_rank,
	get_my_rank,
	decode,
	get_user_info,
	format_time,
    subscirbe_message,
}