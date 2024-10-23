const secciones = document.querySelectorAll(".seccionImg");
secciones.forEach(seccion => {
    const imgInputs = seccion.querySelectorAll('.campoImg');
    const previewImg = seccion.querySelector('#previewImg');

    imgInputs.forEach(imgInput => {
        imgInput.addEventListener('change', function(event) {
            const file = event.target.files[0];
            if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                previewImg.src = e.target.result;  // Cambia la imagen mostrada a la seleccionada
            }
            reader.readAsDataURL(file);  // Leer archivo como Data URL
            }
        });
    });



});
