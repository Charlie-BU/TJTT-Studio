"use strict";
const common_vendor = require("../../common/vendor.js");
const common_assets = require("../../common/assets.js");
const _sfc_main = {
  props: {
    currentPage: {
      type: Number,
      default: 0,
      show: false
    }
  },
  data() {
    return {
      currentItem: 0,
      tabbarList: [
        {
          id: 0,
          path: "/pages/index/index",
          icon: "/static/tabbar/home.png",
          selectIcon: "/static/tabbar/Ahome.png",
          text: "",
          centerItem: false
        },
        {
          id: 1,
          path: "/pages/apps/index",
          icon: "/static/tabbar/shop.png",
          selectIcon: "/static/tabbar/Ashop.png",
          text: "",
          centerItem: false
        },
        {
          id: 2,
          path: "/pages/score-ranking/index",
          icon: "/static/tabbar/g.png",
          selectIcon: "/static/tabbar/g.png",
          text: "",
          centerItem: true
        },
        {
          id: 3,
          path: "/pages/community/index",
          icon: "/static/tabbar/lis.png",
          selectIcon: "/static/tabbar/list.png",
          text: "",
          centerItem: false
        },
        {
          id: 4,
          path: "/pages/my/index",
          icon: "/static/tabbar/my.png",
          selectIcon: "/static/tabbar/Amy.png",
          text: "",
          centerItem: false
        }
      ]
    };
  },
  mounted() {
    this.currentItem = this.currentPage;
  },
  computed: {
    shopNum() {
    },
    flagShow() {
      return false;
    }
  },
  methods: {
    NavChange(e) {
      common_vendor.index.switchTab({
        url: e
      });
    }
  }
};
function _sfc_render(_ctx, _cache, $props, $setup, $data, $options) {
  return common_vendor.e({
    a: $props.currentPage == 0,
    b: common_assets._imports_0,
    c: $props.currentPage != 0,
    d: common_assets._imports_1,
    e: common_vendor.n($props.currentPage == 0 ? "text-blue  " : "text-gray"),
    f: common_vendor.o(($event) => $options.NavChange("/pages/index/index")),
    g: $props.currentPage == 3,
    h: common_assets._imports_2,
    i: $props.currentPage != 3,
    j: common_assets._imports_3,
    k: common_vendor.n($props.currentPage == 3 ? "text-blue" : "text-gray"),
    l: common_vendor.o(($event) => $options.NavChange("/pages/community/index")),
    m: common_assets._imports_4,
    n: common_vendor.n($props.currentPage == 2 ? "text-blue" : "text-gray"),
    o: common_vendor.o(($event) => $options.NavChange("/pages/score-ranking/index")),
    p: $options.flagShow
  }, $options.flagShow ? {
    q: common_vendor.t($options.shopNum)
  } : {}, {
    r: $props.currentPage == 1,
    s: common_assets._imports_5,
    t: $props.currentPage != 1,
    v: common_assets._imports_6,
    w: common_vendor.n($props.currentPage == 1 ? "text-blue" : "text-gray"),
    x: common_vendor.o(($event) => $options.NavChange("/pages/apps/index")),
    y: $props.currentPage == 4,
    z: common_assets._imports_7,
    A: $props.currentPage != 4,
    B: common_assets._imports_8,
    C: common_vendor.n($props.currentPage == 4 ? "text-blue" : "text-gray"),
    D: common_vendor.o(($event) => $options.NavChange("/pages/my/index"))
  });
}
const Component = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["render", _sfc_render], ["__scopeId", "data-v-0e399a7b"]]);
wx.createComponent(Component);
