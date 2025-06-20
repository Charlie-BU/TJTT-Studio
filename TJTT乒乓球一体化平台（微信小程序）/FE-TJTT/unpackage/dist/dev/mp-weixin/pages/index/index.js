"use strict";
const common_vendor = require("../../common/vendor.js");
const static_js_ajax_request = require("../../static/js/ajax_request.js");
const static_js_utils = require("../../static/js/utils.js");
const static_js_magic_power = require("../../static/js/magic_power.js");
if (!Array) {
  const _easycom_u_tabs2 = common_vendor.resolveComponent("u-tabs");
  const _component_tabbar = common_vendor.resolveComponent("tabbar");
  (_easycom_u_tabs2 + _component_tabbar)();
}
const _easycom_u_tabs = () => "../../uni_modules/vk-uview-ui/components/u-tabs/u-tabs.js";
if (!Math) {
  (Nav + _easycom_u_tabs)();
}
const Nav = () => "./components/index.js";
const __default__ = {
  data() {
    return {
      user_id: "",
      username: "",
      usertype: "",
      random_motto: "",
      display_content: [],
      select_list: [
        {
          name: "通知公告"
        },
        {
          name: "Q & A"
        }
      ],
      current: 0,
      hide_this: static_js_magic_power.magic()
    };
  },
  onLoad() {
    common_vendor.index.removeStorageSync("user_id");
    common_vendor.index.removeStorageSync("match_id");
    const user_token = common_vendor.index.getStorageSync("user_token");
    const decoded_user_token = static_js_utils.decode(user_token);
    const regex = /^(\d+)=/;
    const match = decoded_user_token.match(regex);
    const user_id = match ? match[1] : null;
    this.user_id = +user_id;
    if (this.user_id) {
      static_js_ajax_request.fetch_data("POST", "get_index_info", { "user_id": this.user_id }, "user", (res) => {
        this.username = res.data.username;
        this.usertype = res.data.usertype;
      });
    }
    static_js_ajax_request.fetch_data("POST", "get_random_motto", null, "application", (res) => {
      this.random_motto = res.data.random_motto;
    });
    static_js_ajax_request.fetch_data("POST", "get_notice", null, "application", (res) => {
      this.display_content = res.data.notices;
    });
  },
  methods: {
    all_matches() {
      common_vendor.index.navigateTo({
        url: "/page_subjec/match/index"
      });
    },
    img_show() {
      let img_url = "https://tjtt-assets.oss-cn-shanghai.aliyuncs.com/pictures/decorations/studio-intro.png";
      common_vendor.wx$1.previewImage({
        urls: [img_url],
        current: img_url
      });
    },
    enter_ranking() {
      common_vendor.index.switchTab({
        url: "/pages/score-ranking/index"
      });
    },
    enter_community() {
      common_vendor.index.switchTab({
        url: "/pages/community/index"
      });
    },
    change(index) {
      this.current = index;
      if (index == 0) {
        static_js_ajax_request.fetch_data("POST", "get_notice", null, "application", (res) => {
          this.display_content = res.data.notices;
        });
      } else if (index == 1) {
        static_js_ajax_request.fetch_data("POST", "get_QAs", null, "application", (res) => {
          this.display_content = res.data.QAs;
        });
      }
    },
    issue_notice() {
      common_vendor.index.navigateTo({
        url: "/pages/index/issue-notice"
      });
    },
    hide_notice(notice_id) {
      common_vendor.wx$1.showModal({
        title: "隐藏通知公告",
        content: "确定隐藏该通知公告？",
        success: (res) => {
          if (res.confirm) {
            let data = {
              "my_id": this.user_id,
              "notice_id": notice_id
            };
            static_js_ajax_request.fetch_data("POST", "hide_notice", data, "application", (res2) => {
              common_vendor.wx$1.showToast({
                title: res2.data.message,
                icon: "none",
                duration: 1e3
              });
              if (res2.data.status == 200) {
                static_js_ajax_request.fetch_data("POST", "get_notice", null, "application", (res3) => {
                  this.display_content = res3.data.notices;
                });
              }
            });
          }
        }
      });
    },
    delete_notice(notice_id) {
      common_vendor.wx$1.showModal({
        title: "删除通知公告",
        content: "确定删除该通知公告",
        success: (res) => {
          if (res.confirm) {
            let data = {
              "my_id": this.user_id,
              "notice_id": notice_id
            };
            static_js_ajax_request.fetch_data("POST", "delete_notice", data, "application", (res2) => {
              common_vendor.wx$1.showToast({
                title: res2.data.message,
                icon: "none",
                duration: 1e3
              });
              if (res2.data.status == 200) {
                static_js_ajax_request.fetch_data("POST", "get_notice", null, "application", (res3) => {
                  this.display_content = res3.data.notices;
                });
              }
            });
          }
        }
      });
    },
    ask() {
      if (!this.user_id) {
        common_vendor.wx$1.showToast({
          title: "请登录",
          icon: "none",
          duration: 1500
        });
        setTimeout(() => {
          common_vendor.index.navigateTo({
            url: "/pages/login/login"
          });
        }, 1e3);
      } else {
        common_vendor.wx$1.showModal({
          title: "提问",
          placeholderText: "任何乒乓球相关问题",
          editable: true,
          confirmText: "提问",
          success: (res) => {
            if (res.confirm) {
              let data = {
                "my_id": this.user_id,
                "question": res.content
              };
              static_js_ajax_request.fetch_data("POST", "ask_question", data, "application", (res2) => {
                common_vendor.wx$1.showToast({
                  title: res2.data.message,
                  icon: "none",
                  duration: 1500
                });
              });
            }
          }
        });
      }
    },
    modify_QA(QA) {
      common_vendor.wx$1.showModal({
        title: QA.question,
        content: QA.answer,
        editable: true,
        confirmText: "修改",
        success: (res) => {
          if (res.confirm) {
            let data = {
              "my_id": this.user_id,
              "QA_id": QA.id,
              "answer": res.content
            };
            static_js_ajax_request.fetch_data("POST", "modify_QA", data, "application", (res2) => {
              common_vendor.wx$1.showToast({
                title: res2.data.message,
                icon: "none",
                duration: 1e3
              });
              if (res2.data.status == 200) {
                static_js_ajax_request.fetch_data("POST", "get_QAs", null, "application", (res3) => {
                  this.display_content = res3.data.QAs;
                });
              }
            });
          }
        }
      });
    },
    delete_QA(QA_id) {
      common_vendor.wx$1.showModal({
        title: "删除问题回答",
        content: "确定删除该问题与回答",
        success: (res) => {
          if (res.confirm) {
            let data = {
              "my_id": this.user_id,
              "QA_id": QA_id
            };
            static_js_ajax_request.fetch_data("POST", "delete_QA", data, "application", (res2) => {
              common_vendor.wx$1.showToast({
                title: res2.data.message,
                icon: "none",
                duration: 1e3
              });
              if (res2.data.status == 200) {
                static_js_ajax_request.fetch_data("POST", "get_QAs", null, "application", (res3) => {
                  this.display_content = res3.data.QAs;
                });
              }
            });
          }
        }
      });
    }
  },
  onPullDownRefresh() {
    if (this.user_id) {
      let data = {
        "my_id": this.user_id
      };
      static_js_ajax_request.fetch_data("POST", "refresh", data, "user", (res) => {
        var user_id = this.user_id;
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
      url: "/pages/index/index"
    });
    setTimeout(() => {
      common_vendor.index.stopPullDownRefresh();
    }, 1e3);
  }
};
const _sfc_main = /* @__PURE__ */ Object.assign(__default__, {
  __name: "index",
  setup(__props) {
    return (_ctx, _cache) => {
      return common_vendor.e({
        a: _ctx.hide_this
      }, _ctx.hide_this ? {} : {}, {
        b: _ctx.username
      }, _ctx.username ? {
        c: common_vendor.t(_ctx.username)
      } : {}, {
        d: common_vendor.t(_ctx.random_motto.content),
        e: common_vendor.t(_ctx.random_motto.author),
        f: common_vendor.o((...args) => _ctx.img_show && _ctx.img_show(...args)),
        g: common_vendor.o((...args) => _ctx.all_matches && _ctx.all_matches(...args)),
        h: common_vendor.o((...args) => _ctx.enter_ranking && _ctx.enter_ranking(...args)),
        i: common_vendor.o((...args) => _ctx.enter_community && _ctx.enter_community(...args)),
        j: common_vendor.o(_ctx.change),
        k: common_vendor.p({
          list: _ctx.select_list,
          ["active-color"]: "#F25C07",
          ["is-scroll"]: true,
          current: _ctx.current
        }),
        l: (_ctx.usertype == "K9" || _ctx.usertype == "K10" || _ctx.usertype == "K11") && _ctx.current == 0 && !_ctx.hide_this
      }, (_ctx.usertype == "K9" || _ctx.usertype == "K10" || _ctx.usertype == "K11") && _ctx.current == 0 && !_ctx.hide_this ? {
        m: common_vendor.o((...args) => _ctx.issue_notice && _ctx.issue_notice(...args))
      } : {}, {
        n: _ctx.current == 1 && !_ctx.hide_this
      }, _ctx.current == 1 && !_ctx.hide_this ? {
        o: common_vendor.o((...args) => _ctx.ask && _ctx.ask(...args))
      } : {}, {
        p: !_ctx.hide_this
      }, !_ctx.hide_this ? common_vendor.e({
        q: _ctx.current == 0
      }, _ctx.current == 0 ? {
        r: common_vendor.f(_ctx.display_content, (notice, index, i0) => {
          return common_vendor.e({
            a: common_vendor.t(notice.title),
            b: common_vendor.t(notice.content),
            c: common_vendor.t(static_js_utils.format_time(notice.time)),
            d: common_vendor.t(notice.announcer_name)
          }, _ctx.usertype == "K9" || _ctx.usertype == "K10" || _ctx.usertype == "K11" ? {} : {}, _ctx.usertype == "K9" || _ctx.usertype == "K10" || _ctx.usertype == "K11" ? {
            e: common_vendor.o(($event) => _ctx.hide_notice(notice.id), index),
            f: common_vendor.o(($event) => _ctx.delete_notice(notice.id), index)
          } : {}, {
            g: index
          });
        }),
        s: _ctx.usertype == "K9" || _ctx.usertype == "K10" || _ctx.usertype == "K11",
        t: _ctx.usertype == "K9" || _ctx.usertype == "K10" || _ctx.usertype == "K11"
      } : _ctx.current == 1 ? {
        w: common_vendor.f(_ctx.display_content, (QA, index, i0) => {
          return common_vendor.e({
            a: common_vendor.t(QA.question),
            b: common_vendor.t(QA.answer)
          }, _ctx.usertype == "K9" || _ctx.usertype == "K10" || _ctx.usertype == "K11" ? {} : {}, _ctx.usertype == "K9" || _ctx.usertype == "K10" || _ctx.usertype == "K11" ? {
            c: common_vendor.o(($event) => _ctx.modify_QA(QA), index),
            d: common_vendor.o(($event) => _ctx.delete_QA(QA.id), index)
          } : {}, {
            e: index
          });
        }),
        x: _ctx.usertype == "K9" || _ctx.usertype == "K10" || _ctx.usertype == "K11",
        y: _ctx.usertype == "K9" || _ctx.usertype == "K10" || _ctx.usertype == "K11"
      } : {}, {
        v: _ctx.current == 1
      }) : {}, {
        z: common_vendor.p({
          ["current-page"]: 0
        })
      });
    };
  }
});
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["__scopeId", "data-v-1cf27b2a"]]);
wx.createPage(MiniProgramPage);
