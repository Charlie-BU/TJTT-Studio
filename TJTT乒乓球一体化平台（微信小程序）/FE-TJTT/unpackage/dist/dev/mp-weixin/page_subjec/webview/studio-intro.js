"use strict";
const common_vendor = require("../../common/vendor.js");
const _sfc_main = {
  data() {
    return {
      webviewStyles: {
        progress: {
          color: "#FF3333"
        }
      },
      url: "https://docs.qq.com/aio/DZHd6Y2pBR3JQemV4"
    };
  },
  onLoad() {
  },
  methods: {}
};
function _sfc_render(_ctx, _cache, $props, $setup, $data, $options) {
  return {
    a: $data.webviewStyles,
    b: $data.url,
    c: common_vendor.o((...args) => _ctx.getMessage && _ctx.getMessage(...args))
  };
}
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["render", _sfc_render]]);
wx.createPage(MiniProgramPage);
