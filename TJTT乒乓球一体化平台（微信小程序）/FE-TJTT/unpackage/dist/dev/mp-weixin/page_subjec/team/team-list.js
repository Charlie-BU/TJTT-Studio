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
      team_length: "",
      search_team: "",
      teams: [],
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
    static_js_ajax_request.fetch_data("POST", "get_teams", null, "competition", (res) => {
      this.team_length = res.data.team_length;
      this.teams = res.data.teams;
      common_vendor.wx$1.hideToast();
    });
  },
  methods: {
    onInput(e) {
      this.search_team = e.target.value;
    },
    search() {
      let data = { "search_team": this.search_team, "where": "user_list" };
      static_js_ajax_request.fetch_data("POST", "findTeamByName", data, "competition", (res) => {
        this.teams = res.data.teams;
        this.team_length = res.data.team_length;
      });
    },
    add_team() {
      common_vendor.index.navigateTo({
        url: "/page_subjec/team/add-team"
      });
    },
    modify_member_max(team_id) {
      common_vendor.wx$1.showModal({
        title: "变更人数上限",
        placeholderText: "请输入变更后人数上限",
        editable: true,
        confirmText: "确认变更",
        success: (res) => {
          if (res.confirm) {
            let data = {
              "my_id": this.user.id,
              "team_id": team_id,
              "member_max": res.content
            };
            static_js_ajax_request.fetch_data("POST", "modify_member_max", data, "competition", (res2) => {
              common_vendor.wx$1.showToast({
                title: res2.data.message,
                icon: "none",
                duration: 1e3
              });
              if (res2.data.status == 200) {
                static_js_ajax_request.fetch_data("POST", "get_teams", null, "competition", (res3) => {
                  this.teams = res3.data.teams;
                });
              }
            });
          }
        }
      });
    },
    modify_match(team_id) {
      common_vendor.wx$1.showModal({
        title: "变更绑定赛事",
        placeholderText: "请输入准确团体赛事名称",
        editable: true,
        confirmText: "确认变更",
        success: (res) => {
          if (res.confirm) {
            let data = {
              "my_id": this.user.id,
              "team_id": team_id,
              "match_title": res.content
            };
            static_js_ajax_request.fetch_data("POST", "modify_match", data, "competition", (res2) => {
              common_vendor.wx$1.showToast({
                title: res2.data.message,
                icon: "none",
                duration: 1e3
              });
              if (res2.data.status == 200) {
                static_js_ajax_request.fetch_data("POST", "get_teams", null, "competition", (res3) => {
                  this.teams = res3.data.teams;
                });
              }
            });
          }
        }
      });
    },
    members(team) {
      common_vendor.index.setStorageSync("team", team);
      common_vendor.index.navigateTo({
        url: "/page_subjec/team/members"
      });
    },
    delete_team(team_id) {
      common_vendor.wx$1.showModal({
        title: "删除代表队",
        content: "删除代表队后，该代表队所有信息将被永久清除；该操作可能导致数据库混乱、系统崩溃，请上报K11级管理员后操作",
        success: (res) => {
          if (res.confirm) {
            let data = {
              "my_id": this.user.id,
              "team_id": team_id
            };
            static_js_ajax_request.fetch_data("POST", "delete_team", data, "competition", (res2) => {
              common_vendor.wx$1.showToast({
                title: res2.data.message,
                icon: "none",
                duration: 1e3
              });
              if (res2.data.status == 200) {
                static_js_ajax_request.fetch_data("POST", "get_teams", null, "competition", (res3) => {
                  this.teams = res3.data.teams;
                });
              }
            });
          }
        }
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
    a: common_vendor.t($data.team_length),
    b: common_vendor.o(($event) => $data.search_team = $event),
    c: common_vendor.p({
      ["bg-color"]: "#ffffff",
      ["show-action"]: false,
      placeholder: "输入代表队名",
      modelValue: $data.search_team
    }),
    d: common_vendor.o((...args) => $options.search && $options.search(...args)),
    e: !$data.hide_this
  }, !$data.hide_this ? {
    f: common_vendor.o((...args) => $options.add_team && $options.add_team(...args))
  } : {}, {
    g: common_vendor.f($data.teams, (team, index, i0) => {
      return common_vendor.e({
        a: common_vendor.t(index + 1),
        b: common_vendor.t(team.teamname),
        c: team.description
      }, team.description ? {
        d: common_vendor.t(team.description)
      } : {}, {
        e: common_vendor.t(team.members.length),
        f: common_vendor.t(team.member_max),
        g: team.match_title
      }, team.match_title ? {
        h: common_vendor.t(team.match_title)
      } : {}, {
        i: common_vendor.t(team.score)
      }, !$data.hide_this ? {
        j: common_vendor.o(($event) => $options.modify_member_max(team.id), index),
        k: common_vendor.o(($event) => $options.modify_match(team.id), index)
      } : {}, !$data.hide_this ? {
        l: common_vendor.o(($event) => $options.members(team), index),
        m: common_vendor.o(($event) => $options.delete_team(team.id), index)
      } : {}, {
        n: index
      });
    }),
    h: !$data.hide_this,
    i: !$data.hide_this
  });
}
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["render", _sfc_render], ["__scopeId", "data-v-be54e189"]]);
wx.createPage(MiniProgramPage);
