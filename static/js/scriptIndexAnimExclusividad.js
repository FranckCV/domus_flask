// ANIMACIONES EXCLUSIVIDAD EN HOMEPAGE

gsap.registerPlugin(ScrollTrigger);

gsap.fromTo(".domus_title",{
    display: "block",
    opacity: 1,
    y: 0,
    scrollTrigger: {
        trigger: ".article_banner_domus",
        toggleActions: "none none none none",
    }
},{
    display: "none",
    y: 100,
    opacity: 0,
    duration: 0.2,
    scale: 0,
    scrollTrigger: {
        trigger: ".article_banner_domus",
        start: "top 85%",
        end: "top 85%",
        // markers:true,
        toggleActions: "play none reverse none",
    }
});

gsap.fromTo(".domus_img",{
    y: -200,
    opacity: 0,
    scale: 0.5,
    scrollTrigger: {
        trigger: ".article_banner_domus",
        toggleActions: "none none none none",
    }
},{
    y: 0,
    opacity: 1,
    scale:1,
    duration: 0.2,
    scrollTrigger: {
        trigger: ".article_banner_domus",
        start: "top 85%",
        end: "top 85%",        
        toggleActions: "play none reverse none",
    }
});


if (window.innerWidth > 1000 ) {        
    gsap.utils.toArray('.domus_text').forEach(domus_text=>{
        gsap.fromTo(domus_text,{
            x: -500,
            opacity: 0,
            scale: 0.5,
            scrollTrigger: {
                trigger: domus_text,            
                toggleActions: "none none none none",
            }
        },{
            x: 0,
            opacity: 1,
            scale:1,
            duration: 0.2,
            scrollTrigger: {
                trigger: domus_text,
                start: "top 90%",
                end: "top 22.5%",
                // markers: true,
                toggleActions: "play none none none",
            }
        });
    });


    gsap.utils.toArray('.domus_text2').forEach(domus_text2=>{
        gsap.fromTo(domus_text2,{
            x: -500,
            opacity: 0,
            scale: 0.5,
            scrollTrigger: {
                trigger: domus_text2,
                toggleActions: "none none none none",
            }
        },{
            x: 0,
            opacity: 1,
            scale:1,
            duration: 0.2,
            scrollTrigger: {
                trigger: domus_text2,
                start: "top 90%",
                end: "top 22.5%",
                toggleActions: "play none none none",
            }
        });
    });
}