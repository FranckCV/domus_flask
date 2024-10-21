// Obtener el elemento del perfil
const perfil = document.getElementById('header_perfil');
const menu = document.getElementById('perfil_menu');

// Agregar un listener para el clic en el perfil
perfil.addEventListener('click', function () {
    perfil.classList.toggle('active');
});

// Cerrar el menú si se hace clic fuera del perfil
window.addEventListener('click', function (e) {
    if (!perfil.contains(e.target)) {
        perfil.classList.remove('active');
    }
});
