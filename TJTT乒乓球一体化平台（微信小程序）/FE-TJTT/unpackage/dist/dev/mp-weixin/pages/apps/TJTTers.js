"use strict";
const common_vendor = require("../../common/vendor.js");
const static_js_ajax_request = require("../../static/js/ajax_request.js");
const static_js_login_check = require("../../static/js/login_check.js");
const static_js_magic_power = require("../../static/js/magic_power.js");
const _sfc_main = {
  data() {
    return {
      user: "",
      activeBtn: 0,
      current: 0,
      TJTTers: [],
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
    static_js_ajax_request.fetch_data("POST", "update_TJTTers", null, "application", (res) => {
      console.log(res.data.message);
    });
    static_js_ajax_request.fetch_data("POST", "get_TJTTers", null, "application", (res) => {
      this.TJTTers = res.data.TJTTers;
      common_vendor.wx$1.hideToast();
    });
  },
  methods: {
    setAbtn(e) {
      this.activeBtn = e;
      if (e == 0) {
        common_vendor.wx$1.showToast({
          title: "加载中",
          icon: "loading",
          duration: 1e5
        });
        static_js_ajax_request.fetch_data("POST", "get_TJTTers", null, "application", (res) => {
          this.TJTTers = res.data.TJTTers;
          common_vendor.wx$1.hideToast();
        });
      } else if (e == 1) {
        common_vendor.wx$1.showToast({
          title: "加载中",
          icon: "loading",
          duration: 1e5
        });
        static_js_ajax_request.fetch_data("POST", "get_dept_technology_TJTTers", null, "application", (res) => {
          this.TJTTers = res.data.TJTTers;
          common_vendor.wx$1.hideToast();
        });
      } else if (e == 2) {
        common_vendor.wx$1.showToast({
          title: "加载中",
          icon: "loading",
          duration: 1e5
        });
        static_js_ajax_request.fetch_data("POST", "get_dept_organizing_TJTTers", null, "application", (res) => {
          this.TJTTers = res.data.TJTTers;
          common_vendor.wx$1.hideToast();
        });
      } else if (e == 3) {
        common_vendor.wx$1.showToast({
          title: "加载中",
          icon: "loading",
          duration: 1e5
        });
        static_js_ajax_request.fetch_data("POST", "get_dept_culture_TJTTers", null, "application", (res) => {
          this.TJTTers = res.data.TJTTers;
          common_vendor.wx$1.hideToast();
        });
      }
    },
    avatar_operation(TJTTer) {
      if (this.user.usertype != "K11") {
        let avatarUrl = TJTTer.avatar_url;
        if (avatarUrl) {
          common_vendor.wx$1.previewImage({
            urls: [avatarUrl],
            current: avatarUrl
          });
        }
      } else {
        common_vendor.wx$1.showActionSheet({
          itemList: ["查看头像", "修改信息"],
          success: (res) => {
            if (!res.cancel) {
              let avatarUrl = TJTTer.avatar_url;
              if (res.tapIndex == 0) {
                if (avatarUrl) {
                  common_vendor.wx$1.previewImage({
                    urls: [avatarUrl],
                    current: avatarUrl
                  });
                } else {
                  common_vendor.wx$1.showToast({
                    title: "该成员暂未上传头像",
                    icon: "none",
                    duration: 1e3
                  });
                }
              } else if (res.tapIndex == 1) {
                common_vendor.index.setStorageSync("TJTTer_id", TJTTer.id);
                common_vendor.index.navigateTo({
                  url: "/pages/apps/modify-TJTTer-info"
                });
              } else if (res.tapIndex == 2) {
                if (!avatarUrl) {
                  common_vendor.wx$1.showToast({
                    title: "该用户还未上传头像",
                    icon: "none",
                    duration: 1e3
                  });
                  return;
                }
                common_vendor.wx$1.showModal({
                  title: "删除头像",
                  content: "确定删除该用户头像？",
                  success: (res2) => {
                    if (res2.confirm) {
                      let data = {
                        "my_id": this.user.id,
                        "user_id": this.user_x.id
                      };
                      static_js_ajax_request.fetch_data("POST", "delete_user_profile_img", data, "user", (res3) => {
                        common_vendor.wx$1.showToast({
                          title: res3.data.message,
                          icon: "none",
                          duration: 1e3
                        });
                        if (res3.data.status == 200) {
                          setTimeout(() => {
                            common_vendor.index.reLaunch({
                              url: "/page_subjec/user/user-detail"
                            });
                          }, 1e3);
                        }
                      });
                    }
                  }
                });
              }
            }
          }
        });
      }
    }
  }
};
function _sfc_render(_ctx, _cache, $props, $setup, $data, $options) {
  return common_vendor.e({
    a: !$data.hide_this
  }, !$data.hide_this ? {
    b: common_vendor.o(($event) => $options.setAbtn(0)),
    c: common_vendor.n($data.activeBtn == 0 ? "bg-cyan cu-btn" : " cu-btn line-cyan"),
    d: common_vendor.o(($event) => $options.setAbtn(1)),
    e: common_vendor.n($data.activeBtn == 1 ? "cu-btn bg-purple" : "cu-btn line-purple"),
    f: common_vendor.o(($event) => $options.setAbtn(2)),
    g: common_vendor.n($data.activeBtn == 2 ? "cu-btn bg-blue" : "cu-btn line-blue"),
    h: common_vendor.o(($event) => $options.setAbtn(3)),
    i: common_vendor.n($data.activeBtn == 3 ? "cu-btn bg-orange" : "cu-btn line-orange"),
    j: common_vendor.f(this.TJTTers, (TJTTer, index, i0) => {
      return common_vendor.e({
        a: TJTTer.avatar_url
      }, TJTTer.avatar_url ? {
        b: TJTTer.avatar_url
      } : {}, {
        c: common_vendor.o(($event) => $options.avatar_operation(TJTTer), index),
        d: TJTTer.gender == "男"
      }, TJTTer.gender == "男" ? common_vendor.e({
        e: common_vendor.t(TJTTer.name),
        f: TJTTer.email
      }, TJTTer.email ? {
        g: common_vendor.t(TJTTer.email)
      } : {}) : TJTTer.gender == "女" ? common_vendor.e({
        i: common_vendor.t(TJTTer.name),
        j: TJTTer.email
      }, TJTTer.email ? {
        k: common_vendor.t(TJTTer.email)
      } : {}) : {}, {
        h: TJTTer.gender == "女",
        l: common_vendor.t(TJTTer.department),
        m: common_vendor.t(TJTTer.job),
        n: common_vendor.t(TJTTer.property),
        o: TJTTer.description
      }, TJTTer.description ? {
        p: common_vendor.t(TJTTer.description)
      } : {}, {
        q: index
      });
    })
  } : {});
}
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["render", _sfc_render], ["__scopeId", "data-v-a9121e35"]]);
wx.createPage(MiniProgramPage);
