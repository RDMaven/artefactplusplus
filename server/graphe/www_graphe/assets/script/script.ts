//CARROUSSEL

const imageTrack: HTMLDivElement | null = document.getElementById("image_track") as HTMLDivElement | null
const rondPlein: HTMLImageElement | null = document.getElementById("plein") as HTMLImageElement | null

let indice:number = 0;
const totalImage: number = 5;
const tailleRond: number = 2.5; /*en rem*/

function turn_image(): void {
    if (!imageTrack || ! rondPlein) return;
    indice = (indice + 1) % totalImage;

    imageTrack.style.transform = `translateX(-${indice * 100}%)`;

    rondPlein.style.transform = `translateX(${indice * (tailleRond + 0.5)}rem)`
}

setInterval(turn_image, 2500);

//SLIDE TEXT

const textPresentation: HTMLDivElement | null = document.getElementById("text_presentation") as HTMLDivElement | null;

window.addEventListener('scroll',() => {
    if (textPresentation){
        const scrollY: number = window.scrollY;
        textPresentation.style.transform = `translateY(-${0.25 * scrollY}px)`;
        const rect = textPresentation.getBoundingClientRect();
        const shadow: number = rect.top/546.25 * 2.5 - 0.5;
        textPresentation.style.boxShadow = `2rem ${shadow}rem 0.75rem 0.5rem rgba(0,0,0,0.4)`
    }
});

//BUTTONS

const b1: HTMLDivElement | null = document.getElementById("button1") as HTMLDivElement | null
const b2: HTMLDivElement | null = document.getElementById("button2") as HTMLDivElement | null
const b3: HTMLDivElement | null = document.getElementById("button3") as HTMLDivElement | null

if (b1)  {
    b1.addEventListener('mouseenter',() => {
        b1.style.border = "solid black 0.25rem";
        b1.style.fontWeight = "bold";
    })
    b1.addEventListener('mouseleave',() => {
        b1.style.border = "solid black 0.15rem";
        b1.style.fontWeight = "normal";
    })
    b1.addEventListener('click',() => {
        window.open('/team');
    })
}

if (b2)  {
    b2.addEventListener('mouseenter',() => {
        b2.style.border = "solid black 0.25rem";
        b2.style.fontWeight = "bold";
    })
    b2.addEventListener('mouseleave',() => {
        b2.style.border = "solid black 0.15rem";
        b2.style.fontWeight = "normal";
    })
    b2.addEventListener('click',() => {
        window.open('/wait');
    })
}

if (b3)  {
    b3.addEventListener('mouseenter',() => {
        b3.style.border = "solid black 0.25rem";
        b3.style.fontWeight = "bold";
    })
    b3.addEventListener('mouseleave',() => {
        b3.style.border = "solid black 0.15rem";
        b3.style.fontWeight = "normal";
    })
    b3.addEventListener('click',() => {
        window.open('/wait');
    })
}