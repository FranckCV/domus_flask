function colorFromId(id) {
    const color = "#" + (((id + -1) * 54321) % 16777215).toString(16).padStart(6, '0');
    return color;
}

// function colorFromId(id) {
//     const color = "#" + ((id * 54321) % 0x7F7F7F + 0x202020).toString(16).padStart(6, '0');
//     return color;
// }
  
document.querySelectorAll('.color_texto').forEach(bloque => {
    const texto = bloque.querySelector('p');
    const id = parseInt(bloque.getAttribute('data-colorid'));
    texto.style.backgroundColor = colorFromId(id);
});