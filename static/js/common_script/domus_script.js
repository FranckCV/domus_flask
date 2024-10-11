// ANIMACION ITEMS DEL BODY

// if (!window.location.pathname.includes('resumenDePedido.html')) {
//     const body_items = document.querySelector('.body_page').children;
//     gsap.from(body_items,{
//         opacity: 0,
//         y: -100,
//         duration: 0.2,
//         stagger:{
//             amount: 0.5
//         }
//     });
// }


// ANIMACION ITEMS DEL HEADER

const header_items = document.querySelector('header');
gsap.from(header_items.children,{
    opacity: 0,
    y: -50,
    duration: 0.1,
    stagger:{
        amount: 0.5
    }
});

// ESPACIADO MENU DESPLEGLABE

function adjustPadding() {
    const menu = document.querySelector('#menu_content');
    const headerHeight = document.querySelector('header').offsetHeight; 

    menu.style.paddingTop = `calc(15px + ${headerHeight}px)`;
}

window.addEventListener("load", () => {
    adjustPadding();
});
window.addEventListener("resize", () => {
    adjustPadding();
});

// FUNCIONALIDAD Y ANIMACIÓN MENU DESPLEGLABE

const $openClose = document.querySelector("#menu_button"),
    $aside = document.querySelector("#menu_content"),
    $menuElements = document.querySelectorAll(".menu_element"),
    $submenus = document.querySelectorAll(".submenu_content");

    $openClose.addEventListener("click", () => {
        $aside.classList.toggle("desplegar");
        adjustPadding();
    });

$menuElements.forEach((menuElement, index) => {
    menuElement.addEventListener("click", () => {        
        const submenuContent = menuElement.nextElementSibling;
        const iconMenu = menuElement.querySelector(".fa-chevron-down");
        if (submenuContent && submenuContent.classList.contains("submenu_content")) {
            if (submenuContent.style.display === "flex") {
                // Animación de salida
                gsap.to(iconMenu, {
                    rotate: 0,
                    duration: 0.2,
                });
                gsap.to(submenuContent, {
                    height: 0,
                    duration: 0.5,
                    onComplete: () => {
                        submenuContent.style.display = "none";
                    }
                });
                gsap.to(submenuContent.children, {
                    opacity: 0,
                    y: -50,
                    duration: 0.1,
                    stagger: {
                        amount: -0.25
                    }
                });
            } else {
                submenuContent.style.display = "flex";
                const submenuHeight = submenuContent.scrollHeight;
                submenuContent.style.height = "0px";
                gsap.to(iconMenu, {
                    rotate: -180,
                    duration: 0.2,
                });
                gsap.to(submenuContent, {
                    height: submenuHeight,
                    duration: 0.3,
                    onComplete: () => {
                        submenuContent.style.height = "auto";
                    }
                });
                gsap.fromTo(submenuContent.children, {
                    opacity: 0,
                    y: -50
                }, {
                    opacity: 1,
                    y: 0,
                    duration: 0.1,
                    stagger: {
                        amount: 0.25
                    }
                });
            }
        }
    });
});

// ANIMACION TITULOS TIPO 1 ESTILO 1

gsap.utils.toArray('.title1_1').forEach(h1=>{
    gsap.fromTo(h1,{
        letterSpacing:'5px',
        opacity:0,
        y:-150,
    },{
        letterSpacing:'0',
        opacity:1,
        y:0,
        duration: 0.2,
        scrollTrigger: {
            trigger: h1,
            start: "top 85%",
        }
    });
});

// ANIMACION TITULOS TIPO 1 ESTILO 2

gsap.utils.toArray('.title1_2').forEach(h1=>{
    gsap.fromTo(h1,{
        letterSpacing:'5px',
        opacity:0,
        y:-150,
    },{
        letterSpacing:'0',
        opacity:1,
        y:0,
        duration: 0.2,
        scrollTrigger: {
            trigger: h1,
            start: "top 85%",
        }
    });
});