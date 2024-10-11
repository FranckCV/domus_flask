document.addEventListener('DOMContentLoaded', () => {
    const agregarDivs = document.querySelectorAll('.product_option_add');

    agregarDivs.forEach(div => {
        div.addEventListener('click', (event) => {
                actualizarCantidadCarrito();
        });
    });
});
function actualizarCantidadCarrito() {
    const carrito = obtenerCarrito();
    const contadorCarrito = document.getElementById('carrito_cant');
    let totalCantidad = 0;

    for (let producto in carrito) {
        totalCantidad += carrito[producto].cantidad;
    }

    contadorCarrito.innerText =`${totalCantidad}`;
    contadorCarrito.classList.add('animate-bounce');
    setTimeout(() => {
        contadorCarrito.classList.remove('animate-bounce');
    }, 500);
}

document.addEventListener('DOMContentLoaded', actualizarCantidadCarrito);
function obtenerCarrito() {
    return JSON.parse(localStorage.getItem('carrito')) || {};
}

function guardarCarrito(carrito) {
    localStorage.setItem('carrito', JSON.stringify(carrito));
}