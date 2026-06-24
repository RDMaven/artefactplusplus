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