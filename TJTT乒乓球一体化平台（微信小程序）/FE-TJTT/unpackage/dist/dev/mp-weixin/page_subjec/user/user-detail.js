"use strict";
const common_vendor = require("../../common/vendor.js");
const static_js_utils = require("../../static/js/utils.js");
const static_js_ajax_request = require("../../static/js/ajax_request.js");
const static_js_login_check = require("../../static/js/login_check.js");
const static_js_magic_power = require("../../static/js/magic_power.js");
if (!Array) {
  const _easycom_u_icon2 = common_vendor.resolveComponent("u-icon");
  const _easycom_uni_td2 = common_vendor.resolveComponent("uni-td");
  const _easycom_uni_tr2 = common_vendor.resolveComponent("uni-tr");
  const _easycom_uni_table2 = common_vendor.resolveComponent("uni-table");
  (_easycom_u_icon2 + _easycom_uni_td2 + _easycom_uni_tr2 + _easycom_uni_table2)();
}
const _easycom_u_icon = () => "../../uni_modules/vk-uview-ui/components/u-icon/u-icon.js";
const _easycom_uni_td = () => "../../uni_modules/uni-table/components/uni-td/uni-td.js";
const _easycom_uni_tr = () => "../../uni_modules/uni-table/components/uni-tr/uni-tr.js";
const _easycom_uni_table = () => "../../uni_modules/uni-table/components/uni-table/uni-table.js";
if (!Math) {
  (_easycom_u_icon + _easycom_uni_td + _easycom_uni_tr + _easycom_uni_table)();
}
const __default__ = {
  data() {
    return {
      user: "",
      user_x: "",
      actionList: [
        {
          name: "修改用户信息"
        },
        {
          name: "设为私密用户"
        },
        {
          name: "变更用户权限级"
        },
        {
          name: "删除用户"
        }
      ],
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
    let user_id = common_vendor.index.getStorageSync("user_id");
    if (!user_id) {
      common_vendor.wx$1.showToast({
        title: "服务器繁忙，请稍后再试",
        icon: "none",
        duration: 1500
      });
      setTimeout(() => {
        common_vendor.index.reLaunch({
          url: "/page_subjec/user/user-list"
        });
      }, 1e3);
    } else {
      common_vendor.wx$1.showToast({
        title: "加载中",
        icon: "loading",
        duration: 1e5
      });
      setTimeout(() => {
        static_js_ajax_request.fetch_data("POST", "get_this_user", { "user_id": user_id }, "user", (res) => {
          this.user_x = res.data.user;
          common_vendor.wx$1.hideToast();
        });
      }, 400);
    }
  },
  beforeDestroy() {
    common_vendor.index.removeStorageSync("user_id");
  },
  methods: {
    avatar_operation() {
      common_vendor.wx$1.showActionSheet({
        itemList: ["查看头像", "更换头像", "删除头像"],
        success: (res) => {
          if (!res.cancel) {
            let avatarUrl = this.user_x.profile_img;
            if (res.tapIndex == 0) {
              if (avatarUrl) {
                common_vendor.wx$1.previewImage({
                  urls: [avatarUrl],
                  current: avatarUrl
                });
              } else {
                common_vendor.wx$1.showToast({
                  title: "该用户还未上传头像",
                  icon: "none",
                  duration: 1e3
                });
                return;
              }
            } else if (res.tapIndex == 1) {
              common_vendor.wx$1.showModal({
                title: "请输入用户头像URL",
                editable: true,
                success: (res2) => {
                  if (res2.confirm) {
                    let data = {
                      "my_id": this.user.id,
                      "user_id": this.user_x.id,
                      "profile_img": res2.content
                    };
                    static_js_ajax_request.fetch_data("POST", "modify_user_profile_img", data, "user", (res3) => {
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
    },
    modify_user_info() {
      common_vendor.index.setStorageSync("user_id", this.user_x.id);
      common_vendor.index.navigateTo({
        url: "/page_subjec/user/modify-user-info"
      });
    },
    set_private() {
      common_vendor.wx$1.showModal({
        title: "设为私密用户",
        content: "设为私密用户后，该用户在“积分排名”中将以“" + this.user_x.username[0] + "** ”显示。",
        success: (res) => {
          if (res.confirm) {
            let data = {
              "my_id": this.user.id,
              "user_id": this.user_x.id,
              "set": "private"
            };
            static_js_ajax_request.fetch_data("POST", "set_privacy", data, "user", (res2) => {
              common_vendor.wx$1.showToast({
                title: res2.data.message,
                icon: "none",
                duration: 1e3
              });
              if (res2.data.status == 200) {
                static_js_ajax_request.fetch_data("POST", "get_this_user", {
                  "user_id": this.user_x.id
                }, "user", (res3) => {
                  this.user_x = res3.data.user;
                });
              }
            });
          }
        }
      });
    },
    set_public() {
      common_vendor.wx$1.showModal({
        title: "设为公开用户",
        content: "设为公开用户后，该用户在“积分排名”中将以全名显示。",
        success: (res) => {
          if (res.confirm) {
            let data = {
              "my_id": this.user.id,
              "user_id": this.user_x.id,
              "set": "public"
            };
            static_js_ajax_request.fetch_data("POST", "set_privacy", data, "user", (res2) => {
              common_vendor.wx$1.showToast({
                title: res2.data.message,
                icon: "none",
                duration: 1e3
              });
              if (res2.data.status == 200) {
                static_js_ajax_request.fetch_data("POST", "get_this_user", {
                  "user_id": this.user_x.id
                }, "user", (res3) => {
                  this.user_x = res3.data.user;
                });
              }
            });
          }
        }
      });
    },
    modify_usertype() {
      if (this.user.usertype !== "K11") {
        common_vendor.wx$1.showToast({
          title: "权限不足",
          icon: "none",
          duration: 1500
        });
      } else {
        common_vendor.wx$1.showActionSheet({
          itemList: ["普通用户", "K9级管理员", "K10级管理员", "K11级管理员"],
          success: (res) => {
            if (!res.cancel) {
              let usertypeMap = ["0", "K9", "K10", "K11"];
              let newType = usertypeMap[res.tapIndex];
              let contentMap = [
                `用户${this.user_x.username}原权限级"${this.user_x.usertype}"，确认变更为普通用户？`,
                `用户${this.user_x.username}原权限级"${this.user_x.usertype}"，确认变更为K9级管理员？`,
                `用户${this.user_x.username}原权限级"${this.user_x.usertype}"，确认变更为K10级管理员？`,
                `用户${this.user_x.username}原权限级"${this.user_x.usertype}"，确认变更为K11级管理员？`
              ];
              common_vendor.wx$1.showModal({
                title: "变更用户权限级",
                content: contentMap[res.tapIndex],
                success: (res2) => {
                  if (res2.confirm) {
                    let data = {
                      "my_id": this.user.id,
                      "user_id": this.user_x.id,
                      "usertype": newType
                    };
                    static_js_ajax_request.fetch_data("POST", "modify_usertype", data, "user", (res3) => {
                      common_vendor.wx$1.showToast({
                        title: res3.data.message,
                        icon: "none",
                        duration: 700
                      });
                      if (res3.data.status === 200) {
                        static_js_ajax_request.fetch_data("POST", "refresh", { "my_id": this.user.id }, "user", (res4) => {
                          common_vendor.index.setStorageSync("user", res4.data.user);
                        });
                        this.user_x.usertype = newType;
                      }
                    });
                  }
                }
              });
            }
          }
        });
      }
    },
    delete_user() {
      common_vendor.wx$1.showModal({
        title: "删除用户",
        content: "删除用户后，该用户所有信息及赛事记录将被永久清除；该操作可能导致数据库混乱、系统崩溃，请上报K11级管理员后操作",
        success: (res) => {
          if (res.confirm) {
            let data = {
              "my_id": this.user.id,
              "user_id": this.user_x.id
            };
            static_js_ajax_request.fetch_data("POST", "delete_user", data, "user", (res2) => {
              common_vendor.wx$1.showToast({
                title: res2.data.message,
                icon: "none",
                duration: 1e3
              });
              if (res2.data.status == 200) {
                setTimeout(() => {
                  common_vendor.index.reLaunch({
                    url: "/page_subjec/user/user-list"
                  });
                }, 1e3);
              }
            });
          }
        }
      });
    },
    modify_TJTTer() {
      if (this.user.usertype != "K11") {
        return;
      }
      var title = null;
      var content = null;
      if (this.user_x.is_TJTT) {
        title = "移出TJTT Studio";
        content = "是否确定将该用户移出TJTT Studio";
      } else {
        title = "加入TJTT Studio";
        content = "是否确定将该用户加入TJTT Studio";
      }
      common_vendor.wx$1.showModal({
        title,
        content,
        success: (res) => {
          if (res.confirm) {
            let data = {
              "my_id": this.user.id,
              "user_id": this.user_x.id
            };
            static_js_ajax_request.fetch_data("POST", "modify_TJTTer", data, "application", (res2) => {
              common_vendor.wx$1.showToast({
                title: res2.data.message,
                icon: "none",
                duration: 1e3
              });
              if (res2.data.status == 200) {
                setTimeout(() => {
                  common_vendor.index.reLaunch({
                    url: "/pages/apps/TJTTers"
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
const _sfc_main = /* @__PURE__ */ Object.assign(__default__, {
  __name: "user-detail",
  setup(__props) {
    return (_ctx, _cache) => {
      return common_vendor.e({
        a: !_ctx.hide_this
      }, !_ctx.hide_this ? common_vendor.e({
        b: _ctx.user_x.profile_img
      }, _ctx.user_x.profile_img ? {
        c: _ctx.user_x.profile_img
      } : _ctx.user_x.gender == "男" ? {} : _ctx.user_x.gender == "女" ? {} : {}, {
        d: _ctx.user_x.gender == "男",
        e: _ctx.user_x.gender == "女",
        f: common_vendor.o((...args) => _ctx.avatar_operation && _ctx.avatar_operation(...args)),
        g: common_vendor.t(_ctx.user_x.username),
        h: common_vendor.t(_ctx.user_x.school),
        i: _ctx.user_x.organ
      }, _ctx.user_x.organ ? {
        j: common_vendor.t(_ctx.user_x.organ.organname)
      } : {}, {
        k: _ctx.user_x.hand
      }, _ctx.user_x.hand ? {
        l: common_vendor.t(_ctx.user_x.hand)
      } : {}, {
        m: _ctx.user_x.grip
      }, _ctx.user_x.grip ? {
        n: common_vendor.t(_ctx.user_x.grip)
      } : {}, {
        o: _ctx.user_x.particle
      }, _ctx.user_x.particle ? {
        p: common_vendor.t(_ctx.user_x.particle)
      } : {}, {
        q: common_vendor.t(_ctx.user_x.score),
        r: common_vendor.f(_ctx.actionList, (item, index, i0) => {
          return common_vendor.e({
            a: index == 0 && !_ctx.hide_this
          }, index == 0 && !_ctx.hide_this ? {
            b: "914cb6d0-0-" + i0,
            c: common_vendor.p({
              name: "setting-fill",
              size: "40"
            }),
            d: common_vendor.t(item.name),
            e: common_vendor.o((...args) => _ctx.modify_user_info && _ctx.modify_user_info(...args), index)
          } : index == 1 ? common_vendor.e({
            g: _ctx.user_x.privacy == 0
          }, _ctx.user_x.privacy == 0 ? {
            h: "914cb6d0-1-" + i0,
            i: common_vendor.p({
              name: "account-fill",
              size: "40"
            }),
            j: common_vendor.t(item.name),
            k: common_vendor.o((...args) => _ctx.set_private && _ctx.set_private(...args), index)
          } : {
            l: "914cb6d0-2-" + i0,
            m: common_vendor.p({
              name: "account",
              size: "40"
            }),
            n: common_vendor.o((...args) => _ctx.set_public && _ctx.set_public(...args), index)
          }) : index == 2 ? {
            p: "914cb6d0-3-" + i0,
            q: common_vendor.p({
              name: "star-fill",
              size: "40"
            }),
            r: common_vendor.t(item.name),
            s: common_vendor.o((...args) => _ctx.modify_usertype && _ctx.modify_usertype(...args), index)
          } : index == 3 ? {
            v: "914cb6d0-4-" + i0,
            w: common_vendor.p({
              name: "person-delete-fill",
              size: "40"
            }),
            x: common_vendor.t(item.name),
            y: common_vendor.o((...args) => _ctx.delete_user && _ctx.delete_user(...args), index)
          } : {}, {
            f: index == 1,
            o: index == 2,
            t: index == 3,
            z: index
          });
        }),
        s: common_vendor.t(_ctx.user_x.gender),
        t: common_vendor.t(_ctx.user_x.address),
        v: common_vendor.t(_ctx.user_x.phone),
        w: common_vendor.t(_ctx.user_x.email),
        x: common_vendor.t(_ctx.user_x.school),
        y: common_vendor.t(_ctx.user_x.role),
        z: common_vendor.t(_ctx.user_x.stu_num),
        A: _ctx.user_x.organ
      }, _ctx.user_x.organ ? {
        B: common_vendor.t(_ctx.user_x.organ.organname)
      } : {}, {
        C: common_vendor.t(_ctx.user_x.hand),
        D: common_vendor.t(_ctx.user_x.grip),
        E: common_vendor.t(_ctx.user_x.blade),
        F: common_vendor.t(_ctx.user_x.forehand),
        G: common_vendor.t(_ctx.user_x.backhand),
        H: common_vendor.t(_ctx.user_x.particle),
        I: _ctx.user_x.usertype == "0"
      }, _ctx.user_x.usertype == "0" ? {} : {
        J: common_vendor.t(_ctx.user_x.usertype)
      }, {
        K: _ctx.user_x.privacy == 1
      }, _ctx.user_x.privacy == 1 ? {} : {}, {
        L: common_vendor.t(static_js_utils.format_time(_ctx.user_x.join_time)),
        M: _ctx.user_x.is_TJTT == 0
      }, _ctx.user_x.is_TJTT == 0 ? {
        N: common_vendor.o((...args) => _ctx.modify_TJTTer && _ctx.modify_TJTTer(...args))
      } : {
        O: common_vendor.o((...args) => _ctx.modify_TJTTer && _ctx.modify_TJTTer(...args))
      }, {
        P: common_vendor.p({
          stripe: true,
          emptyText: "无数据"
        })
      }) : {});
    };
  }
});
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["__scopeId", "data-v-914cb6d0"]]);
wx.createPage(MiniProgramPage);
