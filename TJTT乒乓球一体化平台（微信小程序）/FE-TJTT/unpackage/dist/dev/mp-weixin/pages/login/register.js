"use strict";
const common_vendor = require("../../common/vendor.js");
const static_js_ajax_request = require("../../static/js/ajax_request.js");
const static_js_magic_power = require("../../static/js/magic_power.js");
const common_assets = require("../../common/assets.js");
const _sfc_main = {
  data() {
    return {
      message: "",
      user: "",
      username: "",
      gender: "",
      phone: "",
      email: "",
      school: "",
      role: "",
      password: "",
      password2: "",
      agree: "disagreed",
      hide_this: static_js_magic_power.magic()
    };
  },
  onLoad() {
  },
  methods: {
    onInput(e) {
      this.username = e.target.value;
      this.phone = e.target.value;
      this.email = e.target.value;
      this.school = e.target.value;
      this.password = e.target.value;
      this.password2 = e.target.value;
    },
    which_gender(e) {
      this.gender = e.detail.value;
    },
    which_role(e) {
      this.role = e.detail.value;
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
    register() {
      common_vendor.wx$1.showToast({
        title: "注册中",
        icon: "loading",
        duration: 1e5
      });
      let data = {
        "username": this.username,
        "gender": this.gender,
        "phone": this.phone,
        "email": this.email,
        "school": this.school,
        "role": this.role,
        "password": this.password,
        "password2": this.password2,
        "agree": this.agree
      };
      static_js_ajax_request.fetch_data("POST", "register", data, "user", (res) => {
        common_vendor.wx$1.showToast({
          title: res.data.message,
          icon: "none",
          duration: 700
        });
        if (res.data.status == 200) {
          setTimeout(() => {
            common_vendor.index.reLaunch({
              url: "/pages/login/wx-bind"
            });
          }, 700);
        }
      });
    },
    login_page() {
      common_vendor.index.navigateTo({
        url: "/pages/login/login"
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
    d: $data.username,
    e: common_vendor.o(($event) => $data.username = $event.detail.value),
    f: common_vendor.o((...args) => $options.which_gender && $options.which_gender(...args)),
    g: $data.phone,
    h: common_vendor.o(($event) => $data.phone = $event.detail.value),
    i: $data.email,
    j: common_vendor.o(($event) => $data.email = $event.detail.value),
    k: $data.school,
    l: common_vendor.o(($event) => $data.school = $event.detail.value),
    m: common_vendor.o((...args) => $options.which_role && $options.which_role(...args)),
    n: $data.password,
    o: common_vendor.o(($event) => $data.password = $event.detail.value),
    p: $data.password2,
    q: common_vendor.o(($event) => $data.password2 = $event.detail.value),
    r: common_vendor.o((...args) => $options.policy && $options.policy(...args)),
    s: common_vendor.o((...args) => $options.whether_agree && $options.whether_agree(...args)),
    t: common_vendor.o((...args) => $options.register && $options.register(...args)),
    v: common_vendor.o((...args) => $options.login_page && $options.login_page(...args))
  } : {});
}
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["render", _sfc_render]]);
wx.createPage(MiniProgramPage);
