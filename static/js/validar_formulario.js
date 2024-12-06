// PARA VALIDAR INICIO
const loginForm = document.querySelector('#login-form');
const emailLoginEl = document.querySelector('#email-login');
const passwordLoginEl = document.querySelector('#password-login');
//PARA VALIDAR REGISTRO
const usernameEl = document.querySelector('#username');
const lastnameEl = document.querySelector('#lastname');
const dniEl = document.querySelector('#dni');
const telefonoEl = document.querySelector('#telefono');
const passwordEl = document.querySelector('#password');
const passwordConfirm=document.querySelector('#confirm-password')
const emailEl = document.querySelector('#email-signup');
const signupForm = document.querySelector('#signup-form');
const terminos = document.querySelector("#terminos");

// Validar solo letras
const checkName = (input) => {
    let valid = false;
    const re = /^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$/; 
    const name = input.value.trim();

    if (!isRequired(name)) {
        showError(input, 'Este campo no puede estar vacío.');
    } else if (!re.test(name)) {
        showError(input, 'Solo se permiten letras y espacios.');
    } else {
        showSuccess(input);
        valid = true;
    }
    return valid;
};

// Validar DNI (8 dígitos, solo números)
const checkDni = () => {
    let valid = false;
    const dni = dniEl.value.trim();

    if (!isRequired(dni)) {
        showError(dniEl, 'El DNI no puede estar vacío.');
    } else if (!/^\d{8}$/.test(dni)) {
        showError(dniEl, 'El DNI debe tener 8 dígitos numéricos.');
    } else {
        showSuccess(dniEl);
        valid = true;
    }
    return valid;
};

// Validar teléfono (9 dígitos, empieza con 9)
const checkTelefono = () => {
    let valid = false;
    const telefono = telefonoEl.value.trim();

    if (!isRequired(telefono)) {
        showError(telefonoEl, 'El número de teléfono no puede estar vacío.');
    } else if (!/^9\d{8}$/.test(telefono)) {
        showError(telefonoEl, 'El teléfono debe tener 9 dígitos y comenzar con 9.');
    } else {
        showSuccess(telefonoEl);
        valid = true;
    }
    return valid;
};

// Validar correo electrónico (formato válido)
const checkEmail = (input) => {
    let valid = false;
    const email = input.value.trim();

    if (!isRequired(email)) {
        showError(input, 'El correo no puede estar vacío.');
    } else if (!isEmailValid(email)) {
        showError(input, 'El correo no es válido.');
    } else {
        showSuccess(input);
        valid = true;
    }
    return valid;
};

// Validar contraseña (mínimo 6, máximo 10 caracteres)
const checkPassword = (input) => {
    let valid = false;
    const password = input.value.trim();

    if (!isRequired(password)) {
        showError(input, 'La contraseña no puede estar vacía.');
    } else if (!/^\S{6,15}$/.test(password)) {
        showError(input, 'La contraseña debe tener entre 6 y 15 caracteres.');
    } else {
        showSuccess(input);
        valid = true;
    }
    return valid;
};

const checkPasswordMatch = () => {
    let valid = false;
    const password = passwordEl.value.trim();
    const confirmPassword = passwordConfirm.value.trim();

    if (!isRequired(confirmPassword)) {
        showError(passwordConfirm, 'La confirmación de contraseña no puede estar vacía.');
    } else if (password !== confirmPassword) {
        showError(passwordConfirm, 'Las contraseñas no coinciden.');
    } else {
        showSuccess(passwordConfirm);
        valid = true;
    }
    return valid;
};

// Validar si los términos están aceptados
const checkTerminos = () => {
    let valid = false;
    if (!terminos.checked) {
        showError(terminos, 'Debes aceptar los términos y condiciones.');
    } else {
        showSuccess(terminos);
        valid = true;
    }
    return valid;
};

// Funciones generales
const isRequired = value => value === '' ? false : true;

const showError = (input, message) => {
    const formField = input.parentElement;
    formField.classList.remove('success');
    formField.classList.add('error');
    
    const error = formField.querySelector('small');
    if (error) {
        error.textContent = message;
    }

    if (input.type === 'checkbox') {
        input.style.border = '2px solid red';
    }
};

const showSuccess = (input) => {
    const formField = input.parentElement;
    formField.classList.remove('error');
    formField.classList.add('success');
    
    const error = formField.querySelector('small');
    if (error) {
        error.textContent = '';
    }

    if (input.type === 'checkbox') {
        input.style.border = '2px solid #ccc';  
    }
};


const isEmailValid = (email) => {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
};

const debounce = (fn, delay = 500) => {
    let timeoutId;
    return (...args) => {
        if (timeoutId) {
            clearTimeout(timeoutId);
        }
        timeoutId = setTimeout(() => {
            fn.apply(null, args);
        }, delay);
    };
};

// Evento de validación del formulario de registro
signupForm.addEventListener('submit', function (e) {
    e.preventDefault();

    const isUsernameValid = checkName(usernameEl),
          isLastnameValid = checkName(lastnameEl),
          isDniValid = checkDni(),
          isTelefonoValid = checkTelefono(),
          isEmailValid = checkEmail(emailEl),
          isPasswordValid = checkPassword(passwordEl),
          isPasswordMatchValid = checkPasswordMatch(), // Validar que las contraseñas coincidan
          areTerminosAccepted = checkTerminos(); 

    const isFormValid = isUsernameValid && isLastnameValid && isDniValid && isTelefonoValid && isEmailValid && isPasswordValid && isPasswordMatchValid && areTerminosAccepted;

    if (isFormValid) {
        console.log('Formulario válido!');
        signupForm.submit(); // Si todo es válido, envía el formulario
    }
});

// Evento de validación del formulario de inicio de sesión
loginForm.addEventListener('submit', function (e) {
    e.preventDefault();

    const isEmailLoginValid = checkEmail(emailLoginEl),
          isPasswordLoginValid = checkPassword(passwordLoginEl);

    const isLoginFormValid = isEmailLoginValid && isPasswordLoginValid;

    if (isLoginFormValid) {
        console.log('Formulario de inicio de sesión válido!');
        // Aquí puedes realizar la acción de enviar o continuar
        loginForm.submit();
    }
});

loginForm.addEventListener('input', debounce(function (e) {
    switch (e.target.id) {
        case 'email-login':
            checkEmail(emailLoginEl);
            break;
        case 'password-login':
            checkPassword(passwordLoginEl);
            break;
    }
}, 500));

signupForm.addEventListener('input', debounce(function (e) {
    switch (e.target.id) {
        case 'username':
            checkName(usernameEl);
            break;
        case 'lastname':
            checkName(lastnameEl);
            break;
        case 'dni':
            checkDni();
            break;
        case 'telefono':
            checkTelefono();
            break;
        case 'email-signup':
            checkEmail(emailEl);
            break;
        case 'password':
            checkPassword(passwordEl);
            break;
        case 'confirm-password':
            checkPasswordMatch();
            break;
    }
}, 500));