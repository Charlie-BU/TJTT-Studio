"use strict";
const common_vendor = require("../../common/vendor.js");
const static_js_utils = require("../../static/js/utils.js");
const static_js_ajax_request = require("../../static/js/ajax_request.js");
const static_js_login_check = require("../../static/js/login_check.js");
const static_js_magic_power = require("../../static/js/magic_power.js");
if (!Array) {
  const _easycom_u_tabs2 = common_vendor.resolveComponent("u-tabs");
  _easycom_u_tabs2();
}
const _easycom_u_tabs = () => "../../uni_modules/vk-uview-ui/components/u-tabs/u-tabs.js";
if (!Math) {
  _easycom_u_tabs();
}
const __default__ = {
  data() {
    return {
      user: "",
      user_length: "",
      student_length: "",
      teacher_length: "",
      admin_length: "",
      items: [],
      agenda_list: [
        {
          name: "待回答问题"
        },
        {
          name: "隐藏通知"
        },
        {
          name: "隐藏赛事"
        }
      ],
      current: 0,
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
    static_js_ajax_request.fetch_data("POST", "get_unanswered_Qs", null, "application", (res) => {
      this.items = res.data.unanswered_Qs;
      common_vendor.wx$1.hideToast();
    });
  },
  methods: {
    change(index) {
      this.current = index;
      if (index == 0) {
        common_vendor.wx$1.showToast({
          title: "加载中",
          icon: "loading",
          duration: 1e5
        });
        static_js_ajax_request.fetch_data("POST", "get_unanswered_Qs", null, "application", (res) => {
          this.items = res.data.unanswered_Qs;
          common_vendor.wx$1.hideToast();
        });
      } else if (index == 1) {
        common_vendor.wx$1.showToast({
          title: "加载中",
          icon: "loading",
          duration: 1e5
        });
        static_js_ajax_request.fetch_data("POST", "get_hidden_notices", null, "application", (res) => {
          this.items = res.data.hidden_notices;
          common_vendor.wx$1.hideToast();
        });
      } else if (index == 2) {
        common_vendor.wx$1.showToast({
          title: "加载中",
          icon: "loading",
          duration: 1e5
        });
        static_js_ajax_request.fetch_data("POST", "get_hidden_matches", null, "application", (res) => {
          this.items = res.data.hidden_matches;
          common_vendor.wx$1.hideToast();
        });
      }
    },
    answer(question) {
      common_vendor.wx$1.showModal({
        title: question.question,
        placeholderText: "请输入回答",
        editable: true,
        success: (res) => {
          if (res.confirm) {
            let data = {
              "my_id": this.user.id,
              "question_id": question.id,
              "answer": res.content
            };
            static_js_ajax_request.fetch_data("POST", "answer_question", data, "application", (res2) => {
              common_vendor.wx$1.showToast({
                title: res2.data.message,
                icon: "none",
                duration: 1500
              });
              static_js_ajax_request.fetch_data("POST", "get_unanswered_Qs", null, "application", (res3) => {
                this.items = res3.data.unanswered_Qs;
              });
            });
          }
        }
      });
    },
    delete_question(question_id) {
      common_vendor.wx$1.showModal({
        title: "删除问题",
        content: "确定删除该问题？",
        success: (res) => {
          if (res.confirm) {
            let data = {
              "my_id": this.user.id,
              "QA_id": question_id
            };
            static_js_ajax_request.fetch_data("POST", "delete_QA", data, "user", (res2) => {
              common_vendor.wx$1.showToast({
                title: res2.data.message,
                icon: "none",
                duration: 1e3
              });
              if (res2.data.status == 200) {
                static_js_ajax_request.fetch_data("POST", "get_unanswered_Qs", null, "application", (res3) => {
                  this.items = res3.data.unanswered_Qs;
                });
              }
            });
          }
        }
      });
    },
    unhide_notice(notice_id) {
      common_vendor.wx$1.showModal({
        title: "取消隐藏",
        content: "确定取消隐藏该通知公告？",
        success: (res) => {
          if (res.confirm) {
            let data = {
              "my_id": this.user.id,
              "notice_id": notice_id
            };
            static_js_ajax_request.fetch_data("POST", "unhide_notice", data, "application", (res2) => {
              common_vendor.wx$1.showToast({
                title: res2.data.message,
                icon: "none",
                duration: 1e3
              });
              if (res2.data.status == 200) {
                static_js_ajax_request.fetch_data("POST", "get_hidden_notices", null, "application", (res3) => {
                  this.items = res3.data.hidden_notices;
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
        content: "确定删除该通知公告？",
        success: (res) => {
          if (res.confirm) {
            let data = {
              "my_id": this.user.id,
              "notice_id": notice_id
            };
            static_js_ajax_request.fetch_data("POST", "delete_notice", data, "application", (res2) => {
              common_vendor.wx$1.showToast({
                title: res2.data.message,
                icon: "none",
                duration: 1e3
              });
              if (res2.data.status == 200) {
                static_js_ajax_request.fetch_data("POST", "get_hidden_notices", null, "application", (res3) => {
                  this.items = res3.data.hidden_notices;
                });
              }
            });
          }
        }
      });
    },
    unhide_match(match_id) {
      common_vendor.wx$1.showModal({
        title: "取消隐藏",
        content: "确定取消隐藏该赛事？",
        success: (res) => {
          if (res.confirm) {
            let data = {
              "my_id": this.user.id,
              "match_id": match_id
            };
            static_js_ajax_request.fetch_data("POST", "unhide_match", data, "competition", (res2) => {
              common_vendor.wx$1.showToast({
                title: res2.data.message,
                icon: "none",
                duration: 1e3
              });
              if (res2.data.status == 200) {
                static_js_ajax_request.fetch_data("POST", "get_hidden_matches", null, "application", (res3) => {
                  this.items = res3.data.hidden_matches;
                });
              }
            });
          }
        }
      });
    },
    delete_match(match_id) {
      common_vendor.wx$1.showModal({
        title: "删除赛事",
        content: "删除赛事后，选手信息、赛事成绩等将一并删除。确认删除该赛事？",
        success: (res) => {
          if (res.confirm) {
            let data = {
              "my_id": this.user.id,
              "match_id": match_id
            };
            static_js_ajax_request.fetch_data("POST", "delete_match", data, "competition", (res2) => {
              common_vendor.wx$1.showToast({
                title: res2.data.message,
                icon: "none",
                duration: 1e3
              });
              if (res2.data.status == 200) {
                static_js_ajax_request.fetch_data("POST", "get_hidden_matches", null, "application", (res3) => {
                  this.items = res3.data.hidden_matches;
                });
              }
            });
          }
        }
      });
    }
  }
};
const _sfc_main = /* @__PURE__ */ Object.assign(__default__, {
  __name: "index",
  setup(__props) {
    return (_ctx, _cache) => {
      return common_vendor.e({
        a: !_ctx.hide_this
      }, !_ctx.hide_this ? {
        b: common_vendor.t(_ctx.user_length),
        c: common_vendor.t(_ctx.student_length),
        d: common_vendor.t(_ctx.teacher_length),
        e: common_vendor.t(_ctx.admin_length),
        f: common_vendor.o(_ctx.change),
        g: common_vendor.p({
          list: _ctx.agenda_list,
          ["bg-color"]: "#ffffff",
          ["active-color"]: "#F25C07",
          f: true,
          ["font-size"]: "20rpx",
          ["is-scroll"]: "true",
          current: _ctx.current
        }),
        h: common_vendor.f(_ctx.items, (item, index, i0) => {
          return common_vendor.e(_ctx.current == 0 ? {
            a: common_vendor.t(index + 1),
            b: common_vendor.t(item.question),
            c: common_vendor.t(item.person_name),
            d: common_vendor.o(($event) => _ctx.answer(item), index),
            e: common_vendor.o(($event) => _ctx.delete_question(item.id), index)
          } : _ctx.current == 1 ? {
            f: common_vendor.t(index + 1),
            g: common_vendor.t(item.title),
            h: common_vendor.t(item.content),
            i: common_vendor.t(item.announcer_name),
            j: common_vendor.o(($event) => _ctx.unhide_notice(item.id), index),
            k: common_vendor.o(($event) => _ctx.delete_notice(item.id), index)
          } : _ctx.current == 2 ? {
            l: common_vendor.t(index + 1),
            m: common_vendor.t(item.title),
            n: common_vendor.t(item.place),
            o: common_vendor.t(static_js_utils.format_time(item.match_time)),
            p: common_vendor.o(($event) => _ctx.unhide_match(item.id), index),
            q: common_vendor.o(($event) => _ctx.delete_match(item.id), index)
          } : {}, {
            r: index
          });
        }),
        i: _ctx.current == 0,
        j: _ctx.current == 1,
        k: _ctx.current == 2
      } : {});
    };
  }
});
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["__scopeId", "data-v-ccc94b5b"]]);
wx.createPage(MiniProgramPage);
