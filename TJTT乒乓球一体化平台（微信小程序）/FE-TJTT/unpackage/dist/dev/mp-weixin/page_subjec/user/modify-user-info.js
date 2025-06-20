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
      user_x: "",
      organs: [],
      gender: "",
      address: "",
      phone: "",
      email: "",
      school: "",
      role: "",
      organ_id: "",
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
          url: "/pages/index/index"
        });
      }, 1e3);
    } else {
      static_js_ajax_request.fetch_data("POST", "get_this_user", { "user_id": user_id }, "user", (res) => {
        this.user_x = res.data.user;
      });
    }
    static_js_ajax_request.fetch_data("POST", "fetch_organs", null, "competition", (res) => {
      this.organs = res.data.organs;
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
    which_organ_id(e) {
      this.organ_id = parseInt(e.detail.value);
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
      common_vendor.wx$1.showToast({
        title: "修改中",
        icon: "loading",
        duration: 1e5
      });
      let data = {
        "my_id": this.user.id,
        "user_id": this.user_x.id,
        "gender": this.gender,
        "address": this.address,
        "phone": this.phone,
        "email": this.email,
        "school": this.school,
        "role": this.role,
        "organ_id": this.organ_id,
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
              url: "/page_subjec/user/user-detail"
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
    d: $data.user_x.username,
    e: $data.user_x.gender == "男"
  }, $data.user_x.gender == "男" ? {} : {}, {
    f: $data.user_x.gender == "女"
  }, $data.user_x.gender == "女" ? {} : {}, {
    g: common_vendor.o((...args) => $options.which_gender && $options.which_gender(...args)),
    h: common_vendor.t($data.address ? $data.address : $data.user_x.address),
    i: common_vendor.p({
      name: "arrow-down",
      size: "28"
    }),
    j: common_vendor.o((...args) => $options.pick_addr && $options.pick_addr(...args)),
    k: $data.user_x.phone,
    l: $data.phone,
    m: common_vendor.o(($event) => $data.phone = $event.detail.value),
    n: $data.user_x.email,
    o: $data.email,
    p: common_vendor.o(($event) => $data.email = $event.detail.value),
    q: $data.user_x.school,
    r: $data.school,
    s: common_vendor.o(($event) => $data.school = $event.detail.value),
    t: $data.user_x.role == "学生"
  }, $data.user_x.role == "学生" ? {} : {}, {
    v: $data.user_x.role == "教师"
  }, $data.user_x.role == "教师" ? {} : {}, {
    w: $data.user_x.role == "校友及校外人士"
  }, $data.user_x.role == "校友及校外人士" ? {} : {}, {
    x: common_vendor.o((...args) => $options.which_role && $options.which_role(...args)),
    y: $data.user_x.stu_num,
    z: $data.stu_num,
    A: common_vendor.o(($event) => $data.stu_num = $event.detail.value),
    B: common_vendor.f(this.organs, (organ, index, i0) => {
      return common_vendor.e({
        a: $data.user_x.organ_id == organ.id
      }, $data.user_x.organ_id == organ.id ? {
        b: organ.id,
        c: common_vendor.t(organ.organname)
      } : {
        d: organ.id,
        e: common_vendor.t(organ.organname)
      }, {
        f: index
      });
    }),
    C: common_vendor.o((...args) => $options.which_organ_id && $options.which_organ_id(...args)),
    D: $data.user_x.hand == "右手"
  }, $data.user_x.hand == "右手" ? {} : {}, {
    E: $data.user_x.hand == "左手"
  }, $data.user_x.hand == "左手" ? {} : {}, {
    F: common_vendor.o((...args) => $options.which_hand && $options.which_hand(...args)),
    G: $data.user_x.grip == "横拍"
  }, $data.user_x.grip == "横拍" ? {} : {}, {
    H: $data.user_x.grip == "直拍"
  }, $data.user_x.grip == "直拍" ? {} : {}, {
    I: common_vendor.o((...args) => $options.which_grip && $options.which_grip(...args)),
    J: $data.user_x.blade,
    K: $data.blade,
    L: common_vendor.o(($event) => $data.blade = $event.detail.value),
    M: $data.user_x.forehand,
    N: $data.forehand,
    O: common_vendor.o(($event) => $data.forehand = $event.detail.value),
    P: $data.user_x.backhand,
    Q: $data.backhand,
    R: common_vendor.o(($event) => $data.backhand = $event.detail.value),
    S: $data.user_x.particle == "是"
  }, $data.user_x.particle == "是" ? {} : {}, {
    T: $data.user_x.particle == "否"
  }, $data.user_x.particle == "否" ? {} : {}, {
    U: common_vendor.o((...args) => $options.which_particle && $options.which_particle(...args)),
    V: common_vendor.o((...args) => $options.modify && $options.modify(...args))
  }) : {});
}
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["render", _sfc_render]]);
wx.createPage(MiniProgramPage);
