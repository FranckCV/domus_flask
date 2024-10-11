document.addEventListener("DOMContentLoaded", function() {
    // Obtener el parámetro de la URL
    const params = new URLSearchParams(window.location.search);
    const promo = params.get('promo');

    // Elementos donde se cambiará el contenido
    const promoImg = document.querySelector('.promo-img');
    const promoH1 = document.querySelector('.promo-text h1');
    const promoH2 = document.querySelector('.promo-text h2');
    const promoP = document.querySelector('.promo-text p');
    const promoTag = document.querySelector('.promo-tag');
    const promoTerms = document.querySelector('.terms p');

    // Información de las promociones
    const promociones = {
        'audifonos-sony': {
            img: 'img/imgLeo/audifonos.jpg', // Ruta corregida
            desc: 'En audífonos Sony',
            price: '30% DSCTO',
            tag: 'Hasta',
            terms: 'Promoción válida del 01.06.2024 al 20.06.2024 para productos Sony. No acumulable con otras ofertas.'
        },
        'medias-nike': {
            img: 'img/imgLeo/mediasNike.png', // Ruta corregida
            desc: 'En medias deportivas Nike',
            price: '3X2',
            tag: 'Promoción',
            terms: 'Promoción válida del 01.06.2024 al 20.06.2024 para productos Nike. No acumulable con otras ofertas.'
        },
        'smartwatch-apple': {
            img: 'img/imgLeo/smartwatch.png', // Ruta corregida
            desc: 'En smartwatchs de Apple',
            price: 'S/.899',
            tag: 'Desde',
            terms: 'Promoción válida del 01.06.2024 al 20.06.2024 para productos Apple. No acumulable con otras ofertas.'
        },
        'xiaomi-pad': {
            img: 'img/imgLeo/xiaomiPad.png', // Ruta corregida
            desc: 'Xiaomi Pad 6',
            price: 'S/. 1499.99',
            tag: 'Promoción',
            terms: 'Promoción válida del 01.06.2024 al 20.06.2024 para productos Xiaomi. No acumulable con otras ofertas.'
        },
        'laptop-lenovo': {
            img: 'img/imgLeo/LQP.webp', // Ruta corregida
            desc: 'En laptops Lenovo',
            price: '25% DSCTO',
            tag: 'Hasta',
            terms: 'Promoción válida del 01.06.2024 al 20.06.2024 para productos Lenovo. No acumulable con otras ofertas.'
        },
        'extractor-oster': {
            img: 'img/imgLeo/extractor.png', // Ruta corregida
            desc: 'En extractores Oster',
            price: 'S/. 550',
            tag: 'Desde',
            terms: 'Promoción válida del 01.06.2024 al 20.06.2024 para productos Oster. No acumulable con otras ofertas.'
        },
        'samsung-s24': {
            img: 'img/imgLeo/samsumg.png', // Ruta corregida
            desc: 'Samsung S24 Ultra',
            price: 'S/. 5000',
            tag: 'Promoción',
            terms: 'Promoción válida del 01.06.2024 al 20.06.2024 para productos Samsung. No acumulable con otras ofertas.'
        },
        'vinos-tabernero': {
            img: 'img/imgLeo/VinoTa.png', // Ruta corregida
            desc: 'En vinos Tabernero',
            price: 'S/. 20',
            tag: 'Desde',
            terms: 'Promoción válida del 01.06.2024 al 20.06.2024 para productos Tabernero. No acumulable con otras ofertas.'
        },
    };

    // Actualizar el contenido de la página si la promoción existe
    if (promociones[promo]) {
        promoImg.src = promociones[promo].img;
        promoP.textContent = promociones[promo].desc;
        promoH1.textContent = promociones[promo].price;
        promoH2.textContent = promociones[promo].tag;
        promoTerms.textContent = promociones[promo].terms;
    } else {
        promoP.textContent = "No se encontró la promoción.";
    }
});
