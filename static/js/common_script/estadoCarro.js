document.addEventListener('DOMContentLoaded', () => {
    const agregarDivs = document.querySelectorAll('.product_option_add');

    agregarDivs.forEach(div => {
        div.addEventListener('click', (event) => {
            actualizarCantidadCarrito();
        });
    });

    actualizarCantidadCarrito();
});

function actualizarCantidadCarrito() {
    const carrito = obtenerCarrito();
    const contadorCarrito = document.getElementById('carrito_cant');
    let totalCantidad = 0;

    // Solo actualizamos si la sesión está activa
    if (isSessionActive()) {
        for (let producto in carrito) {
            totalCantidad += carrito[producto].cantidad;
        }

        contadorCarrito.innerText = `${totalCantidad}`;
        contadorCarrito.classList.add('animate-bounce'); 

        setTimeout(() => {
            contadorCarrito.classList.remove('animate-bounce'); 
        }, 500);
    } else {
        contadorCarrito.innerText = "0";
    }
}

function obtenerCarrito() {
    return JSON.parse(localStorage.getItem('carrito')) || {};
}

function isSessionActive() {
    return document.cookie.split(';').some((cookie) => cookie.trim().startsWith('username='));
}
