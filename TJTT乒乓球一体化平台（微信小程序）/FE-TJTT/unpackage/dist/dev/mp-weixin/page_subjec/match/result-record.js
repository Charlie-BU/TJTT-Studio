"use strict";
const common_vendor = require("../../common/vendor.js");
const static_js_ajax_request = require("../../static/js/ajax_request.js");
const static_js_login_check = require("../../static/js/login_check.js");
const static_js_magic_power = require("../../static/js/magic_power.js");
const _sfc_main = {
  data() {
    return {
      message: "",
      user: "",
      match: "",
      player_x: "",
      player_y: "",
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
    common_vendor.wx$1.showToast({
      title: "加载中",
      icon: "loading",
      duration: 1e5
    });
    let match_id = common_vendor.index.getStorageSync("match_id");
    static_js_ajax_request.fetch_data("POST", "get_this_match", { "match_id": match_id }, "competition", (res) => {
      this.match = res.data.match;
      common_vendor.wx$1.hideToast();
    });
    this.player_x = common_vendor.index.getStorageSync("player_x");
    this.player_y = common_vendor.index.getStorageSync("player_y");
    if (!this.player_x || !this.player_y) {
      common_vendor.wx$1.showToast({
        title: "服务器繁忙，请稍后再试",
        icon: "none",
        duration: 1500
      });
      setTimeout(() => {
        common_vendor.index.navigateBack({
          delta: 1
        });
      }, 1e3);
    }
    common_vendor.index.removeStorageSync("player_x");
    common_vendor.index.removeStorageSync("player_y");
  },
  methods: {
    what_result(e) {
      this.result = e.detail.value;
    },
    confirm_record() {
      if (!this.result) {
        common_vendor.wx$1.showToast({
          title: "请选择比分",
          icon: "none",
          duration: 1e3
        });
      } else {
        common_vendor.wx$1.showModal({
          title: "确认录入",
          content: "成绩录入后选手积分自动计算，该操作不可逆，请务必确认对阵双方及比分正确",
          success: (res) => {
            if (res.confirm) {
              common_vendor.wx$1.showToast({
                title: "计算中",
                icon: "loading",
                duration: 1e5
              });
              let data = {
                "my_id": this.user.id,
                "match_id": this.match.id,
                "player_x_id": this.player_x.id,
                "player_y_id": this.player_y.id,
                "result": this.result
              };
              static_js_ajax_request.fetch_data("POST", "result_record", data, "competition", (res2) => {
                console.log(res2.data.message);
                common_vendor.wx$1.showToast({
                  title: res2.data.message,
                  icon: "none",
                  duration: 1e3
                });
                if (res2.data.status == 200) {
                  static_js_ajax_request.fetch_data("POST", "refresh", { "my_id": this.user.id }, "user", (res3) => {
                    common_vendor.index.setStorageSync("user", res3.data.user);
                    common_vendor.index.setStorageSync("my_rank", res3.data.my_rank);
                  });
                  setTimeout(() => {
                    common_vendor.index.navigateBack({
                      delta: 1
                    });
                  }, 1e3);
                }
              });
            }
          }
        });
      }
    }
  }
};
function _sfc_render(_ctx, _cache, $props, $setup, $data, $options) {
  return common_vendor.e({
    a: !$data.hide_this
  }, !$data.hide_this ? {
    b: common_vendor.t($data.match.title),
    c: common_vendor.t($data.match.system),
    d: common_vendor.t($data.player_x.username),
    e: common_vendor.t($data.player_y.username),
    f: common_vendor.o((...args) => $options.what_result && $options.what_result(...args)),
    g: common_vendor.o((...args) => $options.confirm_record && $options.confirm_record(...args))
  } : {});
}
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["render", _sfc_render], ["__scopeId", "data-v-30e9766d"]]);
wx.createPage(MiniProgramPage);
