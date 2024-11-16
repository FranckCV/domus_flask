const fechas = document.querySelectorAll('input[type="date"]'); 
fechas.forEach(fecha => {
    fecha.addEventListener('change', function () {
        const DIAS = 14;

        const fechaInicio = document.getElementById('fecha_inicio').value;
        const fechaVencimiento = document.getElementById('fecha_vencimiento').value;

        const inicio = new Date(fechaInicio);
        const vencimiento = new Date(fechaVencimiento);

        const posibleVenc = new Date(inicio.getTime() + DIAS * 24 * 60 * 60 * 1000);

        if (vencimiento < inicio) {
            alert(`La fecha de vencimiento debe ser posterior a la fecha de inicio. (Posible fecha minima: ${posibleVenc})`);
            this.value = ""; 
            return;
        }

        const diferenciaEnMilisegundos = vencimiento - inicio;
        const diferenciaEnDias = diferenciaEnMilisegundos / (1000 * 60 * 60 * 24);

        if (diferenciaEnDias < DIAS) {
            alert(`La fecha de vencimiento debe ser al menos ${DIAS} días después de la fecha de inicio. (Posible fecha minima: ${posibleVenc.toISOString().split('T')[0]})`);
            this.value = ""; 
        }
    });
});