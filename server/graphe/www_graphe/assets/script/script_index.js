//CARROUSSEL
var imageTrack = document.getElementById("image_track");
var rondPlein = document.getElementById("plein");
var indice = 0;
var totalImage = 5;
var tailleRond = 2.5; /*en rem*/
function turn_image() {
    if (!imageTrack || !rondPlein)
        return;
    indice = (indice + 1) % totalImage;
    imageTrack.style.transform = "translateX(-".concat(indice * 100, "%)");
    rondPlein.style.transform = "translateX(".concat(indice * (tailleRond + 0.5), "rem)");
}
setInterval(turn_image, 2500);
//SLIDE TEXT
var textPresentation = document.getElementById("text_presentation");
window.addEventListener('scroll', function () {
    if (textPresentation) {
        var scrollY_1 = window.scrollY;
        textPresentation.style.transform = "translateY(-".concat(0.25 * scrollY_1, "px)");
        var rect = textPresentation.getBoundingClientRect();
        var shadow = rect.top / 546.25 * 2.5 - 0.5;
        textPresentation.style.boxShadow = "2rem ".concat(shadow, "rem 0.75rem 0.5rem rgba(0,0,0,0.4)");
    }
});
//BUTTONS
var b1 = document.getElementById("button1");
var b2 = document.getElementById("button2");
var b3 = document.getElementById("button3");
if (b1) {
    b1.addEventListener('mouseenter', function () {
        b1.style.border = "solid black 0.25rem";
        b1.style.fontWeight = "bold";
    });
    b1.addEventListener('mouseleave', function () {
        b1.style.border = "solid black 0.15rem";
        b1.style.fontWeight = "normal";
    });
    b1.addEventListener('click', function () {
        window.open('/team');
    });
}
if (b2) {
    b2.addEventListener('mouseenter', function () {
        b2.style.border = "solid black 0.25rem";
        b2.style.fontWeight = "bold";
    });
    b2.addEventListener('mouseleave', function () {
        b2.style.border = "solid black 0.15rem";
        b2.style.fontWeight = "normal";
    });
    b2.addEventListener('click', function () {
        window.open('/map_build');
    });
}
if (b3) {
    b3.addEventListener('mouseenter', function () {
        b3.style.border = "solid black 0.25rem";
        b3.style.fontWeight = "bold";
    });
    b3.addEventListener('mouseleave', function () {
        b3.style.border = "solid black 0.15rem";
        b3.style.fontWeight = "normal";
    });
    b3.addEventListener('click', function () {
        window.open('/wait');
    });
}
