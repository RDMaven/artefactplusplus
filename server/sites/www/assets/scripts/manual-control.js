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

function sendMoveCam(d, l) { // d = down, l = left
  // if (cameraCurrentMoveInput.d === d && cameraCurrentMoveInput.l === l) return;
  sendWSMessage("move_cam", d, l);
  cameraCurrentMoveInput = { d, l };
}

export function stopMoveCam() {
    if (robotCurrentMoveInput.d === 0 && robotCurrentMoveInput.l === 0) onScreenLog("Robot is not moving.", "success");
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
  ArrowUp:    { keydown: () => sendMoveCam( -1,  0) },
  ArrowLeft:  { keydown: () => sendMoveCam(  0, -1) },
  ArrowDown:  { keydown: () => sendMoveCam(  1,  0) },
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
