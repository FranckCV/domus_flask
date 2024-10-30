//Variable global para saber si se ha aplicado un descuento o no 
let descuentoAplicado = false;


/*************************************************************************************** */

function agregarProducto(nombre, precio, img, id) {//pasa como parametros el nombre, el precio y la imagen
    let carrito = obtenerCarrito(); //Llama a la función que obtiene el carrito de compras
    //Esa función te devuelve un objeto con todos los elementos del carrito, se usa como clave el nombre del producto 
    if (carrito[nombre]) { //Si el producto ya existe en el carrito, aumenta la cantidad
        carrito[nombre].cantidad += 1;
    } else {
        carrito[nombre] = { //Si el producto no existe, crea un objeto y los inicializa
            precio: precio,
            img: img,
            cantidad: 1,
            id: id
        }
    }
    guardarCarrito(carrito); //Se llama a la función guardar en el carrito
    actualizarCarrito(); //Se actualiza el carre
}
function obtenerCarrito() { //Estas son funciones localStorage para obtener los items del carro y para guardarlo
    return JSON.parse(localStorage.getItem('carrito')) || {}; //Busca en el localStorage el carrito, si no lo encuentra, lo crea como un objeto vacío
}

function guardarCarrito(carrito) {
    localStorage.setItem('carrito', JSON.stringify(carrito)); //Guarda el carrito en el localStorage

}


/**********************************************LÓGICA PROPIA DEL CARRO******************************************************/
function aumentar(button) {
    const productElement = button.closest('.product_item'); //Todos los divs que contienen la info del producto empiezan con row, entonces
    //busca la etiqueta más cerca que contenga la clase row de ese botón
    const nombreProducto = productElement.querySelector('.nombreProducto').innerText; //obtiene el nombre de ese producto
    const descuentoElement = document.getElementById('descuento');
    let carrito = obtenerCarrito(); //llamamos al carrito para modificar su cantidad
    if (carrito[nombreProducto].cantidad < 10) {
        carrito[nombreProducto].cantidad += 1;
        descuentoElement.querySelector('span').innerText = `S/.00.00`;
        descuentoAplicado = false;
    }
    else {
        alert("No puedes agregar más de 10 productos");
    }
    guardarCarrito(carrito);
    actualizarCarrito();
    actualizarCantidadCarrito();
}

function disminuir(button) {
    const productElement = button.closest('.product_item');
    const nombreProducto = productElement.querySelector('.nombreProducto').innerText;
    //obtenemos la etiqueta de descuento porque si va a eliminar productos, entonces su descuento ya no es válido
    const descuentoElement = document.getElementById('descuento');
    let carrito = obtenerCarrito();

    if (carrito[nombreProducto]) {
        carrito[nombreProducto].cantidad -= 1;
        descuentoElement.querySelector('span').innerText = `S/.00.00`;
        descuentoAplicado = false;
        if (carrito[nombreProducto].cantidad < 1) { //Si la cantidad agregada de ese elemento es 0
            delete carrito[nombreProducto];
        }
        guardarCarrito(carrito);
        actualizarCarrito();
        actualizarCantidadCarrito();
        console.log(carrito[nombreProducto].cantidad)
    }
}

function actualizarCarrito() {
    const carrito = obtenerCarrito();
    const carritoContenido = document.getElementById('carrito-contenido');
    carritoContenido.innerHTML = '';
    let total = 0;
    let unidades = 0;

    for (let nombre in carrito) {
        const producto = carrito[nombre];
        const totalProducto = producto.precio * producto.cantidad;
        total += totalProducto;
        unidades += producto.cantidad;

    }

    document.getElementById('subtotal').querySelector('span').innerText = `S/. ${total.toFixed(2)}`;
    document.getElementById('total').querySelector('span').innerText = `S/. ${total.toFixed(2)}`;
    document.getElementById('unidades').innerText = unidades;
}

function aplicarDescuento() {
    const cupon = document.getElementById('coupon').value;
    const descuentoElement = document.getElementById('descuento');
    const totalElement = document.getElementById('total');
    let descuento = 0;

    const carrito = obtenerCarrito();
    let disponible = false;

    for (let nombre in carrito) {
        if (carrito[nombre].cantidad > 0) {
            disponible = true;
            break;
        }
    }

    if (descuentoAplicado) {
        alert('Cupón ya aplicado.');
    } else {
        if (cupon === 'DOMUSESMICASA50' && disponible) {
            let total = parseFloat(totalElement.querySelector('span').innerText.replace('S/. ', ''));
            descuento = total * 0.20;  // Aplicar el 20% de descuento
            descuentoElement.querySelector('span').innerText = `S/. ${descuento.toFixed(2)}`;
            total -= descuento;
            totalElement.querySelector('span').innerText = `S/. ${total.toFixed(2)}`;
            document.getElementById('total_fijo').innerText = `S/. ${total.toFixed(2)}`;

            descuentoAplicado = true;
        } else {
            alert('Cupón no es válido o el carrito está vacío.');
        }
    }
}


function validarCarro() {
    const carrito = obtenerCarrito();

    // Verificar si el carrito tiene productos
    let disponible = false;
    for (let nombre in carrito) {
        if (carrito[nombre].cantidad > 0) {
            disponible = true;
            break;
        }
    }

    if (disponible) {
        obtenerTotal();
        return true;
    } else {
        alert('Agregue productos a su carrito antes de continuar.');
        return false;
    }
}


function obtenerTotal() {
    var totalTexto = document.getElementById("total_fijo").innerText;

    var totalValor = totalTexto.replace('S/. ', '').replace(',', '');

    var totalNumero = parseFloat(totalValor) || 0;

    console.log("Total a pagar: ", totalNumero);

    document.getElementById("total_form").value = totalNumero;

    return totalNumero;
}


function obtenerDescuento() {
    if (typeof descuentoAplicado !== 'undefined' && descuentoAplicado) {  
        var descuentoTexto = document.getElementById("descuentoValor").innerText;

        var totalDescuento = descuentoTexto.replace('S/. ', '').replace(',', '');
        var totalNumero = parseFloat(totalDescuento) || 0;  

        console.log("Descuento aplicado: ", totalNumero);

        document.getElementById("total_descuento").value = totalNumero;

        return totalNumero;
    } else {
        console.log("Descuento no aplicado o descuentoAplicado indefinido.");
        return 0;
    }
}

