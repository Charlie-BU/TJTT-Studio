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
      teamname: "",
      description: "",
      member_max: "",
      match_title: "",
      hide_this: static_js_magic_power.magic()
    };
  },
  onLoad() {
    static_js_login_check.login_check((user) => {
      this.user = user;
    });
    if (!this.user || this.user.usertype != "K9" && this.user.usertype != "K10" && this.user.usertype != "K11") {
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
      this.teamname = e.target.value;
      this.description = e.target.value;
      this.member_max = e.target.value;
      this.match_title = e.target.value;
    },
    backref() {
      common_vendor.index.navigateBack({
        delta: 1
      });
    },
    add_team() {
      let data = {
        "my_id": this.user.id,
        "teamname": this.teamname,
        "description": this.description,
        "member_max": this.member_max,
        "match_title": this.match_title
      };
      static_js_ajax_request.fetch_data("POST", "add_team", data, "competition", (res) => {
        common_vendor.wx$1.showToast({
          title: res.data.message,
          icon: "none",
          duration: 700
        });
        if (res.data.status == 200) {
          setTimeout(() => {
            common_vendor.index.reLaunch({
              url: "/page_subjec/team/team-list"
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
    d: $data.teamname,
    e: common_vendor.o(($event) => $data.teamname = $event.detail.value),
    f: $data.description,
    g: common_vendor.o(($event) => $data.description = $event.detail.value),
    h: $data.member_max,
    i: common_vendor.o(($event) => $data.member_max = $event.detail.value),
    j: $data.match_title,
    k: common_vendor.o(($event) => $data.match_title = $event.detail.value),
    l: common_vendor.o((...args) => $options.add_team && $options.add_team(...args))
  } : {});
}
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["render", _sfc_render]]);
wx.createPage(MiniProgramPage);
