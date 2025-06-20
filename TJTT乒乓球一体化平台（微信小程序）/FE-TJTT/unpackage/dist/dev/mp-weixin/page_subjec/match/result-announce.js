"use strict";
const common_vendor = require("../../common/vendor.js");
const static_js_ajax_request = require("../../static/js/ajax_request.js");
const static_js_login_check = require("../../static/js/login_check.js");
const _sfc_main = {
  data() {
    return {
      message: "",
      user: "",
      match: "",
      results: []
    };
  },
  onLoad() {
    static_js_login_check.login_check((user) => {
      this.user = user;
    });
    common_vendor.wx$1.showToast({
      title: "加载中",
      icon: "loading",
      duration: 1e5
    });
    let match_id = common_vendor.index.getStorageSync("match_id");
    static_js_ajax_request.fetch_data("POST", "get_this_match", { "match_id": match_id }, "competition", (res) => {
      this.match = res.data.match;
    });
    static_js_ajax_request.fetch_data("POST", "match_result", { "match_id": match_id }, "competition", (res) => {
      this.results = res.data.results;
      common_vendor.wx$1.hideToast();
    });
  },
  methods: {}
};
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
function _sfc_render(_ctx, _cache, $props, $setup, $data, $options) {
  return {
    a: common_vendor.t($data.match.title),
    b: common_vendor.t($data.match.system),
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
    k: common_vendor.f($data.results, (result, index, i0) => {
      return common_vendor.e({
        a: common_vendor.t(index + 1),
        b: "b55cf8a2-11-" + i0 + "," + ("b55cf8a2-10-" + i0),
        c: result.winner_name == $data.user.username
      }, result.winner_name == $data.user.username ? {
        d: common_vendor.t(result.winner_name)
      } : {
        e: common_vendor.t(result.winner_name)
      }, {
        f: "b55cf8a2-12-" + i0 + "," + ("b55cf8a2-10-" + i0),
        g: common_vendor.t(result.winner_score_before),
        h: "b55cf8a2-13-" + i0 + "," + ("b55cf8a2-10-" + i0),
        i: common_vendor.t(result.winner_score_after),
        j: "b55cf8a2-14-" + i0 + "," + ("b55cf8a2-10-" + i0),
        k: result.loser_name == $data.user.username
      }, result.loser_name == $data.user.username ? {
        l: common_vendor.t(result.loser_name)
      } : {
        m: common_vendor.t(result.loser_name)
      }, {
        n: "b55cf8a2-15-" + i0 + "," + ("b55cf8a2-10-" + i0),
        o: common_vendor.t(result.loser_score_before),
        p: "b55cf8a2-16-" + i0 + "," + ("b55cf8a2-10-" + i0),
        q: common_vendor.t(result.loser_score_after),
        r: "b55cf8a2-17-" + i0 + "," + ("b55cf8a2-10-" + i0),
        s: result.match_title
      }, result.match_title ? {
        t: common_vendor.t(result.result)
      } : {}, {
        v: "b55cf8a2-18-" + i0 + "," + ("b55cf8a2-10-" + i0),
        w: index,
        x: "b55cf8a2-10-" + i0 + ",b55cf8a2-0"
      });
    }),
    l: common_vendor.p({
      stripe: true,
      emptyText: "暂无比赛成绩"
    })
  };
}
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["render", _sfc_render], ["__scopeId", "data-v-b55cf8a2"]]);
wx.createPage(MiniProgramPage);
