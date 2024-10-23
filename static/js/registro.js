document.getElementById('fecha_nacimiento').type = 'text';
function cambiarColor(element) {
    if (element.value) {
      element.classList.add('has-value'); // Añadir clase si hay un valor seleccionado
    } else {
      element.classList.remove('has-value'); // Quitar clase si no hay valor seleccionado
    }
  }
  