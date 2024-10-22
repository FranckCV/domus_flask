let bloquearNavegacion = true;  // Variable para controlar cuándo bloquear

window.addEventListener('beforeunload', function (event) {
    if (bloquearNavegacion) {
        event.preventDefault();
        event.returnValue = '';  // Muestra advertencia solo si está permitido
    }
});

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
    bloquearNavegacion = false;
    let $square = $('.square'),
        $modal = $('.modal-thank');

    // Crear la animación de confirmación con mojs
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

    // Activar los elementos visuales
    $square.addClass('active');
    shape.play();
    $modal.addClass('active');

    // Redirigir y limpiar el carrito después de la animación
    setTimeout(function () {
        eliminarTodos(); // Eliminar el carrito
        window.location.href = '/'; // Redirigir
    }, 2500);
}
