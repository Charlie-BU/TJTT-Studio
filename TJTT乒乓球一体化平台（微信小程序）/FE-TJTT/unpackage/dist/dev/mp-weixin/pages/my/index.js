"use strict";
const common_vendor = require("../../common/vendor.js");
const static_js_ajax_request = require("../../static/js/ajax_request.js");
const static_js_login_check = require("../../static/js/login_check.js");
const static_js_magic_power = require("../../static/js/magic_power.js");
const static_js_utils = require("../../static/js/utils.js");
if (!Array) {
  const _easycom_u_icon2 = common_vendor.resolveComponent("u-icon");
  const _easycom_uni_td2 = common_vendor.resolveComponent("uni-td");
  const _easycom_uni_tr2 = common_vendor.resolveComponent("uni-tr");
  const _easycom_uni_table2 = common_vendor.resolveComponent("uni-table");
  const _component_tabbar = common_vendor.resolveComponent("tabbar");
  (_easycom_u_icon2 + _easycom_uni_td2 + _easycom_uni_tr2 + _easycom_uni_table2 + _component_tabbar)();
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
      my_rank: "",
      this_season: "",
      latest_match: "",
      userList: [
        {
          name: "执拍手"
        },
        {
          name: "握拍方式"
        },
        {
          name: "颗粒"
        },
        {
          name: "所在地区"
        }
      ],
      actionList: [
        {
          name: "修改个人信息"
        },
        {
          name: "修改密码"
        },
        {
          name: "设为私密用户"
        }
      ],
      hide_this: static_js_magic_power.magic()
    };
  },
  onLoad() {
    static_js_login_check.login_check((user) => {
      this.user = user;
    });
    this.my_rank = common_vendor.wx$1.getStorageSync("my_rank");
    static_js_ajax_request.fetch_data("POST", "match_list_current", null, "competition", (res) => {
      this.latest_match = res.data.matches[0];
    });
    static_js_ajax_request.fetch_data("POST", "get_this_season", null, "competition", (res) => {
      this.this_season = res.data.this_season;
    });
  },
  methods: {
    avatar_operation() {
      common_vendor.wx$1.showActionSheet({
        itemList: ["查看头像", "更换头像"],
        success: (res) => {
          if (!res.cancel) {
            if (res.tapIndex == 0) {
              let avatarUrl = this.user.profile_img;
              if (avatarUrl) {
                common_vendor.wx$1.previewImage({
                  urls: [avatarUrl],
                  current: avatarUrl
                });
              } else {
                common_vendor.wx$1.showToast({
                  title: "您还未上传头像",
                  icon: "none",
                  duration: 1e3
                });
                return;
              }
            } else if (res.tapIndex == 1) {
              common_vendor.wx$1.showToast({
                title: "请联系TJTT工作室成员",
                icon: "none",
                duration: 1e3
              });
              return;
            }
          }
        }
      });
    },
    image_operation(image_url) {
      common_vendor.wx$1.previewImage({
        urls: [image_url],
        current: image_url
      });
    },
    modify_info() {
      common_vendor.index.navigateTo({
        url: "/pages/my/modify-info"
      });
    },
    modify_psw() {
      common_vendor.index.navigateTo({
        url: "/pages/my/modify-psw"
      });
    },
    match_detail_page(match_id) {
      if (this.hide_this) {
        return;
      }
      common_vendor.index.setStorageSync("match_id", match_id);
      common_vendor.index.navigateTo({
        url: "/page_subjec/match/detail"
      });
    },
    set_private() {
      common_vendor.wx$1.showModal({
        title: "设为私密用户",
        content: "设为私密用户后，您在“积分排名”中将以“" + this.user.username[0] + "** ”显示。",
        success: (res) => {
          if (res.confirm) {
            let data = {
              "my_id": this.user.id,
              "user_id": "",
              "set": "private"
            };
            static_js_ajax_request.fetch_data("POST", "set_privacy", data, "user", (res2) => {
              common_vendor.wx$1.showToast({
                title: res2.data.message,
                icon: "none",
                duration: 1e3
              });
              if (res2.data.status == 200) {
                static_js_ajax_request.fetch_data("POST", "refresh", { "my_id": this.user.id }, "user", (res3) => {
                  common_vendor.index.setStorageSync("user", res3.data.user);
                });
                this.user = res2.data.user;
                setTimeout(() => {
                  common_vendor.index.reLaunch({
                    url: "/pages/my/index"
                  });
                }, 1e3);
              }
            });
          }
        }
      });
    },
    set_public() {
      common_vendor.wx$1.showModal({
        title: "设为公开用户",
        content: "设为公开用户后，您在“积分排名”中将以全名显示。",
        success: (res) => {
          if (res.confirm) {
            let data = {
              "my_id": this.user.id,
              "user_id": "",
              "set": "public"
            };
            static_js_ajax_request.fetch_data("POST", "set_privacy", data, "user", (res2) => {
              common_vendor.wx$1.showToast({
                title: res2.data.message,
                icon: "none",
                duration: 1e3
              });
              if (res2.data.status == 200) {
                static_js_ajax_request.fetch_data("POST", "refresh", { "my_id": this.user.id }, "user", (res3) => {
                  common_vendor.index.setStorageSync("user", res3.data.user);
                });
                this.user = res2.data.user;
                setTimeout(() => {
                  common_vendor.index.reLaunch({
                    url: "/pages/my/index"
                  });
                }, 1e3);
              }
            });
          }
        }
      });
    },
    wx_bind() {
      common_vendor.index.navigateTo({
        url: "/pages/login/wx-bind"
      });
    },
    management_page() {
      common_vendor.index.navigateTo({
        url: "/pages/management/index"
      });
    },
    logout() {
      common_vendor.index.clearStorageSync();
      common_vendor.index.reLaunch({
        url: "/pages/my/index"
      });
      console.log("已退出登录");
    },
    login_page() {
      common_vendor.index.navigateTo({
        url: "/pages/login/login"
      });
    },
    register_page() {
      common_vendor.index.navigateTo({
        url: "/pages/login/register"
      });
    }
  },
  onPullDownRefresh() {
    if (this.user) {
      let data = { "my_id": this.user.id };
      static_js_ajax_request.fetch_data("POST", "refresh", data, "user", (res) => {
        var user_id = this.user.id;
        function asyncTask(callback) {
          static_js_utils.get_my_rank(user_id);
          callback();
        }
        asyncTask(() => {
          console.log("async task finished");
        });
        common_vendor.index.setStorageSync("user", res.data.user);
      });
    }
    common_vendor.index.reLaunch({
      url: "/pages/my/index"
    });
    setTimeout(() => {
      common_vendor.index.stopPullDownRefresh();
    }, 1e3);
  }
};
const _sfc_main = /* @__PURE__ */ Object.assign(__default__, {
  __name: "index",
  setup(__props) {
    let userListA = common_vendor.ref([
      {
        name: "当前赛事",
        content: 4
      },
      {
        name: "已报名赛事",
        content: 6
      },
      {
        name: "历史赛事",
        content: 5
      },
      {
        name: "全部赛事",
        content: 7
      }
    ]);
    const goAdd = () => {
      common_vendor.index.navigateTo({
        url: "/page_subjec/match/index?id="
      });
    };
    const rank = () => {
      common_vendor.index.reLaunch({
        url: "/pages/score-ranking/index?id="
      });
    };
    return (_ctx, _cache) => {
      return common_vendor.e({
        a: _ctx.user
      }, _ctx.user ? common_vendor.e({
        b: common_vendor.o((...args) => _ctx.logout && _ctx.logout(...args)),
        c: _ctx.user.profile_img
      }, _ctx.user.profile_img ? {
        d: _ctx.user.profile_img
      } : _ctx.user.gender == "男" ? {} : _ctx.user.gender == "女" ? {} : {}, {
        e: _ctx.user.gender == "男",
        f: _ctx.user.gender == "女",
        g: common_vendor.o((...args) => _ctx.avatar_operation && _ctx.avatar_operation(...args)),
        h: common_vendor.t(_ctx.user.username),
        i: common_vendor.t(_ctx.user.school),
        j: _ctx.user.organ
      }, _ctx.user.organ ? {
        k: common_vendor.t(_ctx.user.organ.organname)
      } : {}, {
        l: _ctx.user.hand
      }, _ctx.user.hand ? {
        m: common_vendor.t(_ctx.user.hand)
      } : {
        n: common_vendor.o((...args) => _ctx.modify_info && _ctx.modify_info(...args))
      }, {
        o: _ctx.user.grip
      }, _ctx.user.grip ? {
        p: common_vendor.t(_ctx.user.grip)
      } : {
        q: common_vendor.o((...args) => _ctx.modify_info && _ctx.modify_info(...args))
      }, {
        r: _ctx.user.particle
      }, _ctx.user.particle ? {
        s: common_vendor.t(_ctx.user.particle)
      } : {
        t: common_vendor.o((...args) => _ctx.modify_info && _ctx.modify_info(...args))
      }, {
        v: _ctx.user.address
      }, _ctx.user.address ? {
        w: common_vendor.t(_ctx.user.address)
      } : {
        x: common_vendor.o((...args) => _ctx.modify_info && _ctx.modify_info(...args))
      }, {
        y: common_vendor.p({
          name: "arrow-right",
          color: "#212121",
          size: "28"
        }),
        z: common_vendor.t(_ctx.user.score),
        A: common_vendor.t(_ctx.my_rank),
        B: common_vendor.o(rank),
        C: _ctx.this_season.badge_url,
        D: common_vendor.o(($event) => _ctx.image_operation(_ctx.this_season.badge_url)),
        E: common_vendor.t(_ctx.this_season.season_name),
        F: common_vendor.t(_ctx.user.active),
        G: common_vendor.f(common_vendor.unref(userListA), (item, i, i0) => {
          return {
            a: `../../static/tabbar/Frame (${item.content}).png`,
            b: common_vendor.t(item.name),
            c: common_vendor.o(goAdd, i),
            d: i
          };
        }),
        H: _ctx.latest_match
      }, _ctx.latest_match ? {
        I: common_vendor.t(_ctx.latest_match.title),
        J: common_vendor.t(static_js_utils.format_time(_ctx.latest_match.match_time)),
        K: common_vendor.t(_ctx.latest_match.place),
        L: common_vendor.o(($event) => _ctx.match_detail_page(_ctx.latest_match.id))
      } : {}, {
        M: !_ctx.hide_this
      }, !_ctx.hide_this ? common_vendor.e({
        N: common_vendor.f(_ctx.actionList, (item, index, i0) => {
          return common_vendor.e({
            a: index == 0
          }, index == 0 ? {
            b: "f97bc692-1-" + i0,
            c: common_vendor.p({
              name: "setting-fill",
              size: "40"
            }),
            d: common_vendor.t(item.name),
            e: common_vendor.o((...args) => _ctx.modify_info && _ctx.modify_info(...args), index)
          } : index == 1 ? {
            g: "f97bc692-2-" + i0,
            h: common_vendor.p({
              name: "lock-fill",
              size: "40"
            }),
            i: common_vendor.t(item.name),
            j: common_vendor.o((...args) => _ctx.modify_psw && _ctx.modify_psw(...args), index)
          } : index == 2 ? common_vendor.e({
            l: _ctx.user.privacy == 0
          }, _ctx.user.privacy == 0 ? {
            m: "f97bc692-3-" + i0,
            n: common_vendor.p({
              name: "account-fill",
              size: "40"
            }),
            o: common_vendor.t(item.name),
            p: common_vendor.o((...args) => _ctx.set_private && _ctx.set_private(...args), index)
          } : {
            q: "f97bc692-4-" + i0,
            r: common_vendor.p({
              name: "account",
              size: "40"
            }),
            s: common_vendor.o((...args) => _ctx.set_public && _ctx.set_public(...args), index)
          }) : {}, {
            f: index == 1,
            k: index == 2,
            t: index
          });
        }),
        O: _ctx.user.usertype == "K9" || _ctx.user.usertype == "K10" || _ctx.user.usertype == "K11"
      }, _ctx.user.usertype == "K9" || _ctx.user.usertype == "K10" || _ctx.user.usertype == "K11" ? {
        P: common_vendor.p({
          name: "integral-fill",
          size: "40"
        }),
        Q: common_vendor.o((...args) => _ctx.management_page && _ctx.management_page(...args))
      } : {
        R: common_vendor.p({
          name: "weixin-fill",
          size: "40"
        }),
        S: common_vendor.o((...args) => _ctx.wx_bind && _ctx.wx_bind(...args))
      }) : {}, {
        T: common_vendor.t(_ctx.user.gender),
        U: common_vendor.t(_ctx.user.address),
        V: common_vendor.t(_ctx.user.phone),
        W: common_vendor.t(_ctx.user.email),
        X: common_vendor.t(_ctx.user.school),
        Y: common_vendor.t(_ctx.user.role),
        Z: common_vendor.t(_ctx.user.stu_num),
        aa: _ctx.user.organ
      }, _ctx.user.organ ? {
        ab: common_vendor.t(_ctx.user.organ.organname)
      } : {}, {
        ac: common_vendor.t(_ctx.user.hand),
        ad: common_vendor.t(_ctx.user.grip),
        ae: common_vendor.t(_ctx.user.blade),
        af: common_vendor.t(_ctx.user.forehand),
        ag: common_vendor.t(_ctx.user.backhand),
        ah: common_vendor.t(_ctx.user.particle),
        ai: _ctx.user.privacy == 1
      }, _ctx.user.privacy == 1 ? {} : {}, {
        aj: common_vendor.p({
          stripe: true,
          emptyText: "无数据"
        }),
        ak: common_vendor.p({
          ["current-page"]: 4
        })
      }) : common_vendor.e({
        al: common_vendor.o((...args) => _ctx.login_page && _ctx.login_page(...args)),
        am: !_ctx.hide_this
      }, !_ctx.hide_this ? {
        an: common_vendor.o((...args) => _ctx.register_page && _ctx.register_page(...args))
      } : {}, {
        ao: common_vendor.p({
          ["current-page"]: 4
        })
      }));
    };
  }
});
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["__scopeId", "data-v-f97bc692"]]);
wx.createPage(MiniProgramPage);
