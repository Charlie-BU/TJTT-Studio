"use strict";
const common_vendor = require("../../common/vendor.js");
const static_js_ajax_request = require("../../static/js/ajax_request.js");
const static_js_wx_login = require("../../static/js/wx_login.js");
const static_js_login_check = require("../../static/js/login_check.js");
const static_js_magic_power = require("../../static/js/magic_power.js");
const static_js_utils = require("../../static/js/utils.js");
const common_assets = require("../../common/assets.js");
const _sfc_main = {
  data() {
    return {
      user: "",
      phone: "",
      password: "",
      agree: "disagreed",
      hide_this: static_js_magic_power.magic()
    };
  },
  onLoad() {
    static_js_login_check.login_check((user) => {
      this.user = user;
    });
  },
  methods: {
    onInput(e) {
      this.phone = e.target.value;
      this.password = e.target.value;
    },
    whether_agree(e) {
      this.agree = e.detail.value;
    },
    backref() {
      common_vendor.index.navigateBack({
        delta: 1
      });
    },
    policy() {
      common_vendor.wx$1.showModal({
        title: "用户服务协议与隐私政策",
        content: "1.在您注册、登录本平台之前，请仔细阅读以下用户服务协议。注册/登录本平台，即表示您同意遵守以下协议;2.我们将严格保护用户的个人隐私信息，不会将用户的个人信息透露给任何第三方。但在法律规定的情况下，我们可能会根据相关法律法规要求向有关部门提供用户的个人信息;3. 本平台不对用户因使用本平台服务而产生的任何直接或间接损失承担责任。用户在使用本平台服务时，需自行承担风险，并且同意在任何情况下不追究本平台的责任;4.本平台有权根据需要对用户服务协议进行修改，修改后的协议将在平台上公布。用户继续使用本平台服务即视为同意修改后的协议。",
        showCancel: false,
        confirmText: "同意"
      });
    },
    login() {
      common_vendor.wx$1.showToast({
        title: "登录中",
        icon: "loading",
        duration: 1e5
      });
      let data = {
        "phone": this.phone,
        "password": this.password,
        "agree": this.agree
      };
      static_js_ajax_request.fetch_data("POST", "login_viaph", data, "user", (res) => {
        this.user_token = res.data.user_token;
        common_vendor.wx$1.showToast({
          title: res.data.message,
          icon: "none",
          duration: 700
        });
        if (this.user_token) {
          let asyncTask = function(callback) {
            var user_id = static_js_utils.get_user_info(user_token)[0];
            static_js_utils.get_my_rank(user_id);
            callback();
          };
          common_vendor.index.setStorageSync("user_token", this.user_token);
          var user_token = this.user_token;
          asyncTask(() => {
            console.log("async task finished");
          });
          setTimeout(() => {
            common_vendor.index.reLaunch({
              url: "/pages/index/index"
            });
          }, 700);
          setTimeout(() => {
            console.log("自动退出登录");
            common_vendor.index.clearStorageSync();
          }, 18e5);
        }
      });
    },
    wx_login() {
      if (this.agree != "agreed") {
        common_vendor.wx$1.showToast({
          title: "请阅读并同意小程序的协议与隐私政策",
          icon: "none",
          duration: 700
        });
        return;
      }
      common_vendor.wx$1.showToast({
        title: "登录中",
        icon: "loading",
        duration: 1e5
      });
      static_js_wx_login.wx_login();
    },
    register_page() {
      common_vendor.index.navigateTo({
        url: "/pages/login/register"
      });
    },
    login_page() {
      common_vendor.index.navigateTo({
        url: "/pages/login/login"
      });
    },
    forget_psw_page() {
      common_vendor.index.navigateTo({
        url: "/pages/login/forget_psw"
      });
    }
  }
};
function _sfc_render(_ctx, _cache, $props, $setup, $data, $options) {
  return common_vendor.e({
    a: common_assets._imports_0$1,
    b: common_vendor.o(($event) => $options.backref()),
    c: !$data.hide_this
  }, !$data.hide_this ? {
    d: $data.phone,
    e: common_vendor.o(($event) => $data.phone = $event.detail.value),
    f: $data.password,
    g: common_vendor.o(($event) => $data.password = $event.detail.value),
    h: common_vendor.o((...args) => $options.policy && $options.policy(...args)),
    i: common_vendor.o((...args) => $options.whether_agree && $options.whether_agree(...args)),
    j: common_vendor.o((...args) => $options.login && $options.login(...args)),
    k: common_vendor.o((...args) => $options.wx_login && $options.wx_login(...args)),
    l: common_vendor.o((...args) => $options.register_page && $options.register_page(...args)),
    m: common_vendor.o((...args) => $options.login_page && $options.login_page(...args)),
    n: common_vendor.o((...args) => $options.forget_psw_page && $options.forget_psw_page(...args))
  } : {});
}
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["render", _sfc_render]]);
wx.createPage(MiniProgramPage);
