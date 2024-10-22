document.addEventListener('DOMContentLoaded', function () {    
    agregarResumen();
});

function obtenerCarrito() {
    return JSON.parse(localStorage.getItem('carrito')) || {};
}
function eliminarTodos() {
    localStorage.clear();
    actualizarDatos();
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

    // gsap.globalTimeline.clear();

    let $square = $('.square'),
        $span = $('.circle-expand'),
        $modal = $('.modal-thank')

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

    setTimeout(function() {
        window.location.href = 'index.html';
    }, 4500);
    
    eliminarTodos();
}