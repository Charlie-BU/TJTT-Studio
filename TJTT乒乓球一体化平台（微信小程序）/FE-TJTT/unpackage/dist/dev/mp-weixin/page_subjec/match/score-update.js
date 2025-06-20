"use strict";
const common_vendor = require("../../common/vendor.js");
const static_js_ajax_request = require("../../static/js/ajax_request.js");
const static_js_login_check = require("../../static/js/login_check.js");
const static_js_magic_power = require("../../static/js/magic_power.js");
const common_assets = require("../../common/assets.js");
const _sfc_main = {
  data() {
    return {
      message: "",
      user: "",
      update_match_type: "",
      match_title: "",
      winner1: "",
      winner2: "",
      loser1: "",
      loser2: "",
      result: "",
      hide_this: static_js_magic_power.magic()
    };
  },
  onLoad() {
    static_js_login_check.login_check((user) => {
      this.user = user;
    });
    if (!this.user) {
      common_vendor.wx$1.showToast({
        title: "请登录",
        icon: "none",
        duration: 1500
      });
      setTimeout(() => {
        common_vendor.index.reLaunch({
          url: "/pages/login/login"
        });
      }, 1e3);
    }
    this.update_match_type = common_vendor.index.getStorageSync("update_match_type");
    common_vendor.index.removeStorageSync("update_match_type");
  },
  methods: {
    onInput(e) {
      this.match_title = e.target.value;
      this.winner1 = e.target.value;
      this.loser1 = e.target.value;
      this.winner2 = e.target.value;
      this.loser2 = e.target.value;
    },
    what_result(e) {
      this.result = e.detail.value;
    },
    backref() {
      common_vendor.index.navigateBack({
        delta: 1
      });
    },
    confirm_single() {
      common_vendor.wx$1.showModal({
        title: "确认更新",
        content: "比分录入后选手积分自动计算，该操作不可逆，请务必确认对阵双方及比分正确",
        success: (res) => {
          if (res.confirm) {
            common_vendor.wx$1.showToast({
              title: "计算中",
              icon: "loading",
              duration: 1e5
            });
            let data = {
              "my_id": this.user.id,
              "match_title": this.match_title,
              "winner1": this.winner1,
              "loser1": this.loser1,
              "result": this.result
            };
            static_js_ajax_request.fetch_data("POST", "score_update_single", data, "competition", (res2) => {
              console.log(res2.data.message);
              common_vendor.wx$1.showToast({
                title: res2.data.message,
                icon: "none",
                duration: 700
              });
            });
          }
        }
      });
    },
    confirm_double() {
      common_vendor.wx$1.showModal({
        title: "确认更新",
        content: "比分录入后选手积分自动计算，该操作不可逆，请务必确认对阵双方及比分正确",
        success: (res) => {
          if (res.confirm) {
            common_vendor.wx$1.showToast({
              title: "计算中",
              icon: "loading",
              duration: 1e5
            });
            let data = {
              "my_id": this.user.id,
              "match_title": this.match_title,
              "winner1": this.winner1,
              "loser1": this.loser1,
              "winner2": this.winner2,
              "loser2": this.loser2,
              "result": this.result
            };
            static_js_ajax_request.fetch_data("POST", "score_update_double", data, "competition", (res2) => {
              console.log(res2.data.message);
              common_vendor.wx$1.showToast({
                title: res2.data.message,
                icon: "none",
                duration: 700
              });
            });
          }
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
  }, !$data.hide_this ? common_vendor.e({
    d: $data.update_match_type == "single"
  }, $data.update_match_type == "single" ? {
    e: $data.winner1,
    f: common_vendor.o(($event) => $data.winner1 = $event.detail.value)
  } : {}, {
    g: $data.update_match_type == "single"
  }, $data.update_match_type == "single" ? {
    h: $data.loser1,
    i: common_vendor.o(($event) => $data.loser1 = $event.detail.value)
  } : {}, {
    j: $data.update_match_type == "double"
  }, $data.update_match_type == "double" ? {
    k: $data.winner1,
    l: common_vendor.o(($event) => $data.winner1 = $event.detail.value)
  } : {}, {
    m: $data.update_match_type == "double"
  }, $data.update_match_type == "double" ? {
    n: $data.winner2,
    o: common_vendor.o(($event) => $data.winner2 = $event.detail.value)
  } : {}, {
    p: $data.update_match_type == "double"
  }, $data.update_match_type == "double" ? {
    q: $data.loser1,
    r: common_vendor.o(($event) => $data.loser1 = $event.detail.value)
  } : {}, {
    s: $data.update_match_type == "double"
  }, $data.update_match_type == "double" ? {
    t: $data.loser2,
    v: common_vendor.o(($event) => $data.loser2 = $event.detail.value)
  } : {}, {
    w: common_vendor.o((...args) => $options.what_result && $options.what_result(...args)),
    x: $data.match_title,
    y: common_vendor.o(($event) => $data.match_title = $event.detail.value),
    z: $data.update_match_type == "single"
  }, $data.update_match_type == "single" ? {
    A: common_vendor.o((...args) => $options.confirm_single && $options.confirm_single(...args))
  } : {}, {
    B: $data.update_match_type == "double"
  }, $data.update_match_type == "double" ? {
    C: common_vendor.o((...args) => $options.confirm_double && $options.confirm_double(...args))
  } : {}) : {});
}
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["render", _sfc_render]]);
wx.createPage(MiniProgramPage);
