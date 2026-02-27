
import { onScreenLog, consoleClear } from './log.js';
import { ws } from './ws.js';

// WS : bouton de test
$('#ws-test-button').on("click", () => {
    ws.send("Hello from JS");
})


// WS : controle manuel des robots
const directions = {
    up:    [ 0,  1],
    down:  [ 0, -1],
    left:  [-1,  0],
    right: [ 1,  0]
};

$.each(directions, function(direction, [x, y]) {
    $(`#arrow-${direction}`).on('click', function() {
        ws.send(JSON.stringify({ event: 'move', x, y }));
    });
});


// Toggle button

$(document).ready(function () {

  $("#btnMode").on("change", function () {
    var current_mode = 'Manual';
    if ($(this).is(":checked")) {

      if (!confirm("Are you sure you want to switch to Auto mode? (*FLASHBANG INCOMING*")) {
        $(this).prop("checked", false); // revert toggle
        return;
      }
      current_mode = 'Auto';

    } else {
    }
    onScreenLog(`Switched to ${current_mode} Mode`, "error");

  });

});


$('#btnMode').on('change', function() {
  $('body').toggleClass('light-mode');
});

// Console Clear event listener (requires ws state):
$(".console-btn").on("click", function () {
    consoleClear(ws.readyState);
})
