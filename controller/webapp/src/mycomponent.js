
var m = require("mithril")
// import range from 'mithril-range'

var range = require('mithril-range').default

let myValue = 10


function set_program(value) {
  console.log("Program is:", value)
  m.request({
    method: "POST",
    url: "/",
    data: {
      "program": value,
    }
  })
}
function set_speed(value) {
  console.log("Speed is:", value)
  m.request({
    method: "POST",
    url: "/",
    data: {
      "speed": value,
    }
  })
}
function set_mode(value) {
  console.log("Mode is:", value)
  m.request({
    method: "POST",
    url: "/",
    data: {
      "direction": value,
    }
  })
}

module.exports = {
    view: function() {return [
      m("button", {onclick: function () {set_mode("left")}}, "Left"),
      m("button", {onclick: function () {set_mode("right")}}, "Right"),
      m("button", {onclick: function () {set_mode("up")}}, "Up"),
      m("button", {onclick: function () {set_mode("down")}}, "Down"),
      m(range, {
        min: 1,
        max: 50,
        step: 1,
        value: myValue,
        class: 'app-range',
        onchange: value => {
          myValue = value
        },
        ondrag: value => {
          myValue = value
          // console.log("Value: ", myValue)
          set_speed(value)
          return false  // Can prevent m.redraw
        }
      }),
      m("br"),
      m("button", {onclick: function () {set_program("rb")}}, "Rainbow"),
      m("br"),
      m("button", {onclick: function () {set_program("fall")}}, "Waterfall"),
      m("br"),
      m("button", {onclick: function () {set_program("bounce")}}, "Bounce"),
      m("br"),
      m("button", {onclick: function () {set_program("wave")}}, "Wave"),
      m("br"), m("br"),
      m("button", {onclick: function () {set_program("random")}}, "random"),
    ]}
}
