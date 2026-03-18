"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.FileName = FileName;
exports.uploadFile = uploadFile;
function FileName(file, fileList) {
    //Valide la réception de file et l'écrit dans la div fileList
    if (fileList) {
        var div_elt = document.createElement("div");
        var p_elt = document.createElement("p");
        var img_elt = document.createElement("img");
        img_elt.srcset = "/src/validation.svg";
        img_elt.style.width = "1rem";
        p_elt.innerText = "Fichier : ".concat(file.name, " de type : ").concat(file.type);
        div_elt.style.width = "100%";
        div_elt.style.display = "flex";
        div_elt.style.flexDirection = "row";
        div_elt.appendChild(img_elt);
        div_elt.appendChild(p_elt);
        fileList.prepend(div_elt);
    }
}
function uploadFile(file) {
}
