"use strict";
const common_vendor = require("../../common/vendor.js");
const static_js_ajax_request = require("./ajax_request.js");
const static_js_utils = require("./utils.js");
function wx_pay(amount, description, attach = null, success = null) {
  amount = Number(amount);
  if (amount === NaN) {
    common_vendor.wx$1.showToast({
      title: "支付失败，请稍后重试",
      icon: "none",
      duration: 700
    });
  }
  static_js_utils.get_openid((openid) => {
    if (openid) {
      let data = {
        "openid": openid,
        "amount": amount,
        "description": description,
        "attach": attach
      };
      static_js_ajax_request.fetch_data("POST", "create_pay", data, "application", (res) => {
        if (res.data) {
          common_vendor.wx$1.requestPayment({
            timeStamp: res.data.timeStamp,
            nonceStr: res.data.nonceStr,
            package: res.data.package,
            signType: res.data.signType,
            paySign: res.data.paySign,
            success(r) {
              success(r);
            }
          });
        }
      });
    } else {
      common_vendor.wx$1.showToast({
        title: "支付失败，请稍后重试",
        icon: "none",
        duration: 700
      });
    }
  });
}
exports.wx_pay = wx_pay;
