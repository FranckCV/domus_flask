//Variable global para saber si se ha aplicado un descuento o no 
let descuentoAplicado = false;
/*Empezamos un listener para asegurarnos que el documento esté cargado, por eso dice 'DOMContentLoaded', una vez
haya sido cargado, usamos una función flecha*/
/*Empezamos actualizando el carrito, en caso ya se hayan agregado elementos al carro desde otra página, va a carga
su imagen, su nombre, su precio, la cantidad agregada y el subtotal */
/*Cada vez que se obtiene un valor de una etiqueta html y sabes que no va a cambiar, la declaras como const
Vamos a seleccionar todos los elementos que tengan la clase 'product_option_add', y por cada div que encuentre que ejecuta
el evento de escucha, donde identifique que se hizo click, eso se guarda como un evento */

document.addEventListener('DOMContentLoaded', () => {
    actualizarCarrito();
    actualizarCantidadCarrito();
    const agregarDivs = document.querySelectorAll('.product_option_add');

    agregarDivs.forEach(div => {
        div.addEventListener('click', (event) => { //'click' es el evento que se dispara cuando se hace click en el elemento
            console.log("CLICK EN AGREGAR");//Los consoles que veas fue pq salían errores y no sabía dónde estaba fallando, xd
            const productElement = event.target.closest('.product');//aquí busca la etiqueta más cerca que contenga la clase product
            if (productElement) { //si es que sí se encuentra, se extrae el nombre de producto, la imagen, y el precio
                const nombreProducto = productElement.querySelector('.product_name').innerText;
                const img = productElement.querySelector('.product_pic').src;
                //la etiqueta de precio va a variar según lo que se encuentre
                const priceOferta = productElement.querySelector('.price_for_sale .product_price_number');
                const priceOnline = productElement.querySelector('.price_online .product_price_number');

                let precio = 0; //lo declaramos como let porque va a variar

                if (priceOferta) {//Si encuentra una etiqueta de precio oferta ejecuta la línea de código, sino usa
                    // la etiqueta de precio online
                    //Replace se usa para eliminar la parte del texto que indica la moneda ("S/. ") y dejar solo los números.
                    //El otro replace se usa para eliminar la coma que separa los miles, si es que existe
                    precio = parseFloat(priceOferta.innerText.replace('S/. ', '').replace(',', ''));
                } else if (priceOnline) {
                    precio = parseFloat(priceOnline.innerText.replace('S/. ', '').replace(',', ''));
                }

                agregarProducto(nombreProducto, precio, img); //Llama a la función agregar producto
                actualizarCarrito(); //llama a la función actualizar carre
                actualizarCantidadCarrito(); //Actualiza la cantidad de productos agregados que sale en el header
                console.log(productElement); //por si acaso haya errores
            } else {
                console.log("No se encontró el elemento del producto."); //por si acaso haya errores x2 
            }
        });
    });
});


function agregarProducto(nombre, precio, img) {//pasa como parametros el nombre, el precio y la imagen
    let carrito = obtenerCarrito(); //Llama a la función que obtiene el carrito de compras
    //Esa función te devuelve un objeto con todos los elementos del carrito, se usa como clave el nombre del producto 
    if (carrito[nombre]) { //Si el producto ya existe en el carrito, aumenta la cantidad
        carrito[nombre].cantidad += 1;
    } else {
        carrito[nombre] = { //Si el producto no existe, crea un objeto y los inicializa
            precio: precio,
            img: img,
            cantidad: 1
        };
    }
    guardarCarrito(carrito); //Se llama a la función guardar en el carrito
    actualizarCarrito(); //Se actualiza el carre
}
function obtenerCarrito() { //Estas son funciones localStorage para obtener los items del carro y para guardarlo
    return JSON.parse(localStorage.getItem('carrito')) || {}; //Busca en el localStorage el carrito, si no lo encuentra, lo crea como un objeto vacío
}

