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
      old_psw: "",
      new_psw: "",
      new_psw2: "",
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
      this.old_psw = e.target.value;
      this.new_psw = e.target.value;
      this.new_psw2 = e.target.value;
    },
    backref() {
      common_vendor.index.navigateBack({
        delta: 1
      });
    },
    modify() {
      let data = {
        "my_id": this.user.id,
        "old_psw": this.old_psw,
        "new_psw": this.new_psw,
        "new_psw2": this.new_psw2
      };
      static_js_ajax_request.fetch_data("POST", "modify_psw", data, "user", (res) => {
        console.log(res.data.message);
        common_vendor.wx$1.showToast({
          title: res.data.message,
          icon: "none",
          duration: 700
        });
        if (res.data.status == 200) {
          setTimeout(() => {
            common_vendor.index.reLaunch({
              url: "/pages/my/index"
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
    d: $data.user.username,
    e: $data.old_psw,
    f: common_vendor.o(($event) => $data.old_psw = $event.detail.value),
    g: $data.new_psw,
    h: common_vendor.o(($event) => $data.new_psw = $event.detail.value),
    i: $data.new_psw2,
    j: common_vendor.o(($event) => $data.new_psw2 = $event.detail.value),
    k: common_vendor.o((...args) => $options.modify && $options.modify(...args))
  } : {});
}
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["render", _sfc_render]]);
wx.createPage(MiniProgramPage);
