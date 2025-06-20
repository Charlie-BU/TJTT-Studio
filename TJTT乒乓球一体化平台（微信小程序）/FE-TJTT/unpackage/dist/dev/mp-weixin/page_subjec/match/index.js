"use strict";
const common_vendor = require("../../common/vendor.js");
const static_js_utils = require("../../static/js/utils.js");
const static_js_ajax_request = require("../../static/js/ajax_request.js");
const static_js_login_check = require("../../static/js/login_check.js");
const static_js_magic_power = require("../../static/js/magic_power.js");
if (!Array) {
  const _easycom_u_tabs2 = common_vendor.resolveComponent("u-tabs");
  const _easycom_u_search2 = common_vendor.resolveComponent("u-search");
  (_easycom_u_tabs2 + _easycom_u_search2)();
}
const _easycom_u_tabs = () => "../../uni_modules/vk-uview-ui/components/u-tabs/u-tabs.js";
const _easycom_u_search = () => "../../uni_modules/vk-uview-ui/components/u-search/u-search.js";
if (!Math) {
  (_easycom_u_tabs + _easycom_u_search)();
}
const __default__ = {
  data() {
    return {
      user: "",
      message: "",
      search_match: "",
      matches: [],
      match_list: [
        {
          name: "当前赛事"
        },
        {
          name: "已报名赛事"
        },
        {
          name: "历史赛事"
        },
        {
          name: "全部赛事"
        }
      ],
      current: 0,
      hide_this: static_js_magic_power.magic()
    };
  },
  onLoad() {
    common_vendor.index.removeStorageSync("user_id");
    common_vendor.index.removeStorageSync("match_id");
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
    static_js_ajax_request.fetch_data("POST", "match_list_current", null, "competition", (res) => {
      this.message = res.data.message;
      this.matches = res.data.matches;
      common_vendor.wx$1.hideToast();
    });
  },
  methods: {
    onInput(e) {
      this.search_match = e.target.value;
    },
    back() {
      common_vendor.index.navigateBack({
        delta: 1
      });
    },
    search() {
      this.current = 3;
      common_vendor.wx$1.showToast({
        title: "加载中",
        icon: "loading",
        duration: 1e5
      });
      let data = { "search_match": this.search_match };
      static_js_ajax_request.fetch_data("POST", "findMatchByName", data, "competition", (res) => {
        this.matches = res.data.matches;
        common_vendor.wx$1.hideToast();
      });
    },
    change(index) {
      this.current = index;
      if (index == 0) {
        common_vendor.wx$1.showToast({
          title: "加载中",
          icon: "loading",
          duration: 1e5
        });
        static_js_ajax_request.fetch_data("POST", "match_list_current", null, "competition", (res) => {
          this.matches = res.data.matches;
          common_vendor.wx$1.hideToast();
        });
      } else if (index == 1) {
        common_vendor.wx$1.showToast({
          title: "加载中",
          icon: "loading",
          duration: 1e5
        });
        static_js_ajax_request.fetch_data("POST", "match_list_signed", { "my_id": this.user.id }, "competition", (res) => {
          this.matches = res.data.matches;
          common_vendor.wx$1.hideToast();
        });
      } else if (index == 2) {
        common_vendor.wx$1.showToast({
          title: "加载中",
          icon: "loading",
          duration: 1e5
        });
        static_js_ajax_request.fetch_data("POST", "match_list_history", null, "competition", (res) => {
          this.matches = res.data.matches;
          common_vendor.wx$1.hideToast();
        });
      } else if (index == 3) {
        common_vendor.wx$1.showToast({
          title: "加载中",
          icon: "loading",
          duration: 1e5
        });
        static_js_ajax_request.fetch_data("POST", "match_list_all", null, "competition", (res) => {
          this.matches = res.data.matches;
          common_vendor.wx$1.hideToast();
        });
      }
    },
    sign_up_page(match_id) {
      common_vendor.index.setStorageSync("match_id", match_id);
      common_vendor.index.navigateTo({
        url: "/page_subjec/match/sign_up"
      });
    },
    quit(match_id) {
      common_vendor.wx$1.showModal({
        title: "取消报名",
        content: "确认放弃参加该赛事？",
        success: (res) => {
          if (res.confirm) {
            let data = {
              "my_id": this.user.id,
              "match_id": match_id
            };
            static_js_ajax_request.fetch_data("POST", "quit_match", data, "competition", (res2) => {
              common_vendor.wx$1.showToast({
                title: res2.data.message,
                icon: "none",
                duration: 1e3
              });
              if (res2.data.status == 200) {
                setTimeout(() => {
                  common_vendor.index.reLaunch({
                    url: "/page_subjec/match/index"
                  });
                }, 1e3);
              }
            });
          }
        }
      });
    },
    hide_match(match_id) {
      common_vendor.wx$1.showModal({
        title: "隐藏赛事",
        content: "确定隐藏该赛事？",
        success: (res) => {
          if (res.confirm) {
            let data = {
              "my_id": this.user.id,
              "match_id": match_id
            };
            static_js_ajax_request.fetch_data("POST", "hide_match", data, "competition", (res2) => {
              common_vendor.wx$1.showToast({
                title: res2.data.message,
                icon: "none",
                duration: 1e3
              });
              if (res2.data.status == 200) {
                this.current = 0;
                static_js_ajax_request.fetch_data("POST", "match_list_current", null, "competition", (res3) => {
                  this.matches = res3.data.matches;
                });
              }
            });
          }
        }
      });
    },
    match_detail_page(match_id) {
      common_vendor.index.setStorageSync("match_id", match_id);
      common_vendor.index.navigateTo({
        url: "/page_subjec/match/detail"
      });
    }
  }
};
const _sfc_main = /* @__PURE__ */ Object.assign(__default__, {
  __name: "index",
  setup(__props) {
    return (_ctx, _cache) => {
      return common_vendor.e({
        a: common_vendor.o(_ctx.change),
        b: common_vendor.p({
          list: _ctx.match_list,
          ["bg-color"]: "null",
          ["active-color"]: "#F25C07",
          ["font-size"]: "20rpx",
          ["is-scroll"]: "true",
          current: _ctx.current
        }),
        c: common_vendor.o(($event) => _ctx.search_match = $event),
        d: common_vendor.p({
          ["bg-color"]: "#ffffff",
          ["show-action"]: false,
          placeholder: "输入赛事名称",
          modelValue: _ctx.search_match
        }),
        e: common_vendor.o((...args) => _ctx.search && _ctx.search(...args)),
        f: _ctx.matches.length != 0
      }, _ctx.matches.length != 0 ? {
        g: common_vendor.f(_ctx.matches, (match, index, i0) => {
          return common_vendor.e({
            a: common_vendor.t(index + 1),
            b: common_vendor.t(match.match_type),
            c: common_vendor.t(match.title),
            d: common_vendor.t(static_js_utils.format_time(match.match_time)),
            e: common_vendor.t(match.place),
            f: common_vendor.t(match.restriction),
            g: common_vendor.t(match.description),
            h: isNaN(match.participant - match.players_length)
          }, isNaN(match.participant - match.players_length) ? {} : {
            i: common_vendor.t(match.participant - match.players_length)
          }, !_ctx.hide_this ? common_vendor.e({
            j: (_ctx.user.usertype == "K9" || _ctx.user.usertype == "K10" || _ctx.user.usertype == "K11") && match.players_id.includes(_ctx.user.id)
          }, (_ctx.user.usertype == "K9" || _ctx.user.usertype == "K10" || _ctx.user.usertype == "K11") && match.players_id.includes(_ctx.user.id) ? {
            k: common_vendor.o(($event) => _ctx.hide_match(match.id), index)
          } : (_ctx.user.usertype == "K9" || _ctx.user.usertype == "K10" || _ctx.user.usertype == "K11") && !match.players_id.includes(_ctx.user.id) ? {
            m: common_vendor.o(($event) => _ctx.hide_match(match.id), index)
          } : {}, {
            l: (_ctx.user.usertype == "K9" || _ctx.user.usertype == "K10" || _ctx.user.usertype == "K11") && !match.players_id.includes(_ctx.user.id),
            n: match.players_id.includes(_ctx.user.id)
          }, match.players_id.includes(_ctx.user.id) ? {
            o: common_vendor.o(($event) => _ctx.quit(match.id), index)
          } : {
            p: common_vendor.o(($event) => _ctx.sign_up_page(match.id), index)
          }, {
            q: common_vendor.o(($event) => _ctx.match_detail_page(match.id), index)
          }) : {}, {
            r: index
          });
        }),
        h: !_ctx.hide_this
      } : {});
    };
  }
});
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["__scopeId", "data-v-61ce8ce7"]]);
wx.createPage(MiniProgramPage);
