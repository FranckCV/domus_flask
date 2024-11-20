const seccionesMulti = document.querySelectorAll(".seccionImg");
seccionesMulti.forEach(seccion => {
    const imgInput = seccion.querySelector('.campoImg');
    const previewImgMulti = seccion.querySelector('.espacio_img');

    if (previewImgMulti) {
        imgInput.addEventListener('change', function(event) {
            previewImgMulti.innerHTML = ""; 
            const files = event.target.files;
    
            for (const file of files) {
                const reader = new FileReader();
                reader.onload = function (e) {
                    const img = document.createElement("img");
                    img.src = e.target.result;
                    img.classList.add('clickable-image'); 
                    previewImgMulti.appendChild(img);
                };
                reader.readAsDataURL(file);
            }
        });
    }    
});
