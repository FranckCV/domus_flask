document.addEventListener('DOMContentLoaded', () => {
    const agregarDivs = document.querySelectorAll('.product_option_add');

    agregarDivs.forEach(div => {
        div.addEventListener('click', (event) => {
                actualizarCantidadCarrito();
        });
    });
});
function actualizarCantidadCarrito() {
    const carrito = obtenerCarrito();
    const contadorCarrito = document.getElementById('carrito_cant');
    let totalCantidad = 0;

    for (let producto in carrito) {
        totalCantidad += carrito[producto].cantidad;
    }

    contadorCarrito.innerText =`${totalCantidad}`;
    contadorCarrito.classList.add('animate-bounce');
    setTimeout(() => {
        contadorCarrito.classList.remove('animate-bounce');
    }, 500);
}

document.addEventListener('DOMContentLoaded', actualizarCantidadCarrito);
function obtenerCarrito() {
    return JSON.parse(localStorage.getItem('carrito')) || {};
}

function guardarCarrito(carrito) {
    localStorage.setItem('carrito', JSON.stringify(carrito));
}

//PARA EL PERFIL E INICIO
function cambiarEncabezado(){
    // <a class="header_item header_option" id="header_perfil" href="{{url_for('iniciar_sesion')}}"></a>
    
// @app.route("/login", methods=['POST'])
// def login():
    
//     email = request.form.get('email-login')
//     password = request.form.get('password-login')
//     user=()
//     user=controlador_usuario_cliente.obtener_usuario_cliente_por_email(email)
//     print(user)
//     epassword=encstringsha256(password)
//     print(epassword)
//     if user and user[2]==epassword:
//         session['id']=user[0]
//         session['username'] = email
//         resp=make_response(redirect("/"))
//         resp.set_cookie('username',email)
//         return resp
//     else:
//         return redirect('/iniciar_sesion')
}