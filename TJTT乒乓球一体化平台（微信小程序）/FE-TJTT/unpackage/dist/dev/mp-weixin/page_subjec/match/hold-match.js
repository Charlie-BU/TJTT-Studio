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
      organs: [],
      title: "",
      description: "",
      match_type: "",
      system: "",
      address: "",
      organ_id: "",
      match_time: "",
      place: "",
      sign_start_time: "",
      sign_end_time: "",
      participant: "",
      fee: "",
      restriction: "",
      prize_for_first: "",
      prize_for_second: "",
      prize_for_third: "",
      additional_info: "",
      score_min: "",
      score_max: "",
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
    static_js_ajax_request.fetch_data("POST", "fetch_organs", null, "competition", (res) => {
      this.organs = res.data.organs;
    });
  },
  methods: {
    onInput(e) {
      this.title = e.target.value;
      this.description = e.target.value;
      this.address = e.target.value;
      this.match_time = e.target.value;
      this.place = e.target.value;
      this.sign_start_time = e.target.value;
      this.sign_end_time = e.target.value;
      this.participant = e.target.value;
      this.fee = e.target.value;
      this.prize_for_first = e.target.value;
      this.prize_for_second = e.target.value;
      this.prize_for_third = e.target.value;
      this.additional_info = e.target.value;
      this.score_min = e.target.value;
      this.score_max = e.target.value;
    },
    which_match_type(e) {
      this.match_type = e.detail.value;
    },
    which_system(e) {
      this.system = e.detail.value;
    },
    which_organ_id(e) {
      this.organ_id = parseInt(e.detail.value);
    },
    which_restriction(e) {
      this.restriction = e.detail.value;
    },
    backref() {
      common_vendor.index.navigateBack({
        delta: 1
      });
    },
    confirm_hold() {
      common_vendor.wx$1.showToast({
        title: "举办中",
        icon: "loading",
        duration: 1e5
      });
      let data = {
        "my_id": this.user.id,
        "title": this.title,
        "description": this.description,
        "match_type": this.match_type,
        "system": this.system,
        "address": this.address,
        "organ_id": this.organ_id,
        "match_time": this.match_time,
        "place": this.place,
        "sign_start_time": this.sign_start_time,
        "sign_end_time": this.sign_end_time,
        "participant": this.participant,
        "fee": this.fee,
        "restriction": this.restriction,
        "prize_for_first": this.prize_for_first,
        "prize_for_second": this.prize_for_second,
        "prize_for_third": this.prize_for_third,
        "additional_info": this.additional_info,
        "score_min": this.score_min,
        "score_max": this.score_max
      };
      static_js_ajax_request.fetch_data("POST", "hold_match", data, "competition", (res) => {
        console.log(res.data.message);
        common_vendor.wx$1.showToast({
          title: res.data.message,
          icon: "none",
          duration: 1e3
        });
        if (res.data.status == 200) {
          setTimeout(() => {
            common_vendor.index.reLaunch({
              url: "/page_subjec/match/index"
            });
          }, 1e3);
        }
      });
    }
  }
};
function _sfc_render(_ctx, _cache, $props, $setup, $data, $options) {
  return common_vendor.e({
    a: common_assets._imports_0$1,
    b: common_vendor.o(($event) => $options.backref()),
    c: !$data.hide_this
  }, !$data.hide_this ? {
    d: $data.title,
    e: common_vendor.o(($event) => $data.title = $event.detail.value),
    f: $data.description,
    g: common_vendor.o(($event) => $data.description = $event.detail.value),
    h: common_vendor.o((...args) => $options.which_match_type && $options.which_match_type(...args)),
    i: common_vendor.o((...args) => $options.which_system && $options.which_system(...args)),
    j: $data.address,
    k: common_vendor.o(($event) => $data.address = $event.detail.value),
    l: common_vendor.f(this.organs, (organ, index, i0) => {
      return {
        a: organ.id,
        b: common_vendor.t(organ.organname),
        c: index
      };
    }),
    m: common_vendor.o((...args) => $options.which_organ_id && $options.which_organ_id(...args)),
    n: $data.match_time,
    o: common_vendor.o(($event) => $data.match_time = $event.detail.value),
    p: $data.place,
    q: common_vendor.o(($event) => $data.place = $event.detail.value),
    r: $data.sign_start_time,
    s: common_vendor.o(($event) => $data.sign_start_time = $event.detail.value),
    t: $data.sign_end_time,
    v: common_vendor.o(($event) => $data.sign_end_time = $event.detail.value),
    w: $data.participant,
    x: common_vendor.o(($event) => $data.participant = $event.detail.value),
    y: $data.fee,
    z: common_vendor.o(($event) => $data.fee = $event.detail.value),
    A: $data.score_min,
    B: common_vendor.o(($event) => $data.score_min = $event.detail.value),
    C: $data.score_max,
    D: common_vendor.o(($event) => $data.score_max = $event.detail.value),
    E: common_vendor.o((...args) => $options.which_restriction && $options.which_restriction(...args)),
    F: $data.prize_for_first,
    G: common_vendor.o(($event) => $data.prize_for_first = $event.detail.value),
    H: $data.prize_for_second,
    I: common_vendor.o(($event) => $data.prize_for_second = $event.detail.value),
    J: $data.prize_for_third,
    K: common_vendor.o(($event) => $data.prize_for_third = $event.detail.value),
    L: $data.additional_info,
    M: common_vendor.o(($event) => $data.additional_info = $event.detail.value),
    N: common_vendor.o((...args) => $options.confirm_hold && $options.confirm_hold(...args))
  } : {});
}
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["render", _sfc_render]]);
wx.createPage(MiniProgramPage);
