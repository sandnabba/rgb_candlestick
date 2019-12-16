var m = require("mithril")

// var iro = require('@jaames/iro');

function set_color(value) {
  console.log("Color is:", value.rgb)
  m.request({
    method: "POST",
    url: "/api/color",
    data: {
      "color": value.rgb,
    }
  })
}

function init_picker(vnode) {
  console.log("Hello")
  var colorPicker2 = new iro.ColorPicker("#test")
  colorPicker2.on("color:change", set_color)
}

module.exports = {
  view: function(vnode) {return [
    m("div", {id: "test"}),
    m("script", {src: "https://cdn.jsdelivr.net/npm/@jaames/iro/dist/iro.min.js", onload: function() {init_picker(vnode.attrs.pos)}})
  ]}
}
