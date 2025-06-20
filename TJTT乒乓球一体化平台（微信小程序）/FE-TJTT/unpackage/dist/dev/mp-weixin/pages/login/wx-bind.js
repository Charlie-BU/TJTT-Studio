"use strict";
const common_vendor = require("../../common/vendor.js");
const static_js_ajax_request = require("../../static/js/ajax_request.js");
const static_js_magic_power = require("../../static/js/magic_power.js");
const common_assets = require("../../common/assets.js");
const _sfc_main = {
  data() {
    return {
      hide_this: static_js_magic_power.magic()
    };
  },
  onLoad() {
  },
  methods: {
    onInput(e) {
      this.username = e.target.value;
      this.password = e.target.value;
    },
    backref() {
      common_vendor.index.navigateBack({
        delta: 1
      });
    },
    confirm() {
      common_vendor.wx$1.showToast({
        title: "请稍后...",
        icon: "loading",
        duration: 1e5
      });
      const username = this.username;
      const password = this.password;
      common_vendor.wx$1.login({
        // 这个里面this.xxx变undefined， 所以在外面用const重新定义
        success(r) {
          if (r.code) {
            static_js_ajax_request.fetch_data("POST", "fetch_openid", { "code": r.code }, "user", (res) => {
              if (res.data.openid) {
                let data = { "username": username, "password": password, "openid": res.data.openid };
                static_js_ajax_request.fetch_data("POST", "bind_wx", data, "user", (res2) => {
                  common_vendor.wx$1.showToast({
                    title: res2.data.message,
                    icon: "none",
                    duration: 700
                  });
                  if (res2.data.status == 200) {
                    setTimeout(() => {
                      common_vendor.index.reLaunch({
                        url: "/pages/login/login"
                      });
                    }, 700);
                  }
                });
              }
            });
          } else {
            common_vendor.wx$1.showToast({
              title: "绑定失败，请联系TJTT Studio成员",
              icon: "none",
              duration: 700
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
  }, !$data.hide_this ? {
    d: _ctx.username,
    e: common_vendor.o(($event) => _ctx.username = $event.detail.value),
    f: _ctx.password,
    g: common_vendor.o(($event) => _ctx.password = $event.detail.value),
    h: common_vendor.o((...args) => $options.confirm && $options.confirm(...args))
  } : {});
}
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["render", _sfc_render]]);
wx.createPage(MiniProgramPage);
