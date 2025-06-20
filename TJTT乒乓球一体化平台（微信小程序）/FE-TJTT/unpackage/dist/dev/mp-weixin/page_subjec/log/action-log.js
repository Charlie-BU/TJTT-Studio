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
      action_logs: [],
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
    static_js_ajax_request.fetch_data("POST", "get_action_logs", null, "application", (res) => {
      this.action_logs = res.data.action_logs;
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
  __name: "action-log",
  setup(__props) {
    return (_ctx, _cache) => {
      return common_vendor.e({
        a: !_ctx.hide_this
      }, !_ctx.hide_this ? common_vendor.e({
        b: _ctx.user.id == 1
      }, _ctx.user.id == 1 ? {
        c: common_vendor.p({
          width: "20rpx"
        }),
        d: common_vendor.p({
          width: "1000rpx"
        }),
        e: common_vendor.p({
          width: "20rpx"
        }),
        f: common_vendor.p({
          width: "20rpx"
        }),
        g: common_vendor.f(_ctx.action_logs, (action_log, index, i0) => {
          return {
            a: common_vendor.t(index + 1),
            b: "cd1b9499-7-" + i0 + "," + ("cd1b9499-6-" + i0),
            c: common_vendor.t(action_log.action),
            d: "cd1b9499-8-" + i0 + "," + ("cd1b9499-6-" + i0),
            e: common_vendor.t(action_log.operator_name),
            f: common_vendor.o(($event) => _ctx.user_detail_page(action_log.operator_name), index),
            g: "cd1b9499-9-" + i0 + "," + ("cd1b9499-6-" + i0),
            h: common_vendor.t(static_js_utils.format_time(action_log.time)),
            i: "cd1b9499-10-" + i0 + "," + ("cd1b9499-6-" + i0),
            j: index,
            k: "cd1b9499-6-" + i0 + ",cd1b9499-0"
          };
        }),
        h: common_vendor.p({
          stripe: true,
          emptyText: "无数据"
        })
      } : {}) : {});
    };
  }
});
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["__scopeId", "data-v-cd1b9499"]]);
wx.createPage(MiniProgramPage);
