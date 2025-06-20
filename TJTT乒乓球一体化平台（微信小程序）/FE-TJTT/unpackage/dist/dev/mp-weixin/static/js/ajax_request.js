"use strict";
const common_vendor = require("../../common/vendor.js");
var release_ip = "https://tjtt.asia/";
function fetch_data(request_type = null, url = null, data = null, blue = null, success = null) {
  let full_url = release_ip + blue + "/" + url;
  common_vendor.wx$1.request({
    url: full_url,
    data,
    dataType: "json",
    method: request_type,
    sslVerify: false,
    withCredentials: false,
    firstIpv4: false,
    success(res) {
      if (success) {
        success(res);
      }
    },
    fail(e) {
      console.log("fail :", e);
      common_vendor.wx$1.showToast({
        title: "服务器繁忙，请稍后再试",
        icon: "none",
        duration: 1e3
      });
    }
    // complete(res) {
    // 	console.log("complete :", res);
    // },
  });
}
exports.fetch_data = fetch_data;
