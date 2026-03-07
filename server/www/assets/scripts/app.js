
import { onScreenLog, consoleClear } from './log.js';
import { ws, sendWSMessage } from './ws.js';
import VirtualJoystick from "./imports/virtual-joystick.js";


/* ===================================================== */
/* JOYSTICK CREATION =================================== */
/* ===================================================== */
const joystickContainer = document.querySelector('.joystick');
const joystick = new VirtualJoystick(joystickContainer, {
  // width: 80,
  // height: 80,
  color: "gray",
  handleColor: "white",
  handleRadius: 25,
  onChange: (data) => {
    updateJoystickValues(data);
  },
  onStart: null,
  onEnd: null,
  sensitivity: 1,
  boundaries: true,
  autoCenter: true,
  deadzone: 0.1,
  shape: "circle",
  mode: "static", // 'static' or 'dynamic'
  lockAxis: null, // null, 'x', or 'y'
  zones: [],
  vibration: true,
  theme: {
    base: {
      background: "rgba(70, 70, 70, 0.5)",
      border: "3px solid rgba(0, 0, 0, 0.8)",
      shadow: "0 0 10px rgba(0, 0, 0, 0.3)",
    },
    handle: {
      background: "rgba(255, 255, 255, 0.9)",
      border: "2px solid rgba(0, 0, 0, 0.8)",
      shadow: "0 0 5px rgba(0, 0, 0, 0.5)",
    },
  },
  keyboardEmulation: {
    enabled: false,
    map: {
      up: "ArrowUp",
      down: "ArrowDown",
      left: "ArrowLeft",
      right: "ArrowRight",
    },
  },
  maxMoveRadius: null,
});

// To make sure the joystick has the right dimentions on display
window.dispatchEvent(new Event('resize'));


/* ===================================================== */
/* WEBSOCKET FUNCTIONNALITIES ========================== */
/* ===================================================== */

// WS TESTER - Event listener
$('#ws-test-button').on("click", () => {
  ws.send("Hello from JS");
})

// WS x Joystick : Update and Send joystick data to server
var lastX = null;
var lastY = null;

function updateJoystickValues(data) {

  // Update overlay stats in index.html
  const statX = document.getElementById("stat-x");
  const statY = document.getElementById("stat-y");
  const x = +data.delta.x.toFixed(1);
  const y = +data.delta.y.toFixed(1);
  
    // If both values are unchanged, do nothing
  if (x === lastX && y === lastY) return;

  lastX = x;
  lastY = y;

  sendWSMessage("move", x, y);

  if (statX) statX.textContent = data.delta.x.toFixed(2);
  if (statY) statY.textContent = data.delta.y.toFixed(2);

}

// STOP Button (TODO)


// Mode switch Button
var currentMode = 'Manual';

$("#btnMode").on("change", function () {
  currentMode = 'Manual';
  if ($(this).is(":checked")) {

    // Message de confirmation
    if (!confirm("Are you sure you want to switch to Auto mode? (*FLASHBANG INCOMING*")) {
      $(this).prop("checked", false); // revert toggle
      return;
    }
    currentMode = 'Auto';
  }
  sendWSMessage("mode", currentMode.toLowerCase());
  onScreenLog(`Switched to ${currentMode} Mode`, "error");

});


/* ===================================================== */
/* OTHER FUNCTIONNALITIES ============================== */
/* ===================================================== */

// Change the theme on mode toggle...
$('#btnMode').on('change', function () {
  $('body').toggleClass('light-mode');
  $('.joystick-container').toggle();

});

// Console Clear event listener (requires ws state, so thats why its in app.js and not log.js, sorry):
$(".console-btn").on("click", function () {
  consoleClear(ws.readyState);
})


