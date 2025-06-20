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
      organ_length: "",
      tongji_length: "",
      search_organ: "",
      organs: [],
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
    static_js_ajax_request.fetch_data("POST", "get_info", null, "organization", (res) => {
      this.organ_length = res.data.organ_length;
      this.tongji_length = res.data.tongji_length;
    });
    static_js_ajax_request.fetch_data("POST", "get_organs", null, "organization", (res) => {
      this.organs = res.data.organs;
      common_vendor.wx$1.hideToast();
    });
  },
  methods: {
    onInput(e) {
      this.search_user = e.target.value;
    },
    search() {
      let data = { "search_organ": this.search_organ };
      static_js_ajax_request.fetch_data("POST", "findOrganByName", data, "organization", (res) => {
        this.organs = res.data.organs;
      });
    },
    add_organ() {
      common_vendor.index.navigateTo({
        url: "/page_subjec/organization/add-organ"
      });
    },
    delete_organ(organ_id) {
      common_vendor.wx$1.showModal({
        title: "删除组织",
        content: "删除组织后，该组织所有信息将被永久清除；该操作可能导致数据库混乱、系统崩溃，请上报K11级管理员后操作",
        success: (res) => {
          if (res.confirm) {
            let data = {
              "my_id": this.user.id,
              "organ_id": organ_id
            };
            static_js_ajax_request.fetch_data("POST", "delete_organ", data, "organization", (res2) => {
              common_vendor.wx$1.showToast({
                title: res2.data.message,
                icon: "none",
                duration: 1e3
              });
              if (res2.data.status == 200) {
                setTimeout(() => {
                  common_vendor.index.reLaunch({
                    url: "/page_subjec/organization/organ-list"
                  });
                }, 1e3);
              }
            });
          }
        }
      });
    }
  }
};
if (!Array) {
  const _easycom_u_search2 = common_vendor.resolveComponent("u-search");
  _easycom_u_search2();
}
const _easycom_u_search = () => "../../uni_modules/vk-uview-ui/components/u-search/u-search.js";
if (!Math) {
  _easycom_u_search();
}
function _sfc_render(_ctx, _cache, $props, $setup, $data, $options) {
  return common_vendor.e({
    a: !$data.hide_this
  }, !$data.hide_this ? {
    b: common_vendor.t($data.organ_length),
    c: common_vendor.t($data.tongji_length),
    d: common_vendor.t($data.organ_length),
    e: common_vendor.o(($event) => $data.search_organ = $event),
    f: common_vendor.p({
      ["bg-color"]: "#ffffff",
      ["show-action"]: false,
      placeholder: "输入组织名",
      modelValue: $data.search_organ
    }),
    g: common_vendor.o((...args) => $options.search && $options.search(...args)),
    h: common_vendor.o((...args) => $options.add_organ && $options.add_organ(...args)),
    i: common_vendor.f($data.organs, (organ, index, i0) => {
      return {
        a: common_vendor.t(index + 1),
        b: common_vendor.t(organ.organname),
        c: common_vendor.t(organ.description),
        d: common_vendor.t(organ.member_length),
        e: common_vendor.o(($event) => $options.delete_organ(organ.id), index),
        f: index
      };
    })
  } : {});
}
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["render", _sfc_render], ["__scopeId", "data-v-c5177d32"]]);
wx.createPage(MiniProgramPage);
