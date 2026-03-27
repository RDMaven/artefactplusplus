// import VirtualJoystick from "./imports/virtual-joystick.js";
import { sendWSMessage } from './ws.js';


/* ===================================================== */
/* JOYSTICK CREATION =================================== */
/* ===================================================== */
// const joystickContainer = document.querySelector('.joystick');
// const joystick = new VirtualJoystick(joystickContainer, {
//   // width: 80,
//   // height: 80,
//   color: "gray",
//   handleColor: "white",
//   handleRadius: 25,
//   onChange: (data) => {
//     updateJoystickValues(data);
//   },
//   onStart: null,
//   onEnd: null,
//   sensitivity: 1,
//   boundaries: true,
//   autoCenter: true,
//   deadzone: 0.1,
//   shape: "circle",
//   mode: "static", // 'static' or 'dynamic'
//   lockAxis: null, // null, 'x', or 'y'
//   zones: [],
//   vibration: true,
//   theme: {
//     base: {
//       background: "rgba(70, 70, 70, 0.5)",
//       border: "3px solid rgba(0, 0, 0, 0.8)",
//       shadow: "0 0 10px rgba(0, 0, 0, 0.3)",
//     },
//     handle: {
//       background: "rgba(255, 255, 255, 0.9)",
//       border: "2px solid rgba(0, 0, 0, 0.8)",
//       shadow: "0 0 5px rgba(0, 0, 0, 0.5)",
//     },
//   },
//   keyboardEmulation: {
//     enabled: false,
//     map: {
//       up: "ArrowUp",
//       down: "ArrowDown",
//       left: "ArrowLeft",
//       right: "ArrowRight",
//     },
//   },
//   maxMoveRadius: null,
// });

// // To make sure the joystick has the right dimentions on display
// window.dispatchEvent(new Event('resize'));

// // WS x Joystick : Update and Send joystick data to server
// var lastX = null;
// var lastY = null;

// function updateJoystickValues(data) {

//   // Update overlay stats in index.html
//   const statX = document.getElementById("stat-x");
//   const statY = document.getElementById("stat-y");
//   const x = +data.delta.x.toFixed(1);
//   const y = +data.delta.y.toFixed(1);
  
//     // If both values are unchanged, do nothing
//   if (x === lastX && y === lastY) return;

//   lastX = x;
//   lastY = y;

//   sendWSMessage("move", x, y);

//   if (statX) statX.textContent = data.delta.x.toFixed(2);
//   if (statY) statY.textContent = data.delta.y.toFixed(2);

// }

/* ===================================================== */
/* CONTROLS CREATION =================================== */
/* ===================================================== */
const STOP = { l: 0, r: 0 };
var currentMove = STOP;
let activeButton = null;

function sendMove(l, r) {
  if (currentMove.l === l && currentMove.r === r) return;
  sendWSMessage("move", l, r);
  currentMove = { l, r };
}

export function stopMove() {
    sendMove(0, 0);
    activeButton = null;
    $(".controls-container button").removeClass("active");
}

// --- Control mappings ---
const controls = {
  '#controls-rotate-left':  [-1,  1],
  '#controls-rotate-right': [ 1, -1],
  '#controls-up':           [ 1,  1],
  '#controls-down':         [-1, -1],
  '#controls-left':         [ 0,  1],
  '#controls-right':        [ 1,  0],
};

// --- Toggle logic ---
Object.entries(controls).forEach(([selector, [l, r]]) => {
  $(selector).on("click", function () {

    if (activeButton === this) {
      stopMove();
      return;
    }

    // Otherwise activate new movement
    activeButton = this;

    $(".controls-container button").removeClass("active");
    $(this).addClass("active");

    sendMove(l, r);
  });
});

// --- Keyboard mappings ---
const keyMap = {
  KeyW: [ 1,  1],
  KeyA: [ 1,  0],
  KeyS: [-1, -1],
  KeyD: [ 0,  1],
  KeyQ: [-1,  1],
  KeyE: [ 1, -1],
};

window.addEventListener("keydown", (e) => {
  const move = keyMap[e.code];
  if (move) sendMove(...move);
});

window.addEventListener("keyup", stopMove);


