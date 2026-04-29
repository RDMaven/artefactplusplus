import { onScreenLog } from './log.js';
import { sendWSMessage } from './ws.js';

/* ===================================================== */
/* Move Commands (ROBOT, CAMERA) ======================= */
/* ===================================================== */

const STOP = { l: 0, r: 0 };

// ROBOT conmmands and state variable
var robotCurrentMoveInput = STOP;
let activeButton = null;

function sendMove(l, r) {
  if (robotCurrentMoveInput.l === l && robotCurrentMoveInput.r === r) return;
  sendWSMessage("move", l, r);
  robotCurrentMoveInput = { l, r };
}

export function stopMove() {
    if (robotCurrentMoveInput.l === 0 && robotCurrentMoveInput.r === 0) onScreenLog("Robot is not moving.", "success");
    sendMove(0, 0);
    activeButton = null;
    $(".controls-container button").removeClass("active");
}

// CAMERA commands and state variable
var cameraCurrentMoveInput = STOP;

function sendMoveCam(l, r) {
  if (cameraCurrentMoveInput.l === l && cameraCurrentMoveInput.r === r) return;
  sendWSMessage("move_cam", l, r);
  cameraCurrentMoveInput = { l, r };
}

export function stopMoveCam() {
    if (robotCurrentMoveInput.l === 0 && robotCurrentMoveInput.r === 0) onScreenLog("Robot is not moving.", "success");
    sendMoveCam(0, 0);
}


/* ===================================================== */
/* ONSCREEN BUTTONS MAPPING ============================ */
/* ===================================================== */
// Control mappings
const controls = {
  '#controls-rotate-left':  [-1,  1],
  '#controls-rotate-right': [ 1, -1],
  '#controls-up':           [ 1,  1],
  '#controls-down':         [-1, -1],
  '#controls-left':         [ 0,  1],
  '#controls-right':        [ 1,  0],
};

// Toggle logic
Object.entries(controls).forEach(([selector, [l, r]]) => {
  $(selector).on("click", function () {

    if (activeButton === this) {
      stopMove();
      return;
    }

    activeButton = this;

    $(".controls-container button").removeClass("active");
    $(this).addClass("active");

    sendMove(l, r);
  });
});

// !! BY DESIGN, no onscreen button for the camera, 
// but a helper message for the keyboard mapping instead.


/* ===================================================== */
/* KEYBORAD MAPPING ==================================== */
/* ===================================================== */
// Source - https://stackoverflow.com/a/16345983

const keyAction = {
  // ROBOT
  z: { keydown: () => sendMove( 1,  1),  keyup: stopMove },
  q: { keydown: () => sendMove( 1,  0),  keyup: stopMove },
  s: { keydown: () => sendMove(-1, -1),  keyup: stopMove },
  d: { keydown: () => sendMove( 0,  1),  keyup: stopMove },
  a: { keydown: () => sendMove(-1,  1),  keyup: stopMove },
  e: { keydown: () => sendMove( 1, -1),  keyup: stopMove },
  x: { keydown: stopMove},
  Escape: { keydown: stopMove },

  // CAMERA
  ArrowUp:    { keydown: () => sendMoveCam(  1,  1) },
  ArrowLeft:  { keydown: () => sendMoveCam(  1,  0) },
  ArrowDown:  { keydown: () => sendMoveCam( -1, -1) },
  ArrowRight: { keydown: () => sendMoveCam(  0,  1) },
  o: { keydown: stopMoveCam }
  
};

const keyHandler = (ev) => {
  if (ev.repeat) return;                             
  if (!(ev.key in keyAction) || !(ev.type in keyAction[ev.key])) return;
  keyAction[ev.key][ev.type]();
};

['keydown', 'keyup'].forEach((evType) => {
  document.body.addEventListener(evType, keyHandler);
});




/* ===================================================== */
/* Archive ============================================= */
/* ===================================================== */

// import VirtualJoystick from "./imports/virtual-joystick.js";

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