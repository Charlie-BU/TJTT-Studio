"use strict";
const common_vendor = require("../../common/vendor.js");
const static_js_ajax_request = require("./ajax_request.js");
const static_js_utils = require("./utils.js");
function wx_login() {
  static_js_utils.get_openid((openid) => {
    if (openid) {
      static_js_ajax_request.fetch_data("POST", "wx_login", { "open_id": openid }, "user", (res) => {
        if (res.data.status == 200) {
          let asyncTask = function(callback) {
            var user_id = static_js_utils.get_user_info(user_token)[0];
            static_js_utils.get_my_rank(user_id);
            callback();
          };
          common_vendor.wx$1.showToast({
            title: res.data.message,
            icon: "none",
            duration: 700
          });
          common_vendor.index.setStorageSync("user_token", res.data.user_token);
          var user_token = res.data.user_token;
          asyncTask(() => {
            console.log("async task finished");
          });
          setTimeout(() => {
            common_vendor.index.reLaunch({
              url: "/pages/index/index"
            });
          }, 700);
        } else {
          common_vendor.wx$1.showModal({
            title: res.data.message,
            content: "是否前往绑定微信？",
            success: (res2) => {
              if (res2.confirm) {
                common_vendor.index.navigateTo({
                  url: "/pages/login/wx-bind"
                });
              }
            }
          });
        }
      });
    } else {
      common_vendor.wx$1.showToast({
        title: "登录失败，请换其他方式登录",
        icon: "none",
        duration: 700
      });
    }
  });
}
exports.wx_login = wx_login;
