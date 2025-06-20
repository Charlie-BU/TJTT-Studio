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
      match: "",
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
    static_js_ajax_request.fetch_data("POST", "fetch_organs", null, "competition", (res) => {
      this.organs = res.data.organs;
      common_vendor.wx$1.hideToast();
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
    modify() {
      common_vendor.wx$1.showToast({
        title: "修改中",
        icon: "loading",
        duration: 1e5
      });
      let data = {
        "my_id": this.user.id,
        "match_id": this.match.id,
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
      static_js_ajax_request.fetch_data("POST", "modify_match_info", data, "competition", (res) => {
        common_vendor.wx$1.showToast({
          title: res.data.message,
          icon: "none",
          duration: 1e3
        });
        if (res.data.status == 200) {
          setTimeout(() => {
            common_vendor.index.reLaunch({
              url: "/page_subjec/match/detail"
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
  }, !$data.hide_this ? common_vendor.e({
    d: $data.match.title,
    e: $data.title,
    f: common_vendor.o(($event) => $data.title = $event.detail.value),
    g: $data.match.description,
    h: $data.description,
    i: common_vendor.o(($event) => $data.description = $event.detail.value),
    j: $data.match.match_type == "男子单打"
  }, $data.match.match_type == "男子单打" ? {} : {}, {
    k: $data.match.match_type == "女子单打"
  }, $data.match.match_type == "女子单打" ? {} : {}, {
    l: $data.match.match_type == "混合单打"
  }, $data.match.match_type == "混合单打" ? {} : {}, {
    m: $data.match.match_type == "男子团体"
  }, $data.match.match_type == "男子团体" ? {} : {}, {
    n: $data.match.match_type == "女子团体"
  }, $data.match.match_type == "女子团体" ? {} : {}, {
    o: $data.match.match_type == "混合团体"
  }, $data.match.match_type == "混合团体" ? {} : {}, {
    p: common_vendor.o((...args) => $options.which_match_type && $options.which_match_type(...args)),
    q: $data.match.system == "小组循环赛+淘汰赛"
  }, $data.match.system == "小组循环赛+淘汰赛" ? {} : {}, {
    r: $data.match.system == "淘汰赛"
  }, $data.match.system == "淘汰赛" ? {} : {}, {
    s: $data.match.system == "大循环"
  }, $data.match.system == "大循环" ? {} : {}, {
    t: $data.match.system == "小组循环赛（不决名次）"
  }, $data.match.system == "小组循环赛（不决名次）" ? {} : {}, {
    v: $data.match.system == "其他"
  }, $data.match.system == "其他" ? {} : {}, {
    w: common_vendor.o((...args) => $options.which_system && $options.which_system(...args)),
    x: $data.user.address,
    y: $data.address,
    z: common_vendor.o(($event) => $data.address = $event.detail.value),
    A: common_vendor.f(this.organs, (organ, index, i0) => {
      return common_vendor.e({
        a: $data.match.organ_id == organ.id
      }, $data.match.organ_id == organ.id ? {
        b: organ.id,
        c: common_vendor.t(organ.organname)
      } : {
        d: organ.id,
        e: common_vendor.t(organ.organname)
      }, {
        f: index
      });
    }),
    B: common_vendor.o((...args) => $options.which_organ_id && $options.which_organ_id(...args)),
    C: $data.match_time,
    D: common_vendor.o(($event) => $data.match_time = $event.detail.value),
    E: $data.match.place,
    F: $data.place,
    G: common_vendor.o(($event) => $data.place = $event.detail.value),
    H: $data.sign_start_time,
    I: common_vendor.o(($event) => $data.sign_start_time = $event.detail.value),
    J: $data.sign_end_time,
    K: common_vendor.o(($event) => $data.sign_end_time = $event.detail.value),
    L: $data.match.participant,
    M: $data.participant,
    N: common_vendor.o(($event) => $data.participant = $event.detail.value),
    O: $data.match.fee,
    P: $data.fee,
    Q: common_vendor.o(($event) => $data.fee = $event.detail.value),
    R: $data.match.restriction == "无限制"
  }, $data.match.restriction == "无限制" ? {} : {}, {
    S: $data.match.restriction == "限制（仅）男子"
  }, $data.match.restriction == "限制（仅）男子" ? {} : {}, {
    T: $data.match.restriction == "限制（仅）女子"
  }, $data.match.restriction == "限制（仅）女子" ? {} : {}, {
    U: $data.match.restriction == "限制（仅）学生"
  }, $data.match.restriction == "限制（仅）学生" ? {} : {}, {
    V: $data.match.restriction == "限制（仅）教师"
  }, $data.match.restriction == "限制（仅）教师" ? {} : {}, {
    W: $data.match.restriction == "积分限制"
  }, $data.match.restriction == "积分限制" ? {} : {}, {
    X: $data.match.restriction == "积分限制"
  }, $data.match.restriction == "积分限制" ? {
    Y: $data.match.score_min,
    Z: $data.score_min,
    aa: common_vendor.o(($event) => $data.score_min = $event.detail.value),
    ab: $data.match.score_max,
    ac: $data.score_max,
    ad: common_vendor.o(($event) => $data.score_max = $event.detail.value)
  } : {
    ae: $data.score_min,
    af: common_vendor.o(($event) => $data.score_min = $event.detail.value),
    ag: $data.score_max,
    ah: common_vendor.o(($event) => $data.score_max = $event.detail.value)
  }, {
    ai: common_vendor.o((...args) => $options.which_restriction && $options.which_restriction(...args)),
    aj: $data.match.prize_for_first,
    ak: $data.prize_for_first,
    al: common_vendor.o(($event) => $data.prize_for_first = $event.detail.value),
    am: $data.match.prize_for_second,
    an: $data.prize_for_second,
    ao: common_vendor.o(($event) => $data.prize_for_second = $event.detail.value),
    ap: $data.match.prize_for_third,
    aq: $data.prize_for_third,
    ar: common_vendor.o(($event) => $data.prize_for_third = $event.detail.value),
    as: $data.match.additional_info,
    at: $data.additional_info,
    av: common_vendor.o(($event) => $data.additional_info = $event.detail.value),
    aw: common_vendor.o((...args) => $options.modify && $options.modify(...args))
  }) : {});
}
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["render", _sfc_render]]);
wx.createPage(MiniProgramPage);
