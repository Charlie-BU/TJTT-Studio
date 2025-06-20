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
      getCodeText: "获取验证码",
      getCodeisWaiting: false,
      username: "",
      captcha: "",
      hide_this: static_js_magic_power.magic()
    };
  },
  onLoad() {
  },
  methods: {
    onInput(e) {
      this.username = e.target.value;
      this.captcha = e.target.value;
    },
    backref() {
      common_vendor.index.navigateBack({
        delta: 1
      });
    },
    Timer() {
    },
    getCode() {
      let data = {
        "username": this.username
      };
      static_js_ajax_request.fetch_data("POST", "send_captcha", data, "user", (res) => {
        if (res.data.status == 200) {
          if (this.getCodeisWaiting) {
            return;
          }
          this.getCodeText = "发送中";
          this.getCodeisWaiting = true;
          setTimeout(() => {
            common_vendor.index.showToast({
              title: res.data.message,
              icon: "none",
              duration: 1500
            });
            this.setTimer();
          }, 1e3);
        } else {
          common_vendor.wx$1.showToast({
            title: res.data.message,
            icon: "none",
            duration: 700
          });
        }
      });
    },
    //setTimer： 需要每隔一段时间执行一件事的的时候就需要使用SetTimer函数
    setTimer() {
      let holdTime = 60;
      this.getCodeText = "60秒";
      this.Timer = setInterval(() => {
        if (holdTime <= 0) {
          this.getCodeisWaiting = false;
          this.getCodeText = "获取验证码";
          clearInterval(this.Timer);
          return;
        }
        this.getCodeText = holdTime + "秒";
        holdTime--;
      }, 1e3);
    },
    confirm() {
      common_vendor.wx$1.showToast({
        title: "请稍后...",
        icon: "loading",
        duration: 1e5
      });
      let data = { "username": this.username, "captcha": this.captcha };
      static_js_ajax_request.fetch_data("POST", "forget_psw", data, "user", (res) => {
        console.log(res.data.message);
        common_vendor.wx$1.showToast({
          title: res.data.message,
          icon: "none",
          duration: 700
        });
        if (res.data.status == 200) {
          setTimeout(() => {
            common_vendor.index.reLaunch({
              url: "/pages/login/login"
            });
          }, 700);
        }
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
    f: common_vendor.t($data.getCodeText),
    g: common_vendor.o(($event) => $options.getCode()),
    h: $data.captcha,
    i: common_vendor.o(($event) => $data.captcha = $event.detail.value),
    j: common_vendor.o((...args) => $options.confirm && $options.confirm(...args))
  } : {});
}
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["render", _sfc_render]]);
wx.createPage(MiniProgramPage);
