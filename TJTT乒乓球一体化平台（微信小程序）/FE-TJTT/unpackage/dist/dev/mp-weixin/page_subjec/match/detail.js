"use strict";
const common_vendor = require("../../common/vendor.js");
const static_js_utils = require("../../static/js/utils.js");
const static_js_ajax_request = require("../../static/js/ajax_request.js");
const static_js_login_check = require("../../static/js/login_check.js");
const static_js_magic_power = require("../../static/js/magic_power.js");
const static_js_uqrcode = require("../../static/js/uqrcode.js");
if (!Array) {
  const _easycom_u_icon2 = common_vendor.resolveComponent("u-icon");
  _easycom_u_icon2();
}
const _easycom_u_icon = () => "../../uni_modules/vk-uview-ui/components/u-icon/u-icon.js";
if (!Math) {
  _easycom_u_icon();
}
const __default__ = {
  data() {
    return {
      message: "",
      user: "",
      match: "",
      actionList: [
        {
          name: "修改赛事信息"
        },
        {
          name: "参赛选手"
        },
        {
          name: "赛事成绩管理"
        },
        {
          name: "删除赛事"
        }
      ],
      actionList2: [
        {
          name: "赛程安排"
        },
        {
          name: "比赛成绩"
        },
        {
          name: "现场直播"
        },
        {
          name: "精彩回顾"
        }
      ],
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
    let match_id = common_vendor.index.getStorageSync("match_id");
    static_js_ajax_request.fetch_data("POST", "get_this_match", { "match_id": match_id }, "competition", (res) => {
      this.match = res.data.match;
      common_vendor.wx$1.hideToast();
    });
    var qr = new static_js_uqrcode.b();
    qr.data = "Player's QRcode\n" + match_id + "\n" + this.user.id + "\n" + this.user.fixed_score;
    qr.size = 150;
    qr.make();
    var canvasContext = common_vendor.index.createCanvasContext("qrcode", this);
    qr.canvasContext = canvasContext;
    qr.drawCanvas();
  },
  methods: {
    schedule() {
      common_vendor.wx$1.showToast({
        title: "秩序册将在赛事微信群公布，请关注",
        icon: "none",
        duration: 1e3
      });
    },
    result() {
      common_vendor.index.setStorageSync("match_id", this.match.id);
      common_vendor.index.navigateTo({
        url: "/page_subjec/match/result-announce"
      });
    },
    livestream() {
      common_vendor.wx$1.showToast({
        title: "该功能暂未上线，敬请期待",
        icon: "none",
        duration: 1e3
      });
    },
    replay() {
      common_vendor.wx$1.showToast({
        title: "该功能暂未上线，敬请期待",
        icon: "none",
        duration: 1e3
      });
    },
    modify_info() {
      common_vendor.index.setStorageSync("match_id", this.match.id);
      common_vendor.index.navigateTo({
        url: "/page_subjec/match/modify-match-info"
      });
    },
    player_management() {
      common_vendor.index.setStorageSync("match_id", this.match.id);
      common_vendor.index.navigateTo({
        url: "/page_subjec/match/players"
      });
    },
    result_management() {
      common_vendor.index.setStorageSync("match_id", this.match.id);
      common_vendor.index.navigateTo({
        url: "/page_subjec/match/result-management"
      });
    },
    delete_match() {
      common_vendor.wx$1.showModal({
        title: "删除赛事",
        content: "删除赛事后，选手信息、赛事成绩等将一并删除。确认删除该赛事？",
        success: (res) => {
          if (res.confirm) {
            common_vendor.wx$1.showToast({
              title: "删除中",
              icon: "loading",
              duration: 1e5
            });
            let data = {
              "my_id": this.user.id,
              "match_id": this.match.id
            };
            static_js_ajax_request.fetch_data("POST", "delete_match", data, "competition", (res2) => {
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
    }
  }
};
const _sfc_main = /* @__PURE__ */ Object.assign(__default__, {
  __name: "detail",
  setup(__props) {
    return (_ctx, _cache) => {
      return common_vendor.e({
        a: _ctx.match && !_ctx.hide_this
      }, _ctx.match && !_ctx.hide_this ? common_vendor.e({
        b: common_vendor.t(_ctx.match.title),
        c: common_vendor.t(static_js_utils.format_time(_ctx.match.match_time)),
        d: _ctx.match.players_id.includes(_ctx.user.id)
      }, _ctx.match.players_id.includes(_ctx.user.id) ? {} : {}, {
        e: common_vendor.t(_ctx.match.season.season_name),
        f: common_vendor.t(_ctx.match.description),
        g: common_vendor.t(_ctx.match.address),
        h: common_vendor.t(_ctx.match.organ.organname),
        i: common_vendor.t(static_js_utils.format_time(_ctx.match.match_time)),
        j: common_vendor.t(_ctx.match.place),
        k: common_vendor.t(_ctx.match.match_type),
        l: common_vendor.t(_ctx.match.system),
        m: common_vendor.t(_ctx.match.prize_for_first),
        n: common_vendor.t(_ctx.match.prize_for_second),
        o: common_vendor.t(_ctx.match.prize_for_third),
        p: _ctx.match.additional_info != "" && _ctx.match.additional_info != "None"
      }, _ctx.match.additional_info != "" && _ctx.match.additional_info != "None" ? {} : {}, {
        q: _ctx.match.additional_info != "" && _ctx.match.additional_info != "None"
      }, _ctx.match.additional_info != "" && _ctx.match.additional_info != "None" ? {
        r: common_vendor.t(_ctx.match.additional_info)
      } : {}, {
        s: common_vendor.t(static_js_utils.format_time(_ctx.match.sign_start_time)),
        t: common_vendor.t(static_js_utils.format_time(_ctx.match.sign_end_time)),
        v: common_vendor.t(_ctx.match.participant),
        w: common_vendor.t(_ctx.match.players_id.length),
        x: _ctx.match.restriction == "积分限制"
      }, _ctx.match.restriction == "积分限制" ? {
        y: common_vendor.t(_ctx.match.restriction),
        z: common_vendor.t(_ctx.match.score_min),
        A: common_vendor.t(_ctx.match.score_max)
      } : {
        B: common_vendor.t(_ctx.match.restriction)
      }, {
        C: common_vendor.t(_ctx.match.fee),
        D: _ctx.match.players_id.includes(_ctx.user.id)
      }, _ctx.match.players_id.includes(_ctx.user.id) ? {
        E: common_vendor.t(_ctx.user.username),
        F: common_vendor.t(_ctx.user.phone),
        G: common_vendor.t(_ctx.user.school),
        H: common_vendor.t(_ctx.user.role),
        I: common_vendor.t(_ctx.user.fixed_score)
      } : {}, {
        J: common_vendor.f(_ctx.actionList2, (item, index, i0) => {
          return common_vendor.e({
            a: index == 0
          }, index == 0 ? {
            b: "e747ea51-0-" + i0,
            c: common_vendor.p({
              name: "order",
              size: "40"
            }),
            d: common_vendor.t(item.name),
            e: common_vendor.o((...args) => _ctx.schedule && _ctx.schedule(...args), index)
          } : index == 1 ? {
            g: "e747ea51-1-" + i0,
            h: common_vendor.p({
              name: "list-dot",
              size: "40"
            }),
            i: common_vendor.t(item.name),
            j: common_vendor.o((...args) => _ctx.result && _ctx.result(...args), index)
          } : index == 2 ? {
            l: "e747ea51-2-" + i0,
            m: common_vendor.p({
              name: "play-circle",
              size: "40"
            }),
            n: common_vendor.t(item.name),
            o: common_vendor.o((...args) => _ctx.livestream && _ctx.livestream(...args), index)
          } : index == 3 ? {
            q: "e747ea51-3-" + i0,
            r: common_vendor.p({
              name: "rewind-left",
              size: "40"
            }),
            s: common_vendor.t(item.name),
            t: common_vendor.o((...args) => _ctx.replay && _ctx.replay(...args), index)
          } : {}, {
            f: index == 1,
            k: index == 2,
            p: index == 3,
            v: index
          });
        }),
        K: (_ctx.user.usertype == "K9" || _ctx.user.usertype == "K10" || _ctx.user.usertype == "K11") && !_ctx.hide_this
      }, (_ctx.user.usertype == "K9" || _ctx.user.usertype == "K10" || _ctx.user.usertype == "K11") && !_ctx.hide_this ? {
        L: common_vendor.f(_ctx.actionList, (item, index, i0) => {
          return common_vendor.e({
            a: index == 0
          }, index == 0 ? {
            b: "e747ea51-4-" + i0,
            c: common_vendor.p({
              name: "setting-fill",
              size: "40"
            }),
            d: common_vendor.t(item.name),
            e: common_vendor.o((...args) => _ctx.modify_info && _ctx.modify_info(...args), index)
          } : index == 1 ? {
            g: "e747ea51-5-" + i0,
            h: common_vendor.p({
              name: "account-fill",
              size: "40"
            }),
            i: common_vendor.t(item.name),
            j: common_vendor.o((...args) => _ctx.player_management && _ctx.player_management(...args), index)
          } : index == 2 ? {
            l: "e747ea51-6-" + i0,
            m: common_vendor.p({
              name: "grid-fill",
              size: "40"
            }),
            n: common_vendor.t(item.name),
            o: common_vendor.o((...args) => _ctx.result_management && _ctx.result_management(...args), index)
          } : index == 3 ? {
            q: "e747ea51-7-" + i0,
            r: common_vendor.p({
              name: "trash-fill",
              size: "40"
            }),
            s: common_vendor.t(item.name),
            t: common_vendor.o((...args) => _ctx.delete_match && _ctx.delete_match(...args), index)
          } : {}, {
            f: index == 1,
            k: index == 2,
            p: index == 3,
            v: index
          });
        })
      } : {}) : {});
    };
  }
});
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["__scopeId", "data-v-e747ea51"]]);
wx.createPage(MiniProgramPage);
