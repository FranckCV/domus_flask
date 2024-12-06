let descuento=false
function obtenerCarrito() {
    return fetch('/obtener_carrito')
        .then(response => response.json())
        .then(data => {
            return data.carrito;
        })
        .catch(error => {
            console.error('Error al obtener carrito:', error);
            return {};
        });
}

document.addEventListener('DOMContentLoaded', () => {
    obtenerResumenCarrito();
});

function obtenerResumenCarrito() {
    fetch('/obtener_resumen_carrito')
        .then(response => response.json())
        .then(data => {
            console.log(data); 
            if (data.error) {
                console.error('Error al obtener el carrito:', data.error);
                return;
            }
            
            document.getElementById('subtotal').querySelector('span').innerText = `S/. ${parseFloat(data.subtotal).toFixed(2)}`;
            document.getElementById('descuento').querySelector('span').innerText = `S/. ${parseFloat(data.descuento).toFixed(2)}`;
            document.getElementById('total').querySelector('span').innerText = `S/. ${parseFloat(data.total).toFixed(2)}`;
            
            if (data.descuento_aplicado) {
                document.getElementById('descuento').querySelector('span').style.color = "green";  
            } else {
                document.getElementById('descuento').querySelector('span').style.color = "red";  
            }
        })
        .catch(error => {
            console.error('Error al obtener el resumen del carrito:', error);
        });
}

function aplicarDescuento(){
    if(descuento){
        descuento=false;
       return descuento; 
    }
    else{
        descuento=true;
        return true;
    }
}
