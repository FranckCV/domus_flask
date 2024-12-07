document.addEventListener('DOMContentLoaded', () => {
    const agregarDivs = document.querySelectorAll('.product_option_add');

    agregarDivs.forEach(div => {
        div.addEventListener('click', (event) => {
            actualizarCantidadLocalCarrito();
            // actualizarCantidadCarrito();
        });
    });

    actualizarCantidadCarrito();
});

function actualizarCantidadLocalCarrito() {
    const contadorCarrito = document.getElementById('carrito_cant');
    let totalCantidad = parseInt(contadorCarrito.innerText) || 0;
    totalCantidad++;

    contadorCarrito.innerText = `${totalCantidad}`;
    contadorCarrito.classList.add('animate-bounce'); 

    setTimeout(() => {
        contadorCarrito.classList.remove('animate-bounce'); 
    }, 500);
}

function actualizarCantidadCarrito() {
    const contadorCarrito = document.getElementById('carrito_cant');
    
    if (isSessionActive()) {
        fetch('/obtener_cantidad_carrito', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Error en la respuesta del servidor');
            }
            return response.json();
        })
        .then(data => {
            let totalCantidad = data.cantidad || 0;  
            contadorCarrito.innerText = `${totalCantidad}`;
            
            const unidadesElemento = document.getElementById('unidades');

            if (unidadesElemento) {
                unidadesElemento.innerText = `${totalCantidad}`;
            }

            contadorCarrito.classList.add('animate-bounce'); 

            setTimeout(() => {
                contadorCarrito.classList.remove('animate-bounce'); 
            }, 500);
        })
        .catch(error => {
            console.error('Error al obtener la cantidad del carrito:', error);
            contadorCarrito.innerText = "Error al cargar";
        });
    } else {
        contadorCarrito.innerText = "0"; 
    }
}

function isSessionActive() {
    return document.cookie.split(';').some(cookie => cookie.trim().startsWith('username='));
}