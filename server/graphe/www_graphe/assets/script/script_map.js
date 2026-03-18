// FONCTIONS UTILES
var FILE_LIST = [];
function FileName(file) {
    FILE_LIST.push(file);
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
function uploadFile(files, export_name) {
    var formData = new FormData();
    formData.append("export_name", export_name);
    for (var i = 0; i < files.length; i++) {
        formData.append("file", files[i]);
    }
    ;
    fetch("/upload", {
        method: "POST",
        body: formData,
    })
        .then(function (res) { return res.text(); })
        .then(function (res) { return console.log(res); })
        .catch(function (err) { return console.error("erreur de transmission : ", err); });
}
// GESTION PAGE
var socket = new WebSocket("/ws");
var pictureDone = document.getElementById("picture_done");
var fillInput = document.getElementById('fileInput');
var buttonFile = document.getElementById("buttonFile");
var fileList = document.getElementById("fileList");
if (pictureDone) {
    pictureDone.addEventListener('dragover', function (e) {
        e.preventDefault();
        pictureDone.style.border = "dashed rgb(45, 105, 194) 0.4rem";
        pictureDone.style.backgroundColor = "rgba(45, 105, 194, 0.3)";
        pictureDone.style.fontSize = "2.2rem";
    });
    pictureDone.addEventListener('dragleave', function () {
        pictureDone.style.border = "dashed rgb(45, 105, 194) 0.3rem";
        pictureDone.style.backgroundColor = "rgba(255,255,255)";
        pictureDone.style.fontSize = "2rem";
    });
    pictureDone.addEventListener('drop', function (e) {
        var _a;
        e.preventDefault();
        var files_List = (_a = e.dataTransfer) === null || _a === void 0 ? void 0 : _a.files;
        if (!files_List || files_List.length == 0) {
            console.error("Aucun fichier détecté");
            return;
        }
        var files = [];
        for (var i = 0; i < files_List.length; i++) {
            files.push(files_List[i]);
        }
        var file = files[0];
        console.log("Nom : ".concat(file.name));
        pictureDone.style.border = "dashed rgb(45, 105, 194) 0.3rem";
        pictureDone.style.backgroundColor = "rgba(255,255,255)";
        pictureDone.style.fontSize = "2rem";
        FileName(file);
    });
}
if (buttonFile && fillInput) {
    buttonFile.addEventListener('mouseenter', function () {
        buttonFile.style.fontWeight = "bold";
        buttonFile.style.border = "solid black 0.2rem";
    });
    buttonFile.addEventListener('mouseleave', function () {
        buttonFile.style.fontWeight = "normal";
        buttonFile.style.border = "solid black 0.1rem";
    });
    buttonFile.addEventListener('click', function () {
        fillInput.click();
    });
    fillInput.addEventListener('change', function () {
        if (!fillInput.files)
            return;
        FileName(fillInput.files[0]);
    });
}
var vertex = /** @class */ (function () {
    function vertex(id, x, y) {
        this.x = x;
        this.y = y;
        this.id = id;
    }
    vertex.prototype.getCaracteristics = function () {
        return [this.id, this.x, this.y];
    };
    return vertex;
}());
/*
TODO:
- récpetion coté python normalement ok pour la création d'un graphe.
- to do:
    - réception des message de validation
    - envoie des messages json de vertex (classes Ts à écrire)
    - IG
*/
/* TESTS */
var buttonExport = document.getElementById("buttonExport");
if (buttonExport) {
    buttonExport.addEventListener('click', function () {
        if (FILE_LIST.length == 0)
            return;
        uploadFile(FILE_LIST, 'test');
        if (fileList) {
            fileList.innerHTML = "";
            FILE_LIST = [];
        }
    });
}
