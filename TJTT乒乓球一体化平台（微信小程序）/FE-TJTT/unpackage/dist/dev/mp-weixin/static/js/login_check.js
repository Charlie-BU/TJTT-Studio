"use strict";
const common_vendor = require("../../common/vendor.js");
const static_js_utils = require("./utils.js");
function login_check(success = null) {
  const user_token = common_vendor.index.getStorageSync("user_token");
  if (user_token) {
    const user = static_js_utils.get_user_info(user_token)[1];
    if (!user) {
      console.log("登录失效");
    }
    success(user);
    console.log("用户已登录");
  } else {
    console.log("未登录");
  }
}
exports.login_check = login_check;
