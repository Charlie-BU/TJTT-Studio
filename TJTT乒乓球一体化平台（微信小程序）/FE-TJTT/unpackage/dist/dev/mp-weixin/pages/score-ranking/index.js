"use strict";
const common_vendor = require("../../common/vendor.js");
const static_js_ajax_request = require("../../static/js/ajax_request.js");
const static_js_login_check = require("../../static/js/login_check.js");
const static_js_utils = require("../../static/js/utils.js");
const common_assets = require("../../common/assets.js");
const _sfc_main = {
  data() {
    return {
      user: "",
      school_list: [],
      school_index: 0,
      search_user: "",
      users: [],
      user1_url: "",
      user2_url: "",
      user3_url: "",
      ids: "",
      my_rank: "",
      range_list: [
        {
          name: "全国"
        },
        {
          name: "男子"
        },
        {
          name: "女子"
        }
      ],
      current: 0
    };
  },
  onLoad() {
    common_vendor.wx$1.showToast({
      title: "加载中",
      icon: "loading",
      duration: 1e5
    });
    static_js_login_check.login_check((user) => {
      this.user = user;
    });
    static_js_ajax_request.fetch_data("POST", "get_users", null, "user", (res) => {
      this.users = res.data.users;
      this.school_list = res.data.school_list;
      this.user1_url = res.data.users[0].profile_img;
      this.user2_url = res.data.users[1].profile_img;
      this.user3_url = res.data.users[2].profile_img;
      [this.ids, this.my_rank] = static_js_utils.get_rank(this.users, this.user.id);
      if (this.users) {
        common_vendor.wx$1.hideToast();
      }
    });
  },
  methods: {
    onInput(e) {
      this.search_user = e.target.value;
    },
    back() {
      common_vendor.index.navigateBack({
        delta: 1
      });
    },
    search() {
      common_vendor.wx$1.showToast({
        title: "加载中",
        icon: "loading",
        duration: 1e5
      });
      this.current = 0;
      let data = {
        "search_user": this.search_user,
        "where": "score_rank"
      };
      static_js_ajax_request.fetch_data("POST", "findUserByName", data, "user", (res) => {
        this.user1_url = null;
        this.user2_url = null;
        this.user3_url = null;
        this.users = res.data.users;
        if (res.data.users.length > 0) {
          this.user1_url = res.data.users[0].profile_img;
        }
        if (res.data.users.length > 1) {
          this.user2_url = res.data.users[1].profile_img;
        }
        if (res.data.users.length > 2) {
          this.user3_url = res.data.users[2].profile_img;
        }
        [this.ids, this.my_rank] = static_js_utils.get_rank(this.users, this.user.id);
        common_vendor.wx$1.hideToast();
      });
    },
    change(index) {
      common_vendor.wx$1.showToast({
        title: "加载中",
        icon: "loading",
        duration: 1e5
      });
      this.current = index;
      if (index == 0) {
        this.school_index = 0;
        static_js_ajax_request.fetch_data("POST", "get_users", null, "user", (res) => {
          this.user1_url = null;
          this.user2_url = null;
          this.user3_url = null;
          this.users = res.data.users;
          if (res.data.users.length > 0) {
            this.user1_url = res.data.users[0].profile_img;
          }
          if (res.data.users.length > 1) {
            this.user2_url = res.data.users[1].profile_img;
          }
          if (res.data.users.length > 2) {
            this.user3_url = res.data.users[2].profile_img;
          }
          [this.ids, this.my_rank] = static_js_utils.get_rank(this.users, this.user.id);
          common_vendor.wx$1.hideToast();
        });
      } else if (index == 1) {
        this.school_index = 0;
        static_js_ajax_request.fetch_data("POST", "get_male_users", null, "user", (res) => {
          this.user1_url = null;
          this.user2_url = null;
          this.user3_url = null;
          this.users = res.data.male_users;
          if (res.data.male_users.length > 0) {
            this.user1_url = res.data.male_users[0].profile_img;
          }
          if (res.data.male_users.length > 1) {
            this.user2_url = res.data.male_users[1].profile_img;
          }
          if (res.data.male_users.length > 2) {
            this.user3_url = res.data.male_users[2].profile_img;
          }
          [this.ids, this.my_rank] = static_js_utils.get_rank(this.users, this.user.id);
          common_vendor.wx$1.hideToast();
        });
      } else if (index == 2) {
        this.school_index = 0;
        static_js_ajax_request.fetch_data("POST", "get_female_users", null, "user", (res) => {
          this.user1_url = null;
          this.user2_url = null;
          this.user3_url = null;
          this.users = res.data.female_users;
          if (res.data.female_users.length > 0) {
            this.user1_url = res.data.female_users[0].profile_img;
          }
          if (res.data.female_users.length > 1) {
            this.user2_url = res.data.female_users[1].profile_img;
          }
          if (res.data.female_users.length > 2) {
            this.user3_url = res.data.female_users[2].profile_img;
          }
          [this.ids, this.my_rank] = static_js_utils.get_rank(this.users, this.user.id);
          common_vendor.wx$1.hideToast();
        });
      }
    },
    pick_school(e) {
      if (e.detail.value == 0) {
        common_vendor.wx$1.showToast({
          title: "请选择学校",
          icon: "none",
          duration: 1e3
        });
        return;
      }
      common_vendor.wx$1.showToast({
        title: "加载中",
        icon: "loading",
        duration: 1e5
      });
      this.school_index = e.detail.value;
      this.current = 3;
      let school = this.school_list[this.school_index];
      static_js_ajax_request.fetch_data("POST", "get_users_by_school", { "school": school }, "user", (res) => {
        this.user1_url = null;
        this.user2_url = null;
        this.user3_url = null;
        this.users = res.data.users;
        if (res.data.users.length > 0) {
          this.user1_url = res.data.users[0].profile_img;
        }
        if (res.data.users.length > 1) {
          this.user2_url = res.data.users[1].profile_img;
        }
        if (res.data.users.length > 2) {
          this.user3_url = res.data.users[2].profile_img;
        }
        [this.ids, this.my_rank] = static_js_utils.get_rank(this.users, this.user.id);
        common_vendor.wx$1.hideToast();
      });
    },
    active_instruction() {
      common_vendor.wx$1.showModal({
        title: "活跃度计算规则",
        content: "赛季活跃度反映用户在本赛季参加TJTT积分赛、参与约球、约教、提问等活动的频率。计算方式为：(本赛季完赛积分赛数 × 0.7 + 本赛季匹配成功约球帖数 × 0.1 + 本赛季被采纳提问问题数 × 0.1 + 本赛季约教成功次数 × 0.1) × 100。",
        showCancel: false,
        confirmText: "了解"
      });
    }
  },
  onPullDownRefresh() {
    if (this.user) {
      let data = { "my_id": this.user.id };
      static_js_ajax_request.fetch_data("POST", "refresh", data, "user", (res) => {
        var user_id = this.user.id;
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
    common_vendor.wx$1.showToast({
      title: "加载中",
      icon: "loading",
      duration: 1e5
    });
    static_js_login_check.login_check((user) => {
      this.user = user;
    });
    static_js_ajax_request.fetch_data("POST", "get_users", null, "user", (res) => {
      this.users = res.data.users;
      [this.ids, this.my_rank] = static_js_utils.get_rank(this.users, this.user.id);
      if (this.users) {
        common_vendor.wx$1.hideToast();
      }
    });
    common_vendor.index.reLaunch({
      url: "/pages/score-ranking/index"
    });
    setTimeout(() => {
      common_vendor.index.stopPullDownRefresh();
    }, 1e3);
  }
};
if (!Array) {
  const _easycom_u_tabs2 = common_vendor.resolveComponent("u-tabs");
  const _easycom_u_icon2 = common_vendor.resolveComponent("u-icon");
  const _easycom_u_search2 = common_vendor.resolveComponent("u-search");
  const _easycom_uni_th2 = common_vendor.resolveComponent("uni-th");
  const _easycom_uni_tr2 = common_vendor.resolveComponent("uni-tr");
  const _easycom_uni_td2 = common_vendor.resolveComponent("uni-td");
  const _easycom_uni_table2 = common_vendor.resolveComponent("uni-table");
  const _component_tabbar = common_vendor.resolveComponent("tabbar");
  (_easycom_u_tabs2 + _easycom_u_icon2 + _easycom_u_search2 + _easycom_uni_th2 + _easycom_uni_tr2 + _easycom_uni_td2 + _easycom_uni_table2 + _component_tabbar)();
}
const _easycom_u_tabs = () => "../../uni_modules/vk-uview-ui/components/u-tabs/u-tabs.js";
const _easycom_u_icon = () => "../../uni_modules/vk-uview-ui/components/u-icon/u-icon.js";
const _easycom_u_search = () => "../../uni_modules/vk-uview-ui/components/u-search/u-search.js";
const _easycom_uni_th = () => "../../uni_modules/uni-table/components/uni-th/uni-th.js";
const _easycom_uni_tr = () => "../../uni_modules/uni-table/components/uni-tr/uni-tr.js";
const _easycom_uni_td = () => "../../uni_modules/uni-table/components/uni-td/uni-td.js";
const _easycom_uni_table = () => "../../uni_modules/uni-table/components/uni-table/uni-table.js";
if (!Math) {
  (_easycom_u_tabs + _easycom_u_icon + _easycom_u_search + _easycom_uni_th + _easycom_uni_tr + _easycom_uni_td + _easycom_uni_table)();
}
function _sfc_render(_ctx, _cache, $props, $setup, $data, $options) {
  return common_vendor.e({
    a: common_assets._imports_0$2,
    b: common_vendor.o($options.change),
    c: common_vendor.p({
      list: $data.range_list,
      ["show-bar"]: false,
      duration: 0,
      ["active-color"]: "#2979FF",
      ["is-scroll"]: true,
      current: $data.current
    }),
    d: $data.current >= 0 && $data.current <= 2
  }, $data.current >= 0 && $data.current <= 2 ? {
    e: common_vendor.t($data.school_list[$data.school_index]),
    f: common_vendor.p({
      name: "arrow-down",
      size: "28"
    })
  } : {
    g: common_vendor.t($data.school_list[$data.school_index]),
    h: common_vendor.p({
      name: "arrow-down",
      size: "28"
    })
  }, {
    i: common_vendor.o((...args) => $options.pick_school && $options.pick_school(...args)),
    j: $data.school_index,
    k: $data.school_list,
    l: common_vendor.o(($event) => $data.search_user = $event),
    m: common_vendor.p({
      ["bg-color"]: "#ffffff",
      ["show-action"]: false,
      placeholder: "输入选手姓名",
      modelValue: $data.search_user
    }),
    n: common_vendor.o((...args) => $options.search && $options.search(...args)),
    o: $data.user
  }, $data.user ? common_vendor.e({
    p: common_vendor.t($data.my_rank),
    q: $data.user.profile_img
  }, $data.user.profile_img ? {
    r: $data.user.profile_img
  } : $data.user.gender == "男" ? {} : $data.user.gender == "女" ? {} : {}, {
    s: $data.user.gender == "男",
    t: $data.user.gender == "女",
    v: common_vendor.t($data.user.username),
    w: common_vendor.t($data.user.address),
    x: common_vendor.t($data.user.school),
    y: common_vendor.t($data.user.score)
  }) : {}, {
    z: common_assets._imports_1$1,
    A: $data.user2_url
  }, $data.user2_url ? {
    B: $data.user2_url
  } : {}, {
    C: common_assets._imports_2$1,
    D: $data.users[1]
  }, $data.users[1] ? common_vendor.e({
    E: $data.users[1].privacy == 1
  }, $data.users[1].privacy == 1 ? {
    F: common_vendor.t($data.users[1].username[0])
  } : {
    G: common_vendor.t($data.users[1].username)
  }, {
    H: common_vendor.t($data.users[1].address),
    I: common_vendor.t($data.users[1].school),
    J: common_vendor.t($data.users[1].score)
  }) : {}, {
    K: common_assets._imports_1$1,
    L: $data.user1_url
  }, $data.user1_url ? {
    M: $data.user1_url
  } : {}, {
    N: common_assets._imports_3$1,
    O: $data.users[0]
  }, $data.users[0] ? common_vendor.e({
    P: $data.users[0].privacy == 1
  }, $data.users[0].privacy == 1 ? {
    Q: common_vendor.t($data.users[0].username[0])
  } : {
    R: common_vendor.t($data.users[0].username)
  }, {
    S: common_vendor.t($data.users[0].address),
    T: common_vendor.t($data.users[0].school),
    U: common_vendor.t($data.users[0].score)
  }) : {}, {
    V: common_assets._imports_1$1,
    W: $data.user3_url
  }, $data.user3_url ? {
    X: $data.user3_url
  } : {}, {
    Y: common_assets._imports_4$1,
    Z: $data.users[2]
  }, $data.users[2] ? common_vendor.e({
    aa: $data.users[2].privacy == 1
  }, $data.users[2].privacy == 1 ? {
    ab: common_vendor.t($data.users[2].username[0])
  } : {
    ac: common_vendor.t($data.users[2].username)
  }, {
    ad: common_vendor.t($data.users[2].address),
    ae: common_vendor.t($data.users[2].school),
    af: common_vendor.t($data.users[2].score)
  }) : {}, {
    ag: common_vendor.p({
      width: "20rpx"
    }),
    ah: common_vendor.p({
      width: "20rpx"
    }),
    ai: common_vendor.p({
      width: "20rpx"
    }),
    aj: common_vendor.o($options.active_instruction),
    ak: common_vendor.p({
      name: "question-circle",
      color: "#F25C07",
      size: "27"
    }),
    al: common_vendor.p({
      width: "20rpx"
    }),
    am: common_vendor.p({
      width: "20rpx"
    }),
    an: common_vendor.f($data.users, (user_x, index, i0) => {
      return common_vendor.e({
        a: user_x.id == $data.user.id
      }, user_x.id == $data.user.id ? {
        b: common_vendor.t($data.ids[index]),
        c: "f6ab0491-13-" + i0 + "," + ("f6ab0491-12-" + i0)
      } : {
        d: common_vendor.t($data.ids[index]),
        e: "f6ab0491-14-" + i0 + "," + ("f6ab0491-12-" + i0)
      }, {
        f: user_x.id == $data.user.id
      }, user_x.id == $data.user.id ? {
        g: common_vendor.t(user_x.username),
        h: "f6ab0491-15-" + i0 + "," + ("f6ab0491-12-" + i0)
      } : common_vendor.e({
        i: user_x.privacy == 1
      }, user_x.privacy == 1 ? {
        j: common_vendor.t(user_x.username[0])
      } : user_x.username.length >= 7 ? {
        l: common_vendor.t(user_x.username.slice(0, 7))
      } : {
        m: common_vendor.t(user_x.username)
      }, {
        k: user_x.username.length >= 7,
        n: "f6ab0491-16-" + i0 + "," + ("f6ab0491-12-" + i0)
      }), {
        o: user_x.id == $data.user.id
      }, user_x.id == $data.user.id ? {
        p: common_vendor.t(user_x.gender),
        q: "f6ab0491-17-" + i0 + "," + ("f6ab0491-12-" + i0)
      } : {
        r: common_vendor.t(user_x.gender),
        s: "f6ab0491-18-" + i0 + "," + ("f6ab0491-12-" + i0)
      }, {
        t: user_x.id == $data.user.id
      }, user_x.id == $data.user.id ? {
        v: common_vendor.t(user_x.active),
        w: "f6ab0491-19-" + i0 + "," + ("f6ab0491-12-" + i0)
      } : {
        x: common_vendor.t(user_x.active),
        y: "f6ab0491-20-" + i0 + "," + ("f6ab0491-12-" + i0)
      }, {
        z: user_x.score == 0
      }, user_x.score == 0 ? {
        A: "f6ab0491-21-" + i0 + "," + ("f6ab0491-12-" + i0)
      } : {
        B: common_vendor.t(user_x.score),
        C: "f6ab0491-22-" + i0 + "," + ("f6ab0491-12-" + i0)
      }, {
        D: index,
        E: "f6ab0491-12-" + i0 + ",f6ab0491-4"
      });
    }),
    ao: common_vendor.p({
      stripe: true,
      emptyText: "无数据"
    }),
    ap: common_vendor.p({
      ["current-page"]: 2
    })
  });
}
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["render", _sfc_render], ["__scopeId", "data-v-f6ab0491"]]);
wx.createPage(MiniProgramPage);
