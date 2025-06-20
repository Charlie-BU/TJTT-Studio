"use strict";
const common_vendor = require("../../common/vendor.js");
const static_js_login_check = require("../../static/js/login_check.js");
const static_js_magic_power = require("../../static/js/magic_power.js");
const _sfc_main = {
  data() {
    return {
      user: "",
      standard_list: [
        {
          name: "TJTT积分标准"
        },
        {
          name: "TJTT积分预估值参考"
        }
      ],
      current: 0,
      rules: [
        {
          difference: "0-12",
          high_win_low: 8,
          low_win_high: 8
        },
        {
          difference: "13-37",
          high_win_low: 7,
          low_win_high: 10
        },
        {
          difference: "38-62",
          high_win_low: 6,
          low_win_high: 13
        },
        {
          difference: "63-87",
          high_win_low: 5,
          low_win_high: 16
        },
        {
          difference: "88-112",
          high_win_low: 4,
          low_win_high: 20
        },
        {
          difference: "113-137",
          high_win_low: 3,
          low_win_high: 25
        },
        {
          difference: "138-162",
          high_win_low: 2,
          low_win_high: 30
        },
        {
          difference: "163-187",
          high_win_low: 2,
          low_win_high: 35
        },
        {
          difference: "188-212",
          high_win_low: 1,
          low_win_high: 40
        },
        {
          difference: "213-237",
          high_win_low: 1,
          low_win_high: 45
        },
        {
          difference: "238以上",
          high_win_low: 0,
          low_win_high: 50
        }
      ],
      standards: [
        { score: "400", description: "刚开始打乒乓球。" },
        { score: "600", description: "很有限的打球经验，主要练习能够打到球。" },
        { score: "800", description: "需要打球经验，有明显的击球弱点，能打一些和平球，发一些和平球。" },
        { score: "1000", description: "开始学习判断球的旋转，对球的控制能力弱，能打一些速度、力量一般的球。" },
        { score: "1200", description: "能协调地回击中速球，能简单的使用搓、推、挡、攻等各种击球方法，但缺乏较好方向性、力度和旋转的控制，能发一些有力度和旋转球。" },
        { score: "1400", description: "对来球的旋转性和方向性有一定的判断，球的控制能力有提高，能较熟练的使用搓、推、挡、攻等各种击球方法，发球有一些落点、旋转、速度的变化。" },
        { score: "1600", description: "正反手击球较稳定，方向感较好。基本掌握前冲弧圈球、高吊弧圈球的区别，对不同打法有一定的了解，熟练掌握3套以上的发球方法，接发球判断较好。" },
        { score: "1800", description: "熟练运用击球力量、速度、旋转的变化，开始注意步法；了解反胶、长胶、生胶、正胶的不同特点。针对不同的对手采用不同的战术打法，回球落点好，能连续进攻，已经形成自己的打法特点。利用发球为自己创造进攻机会或直接得分，在对手不易判断、用近乎相同的发球动作发出上下旋转变化的球。" },
        { score: "2000", description: "有很好的球感、手感和判断力，经常能在比赛中打出精彩的对攻回合球来。经常使用摆、晃、切、挑、挤、弹、抹、快带等技术，能迅速洞悉对手的弱点，及时调整战术，发挥自己的特长和优势。" },
        { score: "2200", description: "形成了以速度、技巧、力量和顽强作风作为取胜法宝的风格。在比赛中变化不同的战术，在有压力的情况下仍能稳定地发挥水平，曾接受过一定专业训练，参加过省级水平的比赛。" },
        { score: "2400", description: "经过专业强化训练，参加国家级水平的比赛，并有国家定义的运动员级别。" },
        { score: "2600", description: "参加规模较小的世界范围内的锦标赛，有合适的机会便会跃升到下一级。" },
        { score: "2800", description: "世界级选手，经常参加国际级的比赛，主要收入来自于比赛的奖金。" },
        { score: "3000", description: "奥运冠军、世乒赛单打冠军选手。" }
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
  },
  methods: {
    back() {
      common_vendor.index.navigateBack({
        delta: 1
      });
    },
    change(index) {
      this.current = index;
    }
  }
};
if (!Array) {
  const _easycom_u_tabs2 = common_vendor.resolveComponent("u-tabs");
  const _easycom_uni_th2 = common_vendor.resolveComponent("uni-th");
  const _easycom_uni_tr2 = common_vendor.resolveComponent("uni-tr");
  const _easycom_uni_td2 = common_vendor.resolveComponent("uni-td");
  const _easycom_uni_table2 = common_vendor.resolveComponent("uni-table");
  (_easycom_u_tabs2 + _easycom_uni_th2 + _easycom_uni_tr2 + _easycom_uni_td2 + _easycom_uni_table2)();
}
const _easycom_u_tabs = () => "../../uni_modules/vk-uview-ui/components/u-tabs/u-tabs.js";
const _easycom_uni_th = () => "../../uni_modules/uni-table/components/uni-th/uni-th.js";
const _easycom_uni_tr = () => "../../uni_modules/uni-table/components/uni-tr/uni-tr.js";
const _easycom_uni_td = () => "../../uni_modules/uni-table/components/uni-td/uni-td.js";
const _easycom_uni_table = () => "../../uni_modules/uni-table/components/uni-table/uni-table.js";
if (!Math) {
  (_easycom_u_tabs + _easycom_uni_th + _easycom_uni_tr + _easycom_uni_td + _easycom_uni_table)();
}
function _sfc_render(_ctx, _cache, $props, $setup, $data, $options) {
  return common_vendor.e({
    a: common_vendor.o($options.change),
    b: common_vendor.p({
      list: $data.standard_list,
      ["bg-color"]: "null",
      ["active-color"]: "#F25C07",
      ["font-size"]: "20rpx",
      ["is-scroll"]: "true",
      current: $data.current
    }),
    c: $data.current == 0
  }, $data.current == 0 ? {
    d: common_vendor.p({
      width: "20rpx"
    }),
    e: common_vendor.p({
      width: "20rpx"
    }),
    f: common_vendor.p({
      width: "20rpx"
    }),
    g: common_vendor.f($data.rules, (rule, index, i0) => {
      return {
        a: common_vendor.t(rule.difference),
        b: "9e239910-7-" + i0 + "," + ("9e239910-6-" + i0),
        c: common_vendor.t(rule.high_win_low),
        d: "9e239910-8-" + i0 + "," + ("9e239910-6-" + i0),
        e: common_vendor.t(rule.low_win_high),
        f: "9e239910-9-" + i0 + "," + ("9e239910-6-" + i0),
        g: index,
        h: "9e239910-6-" + i0 + ",9e239910-1"
      };
    }),
    h: common_vendor.p({
      stripe: true,
      emptyText: "无数据"
    })
  } : {}, {
    i: $data.current == 1
  }, $data.current == 1 ? {
    j: common_vendor.f($data.standards, (standard, index, i0) => {
      return {
        a: common_vendor.t(standard.score),
        b: "9e239910-15-" + i0 + "," + ("9e239910-14-" + i0),
        c: common_vendor.t(standard.description),
        d: "9e239910-16-" + i0 + "," + ("9e239910-14-" + i0),
        e: index,
        f: "9e239910-14-" + i0 + ",9e239910-10"
      };
    }),
    k: common_vendor.p({
      stripe: true,
      emptyText: "无数据"
    })
  } : {});
}
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["render", _sfc_render], ["__scopeId", "data-v-9e239910"]]);
wx.createPage(MiniProgramPage);
