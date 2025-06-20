"use strict";
const common_vendor = require("../../../common/vendor.js");
const _sfc_main = {
  data() {
    return {
      StatusBar: this.StatusBar,
      CustomBar: this.CustomBar
    };
  },
  name: "cu-custom",
  computed: {
    style() {
      var StatusBar = this.StatusBar;
      var CustomBar = this.CustomBar;
      var bgImage = this.bgImage;
      var style = `height:${CustomBar}px;padding-top:${StatusBar}px;`;
      if (this.bgImage) {
        style = `${style}background-image:url(${bgImage});`;
      }
      return style;
    }
  },
  props: {
    bgColor: {
      type: String,
      default: ""
    },
    isBack: {
      type: [Boolean, String],
      default: false
    },
    bgImage: {
      type: String,
      default: ""
    }
  },
  methods: {
    BackPage() {
      common_vendor.index.navigateBack({
        delta: 1
      });
    }
  }
};
function _sfc_render(_ctx, _cache, $props, $setup, $data, $options) {
  return common_vendor.e({
    a: $props.isBack
  }, $props.isBack ? {
    b: common_vendor.o((...args) => $options.BackPage && $options.BackPage(...args))
  } : {}, {
    c: common_vendor.s({
      top: $data.StatusBar + "px"
    }),
    d: common_vendor.s($options.style),
    e: common_vendor.n($props.bgImage != "" ? "none-bg text-white bg-img" : ""),
    f: common_vendor.n($props.bgColor),
    g: common_vendor.s({
      height: $data.CustomBar + "px"
    })
  });
}
const Component = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["render", _sfc_render]]);
wx.createComponent(Component);
