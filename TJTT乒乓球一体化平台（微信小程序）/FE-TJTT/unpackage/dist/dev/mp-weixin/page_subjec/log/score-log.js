"use strict";
const common_vendor = require("../../common/vendor.js");
const static_js_utils = require("../../static/js/utils.js");
const static_js_ajax_request = require("../../static/js/ajax_request.js");
const static_js_login_check = require("../../static/js/login_check.js");
const static_js_magic_power = require("../../static/js/magic_power.js");
if (!Array) {
  const _easycom_uni_th2 = common_vendor.resolveComponent("uni-th");
  const _easycom_uni_tr2 = common_vendor.resolveComponent("uni-tr");
  const _easycom_uni_td2 = common_vendor.resolveComponent("uni-td");
  const _easycom_uni_table2 = common_vendor.resolveComponent("uni-table");
  (_easycom_uni_th2 + _easycom_uni_tr2 + _easycom_uni_td2 + _easycom_uni_table2)();
}
const _easycom_uni_th = () => "../../uni_modules/uni-table/components/uni-th/uni-th.js";
const _easycom_uni_tr = () => "../../uni_modules/uni-table/components/uni-tr/uni-tr.js";
const _easycom_uni_td = () => "../../uni_modules/uni-table/components/uni-td/uni-td.js";
const _easycom_uni_table = () => "../../uni_modules/uni-table/components/uni-table/uni-table.js";
if (!Math) {
  (_easycom_uni_th + _easycom_uni_tr + _easycom_uni_td + _easycom_uni_table)();
}
const __default__ = {
  data() {
    return {
      message: "",
      user: "",
      score_logs: [],
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
    common_vendor.wx$1.showToast({
      title: "加载中",
      icon: "loading",
      duration: 1e5
    });
    static_js_ajax_request.fetch_data("POST", "get_score_logs", null, "competition", (res) => {
      this.score_logs = res.data.score_logs;
      common_vendor.wx$1.hideToast();
    });
  },
  methods: {
    user_detail_page(username) {
      if (!username) {
        return;
      }
      static_js_ajax_request.fetch_data("POST", "get_user_id_by_username", { "username": username }, "user", (res) => {
        let user_id = res.data.user_id;
        common_vendor.index.setStorageSync("user_id", user_id);
        common_vendor.index.navigateTo({
          url: "/page_subjec/user/user-detail"
        });
      });
    }
  }
};
const _sfc_main = /* @__PURE__ */ Object.assign(__default__, {
  __name: "score-log",
  setup(__props) {
    return (_ctx, _cache) => {
      return common_vendor.e({
        a: !_ctx.hide_this
      }, !_ctx.hide_this ? common_vendor.e({
        b: _ctx.user.usertype == "K9" || _ctx.user.usertype == "K10" || _ctx.user.usertype == "K11"
      }, _ctx.user.usertype == "K9" || _ctx.user.usertype == "K10" || _ctx.user.usertype == "K11" ? {
        c: common_vendor.p({
          width: "20rpx"
        }),
        d: common_vendor.p({
          width: "20rpx"
        }),
        e: common_vendor.p({
          width: "20rpx"
        }),
        f: common_vendor.p({
          width: "20rpx"
        }),
        g: common_vendor.p({
          width: "20rpx"
        }),
        h: common_vendor.p({
          width: "20rpx"
        }),
        i: common_vendor.p({
          width: "20rpx"
        }),
        j: common_vendor.p({
          width: "20rpx"
        }),
        k: common_vendor.p({
          width: "20rpx"
        }),
        l: common_vendor.p({
          width: "20rpx"
        }),
        m: common_vendor.f(_ctx.score_logs, (score_log, index, i0) => {
          return common_vendor.e({
            a: common_vendor.t(index + 1),
            b: "0b3a4a02-13-" + i0 + "," + ("0b3a4a02-12-" + i0),
            c: score_log.winner_name == _ctx.user.username
          }, score_log.winner_name == _ctx.user.username ? {
            d: common_vendor.t(score_log.winner_name),
            e: common_vendor.o(($event) => _ctx.user_detail_page(score_log.winner_name), index)
          } : {
            f: common_vendor.t(score_log.winner_name),
            g: common_vendor.o(($event) => _ctx.user_detail_page(score_log.winner_name), index)
          }, {
            h: "0b3a4a02-14-" + i0 + "," + ("0b3a4a02-12-" + i0),
            i: common_vendor.t(score_log.winner_score_before),
            j: "0b3a4a02-15-" + i0 + "," + ("0b3a4a02-12-" + i0),
            k: common_vendor.t(score_log.winner_score_after),
            l: "0b3a4a02-16-" + i0 + "," + ("0b3a4a02-12-" + i0),
            m: score_log.loser_name == _ctx.user.username
          }, score_log.loser_name == _ctx.user.username ? {
            n: common_vendor.t(score_log.loser_name),
            o: common_vendor.o(($event) => _ctx.user_detail_page(score_log.loser_name), index)
          } : {
            p: common_vendor.t(score_log.loser_name),
            q: common_vendor.o(($event) => _ctx.user_detail_page(score_log.loser_name), index)
          }, {
            r: "0b3a4a02-17-" + i0 + "," + ("0b3a4a02-12-" + i0),
            s: common_vendor.t(score_log.loser_score_before),
            t: "0b3a4a02-18-" + i0 + "," + ("0b3a4a02-12-" + i0),
            v: common_vendor.t(score_log.loser_score_after),
            w: "0b3a4a02-19-" + i0 + "," + ("0b3a4a02-12-" + i0),
            x: score_log.match_title
          }, score_log.match_title ? {
            y: common_vendor.t(score_log.match_title)
          } : {}, {
            z: "0b3a4a02-20-" + i0 + "," + ("0b3a4a02-12-" + i0),
            A: common_vendor.t(static_js_utils.format_time(score_log.time)),
            B: "0b3a4a02-21-" + i0 + "," + ("0b3a4a02-12-" + i0),
            C: common_vendor.t(score_log.operator_name),
            D: "0b3a4a02-22-" + i0 + "," + ("0b3a4a02-12-" + i0),
            E: index,
            F: "0b3a4a02-12-" + i0 + ",0b3a4a02-0"
          });
        }),
        n: common_vendor.p({
          stripe: true,
          emptyText: "无数据"
        })
      } : {}) : {});
    };
  }
});
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["__scopeId", "data-v-0b3a4a02"]]);
wx.createPage(MiniProgramPage);
