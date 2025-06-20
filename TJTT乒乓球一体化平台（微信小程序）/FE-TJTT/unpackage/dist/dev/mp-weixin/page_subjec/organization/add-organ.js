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
      organname: "",
      description: "",
      hide_this: static_js_magic_power.magic()
    };
  },
  onLoad() {
    static_js_login_check.login_check((user) => {
      this.user = user;
    });
    if (!this.user || this.user.usertype != "K10" && this.user.usertype != "K11") {
      common_vendor.wx$1.showToast({
        title: "权限不足",
        icon: "none",
        duration: 1500
      });
      setTimeout(() => {
        common_vendor.index.reLaunch({
          url: "/pages/index/index"
        });
      }, 1e3);
    }
  },
  methods: {
    onInput(e) {
      this.organname = e.target.value;
      this.description = e.target.value;
    },
    backref() {
      common_vendor.index.navigateBack({
        delta: 1
      });
    },
    add_user() {
      let data = {
        "my_id": this.user.id,
        "organname": this.organname,
        "description": this.description
      };
      static_js_ajax_request.fetch_data("POST", "add_organ", data, "organization", (res) => {
        common_vendor.wx$1.showToast({
          title: res.data.message,
          icon: "none",
          duration: 700
        });
        if (res.data.status == 200) {
          setTimeout(() => {
            common_vendor.index.reLaunch({
              url: "/page_subjec/organization/organ-list"
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
    d: $data.organname,
    e: common_vendor.o(($event) => $data.organname = $event.detail.value),
    f: $data.description,
    g: common_vendor.o(($event) => $data.description = $event.detail.value),
    h: common_vendor.o((...args) => $options.add_user && $options.add_user(...args))
  } : {});
}
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["render", _sfc_render]]);
wx.createPage(MiniProgramPage);
