"use strict";
const common_vendor = require("../../common/vendor.js");
const static_js_ajax_request = require("../../static/js/ajax_request.js");
const static_js_login_check = require("../../static/js/login_check.js");
const static_js_magic_power = require("../../static/js/magic_power.js");
const _sfc_main = {
  data() {
    return {
      message: "",
      user: "",
      team: "",
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
    this.team = common_vendor.index.getStorageSync("team");
    if (!this.team) {
      common_vendor.wx$1.showToast({
        title: "服务器繁忙，请稍后再试",
        icon: "none",
        duration: 1500
      });
      setTimeout(() => {
        common_vendor.index.navigateBack({
          delta: 1
        });
      }, 1e3);
    }
    common_vendor.index.removeStorageSync("team");
  },
  methods: {
    add_member() {
      common_vendor.wx$1.showModal({
        title: "添加队员",
        placeholderText: "请输入队员姓名",
        editable: true,
        success: (res) => {
          if (res.confirm) {
            let data = {
              "my_id": this.user.id,
              "team_id": this.team.id,
              "member_name": res.content
            };
            static_js_ajax_request.fetch_data("POST", "add_member", data, "competition", (res2) => {
              common_vendor.wx$1.showToast({
                title: res2.data.message,
                icon: "none",
                duration: 1e3
              });
              if (res2.data.status == 200) {
                static_js_ajax_request.fetch_data("POST", "get_this_team", { team_id: this.team.id }, "competition", (res3) => {
                  this.team = res3.data.team;
                });
                common_vendor.index.setStorageSync("team", this.team);
              }
            });
          }
        }
      });
    },
    remove_member(member_id) {
      common_vendor.wx$1.showModal({
        title: "移除队员",
        content: "确认移除该队员？",
        success: (res) => {
          if (res.confirm) {
            let data = {
              "my_id": this.user.id,
              "member_id": member_id,
              "team_id": this.team.id
            };
            static_js_ajax_request.fetch_data("POST", "remove_member", data, "competition", (res2) => {
              common_vendor.wx$1.showToast({
                title: res2.data.message,
                icon: "none",
                duration: 1e3
              });
              if (res2.data.status == 200) {
                this.team.members.forEach(function(item, index, arr) {
                  if (item.id == member_id) {
                    arr.splice(
                      index,
                      1
                    );
                  }
                });
                common_vendor.index.setStorageSync("team", this.team);
              }
            });
          }
        }
      });
    }
  }
};
function _sfc_render(_ctx, _cache, $props, $setup, $data, $options) {
  return common_vendor.e({
    a: !$data.hide_this
  }, !$data.hide_this ? {
    b: common_vendor.t($data.team.teamname),
    c: common_vendor.o((...args) => $options.add_member && $options.add_member(...args)),
    d: common_vendor.f($data.team.members, (member, index, i0) => {
      return common_vendor.e({
        a: common_vendor.t(member.username),
        b: common_vendor.t(member.gender),
        c: common_vendor.t(member.school),
        d: common_vendor.t(member.role),
        e: member.organ
      }, member.organ ? {
        f: common_vendor.t(member.organ.organname)
      } : {}, {
        g: common_vendor.t(member.score),
        h: common_vendor.o(($event) => $options.remove_member(member.id), index),
        i: index
      });
    })
  } : {});
}
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["render", _sfc_render], ["__scopeId", "data-v-b484fd6e"]]);
wx.createPage(MiniProgramPage);
