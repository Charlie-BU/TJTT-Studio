"use strict";
const common_vendor = require("../../common/vendor.js");
const static_js_ajax_request = require("../../static/js/ajax_request.js");
const static_js_login_check = require("../../static/js/login_check.js");
const static_js_magic_power = require("../../static/js/magic_power.js");
const _sfc_main = {
  data() {
    return {
      user: "",
      message: "",
      user_length: "",
      match_length: "",
      TJTTers_length: "",
      foreign_admins: "",
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
    static_js_ajax_request.fetch_data("POST", "get_info", null, "user", (res) => {
      this.user_length = res.data.user_length;
      this.match_length = res.data.match_length;
      this.TJTTers_length = res.data.TJTTers_length;
      this.foreign_admins = res.data.foreign_admins;
    });
  },
  methods: {
    scan_qr() {
      if (this.hide_this) {
        return;
      }
      common_vendor.index.scanCode({
        success: (res) => {
          if (res.result.includes("Player's QRcode")) {
            let data = {
              "my_id": this.user.id,
              "qr_content": res.result
            };
            static_js_ajax_request.fetch_data("POST", "player_sign_in", data, "competition", (res2) => {
              common_vendor.wx$1.showToast({
                title: res2.data.message,
                icon: "none",
                duration: 1200
              });
            });
          } else {
            common_vendor.wx$1.showToast({
              title: "二维码无效",
              icon: "none",
              duration: 1200
            });
          }
        }
      });
    },
    user_list() {
      if (this.hide_this) {
        return;
      }
      common_vendor.index.navigateTo({
        url: "/page_subjec/user/user-list"
      });
    },
    organ_list() {
      if (this.hide_this) {
        return;
      }
      common_vendor.index.navigateTo({
        url: "/page_subjec/organization/organ-list"
      });
    },
    wx_bind() {
      if (this.hide_this) {
        return;
      }
      common_vendor.index.navigateTo({
        url: "/pages/login/wx-bind"
      });
    },
    score_update() {
      if (this.hide_this) {
        return;
      }
      common_vendor.wx$1.showActionSheet({
        itemList: ["单打", "双打"],
        success: function(res) {
          if (!res.cancel) {
            if (res.tapIndex == 0) {
              common_vendor.index.setStorageSync("update_match_type", "single");
            } else if (res.tapIndex == 1) {
              common_vendor.index.setStorageSync("update_match_type", "double");
            }
            common_vendor.index.navigateTo({
              url: "/page_subjec/match/score-update"
            });
          }
        }
      });
    },
    team_list() {
      if (this.hide_this) {
        return;
      }
      common_vendor.index.navigateTo({
        url: "/page_subjec/team/team-list"
      });
    },
    hold_match() {
      if (this.hide_this) {
        return;
      }
      common_vendor.index.navigateTo({
        url: "/page_subjec/match/hold-match"
      });
    },
    agendas() {
      if (this.hide_this) {
        return;
      }
      common_vendor.index.navigateTo({
        url: "/page_subjec/agendas/index"
      });
    },
    score_log() {
      if (this.hide_this) {
        return;
      }
      common_vendor.index.navigateTo({
        url: "/page_subjec/log/score-log"
      });
    },
    action_log() {
      if (this.hide_this) {
        return;
      }
      common_vendor.index.navigateTo({
        url: "/page_subjec/log/action-log"
      });
    },
    add_motto() {
      if (this.hide_this) {
        return;
      }
      common_vendor.index.navigateTo({
        url: "/page_subjec/motto/add-motto"
      });
    }
  }
};
if (!Array) {
  const _easycom_u_icon2 = common_vendor.resolveComponent("u-icon");
  const _easycom_uni_icons2 = common_vendor.resolveComponent("uni-icons");
  (_easycom_u_icon2 + _easycom_uni_icons2)();
}
const _easycom_u_icon = () => "../../uni_modules/vk-uview-ui/components/u-icon/u-icon.js";
const _easycom_uni_icons = () => "../../uni_modules/uni-icons/components/uni-icons/uni-icons.js";
if (!Math) {
  (_easycom_u_icon + _easycom_uni_icons)();
}
function _sfc_render(_ctx, _cache, $props, $setup, $data, $options) {
  return common_vendor.e({
    a: $data.user.usertype == "K9" || $data.user.usertype == "K10" || $data.user.usertype == "K11"
  }, $data.user.usertype == "K9" || $data.user.usertype == "K10" || $data.user.usertype == "K11" ? common_vendor.e({
    b: $data.user.id == 1
  }, $data.user.id == 1 ? {
    c: common_vendor.t($data.user.username),
    d: common_vendor.t($data.user.usertype)
  } : {
    e: common_vendor.t($data.user.username),
    f: common_vendor.t($data.user.usertype)
  }, {
    g: common_vendor.p({
      name: "integral",
      color: "#F25C07",
      size: "28"
    }),
    h: common_vendor.o($options.scan_qr),
    i: common_vendor.p({
      name: "scan",
      color: "#F25C07",
      size: "50"
    })
  }) : {}, {
    j: common_vendor.t($data.user_length),
    k: common_vendor.p({
      name: "account-fill",
      color: "#F25C07",
      size: "28"
    }),
    l: common_vendor.t($data.match_length),
    m: common_vendor.p({
      name: "coupon-fill",
      color: "#F25C07",
      size: "28"
    }),
    n: common_vendor.t($data.TJTTers_length),
    o: common_vendor.p({
      name: "integral-fill",
      color: "#F25C07",
      size: "28"
    }),
    p: common_vendor.p({
      name: "account",
      color: "#F25C07",
      size: "28"
    }),
    q: common_vendor.p({
      type: "person-filled",
      color: "#1f3347",
      size: "50"
    }),
    r: common_vendor.o((...args) => $options.user_list && $options.user_list(...args)),
    s: common_vendor.p({
      type: "staff-filled",
      color: "#1f3347",
      size: "50"
    }),
    t: common_vendor.o((...args) => $options.organ_list && $options.organ_list(...args)),
    v: common_vendor.p({
      type: "weixin",
      color: "#1f3347",
      size: "50"
    }),
    w: common_vendor.o((...args) => $options.wx_bind && $options.wx_bind(...args)),
    x: common_vendor.p({
      name: "coupon",
      color: "#F25C07",
      size: "28"
    }),
    y: common_vendor.p({
      type: "cloud-upload",
      color: "#1f3347",
      size: "50"
    }),
    z: common_vendor.o((...args) => $options.score_update && $options.score_update(...args)),
    A: common_vendor.p({
      type: "staff",
      color: "#1f3347",
      size: "50"
    }),
    B: common_vendor.o((...args) => $options.team_list && $options.team_list(...args)),
    C: common_vendor.p({
      type: "plus",
      color: "#1f3347",
      size: "50"
    }),
    D: common_vendor.o((...args) => $options.hold_match && $options.hold_match(...args)),
    E: common_vendor.p({
      name: "order",
      color: "#F25C07",
      size: "28"
    }),
    F: common_vendor.p({
      type: "wallet",
      color: "#1f3347",
      size: "50"
    }),
    G: common_vendor.o((...args) => $options.score_log && $options.score_log(...args)),
    H: $data.user.id == 1
  }, $data.user.id == 1 ? {
    I: common_vendor.p({
      type: "wallet-filled",
      color: "#1f3347",
      size: "50"
    }),
    J: common_vendor.o((...args) => $options.action_log && $options.action_log(...args))
  } : {}, {
    K: common_vendor.p({
      name: "flag",
      color: "#F25C07",
      size: "28"
    }),
    L: common_vendor.p({
      type: "home",
      color: "#1f3347",
      size: "50"
    }),
    M: common_vendor.o((...args) => $options.agendas && $options.agendas(...args)),
    N: common_vendor.p({
      type: "flag",
      color: "#1f3347",
      size: "50"
    }),
    O: common_vendor.o((...args) => $options.add_motto && $options.add_motto(...args))
  });
}
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["render", _sfc_render], ["__scopeId", "data-v-6f13f53e"]]);
wx.createPage(MiniProgramPage);
