
import { onScreenLog, consoleClear } from './log.js';
import { ws, sendWSMessage, MAPS } from './ws.js';
import { stopMove } from './manual-control.js';


/* ===================================================== */
/* WEBSOCKET FUNCTIONNALITIES ========================== */
/* ===================================================== */

// WS TESTER - Event listener
$('#ws-test-button').on("click", () => {
  ws.send("Hello from JS");
})

// Mode switch Button
var currentMode = 'manual';

$("#btnMode").on("change", function () {
  currentMode = 'manual';
  if ($(this).is(":checked")) {

    // Message de confirmation
    if (!confirm("Are you sure you want to switch to Auto mode?")) {

      $(this).prop("checked", false); // revert toggle
      return;
    }
    stopMove();
    currentMode = 'auto';
  }
  sendWSMessage("set_parameter", "mode", currentMode.toLowerCase());
  onScreenLog(`Switched to ${currentMode} Mode`, "error");

});

// Lancer les prompt pour lancer un mode auto traque ou carto
$("#btnMode").on("change", function () {
  if (currentMode == 'auto') {
    async function lancerConfiguration() {

      // Choix du mode
      const { value: mode } = await Swal.fire({
        title: 'Choisir un mode',
        input: 'select',
        inputOptions: {
          traque: 'Traque',
          cartographie: 'Cartographie'
        },
        inputPlaceholder: 'Sélectionner un mode',
        showCancelButton: true
      });

      if (!mode) return;

      // Mode traque
      if (mode === 'traque') {
        const result = await Swal.fire({
          title: 'Mode traque',
          text: 'Confirmer ?',
          icon: 'question',
          showCancelButton: true,
          confirmButtonText: 'Confirmer'
        });

        if (result.isConfirmed) {
          sendWSMessage("set_parameter", "automode", mode);
        }
        return;
      }

      // sendWSMessage("set_parameter", "automode", mode);

      
      // Mode cartographie
      const { value: fichierCarte } = await Swal.fire({
        title: 'Choisir le fichier carte',
        input: 'select',
        inputOptions: MAPS,
        showCancelButton: true
      });

      if (!fichierCarte) return;

      const { value: positionDepart } = await Swal.fire({
        title: 'Choisir la position de départ',
        input: 'select',
        inputOptions: {
          nord: 'Nord',
          sud: 'Sud',
          est: 'Est',
          ouest: 'Ouest'
        },
        showCancelButton: true
      });

      if (!positionDepart) return;

      const confirmation = await Swal.fire({
        title: 'Confirmer la configuration ?',
        html: `
      <b>Carte :</b> ${fichierCarte}<br>
      <b>Position :</b> ${positionDepart}
    `,
        icon: 'question',
        showCancelButton: true,
        confirmButtonText: 'Confirmer'
      });

      if (confirmation.isConfirmed) {
        console.log({
          mode: 'cartographie',
          fichierCarte,
          positionDepart
        });
      }
    }

    lancerConfiguration();



  }
})

var currentCaptureMode = "False";

$("#btnCapture").on("change", function () {
  currentCaptureMode = "False";
  if ($(this).is(":checked")) {

    // Message de confirmation
    if (!confirm("Are you sure you want to switch the frames capture mode ?")) {

      $(this).prop("checked", "False"); // revert toggle
      return;
    }
    stopMove();
    currentCaptureMode = "True";

  }
  sendWSMessage("set_parameter", "mode_capture", currentCaptureMode);
  onScreenLog(`Switched to ${currentCaptureMode} Capture Mode`, "error");

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

const $cameraButtonContainer = $(".camera-buttons-container");
const $cameraRevealArrow = $(".camera-buttons-reveal-arrow img");
$(".camera-buttons-reveal-arrow").on("click", function () {
  $cameraRevealArrow.toggleClass('rotate180');
  if ($cameraButtonContainer.hasClass("slide-hide")) {
    $cameraButtonContainer.removeClass("slide-hide");
    $cameraButtonContainer.addClass("slide-open");
  } else {
    $cameraButtonContainer.removeClass("slide-open");
    $cameraButtonContainer.addClass("slide-hide");
  }
})


$('.btn-stop').on('click', () => {
  $('.btn-stop').toggleClass("active");
  stopMove();
  setTimeout(() => $('.btn-stop').removeClass('active'), 1000);
})
