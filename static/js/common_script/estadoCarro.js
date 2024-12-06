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
    const contadorCarrito = document.getElementById('carrito_cant');
    
    // Solo actualizamos si la sesión está activa
    if (isSessionActive()) {
        fetch('/obtener_cantidad_carrito', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            let totalCantidad = data.cantidad || 0;  // Obtener la cantidad del carrito desde la base de datos

            contadorCarrito.innerText = `${totalCantidad}`;
            contadorCarrito.classList.add('animate-bounce');  // Agrega la animación

            setTimeout(() => {
                contadorCarrito.classList.remove('animate-bounce');  // Elimina la animación después de 500ms
            }, 500);
        })
        .catch(error => {
            console.error('Error al obtener la cantidad del carrito:', error);
        });
    } else {
        contadorCarrito.innerText = "0";  // Si la sesión no está activa, muestra 0
    }
}

function isSessionActive() {
    return document.cookie.split(';').some((cookie) => cookie.trim().startsWith('username='));
}
