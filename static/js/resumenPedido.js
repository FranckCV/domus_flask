let bloquearNavegacion = true;  // Variable para controlar cuándo bloquear


// Evitar retroceso
window.history.pushState(null, null, window.location.href);
window.addEventListener('popstate', function (event) {
    window.history.pushState(null, null, window.location.href);
});

function obtenerCarrito() {
    return JSON.parse(localStorage.getItem('carrito')) || {};
}
function eliminarTodos() {
    localStorage.clear();
}
function agregarResumen() {
    const elementosTotal = document.getElementsByClassName('total');
    const costoEnvio = document.getElementById('costo_envio');
    let costo = parseFloat(costoEnvio.value);

    let acumulador = 0;

    for (let i = 0; i < elementosTotal.length; i++) {
        acumulador += parseFloat(elementosTotal[i].innerText);
    }

    document.getElementById('total').innerText = `S/. ${(costo + acumulador).toFixed(2)}`;
    document.getElementById('subtotal').innerText = `S/. ${acumulador.toFixed(2)}`;
}


function cancelarCompra(button) {
    window.location.href = 'carrito.html';
}


function confirmarCompra(button) {
    var metodoPago = document.getElementById('metodo_pago').value;
    
    if (!metodoPago) {
        alert('Por favor, selecciona un método de pago antes de confirmar la compra.');
        return;  
    }

    var modalConfirmar = new bootstrap.Modal(document.getElementById('modalConfirmarCompra'));
    modalConfirmar.show();

    document.getElementById('btnConfirmarCompra').addEventListener('click', function() {
        bloquearNavegacion = false;
        let $square = $('.square'),
            $modal = $('.modal-thank');

        var shape = new mojs.Shape({
            shape: 'circle',
            isShowStart: true,
            fill: '#3847b8',
            opacity: { 0: 1 },
            stroke: '#FFF',
            strokeWidth: 0,
            duration: 300,
            delay: 0
        }).then({
            scale: { 0.5: 40 },
            duration: 500,
        });

        $square.addClass('active');
        shape.play();
        $modal.addClass('active');

        setTimeout(function () {
            eliminarTodos(); 
            window.location.href = '/'; 
        }, 2500);

        // Cerrar el modal
        modalConfirmar.hide();
    });
}


function cancelarCompra(button) {
    // Redirigir a la ruta para cancelar la compra en Flask
    window.location.href = '/cancelar_compra';
}

