// FONCTIONS UTILES

let FILE_LIST: File[] = [];

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




// GESTION PAGE

const socket = new WebSocket("/ws");

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
    })

    buttonFile.addEventListener('mouseleave', () => {
        buttonFile.style.fontWeight = "normal";
        buttonFile.style.border = "solid black 0.1rem"
    })

    buttonFile.addEventListener('click', () => {
        fillInput.click()
    })

    fillInput.addEventListener('change', () => {
        if (!fillInput.files) return;
        FileName(fillInput.files[0]);
    })
}

class vertex {
    private id: number;
    private x: number;
    private y: number;

    constructor(id: number, x: number, y: number) {
        this.x = x;
        this.y = y;
        this.id = id;
    }

    getCaracteristics(): number[] {
        return [this.id, this.x, this.y]
    }
}
/*
TODO:
- récpetion coté python normalement ok pour la création d'un graphe.
- to do:
    - réception des message de validation
    - envoie des messages json de vertex (classes Ts à écrire)
    - IG
*/

















/* TESTS */
const buttonExport: HTMLDivElement | null = document.getElementById("buttonExport") as HTMLDivElement | null;
if (buttonExport) {
    buttonExport.addEventListener('click', () => {
        if (FILE_LIST.length == 0) return;
        uploadFile(FILE_LIST, 'test');
        if (fileList) {
            fileList.innerHTML = "";
            FILE_LIST = [];
        }
    })
}
