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
      username: "",
      gender: "",
      phone: "",
      email: "",
      address: "",
      school: "",
      role: "",
      stu_num: "",
      password: "",
      score: "",
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
      this.username = e.target.value;
      this.phone = e.target.value;
      this.email = e.target.value;
      this.school = e.target.value;
      this.stu_num = e.target.value;
      this.password = e.target.value;
      this.score = e.target.value;
    },
    pick_addr(event) {
      const selected_addr = event.detail.value;
      this.address = selected_addr[1];
    },
    which_gender(e) {
      this.gender = e.detail.value;
    },
    which_role(e) {
      this.role = e.detail.value;
    },
    backref() {
      common_vendor.index.navigateBack({
        delta: 1
      });
    },
    add_user() {
      common_vendor.wx$1.showToast({
        title: "添加中",
        icon: "loading",
        duration: 1e5
      });
      let data = {
        "my_id": this.user.id,
        "username": this.username,
        "gender": this.gender,
        "phone": this.phone,
        "email": this.email,
        "address": this.address,
        "school": this.school,
        "role": this.role,
        "stu_num": this.stu_num,
        "password": this.password,
        "score": this.score
      };
      static_js_ajax_request.fetch_data("POST", "add_user", data, "user", (res) => {
        common_vendor.wx$1.showToast({
          title: res.data.message,
          icon: "none",
          duration: 700
        });
        if (res.data.status == 200) {
          setTimeout(() => {
            common_vendor.index.reLaunch({
              url: "/page_subjec/user/user-list"
            });
          }, 700);
        }
      });
    }
  }
};
if (!Array) {
  const _easycom_u_icon2 = common_vendor.resolveComponent("u-icon");
  _easycom_u_icon2();
}
const _easycom_u_icon = () => "../../uni_modules/vk-uview-ui/components/u-icon/u-icon.js";
if (!Math) {
  _easycom_u_icon();
}
function _sfc_render(_ctx, _cache, $props, $setup, $data, $options) {
  return common_vendor.e({
    a: common_assets._imports_0$1,
    b: common_vendor.o(($event) => $options.backref()),
    c: !$data.hide_this
  }, !$data.hide_this ? {
    d: $data.username,
    e: common_vendor.o(($event) => $data.username = $event.detail.value),
    f: common_vendor.o((...args) => $options.which_gender && $options.which_gender(...args)),
    g: $data.phone,
    h: common_vendor.o(($event) => $data.phone = $event.detail.value),
    i: $data.email,
    j: common_vendor.o(($event) => $data.email = $event.detail.value),
    k: common_vendor.t($data.address ? $data.address : "请选择用户所在地区"),
    l: common_vendor.p({
      name: "arrow-down",
      size: "28"
    }),
    m: common_vendor.o((...args) => $options.pick_addr && $options.pick_addr(...args)),
    n: $data.school,
    o: common_vendor.o(($event) => $data.school = $event.detail.value),
    p: common_vendor.o((...args) => $options.which_role && $options.which_role(...args)),
    q: $data.stu_num,
    r: common_vendor.o(($event) => $data.stu_num = $event.detail.value),
    s: $data.password,
    t: common_vendor.o(($event) => $data.password = $event.detail.value),
    v: $data.score,
    w: common_vendor.o(($event) => $data.score = $event.detail.value),
    x: common_vendor.o((...args) => $options.add_user && $options.add_user(...args))
  } : {});
}
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["render", _sfc_render]]);
wx.createPage(MiniProgramPage);
