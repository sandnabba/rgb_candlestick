var m = require("mithril")

// var iro = require('@jaames/iro');

var last_time = Date.now()

function set_color(value) {
  current_time = Date.now()
  // console.log("Color is:", value.rgb)
  if ((current_time - last_time) > 100) {
    m.request({
      method: "POST",
      url: "/api/color",
      data: {
        "color": value.rgb,
      }
    })
    last_time = current_time
  } else {
    console.log("Wait a few more milli-seconds")
  }
}

function init_picker(vnode) {
  var colorPicker2 = new iro.ColorPicker("#test")
  colorPicker2.on("color:change", set_color)
}

module.exports = {
  view: function(vnode) {return [
    m("div", {id: "test"}),
    m("script", {src: "https://cdn.jsdelivr.net/npm/@jaames/iro/dist/iro.min.js", onload: function() {init_picker(vnode.attrs.pos)}})
  ]}
}