function guardarCarrito(carrito) {
    localStorage.setItem('carrito', JSON.stringify(carrito)); //Guarda el carrito en el localStorage
    //Carrito es un objeto de objetos, se guarda algo así
    /*
    {
  "nombreProducto1": {
    "precio": 20,
    "img": "imagen1.png",
    "cantidad": 1
  },
  "nombreProducto2": {
    "precio": 30,
    "img": "imagen2.png",
    "cantidad": 1
  }
}
     */
}


/**********************************************LÓGICA PROPIA DEL CARRO******************************************************/
function aumentar(button) {
    const productElement = button.closest('.product_item'); //Todos los divs que contienen la info del producto empiezan con row, entonces
    //busca la etiqueta más cerca que contenga la clase row de ese botón
    const nombreProducto = productElement.querySelector('.nombreProducto').innerText; //obtiene el nombre de ese producto
    const descuentoElement = document.getElementById('descuento'); 
    let carrito = obtenerCarrito(); //llamamos al carrito para modificar su cantidad
    if(carrito[nombreProducto].cantidad<10) {
        carrito[nombreProducto].cantidad += 1;
        descuentoElement.querySelector('span').innerText = `S/.00.00`;
        descuentoAplicado = false;    
    }
    else{
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

        const productoHTML = `
            <div class="product_item">
                <div class="product_item_info">
                    <img src="${producto.img}" class="product_item_pic" alt="Imagen del Producto">
                    
                    <div class="product_item_name">
                        <p class="nombreProducto">${nombre}</p>
                        <p class="vendido-por">Vendido por: <strong>Domus</strong></p>
                    </div>
                </div>

                <div class="product_item_price_unit">
                    <p class="precioProducto">S/ ${producto.precio.toFixed(2)}</p>
                </div>

                <div class="product_item_count">
                    <button type="button" class="btn btn-outline-primary btn-responsive btn-round mx-3" onclick="disminuir(this)"><span class="signo">-</span></button>
                    <label class="cant">${producto.cantidad}</label>
                    <button type="button" class="btn btn-outline-primary btn-responsive btn-round mx-3" onclick="aumentar(this)"><span class="signo">+</span></button>
                </div>

                <div class="product_item_price_total">
                    <p class="total"> S/ ${totalProducto.toFixed(2)}</p>
                </div>
            </div>
        `;

        carritoContenido.insertAdjacentHTML('beforeend', productoHTML);
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
        alert('Cupon aplicado exitosamente.');
    } else {
        if (cupon === 'DOMUSESMICASA50' && disponible) {
            let total = parseFloat(totalElement.querySelector('span').innerText.replace('S/. ', ''));
            descuento = total * 0.20;
            descuentoElement.querySelector('span').innerText = `S/. ${descuento.toFixed(2)}`;
            total -= descuento;
            totalElement.querySelector('span').innerText = `S/. ${total.toFixed(2)}`;
            descuentoAplicado = true;
        } else {
            alert('Cupón no es válido o el carrito está vacío.');
        }
    }
}

function validarCarro() {
    const carrito = obtenerCarrito();
    let disponible = false;
    for (let nombre in carrito) {
        if (carrito[nombre].cantidad > 0) {
            disponible = true;
            break;
        }
    }
    if (disponible) {
        window.location.href = "resumenDePedido.html";
    } else {
        alert('Agregue productos a su carrito');
    }
}

/***************************************PARA EL CONTADOR DE PRODUCTOS*****************************************************/
function actualizarCantidadCarrito() {
    const carrito = obtenerCarrito();
    const contadorCarrito = document.getElementById('carrito_cant');
    let totalCantidad = 0;

    for (let producto in carrito) {
        totalCantidad += carrito[producto].cantidad;
    }

    contadorCarrito.innerText = `${totalCantidad}`;
    contadorCarrito.classList.add('animate-bounce');
    setTimeout(() => {
        contadorCarrito.classList.remove('animate-bounce');
    }, 500);
}
