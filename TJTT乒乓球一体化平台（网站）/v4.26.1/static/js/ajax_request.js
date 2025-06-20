res = ""
// 服务器ip（部署公网要改）
my_ip = '/'
function send_ajax_request(request_type = null, url = null, data = null) {
    if (request_type === 'POST') {
        var json_data = JSON.stringify(data);
    }
    let xhr = new XMLHttpRequest(); // 创建XMLHttpRequest对象
    let all_url = my_ip + 'user/' + url
    xhr.open(request_type, all_url); // 设置请求类型
    xhr.setRequestHeader('Content-Type', 'application/json; charset=UTF-8')
    console.log(xhr)
    xhr.onreadystatechange = function () { // 定义状态改变时的回调函数
        res = JSON.parse(xhr.responseText); // 获取服务器返回的文本内容
    };
    if (request_type === 'GET') {
        xhr.send();
    } else {
        xhr.send(json_data); // 发送请求
    }
}


function fetch_ajax(request_type=null, url=null, data=null, blue=null) {
    // 使用 Fetch API 发送 POST 请求
    // 访问地址的获取及形式搭建，这样就能拿到一个完整的ip：xx.xx.x.x:5000/user/接口
    // 后期其他的bluePrint要用到时，就需要改这个函数了，明白吗?
    // 下面写死了user，对于organ怎么办
    // 看我操作
    // 现在很多html页面用到这个函数，因为之前user写死的，没有blue这个变量，所以调用这个函数的地方都需要改
    let all_url = my_ip + blue + '/' + url

    fetch(all_url, {
        method: request_type,  // 或 "GET"、"PUT" 等
        headers: {
            "Content-Type": "application/json; charset=UTF-8"
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        // 检查响应状态
        if (!response.ok) {
            throw new Error("Network response was not ok");
        }
        // 返回响应数据
        return response.json();
    })
    .then(data => {
        // 处理响应数据
        console.log(data);
        res = data;
    })
    .catch(error => {
        // 处理错误
        console.error("There was a problem with the fetch operation:", error);
    });
}
