var FILE_LIST = [];
var GRAPHIC_LIST = []; //Liste des images déposées
var IMG_LIST = []; //IMAGES SERVANRT A FAIRE LES CARTES
var ID_LIST = [];
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
function resetFile() {
    FILE_LIST = [];
    if (fileList) {
        fileList.innerHTML = "";
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
function verify_name_project(name) {
    //Verifie que le nom du projet est unique
    return fetch("/getProjects?name=".concat(encodeURIComponent(name)), {
        method: "GET",
    })
        .then(function (res) { return res.json(); })
        .then(function (data) { return data.isUnique; });
}
function buildWindows(FILE_LIST) {
    var ongletBox = document.getElementById("onglet_box");
    if (ongletBox) {
        IMG_LIST.length = 0;
        ID_LIST.length = 0;
        GRAPHIC_LIST.length = 0;
        for (var i = 0; i < FILE_LIST.length; i++) {
            var div = document.createElement("div");
            div.id = "image_content".concat(i);
            div.style.display = "none";
            div.style.width = "100%";
            div.style.height = "80vh";
            div.style.overflow = "hidden";
            var img = document.createElement("img");
            img.src = URL.createObjectURL(FILE_LIST[i]);
            img.style.width = "auto";
            img.style.height = "auto";
            img.style.maxHeight = "100%";
            img.style.maxWidth = "100%";
            img.id = "image_id".concat(i);
            img.style.objectFit = "contain";
            IMG_LIST.push(img);
            div.appendChild(img);
            ongletBox.appendChild(div);
            var graph = new GraphicFile(i, []);
            GRAPHIC_LIST.push(graph);
            ID_LIST.push(div.id);
        }
        //Onglet du bas
        var onglet_bottom_box_1 = document.getElementById("onglet_box_bottom");
        if (onglet_bottom_box_1) {
            var _loop_1 = function (i) {
                var div = document.createElement("div");
                var img = document.createElement("img");
                var p = document.createElement("p");
                div.style.display = "flex";
                div.style.width = "6rem";
                div.style.width = "8rem";
                div.style.alignItems = "center";
                div.style.flexDirection = "column";
                img.src = "/src/picture.svg";
                img.style.width = "4rem";
                img.style.height = "4rem";
                img.style.margin = "1rem";
                p.innerText = "Onglet ".concat(i);
                p.style.fontWeight = "bold";
                p.style.display = "inline";
                div.appendChild(img);
                div.appendChild(p);
                onglet_bottom_box_1.appendChild(div);
                div.addEventListener('click', function () {
                    for (var j = 0; j < ID_LIST.length; j++) {
                        var contentDiv = document.getElementById(ID_LIST[j]);
                        if (contentDiv)
                            contentDiv.style.display = "none";
                        if (IMG_LIST[j])
                            IMG_LIST[j].style.display = "none";
                        var otherTab = onglet_bottom_box_1.children[j];
                        if (otherTab) {
                            otherTab.style.backgroundColor = "transparent";
                            otherTab.style.border = "solid black 0rem";
                            otherTab.style.borderRadius = "0rem";
                        }
                    }
                    var currentImg = IMG_LIST[i];
                    if (currentImg) {
                        currentImg.parentElement.style.display = "block";
                        currentImg.style.display = "block";
                        div.style.backgroundColor = "rgb(200, 196, 183)";
                        div.style.border = "solid black 0.1rem";
                        setTimeout(function () {
                            panzoom(currentImg);
                        }, 50);
                    }
                });
            };
            for (var i = 0; i < GRAPHIC_LIST.length; i++) {
                _loop_1(i);
            }
        }
    }
}
function panzoom(img) {
    var panzoom = new Panzoom(img, {
        maxScale: 20,
        minScale: 0.1,
        canvas: true
    });
    panzoom.zoom(0.5);
    panzoom.pan(0, 0);
    img.addEventListener('wheel', panzoom.zoomWithWheel);
    document.addEventListener('keydown', function (e) {
        if (e.key === "+") {
            panzoom.zoomIn();
        }
        if (e.key === "-") {
            panzoom.zoomOut();
        }
    });
}
var GraphicFile = /** @class */ (function () {
    function GraphicFile(name, graphe) {
        if (graphe === void 0) { graphe = []; }
        this.name = name;
        this.graphe = graphe;
    }
    GraphicFile.prototype.getName = function () {
        return this.name;
    };
    GraphicFile.prototype.getGraphe = function () {
        return this.graphe;
    };
    return GraphicFile;
}());
var Vertex = /** @class */ (function () {
    function Vertex(x, y, id) {
        this.x = x;
        this.y = y;
        this.id = id;
    }
    Vertex.prototype.getX = function () {
        return this.x;
    };
    Vertex.prototype.getY = function () {
        return this.y;
    };
    Vertex.prototype.getId = function () {
        return this.id;
    };
    Vertex.prototype.setX = function (x) {
        this.x = x;
    };
    Vertex.prototype.setY = function (y) {
        this.y = y;
    };
    return Vertex;
}());
// GESTION PAGE
var socket = new WebSocket("/ws");
var PARTIE1 = document.getElementById("part_1");
var PARTIE2 = document.getElementById("part_2");
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
//VALIDATION DU NOM DE PROJET
var buttonProjetName = document.getElementById("project_name_validate");
var nameInput = document.getElementById("project_name");
var verifNameProject = document.getElementById("verif_project_name");
if (buttonProjetName && nameInput && verifNameProject) {
    buttonProjetName.addEventListener('mouseenter', function () {
        buttonProjetName.style.border = "solid black 0.2rem";
        buttonProjetName.style.fontWeight = "bold";
    });
    buttonProjetName.addEventListener('mouseleave', function () {
        buttonProjetName.style.border = "solid black 0.1rem";
        buttonProjetName.style.fontWeight = "normal";
    });
    buttonProjetName.addEventListener('click', function () {
        var p_elt = document.createElement("p");
        p_elt.style.fontWeight = "bold";
        var new_project_name = nameInput.value;
        p_elt.innerText = "";
        verifNameProject.innerHTML = "";
        if (new_project_name === "") {
            p_elt.innerText = "Nom de projet vide...";
            verifNameProject.appendChild(p_elt);
        }
        else {
            verify_name_project(new_project_name).then(function (isUnique) {
                if (FILE_LIST.length == 0) {
                    p_elt.innerText = "Veuillez déjà sélectionner des fichiers.";
                    verifNameProject.appendChild(p_elt);
                }
                else {
                    if (isUnique) {
                        p_elt.innerText = "Le Nom a été validé, le projet peut être créé !";
                        verifNameProject.appendChild(p_elt);
                        var p1 = document.createElement("p");
                        p1.innerText = "Documents qui seront créés :";
                        p1.style.margin = "0";
                        verifNameProject.appendChild(p1);
                        var divList = [];
                        for (var i = 0; i < FILE_LIST.length; i++) {
                            var div = document.createElement("div");
                            var p_file = document.createElement("p");
                            var p_graphe = document.createElement("p");
                            p_file.innerText = "./".concat(new_project_name, "/Image_").concat(i, "_").concat(FILE_LIST[i].name);
                            p_graphe.innerText = "./".concat(new_project_name, "/graphe").concat(i, ".txt");
                            p_file.style.margin = "0";
                            p_file.style.marginLeft = "3rem";
                            p_graphe.style.margin = "0";
                            p_graphe.style.marginLeft = "3rem";
                            div.appendChild(p_file);
                            div.appendChild(p_graphe);
                            divList.push(div);
                        }
                        divList.forEach(function (div) {
                            verifNameProject.appendChild(div);
                        });
                    }
                    else {
                        p_elt.innerText = "Nom déjà utilisé... Veuillez en saisir un nouveau.";
                        verifNameProject.appendChild(p_elt);
                    }
                }
            });
        }
    });
}
var continueButton = document.getElementById("create_project_button");
if (continueButton) {
    continueButton.addEventListener('mouseenter', function () {
        continueButton.style.border = "solid black 0.2rem";
        continueButton.style.fontWeight = "bold";
    });
    continueButton.addEventListener('mouseleave', function () {
        continueButton.style.border = "solid black 0.1rem";
        continueButton.style.fontWeight = "normal";
    });
    continueButton.addEventListener('click', function () {
        if (PARTIE1 && PARTIE2) {
            PARTIE1.style.display = "none";
            PARTIE2.style.display = "flex";
            buildWindows(FILE_LIST);
        }
    });
}
/*
TODO:
- récpetion coté python normalement ok pour la création d'un graphe.
- to do:
    - réception des message de validation
    - envoie des messages json de vertex (classes Ts à écrire)
    - IG
*/
//PARTIE 2
var Caract = document.getElementById("caracteristics");
var plusCaract = document.getElementById("plus_caracteristics");
var CARACT_OPEN = false;
if (plusCaract && Caract) {
    plusCaract.addEventListener('click', function () {
        if (CARACT_OPEN) {
            Caract.style.left = "-14.5rem";
            plusCaract.style.left = "0.7rem";
            CARACT_OPEN = false;
        }
        else {
            Caract.style.left = "0rem";
            plusCaract.style.left = "15.2rem";
            CARACT_OPEN = true;
        }
    });
}
var grapheBox = document.getElementById("graphe_box");
var plusGraphe = document.getElementById("plus_graphe");
var GRAPHE_OPEN = false;
if (plusGraphe && grapheBox) {
    plusGraphe.addEventListener('click', function () {
        if (GRAPHE_OPEN) {
            grapheBox.style.right = "-9.5rem";
            plusGraphe.style.right = "0.7rem";
            GRAPHE_OPEN = false;
        }
        else {
            grapheBox.style.right = "0rem";
            plusGraphe.style.right = "10.2rem";
            GRAPHE_OPEN = true;
        }
    });
}
var ongletBoxBottom = document.getElementById("onglet_box_bottom");
var plusOnglet = document.getElementById("plus_onglet");
var ONGLET_OPEN = false;
if (plusOnglet && ongletBoxBottom) {
    plusOnglet.addEventListener('click', function () {
        if (ONGLET_OPEN) {
            ongletBoxBottom.style.bottom = "-9.5rem";
            plusOnglet.style.bottom = "0.7rem";
            ONGLET_OPEN = false;
        }
        else {
            ongletBoxBottom.style.bottom = "0rem";
            plusOnglet.style.bottom = "10.2rem";
            ONGLET_OPEN = true;
        }
    });
}
/*ID_LIST.forEach((id) => {
    const div: HTMLDivElement | null = document.getElementById(id) as HTMLDivElement | null;
    if (div) {
        div.addEventListener(('click'), () => {
            ID_LIST.forEach((id) => {
                const div: HTMLDivElement | null = document.getElementById(id) as HTMLDivElement | null;
                if (div) {
                    div.style.border = "solid black 0rem";
                    div.style.borderRadius = "0rem";
                    div.style.backgroundColor = "white";
                    const index: number = ID_LIST.indexOf(div.id);
                    const img: HTMLImageElement = IMG_LIST[index];
                    img.style.display = "none";
                }
            })
            div.style.border = "solid black 0.1rem";
            div.style.borderRadius = "0.5rem";
            div.style.backgroundColor = "rgb(200, 196, 183)";
            const index: number = ID_LIST.indexOf(div.id);
            const img: HTMLImageElement = IMG_LIST[index];
            img.style.display = "block";
            setTimeout(() => {
                panzoom(img),
                    10
            })
        })
    }
})*/
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
