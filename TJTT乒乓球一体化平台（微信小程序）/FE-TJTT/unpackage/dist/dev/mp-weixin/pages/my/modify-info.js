"use strict";
const common_vendor = require("../../common/vendor.js");
const static_js_ajax_request = require("../../static/js/ajax_request.js");
const static_js_login_check = require("../../static/js/login_check.js");
const static_js_magic_power = require("../../static/js/magic_power.js");
const common_assets = require("../../common/assets.js");
const _sfc_main = {
  data() {
    return {
      message: "",
      user: "",
      gender: "",
      address: "",
      phone: "",
      email: "",
      school: "",
      role: "",
      stu_num: "",
      hand: "",
      grip: "",
      blade: "",
      forehand: "",
      backhand: "",
      particle: "",
      hide_this: static_js_magic_power.magic()
    };
  },
  onLoad() {
    static_js_login_check.login_check((user) => {
      this.user = user;
    });
  },
  methods: {
    onInput(e) {
      this.phone = e.target.value;
      this.email = e.target.value;
      this.school = e.target.value;
      this.stu_num = e.target.value;
      this.blade = e.target.value;
      this.forehand = e.target.value;
      this.backhand = e.target.value;
    },
    pick_addr(event) {
      const selected_addr = event.detail.value;
      this.address = selected_addr[1];
    },
    which_gender(e) {
      this.gender = e.detail.value;
    },
    which_role(e) {
      this.role = e.detail.value;
    },
    which_hand(e) {
      this.hand = e.detail.value;
    },
    which_grip(e) {
      this.grip = e.detail.value;
    },
    which_particle(e) {
      this.particle = e.detail.value;
    },
    backref() {
      common_vendor.index.navigateBack({
        delta: 1
      });
    },
    modify() {
      let data = {
        "my_id": this.user.id,
        "user_id": this.user.id,
        "gender": this.gender,
        "address": this.address,
        "phone": this.phone,
        "email": this.email,
        "school": this.school,
        "role": this.role,
        "stu_num": this.stu_num,
        "hand": this.hand,
        "grip": this.grip,
        "blade": this.blade,
        "forehand": this.forehand,
        "backhand": this.backhand,
        "particle": this.particle
      };
      static_js_ajax_request.fetch_data("POST", "modify_user", data, "user", (res) => {
        common_vendor.wx$1.showToast({
          title: res.data.message,
          icon: "none",
          duration: 1e3
        });
        if (res.data.status == 200) {
          setTimeout(() => {
            common_vendor.index.reLaunch({
              url: "/pages/my/index"
            });
          }, 1e3);
        }
      });
    }
  }
};
if (!Array) {
  const _easycom_u_icon2 = common_vendor.resolveComponent("u-icon");
  _easycom_u_icon2();
}
const _easycom_u_icon = () => "../../uni_modules/vk-uview-ui/components/u-icon/u-icon.js";
if (!Math) {
  _easycom_u_icon();
}
function _sfc_render(_ctx, _cache, $props, $setup, $data, $options) {
  return common_vendor.e({
    a: common_assets._imports_0$1,
    b: common_vendor.o(($event) => $options.backref()),
    c: !$data.hide_this
  }, !$data.hide_this ? common_vendor.e({
    d: $data.user.username,
    e: $data.user.gender == "男"
  }, $data.user.gender == "男" ? {} : {}, {
    f: $data.user.gender == "女"
  }, $data.user.gender == "女" ? {} : {}, {
    g: common_vendor.o((...args) => $options.which_gender && $options.which_gender(...args)),
    h: common_vendor.t($data.address ? $data.address : $data.user.address),
    i: common_vendor.p({
      name: "arrow-down",
      size: "28"
    }),
    j: common_vendor.o((...args) => $options.pick_addr && $options.pick_addr(...args)),
    k: $data.user.phone,
    l: $data.phone,
    m: common_vendor.o(($event) => $data.phone = $event.detail.value),
    n: $data.user.email,
    o: $data.email,
    p: common_vendor.o(($event) => $data.email = $event.detail.value),
    q: $data.user.school,
    r: $data.school,
    s: common_vendor.o(($event) => $data.school = $event.detail.value),
    t: $data.user.role == "学生"
  }, $data.user.role == "学生" ? {} : {}, {
    v: $data.user.role == "教师"
  }, $data.user.role == "教师" ? {} : {}, {
    w: $data.user.role == "校友及校外人士"
  }, $data.user.role == "校友及校外人士" ? {} : {}, {
    x: common_vendor.o((...args) => $options.which_role && $options.which_role(...args)),
    y: $data.user.stu_num,
    z: $data.stu_num,
    A: common_vendor.o(($event) => $data.stu_num = $event.detail.value),
    B: $data.user.hand == "右手"
  }, $data.user.hand == "右手" ? {} : {}, {
    C: $data.user.hand == "左手"
  }, $data.user.hand == "左手" ? {} : {}, {
    D: common_vendor.o((...args) => $options.which_hand && $options.which_hand(...args)),
    E: $data.user.grip == "横拍"
  }, $data.user.grip == "横拍" ? {} : {}, {
    F: $data.user.grip == "直拍"
  }, $data.user.grip == "直拍" ? {} : {}, {
    G: common_vendor.o((...args) => $options.which_grip && $options.which_grip(...args)),
    H: $data.user.blade,
    I: $data.blade,
    J: common_vendor.o(($event) => $data.blade = $event.detail.value),
    K: $data.user.forehand,
    L: $data.forehand,
    M: common_vendor.o(($event) => $data.forehand = $event.detail.value),
    N: $data.user.backhand,
    O: $data.backhand,
    P: common_vendor.o(($event) => $data.backhand = $event.detail.value),
    Q: $data.user.particle == "是"
  }, $data.user.particle == "是" ? {} : {}, {
    R: $data.user.particle == "否"
  }, $data.user.particle == "否" ? {} : {}, {
    S: common_vendor.o((...args) => $options.which_particle && $options.which_particle(...args)),
    T: common_vendor.o((...args) => $options.modify && $options.modify(...args))
  }) : {});
}
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["render", _sfc_render]]);
wx.createPage(MiniProgramPage);
