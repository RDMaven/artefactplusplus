/*const socket = new WebSocket("/ws"); */

/*======###### MENU ######======*/

const button_menu = document.getElementById("menu");
const block_menu = document.getElementById("block_menu");
let isOpenMenu = 0;


if (button_menu && block_menu) {
    
    button_menu.addEventListener('click', ()=>{
        isOpenMenu = 1-isOpenMenu;
        if (isOpenMenu){
            block_menu.style.transform = "translateX(0%)";
        } else{
            block_menu.style.transform = "translateX(-100%)";
        }
    })
};

async function ask_client() {
    try {
        client = await fetch("http://137.194.194.180:8081/connected")
        if (!client.ok) {
            throw new Error("erreur de video...")
            
        }
        const data = await client.text()
        console.log(data)
    }
    catch(erreur) {
        console.error("Echouage : ", erreur)
    }
}

async function build_video() {
    const client = await ask_client();
}

ask_client()