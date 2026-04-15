
import { onScreenLog, consoleClear } from './log.js';
import { ws, sendWSMessage } from './ws.js';
import { stopMove } from './manual-control.js';


/* ===================================================== */
/* WEBSOCKET FUNCTIONNALITIES ========================== */
/* ===================================================== */

// WS TESTER - Event listener
$('#ws-test-button').on("click", () => {
  ws.send("Hello from JS");
})


// STOP Button (TODO)


// Mode switch Button
var currentMode = 'Manual';

$("#btnMode").on("change", function () {
  currentMode = 'Manual';
  if ($(this).is(":checked")) {

    // Message de confirmation
    if (!confirm("Are you sure you want to switch to Auto mode?")) {
      
      $(this).prop("checked", false); // revert toggle
      return;
    }
    stopMove();
    currentMode = 'Auto';
  }
  sendWSMessage("set_parameter", "mode", currentMode.toLowerCase());
  onScreenLog(`Switched to ${currentMode} Mode`, "error");

});


/* ===================================================== */
/* OTHER FUNCTIONNALITIES ============================== */
/* ===================================================== */

// Change the theme on mode toggle...
$('#btnMode').on('change', function () {
  $('body').toggleClass('light-mode');
  $('.controls-container').toggle();

});

// Console Clear event listener (requires ws state, so thats why its in app.js and not log.js, sorry):
$(".console-btn").on("click", function () {
  consoleClear(ws.readyState);
})


