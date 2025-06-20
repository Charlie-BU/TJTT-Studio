"use strict";
function get_time_now() {
  const date = /* @__PURE__ */ new Date();
  const year = date.getFullYear().toString().padStart(4, "0");
  const month = (date.getMonth() + 1).toString().padStart(2, "0");
  const day = date.getDate().toString().padStart(2, "0");
  const hour = date.getHours().toString().padStart(2, "0");
  const timecode = year + month + day + hour;
  return timecode;
}
function magic() {
  const timecode = get_time_now();
  const daycode = timecode.slice(0, -2);
  if (timecode === "20240906xx" || timecode === "20240906xx" || timecode === "20240906xx" || timecode === "20240906xx") {
    return true;
  } else if (daycode === "2024091x") {
    return true;
  } else {
    return false;
  }
}
exports.magic = magic;
