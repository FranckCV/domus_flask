if (!window.location.pathname.includes('carrito') || !window.location.pathname.includes('carrito.html') ) {        
    document.addEventListener('DOMContentLoaded', () => {
        const agregarDivs = document.querySelectorAll('.product_option_add');

        agregarDivs.forEach(div => {
            div.addEventListener('click', (event) => {
                console.log("CLICK EN AGREGAR");
                const productElement = event.target.closest('.product');
                if (productElement) {
                    const nombreProducto = productElement.querySelector('.product_name').innerText;
                    const img = productElement.querySelector('.product_pic').src;

                    const priceForSaleElement = productElement.querySelector('.price_for_sale .product_price_number');
                    const priceOnlineElement = productElement.querySelector('.price_online .product_price_number');

                    let precio = 0;

                    if (priceForSaleElement) {
                        precio = parseFloat(priceForSaleElement.innerText.replace('S/. ', '').replace(',', ''));
                    } else if (priceOnlineElement) {
                        precio = parseFloat(priceOnlineElement.innerText.replace('S/. ', '').replace(',', ''));
                    }

                    agregarProducto(nombreProducto, precio, img);

                    console.log(productElement);
                } else {
                    console.log("No se encontró el elemento del producto.");
                }
            });
        });
    });
    /***********************************************FUNCIONES GENERALES DEL LOCAL STORAGE***************************************/
    function obtenerCarrito() {
        return JSON.parse(localStorage.getItem('carrito')) || {};
    }

    function guardarCarrito(carrito) {
        localStorage.setItem('carrito', JSON.stringify(carrito));
    }
    /************************************************************************************************************/
    function agregarProducto(nombre, precio, img) {

        let carrito = obtenerCarrito();
        
        if (carrito[nombre]) {
            carrito[nombre].cantidad += 1;
        } else {
            carrito[nombre] = { 
                precio: precio, 
                cantidad: 1, 
                img: img };
        }

        guardarCarrito(carrito);
    }

}
