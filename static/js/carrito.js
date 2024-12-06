let descuento = false; // Para manejar si se ha aplicado el descuento

// Función para aplicar el descuento
function aplicarDescuento() {
    const subtotalElemento = document.getElementById('subtotal').querySelector('span');
    const descuentoElemento = document.getElementById('descuentoValor');
    const totalElemento = document.getElementById('total').querySelector('span');
    const totalFijoElemento = document.getElementById('total_fijo');
    const botonAplicar = document.getElementById('aplicar');  // Obtener el botón de aplicar descuento

    // Verificar si el descuento ya ha sido aplicado
    if (descuento) {
        mostrarModalError('El descuento aplicado con éxito.');
        botonAplicar.disabled = true; 
    }

    const subtotal = parseFloat(subtotalElemento.innerText.replace('S/. ', '').replace(',', '').trim());  // Obtener el subtotal
    const descuentoValor = subtotal * 0.20;

    descuentoElemento.innerText = `S/. ${descuentoValor.toFixed(2)}`;
    totalElemento.innerText = `S/. ${(subtotal - descuentoValor).toFixed(2)}`; // Total con descuento

    document.getElementById('total_form').value = (subtotal - descuentoValor).toFixed(2);
    document.getElementById('total_descuento').value = descuentoValor.toFixed(2);

    descuento = true;
    botonAplicar.setAttribute('data-aplicado', 'true');
    botonAplicar.innerText = 'Descuento aplicado';
    botonAplicar.disabled = true;  
}

function mostrarModalError(mensaje) {
    const modal = new bootstrap.Modal(document.getElementById('errorModal')); // Obtener el modal de Bootstrap
    const mensajeModal = document.querySelector('#errorModal .modal-body p'); // Obtener el párrafo dentro del modal
    mensajeModal.innerText = mensaje; 
    modal.show();
}

// Función para obtener el resumen del carrito desde el backend
function obtenerResumenCarrito() {
    fetch('/obtener_resumen_carrito')
        .then(response => response.json())
        .then(data => {
            console.log(data);
            if (data.error) {
                console.error('Error al obtener el carrito:', data.error);
                return;
            }

            // Actualizar los valores del subtotal, descuento y total en la interfaz
            document.getElementById('subtotal').querySelector('span').innerText = `S/. ${parseFloat(data.subtotal).toFixed(2)}`;
            document.getElementById('descuento').querySelector('span').innerText = `S/. ${parseFloat(data.descuento).toFixed(2)}`;
            document.getElementById('total').querySelector('span').innerText = `S/. ${parseFloat(data.total).toFixed(2)}`;

            // Si el descuento ha sido aplicado, cambiar el color del texto
            if (data.descuento_aplicado) {
                document.getElementById('descuento').querySelector('span').style.color = "green";
                descuento = true;  // Marcar que el descuento ha sido aplicado
                document.getElementById('aplicar').disabled = true;  // Deshabilitar el botón de aplicar descuento
                document.getElementById('aplicar').innerText = 'Descuento aplicado';  // Cambiar el texto del botón
            } else {
                document.getElementById('descuento').querySelector('span').style.color = "red";
                descuento = false;  // Reiniciar el estado del descuento
                document.getElementById('aplicar').disabled = false;  // Habilitar el botón de aplicar descuento
                document.getElementById('aplicar').innerText = 'Aplicar';  // Cambiar el texto del botón
            }
        })
        .catch(error => {
            console.error('Error al obtener el resumen del carrito:', error);
        });
}

document.addEventListener('DOMContentLoaded', () => {
    obtenerResumenCarrito();
});

function reiniciarDescuento() {
    descuento = false;  
    const botonAplicar = document.getElementById('aplicar');
    botonAplicar.disabled = false; 
    botonAplicar.innerText = 'Aplicar';  // Cambiar el texto del botón a "Aplicar"
}

document.getElementById('aplicar').addEventListener('click', () => {
    aplicarDescuento();
});

