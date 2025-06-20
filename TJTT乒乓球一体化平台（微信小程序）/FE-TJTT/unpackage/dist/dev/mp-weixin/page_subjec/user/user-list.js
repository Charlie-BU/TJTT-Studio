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
      student_length: "",
      teacher_length: "",
      admin_length: "",
      search_user: "",
      users: [],
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
    static_js_ajax_request.fetch_data("POST", "get_info", null, "user", (res) => {
      this.user_length = res.data.user_length;
      this.student_length = res.data.student_length;
      this.teacher_length = res.data.teacher_length;
      this.admin_length = res.data.admin_length;
    });
    static_js_ajax_request.fetch_data("POST", "get_users_by_join_time", null, "user", (res) => {
      this.users = res.data.users;
      common_vendor.wx$1.hideToast();
    });
  },
  methods: {
    onInput(e) {
      this.search_user = e.target.value;
    },
    search() {
      let data = { "search_user": this.search_user, "where": "user_list" };
      static_js_ajax_request.fetch_data("POST", "findUserByName", data, "user", (res) => {
        this.users = res.data.users;
      });
    },
    add_user() {
      common_vendor.index.navigateTo({
        url: "/page_subjec/user/add-user"
      });
    },
    modify_score(user_id) {
      common_vendor.wx$1.showModal({
        title: "变更用户积分",
        placeholderText: "请输入变更后积分",
        editable: true,
        confirmText: "确认变更",
        success: (res) => {
          if (res.confirm) {
            let data = {
              "my_id": this.user.id,
              "user_id": user_id,
              "score": res.content
            };
            static_js_ajax_request.fetch_data("POST", "modify_score", data, "user", (res2) => {
              common_vendor.wx$1.showToast({
                title: res2.data.message,
                icon: "none",
                duration: 1e3
              });
              if (res2.data.status == 200) {
                static_js_ajax_request.fetch_data("POST", "get_users", null, "user", (res3) => {
                  this.users = res3.data.users;
                  if (res3.data.status == 200) {
                    common_vendor.wx$1.showToast({
                      title: res3.data.message,
                      icon: "none",
                      duration: 1e3
                    });
                  }
                });
              }
            });
          }
        }
      });
    },
    user_detail(user_id) {
      common_vendor.index.setStorageSync("user_id", user_id);
      common_vendor.index.navigateTo({
        url: "/page_subjec/user/user-detail"
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
    a: common_vendor.t($data.user_length),
    b: common_vendor.t($data.student_length),
    c: common_vendor.t($data.teacher_length),
    d: common_vendor.t($data.admin_length),
    e: common_vendor.o(($event) => $data.search_user = $event),
    f: common_vendor.p({
      ["bg-color"]: "#ffffff",
      ["show-action"]: false,
      placeholder: "输入用户姓名",
      modelValue: $data.search_user
    }),
    g: common_vendor.o((...args) => $options.search && $options.search(...args)),
    h: !$data.hide_this
  }, !$data.hide_this ? {
    i: common_vendor.o((...args) => $options.add_user && $options.add_user(...args))
  } : {}, {
    j: common_vendor.f($data.users, (user, index, i0) => {
      return common_vendor.e({
        a: user.profile_img
      }, user.profile_img ? {
        b: user.profile_img
      } : {}, {
        c: common_vendor.t(index + 1),
        d: common_vendor.t(user.username),
        e: common_vendor.t(user.gender),
        f: common_vendor.t(user.school),
        g: common_vendor.t(user.role),
        h: common_vendor.t(user.score),
        i: common_vendor.o(($event) => $options.modify_score(user.id), index),
        j: common_vendor.o(($event) => $options.user_detail(user.id), index),
        k: index
      });
    })
  });
}
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["render", _sfc_render], ["__scopeId", "data-v-71cc360c"]]);
wx.createPage(MiniProgramPage);
