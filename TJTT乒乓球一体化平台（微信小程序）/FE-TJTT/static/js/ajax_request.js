var res = ""

// 服务器ip
var local_ip = 'http://127.0.0.1:5000/'
var release_ip = 'https://tjtt.asia/'

function fetch_data(request_type=null, url=null, data=null, blue=null, success=null){
	let full_url = release_ip + blue + '/' + url
	wx.request({
		url: full_url,
		data: data,
		dataType: "json",
		method: request_type,
		sslVerify: false,
		withCredentials: false,
		firstIpv4: false,
		success(res) {
		    if(success){
			    success(res)
			    // console.log("success :", res.data)		// 包含敏感信息，生产环境切勿加
		    }
		},
		fail(e) {
			console.log('fail :',e);
			wx.showToast({
				title: "服务器繁忙，请稍后再试",
				icon: "none",
				duration: 1000,
			});
		},
		// complete(res) {
		// 	console.log("complete :", res);
		// },
	});
}

export {
	fetch_data
}