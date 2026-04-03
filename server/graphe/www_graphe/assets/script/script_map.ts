// FONCTIONS UTILES
declare const Panzoom: any; // Obligatoire pour le TS Uniquement

let FILE_LIST: File[] = [];
let GRAPHIC_LIST: GraphicFile[] = []; //Liste des images déposées
const IMG_LIST: HTMLImageElement[] = [];  //IMAGES SERVANRT A FAIRE LES CARTES
const ID_LIST: string[] = [];

function FileName(file: File): void {
    FILE_LIST.push(file);
    //Valide la réception de file et l'écrit dans la div fileList
    if (fileList) {
        const div_elt: HTMLDivElement = document.createElement("div");
        const p_elt: HTMLParagraphElement = document.createElement("p");
        const img_elt: HTMLImageElement = document.createElement("img");

        img_elt.srcset = "/src/validation.svg";
        img_elt.style.width = "1rem";
        p_elt.innerText = `Fichier : ${file.name} de type : ${file.type}`;
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

function uploadFile(files: File[], export_name: string): void {
    const formData = new FormData();
    formData.append("export_name", export_name);
    for (let i = 0; i < files.length; i++) {
        formData.append("file", files[i])
    };

    fetch("/upload", {
        method: "POST",
        body: formData,
    })
        .then(res => res.text())
        .then(res => console.log(res))
        .catch((err) => console.error("erreur de transmission : ", err))
}

function verify_name_project(name: string): Promise<boolean> {
    //Verifie que le nom du projet est unique
    return fetch(`/getProjects?name=${encodeURIComponent(name)}`, {
        method: "GET",
    })
        .then(res => res.json())
        .then(data => data.isUnique)
}

function buildWindows(FILE_LIST: File[]): void {
    const ongletBox: HTMLDivElement | null = document.getElementById("onglet_box") as HTMLDivElement | null;
    if (ongletBox) {
        IMG_LIST.length = 0;
        ID_LIST.length = 0;
        GRAPHIC_LIST.length = 0;
        for (let i = 0; i < FILE_LIST.length; i++) {
            const div: HTMLDivElement = document.createElement("div");
            div.id = `image_content${i}`;
            div.style.display = "none";
            div.style.width = "100%";
            div.style.height = "80vh";
            div.style.overflow = "hidden";

            const img: HTMLImageElement = document.createElement("img");
            img.src = URL.createObjectURL(FILE_LIST[i])
            img.style.width = "auto";
            img.style.height = "auto";
            img.style.maxHeight = "100%";
            img.style.maxWidth = "100%";
            img.id = `image_id${i}`;
            img.style.objectFit = "contain";
            IMG_LIST.push(img);
            div.appendChild(img)

            ongletBox.appendChild(div)

            const graph: GraphicFile = new GraphicFile(i, []);
            GRAPHIC_LIST.push(graph);
            ID_LIST.push(div.id);

        }

        //Onglet du bas
        const onglet_bottom_box: HTMLDivElement | null = document.getElementById("onglet_box_bottom") as HTMLDivElement | null;
        if (onglet_bottom_box) {
            for (let i = 0; i < GRAPHIC_LIST.length; i++) {
                const div: HTMLDivElement = document.createElement("div");
                const img: HTMLImageElement = document.createElement("img");
                const p: HTMLParagraphElement = document.createElement("p");

                div.style.display = "flex";
                div.style.width = "6rem";
                div.style.width = "8rem";
                div.style.alignItems = "center";
                div.style.flexDirection = "column";

                img.src = "/src/picture.svg";
                img.style.width = "4rem";
                img.style.height = "4rem";
                img.style.margin = "1rem";

                p.innerText = `Onglet ${i}`;
                p.style.fontWeight = "bold";
                p.style.display = "inline";

                div.appendChild(img);
                div.appendChild(p);

                onglet_bottom_box.appendChild(div);
                div.addEventListener('click', () => {
                    for (let j = 0; j < ID_LIST.length; j++) {
                        const contentDiv = document.getElementById(ID_LIST[j]);
                        if (contentDiv) contentDiv.style.display = "none";
                        if (IMG_LIST[j]) IMG_LIST[j].style.display = "none";
                        const otherTab = onglet_bottom_box.children[j] as HTMLDivElement;
                        if (otherTab) {
                            otherTab.style.backgroundColor = "transparent";
                            otherTab.style.border = "solid black 0rem";
                            otherTab.style.borderRadius = "0rem";
                        }
                    }
                    const currentImg = IMG_LIST[i];
                    if (currentImg) {
                        currentImg.parentElement!.style.display = "block";
                        currentImg.style.display = "block";
                        div.style.backgroundColor = "rgb(200, 196, 183)";
                        div.style.border = "solid black 0.1rem";
                        setTimeout(() => {
                            panzoom(currentImg);
                        }, 50);
                    }
                });
            }
        }

    }
}

function panzoom(img: HTMLImageElement) {
    const panzoom = new Panzoom(img, {
        maxScale: 20,
        minScale: 0.1,
        canvas: true
    })
    panzoom.zoom(0.5);
    panzoom.pan(0, 0);
    img.addEventListener('wheel', panzoom.zoomWithWheel);
    document.addEventListener('keydown', (e) => {
        if (e.key === "+") {
            panzoom.zoomIn()
        }
        if (e.key === "-") {
            panzoom.zoomOut()
        }
    })
}

class GraphicFile {
    // Classe gérant les vertex stockés pour une des photos
    private name: number;
    private graphe: Vertex[];

    constructor(name: number, graphe: Vertex[] = []) {
        this.name = name;
        this.graphe = graphe;
    }

    getName(): number {
        return this.name
    }

    getGraphe(): Vertex[] {
        return this.graphe
    }
}


// GESTION PAGE

const socket = new WebSocket("/ws");

const PARTIE1: HTMLDivElement | null = document.getElementById("part_1") as HTMLDivElement | null;
const PARTIE2: HTMLDivElement | null = document.getElementById("part_2") as HTMLDivElement | null;

const pictureDone: HTMLDivElement | null = document.getElementById("picture_done") as HTMLDivElement | null;
const fillInput: HTMLInputElement | null = document.getElementById('fileInput') as HTMLInputElement | null;
const buttonFile: HTMLDivElement | null = document.getElementById("buttonFile") as HTMLDivElement | null;
const fileList: HTMLDivElement | null = document.getElementById("fileList") as HTMLDivElement | null;

if (pictureDone) {
    pictureDone.addEventListener('dragover', (e) => {
        e.preventDefault();
        pictureDone.style.border = "dashed rgb(45, 105, 194) 0.4rem";
        pictureDone.style.backgroundColor = "rgba(45, 105, 194, 0.3)";
        pictureDone.style.fontSize = "2.2rem";
    })

    pictureDone.addEventListener('dragleave', () => {
        pictureDone.style.border = "dashed rgb(45, 105, 194) 0.3rem";
        pictureDone.style.backgroundColor = "rgba(255,255,255)";
        pictureDone.style.fontSize = "2rem";
    })

    pictureDone.addEventListener('drop', (e) => {
        e.preventDefault()
        const files_List: FileList | undefined = e.dataTransfer?.files;

        if (!files_List || files_List.length == 0) {
            console.error("Aucun fichier détecté");
            return;
        }

        let files: File[] = [];
        for (let i = 0; i < files_List.length; i++) {
            files.push(files_List[i])
        }
        const file: File = files[0]
        console.log(`Nom : ${file.name}`)
        pictureDone.style.border = "dashed rgb(45, 105, 194) 0.3rem";
        pictureDone.style.backgroundColor = "rgba(255,255,255)";
        pictureDone.style.fontSize = "2rem";
        FileName(file);
    })
}

if (buttonFile && fillInput) {
    buttonFile.addEventListener('mouseenter', () => {
        buttonFile.style.fontWeight = "bold";
        buttonFile.style.border = "solid black 0.2rem";
        buttonFile.style.width="11.8rem";
        buttonFile.style.height="2.8rem";
    })

    buttonFile.addEventListener('mouseleave', () => {
        buttonFile.style.fontWeight = "normal";
        buttonFile.style.border = "solid black 0.1rem";
        buttonFile.style.width="12rem";
        buttonFile.style.height="3rem";
    })

    buttonFile.addEventListener('click', () => {
        fillInput.click()
    })

    fillInput.addEventListener('change', () => {
        if (!fillInput.files) return;
        FileName(fillInput.files[0]);
    })
}



//VALIDATION DU NOM DE PROJET
const buttonProjetName: HTMLDivElement | null = document.getElementById("project_name_validate") as HTMLDivElement | null;
const nameInput: HTMLInputElement | null = document.getElementById("project_name") as HTMLInputElement | null;
const verifNameProject: HTMLDivElement | null = document.getElementById("verif_project_name") as HTMLDivElement | null;

if (buttonProjetName && nameInput && verifNameProject) {
    buttonProjetName.addEventListener('mouseenter', () => {
        buttonProjetName.style.border = "solid black 0.2rem";
        buttonProjetName.style.fontWeight = "bold";
        buttonProjetName.style.width="9.8rem";
        buttonProjetName.style.height="1.3rem";
    })

    buttonProjetName.addEventListener('mouseleave', () => {
        buttonProjetName.style.border = "solid black 0.1rem";
        buttonProjetName.style.fontWeight = "normal";
        buttonProjetName.style.width="10rem";
        buttonProjetName.style.height="1.5rem";
    })

    buttonProjetName.addEventListener('click', () => {
        const p_elt: HTMLParagraphElement = document.createElement("p");
        p_elt.style.fontWeight = "bold";
        const new_project_name: string = nameInput.value;
        p_elt.innerText = "";
        verifNameProject.innerHTML = "";
        if (new_project_name === "") {
            p_elt.innerText = "Nom de projet vide..."
            verifNameProject.appendChild(p_elt);
        }
        else {

            verify_name_project(new_project_name).then(isUnique => {
                if (FILE_LIST.length == 0) {
                    p_elt.innerText = "Veuillez déjà sélectionner des fichiers."
                    verifNameProject.appendChild(p_elt);
                }
                else {
                    if (isUnique) {
                        p_elt.innerText = "Le Nom a été validé, le projet peut être créé !"
                        verifNameProject.appendChild(p_elt);
                        const p1: HTMLParagraphElement = document.createElement("p");
                        p1.innerText = "Documents qui seront créés :";
                        p1.style.margin = "0";
                        verifNameProject.appendChild(p1)
                        let divList: HTMLDivElement[] = [];
                        for (let i = 0; i < FILE_LIST.length; i++) {
                            const div: HTMLDivElement = document.createElement("div");
                            const p_file: HTMLParagraphElement = document.createElement("p");
                            const p_graphe: HTMLParagraphElement = document.createElement("p");
                            p_file.innerText = `./${new_project_name}/Image_${i}_${FILE_LIST[i].name}`;
                            p_graphe.innerText = `./${new_project_name}/graphe${i}.txt`;
                            p_file.style.margin = "0";
                            p_file.style.marginLeft = "3rem";
                            p_graphe.style.margin = "0";
                            p_graphe.style.marginLeft = "3rem";
                            div.appendChild(p_file);
                            div.appendChild(p_graphe);
                            divList.push(div);
                        }
                        divList.forEach((div) => {
                            verifNameProject.appendChild(div)
                        })
                    }
                    else {
                        p_elt.innerText = "Nom déjà utilisé... Veuillez en saisir un nouveau."
                        verifNameProject.appendChild(p_elt);

                    }
                }
            })
        }
    })
}

const continueButton: HTMLDivElement | null = document.getElementById("create_project_button") as HTMLDivElement | null;
if (continueButton) {
    continueButton.addEventListener('mouseenter', () => {
        continueButton.style.border = "solid black 0.2rem";
        continueButton.style.fontWeight = "bold";
        continueButton.style.width="14.8rem";
        continueButton.style.height="1.3rem";
    })

    continueButton.addEventListener('mouseleave', () => {
        continueButton.style.border = "solid black 0.1rem";
        continueButton.style.fontWeight = "normal";
        continueButton.style.width="15rem";
        continueButton.style.height="1.5rem";
    })

    continueButton.addEventListener('click', () => {
        if (PARTIE1 && PARTIE2) {
            PARTIE1.style.display = "none";
            PARTIE2.style.display = "flex";
            buildWindows(FILE_LIST);
        }
    })
}


//PARTIE 2
const Caract: HTMLDivElement | null = document.getElementById("caracteristics") as HTMLDivElement | null;
const plusCaract: HTMLDivElement | null = document.getElementById("plus_caracteristics") as HTMLDivElement | null;
let CARACT_OPEN = false;

if (plusCaract && Caract) {
    plusCaract.addEventListener('click', () => {
        if (CARACT_OPEN) {
            Caract.style.left = "-14.5rem";
            plusCaract.style.left = "0.7rem"
            CARACT_OPEN = false
        }
        else {
            Caract.style.left = "0rem";
            plusCaract.style.left = "15.2rem"
            CARACT_OPEN = true
        }
    })
}

const grapheBox: HTMLDivElement | null = document.getElementById("graphe_box") as HTMLDivElement | null;
const plusGraphe: HTMLDivElement | null = document.getElementById("plus_graphe") as HTMLDivElement | null;
let GRAPHE_OPEN: boolean = false;

if (plusGraphe && grapheBox) {
    plusGraphe.addEventListener('click', () => {
        if (GRAPHE_OPEN) {
            grapheBox.style.right = "-9.5rem";
            plusGraphe.style.right = "0.7rem"
            GRAPHE_OPEN = false
        }
        else {
            grapheBox.style.right = "0rem";
            plusGraphe.style.right = "10.2rem"
            GRAPHE_OPEN = true
        }
    })
}

const ongletBoxBottom: HTMLDivElement | null = document.getElementById("onglet_box_bottom") as HTMLDivElement | null;
const plusOnglet: HTMLDivElement | null = document.getElementById("plus_onglet") as HTMLDivElement | null;
let ONGLET_OPEN: boolean = false;

if (plusOnglet && ongletBoxBottom) {
    plusOnglet.addEventListener('click', () => {
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
    })
}







/* TESTS */
const buttonReset: HTMLDivElement | null = document.getElementById("buttonExport") as HTMLDivElement | null;
if (buttonReset) {
    buttonReset.addEventListener('click', () => {
        if (FILE_LIST.length == 0) return;
        if (fileList) {
            fileList.innerHTML = "";
            FILE_LIST = [];
        }
    })

    buttonReset.addEventListener('mouseenter', () => {
        buttonReset.style.border = "solid 0.2rem black";
        buttonReset.style.fontWeight = "bold";
        buttonReset.style.width = "9.8rem";
        buttonReset.style.height= "1.3rem";
    })

    buttonReset.addEventListener('mouseleave', () => {
        buttonReset.style.border = "solid 0.1rem black";
        buttonReset.style.fontWeight = "normal";
        buttonReset.style.width = "10rem";
        buttonReset.style.height= "1.5rem";
    })
}

/*
TODO:
- récpetion coté python normalement ok pour la création d'un graphe.
- to do:
    - réception des message de validation
    - envoie des messages json de vertex (classes Ts à écrire)
    - IG
    - Logs lorsqu'un sommet est créé
    - Bouton Reset
- Lecture de carte
*/

//CREATION DE SOMMETS - ARRETE

class Vertex {
    //Classe représentant les sommets
    private x: number;
    private y: number;
    private id: number;

    constructor(x: number, y: number, id: number) {
        this.x = x;
        this.y = y;
        this.id = id;
    }

    getX(): number {
        return this.x
    }
    getY(): number {
        return this.y
    }
    getId(): number {
        return this.id
    }
    setX(x: number): void {
        this.x = x
    }
    setY(y: number): void {
        this.y = y
    }
}

const sommet: HTMLImageElement | null = document.getElementById("sommet") as HTMLImageElement | null;
const arrete: HTMLImageElement | null = document.getElementById("arrete") as HTMLImageElement | null;
let x_souris: number = 0;
let y_souris: number = 0;

document.addEventListener('mousemove', (event: MouseEvent) => {
    x_souris = event.clientX;
    y_souris = event.clientY;
})

if (sommet && arrete) {
    sommet.addEventListener('click', () => {
        
    })
}
