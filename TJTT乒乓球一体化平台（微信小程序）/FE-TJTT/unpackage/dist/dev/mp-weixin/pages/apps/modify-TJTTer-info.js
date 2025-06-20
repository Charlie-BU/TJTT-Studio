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
      TJTTer: "",
      department: "",
      job: "",
      property: "",
      description: "",
      hide_this: static_js_magic_power.magic()
    };
  },
  onLoad() {
    static_js_login_check.login_check((user) => {
      this.user = user;
    });
    if (!this.user || this.user.usertype != "K11") {
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
    let TJTTer_id = common_vendor.index.getStorageSync("TJTTer_id");
    if (!TJTTer_id) {
      common_vendor.wx$1.showToast({
        title: "服务器繁忙，请稍后再试",
        icon: "none",
        duration: 1500
      });
      setTimeout(() => {
        common_vendor.index.reLaunch({
          url: "/pages/index/index"
        });
      }, 1e3);
    } else {
      static_js_ajax_request.fetch_data("POST", "get_this_TJTTer", { "TJTTer_id": TJTTer_id }, "user", (res) => {
        this.TJTTer = res.data.TJTTer;
      });
    }
  },
  methods: {
    onInput(e) {
      this.description = e.target.value;
    },
    which_department(e) {
      this.department = e.detail.value;
    },
    which_job(e) {
      this.job = e.detail.value;
    },
    which_property(e) {
      this.property = e.detail.value;
    },
    backref() {
      common_vendor.index.navigateBack({
        delta: 1
      });
    },
    modify() {
      common_vendor.wx$1.showToast({
        title: "修改中",
        icon: "loading",
        duration: 1e5
      });
      let data = {
        "my_id": this.user.id,
        "TJTTer_id": this.TJTTer.id,
        "department": this.department,
        "job": this.job,
        "property": this.property,
        "description": this.description
      };
      static_js_ajax_request.fetch_data("POST", "modify_TJTTer_info", data, "user", (res) => {
        common_vendor.wx$1.showToast({
          title: res.data.message,
          icon: "none",
          duration: 1e3
        });
        if (res.data.status == 200) {
          setTimeout(() => {
            common_vendor.index.reLaunch({
              url: "/pages/apps/TJTTers"
            });
          }, 1e3);
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
    d: $data.TJTTer.name,
    e: common_vendor.f(["技术端", "组织端", "文化端"], (department, k0, i0) => {
      return {
        a: department,
        b: $data.TJTTer.department === department,
        c: common_vendor.t(department),
        d: department
      };
    }),
    f: common_vendor.o((...args) => $options.which_department && $options.which_department(...args)),
    g: common_vendor.f(["负责人", "顾问", "组长", "成员"], (job, k0, i0) => {
      return {
        a: job,
        b: $data.TJTTer.job === job,
        c: common_vendor.t(job),
        d: job
      };
    }),
    h: common_vendor.o((...args) => $options.which_job && $options.which_job(...args)),
    i: common_vendor.f(["0期创始成员", "1期成员", "2期成员"], (property, k0, i0) => {
      return {
        a: property,
        b: $data.TJTTer.property === property,
        c: common_vendor.t(property),
        d: property
      };
    }),
    j: common_vendor.o((...args) => $options.which_property && $options.which_property(...args)),
    k: $data.TJTTer.description,
    l: $data.description,
    m: common_vendor.o(($event) => $data.description = $event.detail.value),
    n: common_vendor.o((...args) => $options.modify && $options.modify(...args))
  } : {});
}
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["render", _sfc_render]]);
wx.createPage(MiniProgramPage);
