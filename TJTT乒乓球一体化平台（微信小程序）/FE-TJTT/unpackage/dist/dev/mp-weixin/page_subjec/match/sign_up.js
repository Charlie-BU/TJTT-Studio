"use strict";
const common_vendor = require("../../common/vendor.js");
const static_js_ajax_request = require("../../static/js/ajax_request.js");
const static_js_login_check = require("../../static/js/login_check.js");
const static_js_wx_pay = require("../../static/js/wx_pay.js");
const static_js_magic_power = require("../../static/js/magic_power.js");
const _sfc_main = {
  data() {
    return {
      message: "",
      user: "",
      match: "",
      team_id: "",
      agree: "",
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
  },
  methods: {
    which_team(e) {
      this.team_id = e.detail.value;
    },
    whether_agree(e) {
      this.agree = e.detail.value;
    },
    backref() {
      common_vendor.index.navigateBack({
        delta: 1
      });
    },
    sign_up() {
      if (this.agree !== "agreed") {
        common_vendor.wx$1.showToast({
          title: "请阅读并同意承诺书",
          icon: "none",
          duration: 1e3
        });
        return;
      }
      if (this.match.fee > 0) {
        this.initiate_payment();
      } else {
        this.confirm_sign_up();
      }
    },
    initiate_payment() {
      common_vendor.wx$1.showToast({
        title: "请稍后",
        icon: "loading",
        duration: 1e5
      });
      static_js_wx_pay.wx_pay(this.match.fee, this.user.username + "赛事报名", null, (res) => {
        if (res) {
          this.confirm_sign_up();
        } else {
          common_vendor.wx$1.showToast({
            title: "支付失败，请重试",
            icon: "none",
            duration: 1e3
          });
        }
      });
    },
    // 确认报名流程
    confirm_sign_up() {
      common_vendor.wx$1.showToast({
        title: "报名中",
        icon: "loading",
        duration: 1e5
      });
      const data = {
        match_id: this.match.id,
        user_id: this.user.id,
        team_id: parseInt(this.team_id),
        agree: this.agree
      };
      static_js_ajax_request.fetch_data("POST", "match_sign_up", data, "competition", (res) => {
        common_vendor.wx$1.showToast({
          title: res.data.message,
          icon: "none",
          duration: 1e3
        });
        if (res.data.status === 200) {
          setTimeout(() => {
            common_vendor.index.reLaunch({
              url: "/page_subjec/match/index"
            });
          }, 1e3);
        }
      });
    }
  }
};
function _sfc_render(_ctx, _cache, $props, $setup, $data, $options) {
  return common_vendor.e({
    a: !$data.hide_this
  }, !$data.hide_this ? common_vendor.e({
    b: $data.user.username,
    c: $data.user.phone,
    d: $data.user.role,
    e: $data.user.score,
    f: $data.match
  }, $data.match ? {
    g: $data.match.title
  } : {}, {
    h: $data.match
  }, $data.match ? {
    i: $data.match.restriction
  } : {}, {
    j: isNaN($data.match.participant - $data.match.players_length)
  }, isNaN($data.match.participant - $data.match.players_length) ? {} : {
    k: $data.match.participant - $data.match.players_length
  }, {
    l: $data.match.teams_length != 0
  }, $data.match.teams_length != 0 ? {
    m: common_vendor.f($data.match.teams, (team_x, index, i0) => {
      return {
        a: team_x.id,
        b: common_vendor.t(team_x.teamname),
        c: index
      };
    }),
    n: $data.message,
    o: common_vendor.o((...args) => $options.which_team && $options.which_team(...args))
  } : {}, {
    p: common_vendor.t($data.match.fee),
    q: common_vendor.t($data.user.username),
    r: common_vendor.o((...args) => $options.whether_agree && $options.whether_agree(...args)),
    s: common_vendor.o((...args) => $options.sign_up && $options.sign_up(...args)),
    t: common_vendor.o((...args) => $options.backref && $options.backref(...args))
  }) : {});
}
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["render", _sfc_render]]);
wx.createPage(MiniProgramPage);
