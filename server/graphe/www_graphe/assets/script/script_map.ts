const socket = new WebSocket("/ws");

const pictureDone: HTMLDivElement | null = document.getElementById("picture_done") as HTMLDivElement | null;

if (pictureDone) {
    pictureDone.addEventListener('mouseenter', () => {
        pictureDone.style.border = "dashed rgb(45, 105, 194) 0.4rem";
        pictureDone.style.backgroundColor = "rgba(45, 105, 194, 0.3)";
        pictureDone.style.fontSize = "2.2rem";
    })

    pictureDone.addEventListener('mouseleave', () => {
        pictureDone.style.border = "dashed rgb(45, 105, 194) 0.3rem";
        pictureDone.style.backgroundColor = "rgba(255,255,255)";
        pictureDone.style.fontSize = "2rem";
    })
}

class vertex {
    private id: number;
    private x: number;
    private y: number;

    constructor(id: number, x: number, y: number) {
        this.x = x;
        this.y = y;
        this.id =id;
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
