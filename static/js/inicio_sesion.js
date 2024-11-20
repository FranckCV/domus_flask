const container=document.querySelector(".container");
const btnSignIn=document.getElementById("btn-sign-in");
const btnSignUp=document.getElementById("btn-sign-up");

btnSignIn.addEventListener("click",()=>{
    container.classList.remove("toggle");
});

btnSignUp.addEventListener("click",()=>{
    container.classList.add("toggle");
});

function forgotPassword(){
    window.alert("Correo enviado para recuperación de contraseña");
}

function cambiarColor(element) {
    if (element.value) {
      element.classList.add('has-value'); // Añadir clase si hay un valor seleccionado
    } else {
      element.classList.remove('has-value'); // Quitar clase si no hay valor seleccionado
    }
  }
  