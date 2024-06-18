// Funciones de validación

// Chequea si un input de tipo string es no vacio
const validateGeneralInput = (input) => {
    if(input === ""){
        return false
    }
    return true;
}

// Función que valida el nombre del comprador/vendedor min 3 caracteres maximo 80
const validateName = (name) => {
    // Usa la validación general para nombres
    return name.trim().length >= 3 && name.trim().length <= 80;
}


// Chequea input de Productos, mínimo 1 máximo 5
const validateProducto = () => {
    // Obligatorio elegir una opción
    const productoInput = document.getElementById("productos");
    const opciones_seleccionadas = productoInput.selectedOptions.length;

    // No seleccionó o seleccionó muchas
    return opciones_seleccionadas >= 1 && opciones_seleccionadas <= 5;
}
// Función para validar el email
const validateEmail = (email) => {
    // Expresión regular para validar el formato del email
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Función para validar el teléfono
const validateTelefono = (phone) => {
    // Expresión regular para validar el formato del teléfono (código chileno)
    const regexTelefono = /^569\d{8}$/;
    return regexTelefono.test(phone);
}

// Función para abrir el modal
function abrirModal(input) {
    // Obtener el modal
    const modal = document.getElementById(input);
    // Mostrar el modal en pantalla
    modal.style.display = "block";
}

// --- Form Submission Function ---

function submitPedido() {
    console.log("Submitting form...");

    // Obtener los botones
    const confirmarBtn = document.getElementById("confirmarBtn2");
    const cancelarBtn = document.getElementById("cancelarBtn2");

    // Get form elements by ID
    const productoInput = document.getElementById("productos");
    const comunaInput = document.getElementById("comunas");
    const nombreInput = document.getElementById("name");
    const emailInput = document.getElementById("email");
    const phoneInput = document.getElementById("phone");

    let isValid = true;
    let errorMessage = "";

    // Reset input borders to default
    const inputs = [productoInput,comunaInput,nombreInput, emailInput, phoneInput];
    inputs.forEach((input) => {
        input.style.borderColor = "";
    });
    // Validate Productos
    if (!validateProducto()) {
        isValid = false;
        errorMessage += "Por favor, selecciona al menos 1 producto y máximo 5\n";
    }
    // Validate Comuna 
    if (!validateGeneralInput(comunaInput.value)) {
        isValid = false;
        errorMessage += "Por favor, selecciona una Comuna \n";
        emailInput.style.borderColor = "red";
    }  
    // Validate name 
    if (!validateName(nombreInput.value)) {
        isValid = false;
        errorMessage += "Por favor, ingresa un nombre válido.\n";
        nombreInput.style.borderColor = "red";
    }

    // Validate email
    if (!validateEmail(emailInput.value)) {
        isValid = false;
        errorMessage += "Por favor, ingresa un correo electrónico válido.\n";
        emailInput.style.borderColor = "red";
    }

    // Validate phone number
    if (!validateTelefono(phoneInput.value)) {
        isValid = false;
        errorMessage += "Por favor, ingresa un número válido. El formato debe ser 569XXXXXXXX\n";
        phoneInput.style.borderColor = "red";
    }

    // Display error message or success message
    if (!isValid) {
        alert(errorMessage); // Use a more user-friendly approach like a modal
    } else {
        // Si los datos son válidos, muestra el modal de confirmación
        abrirModal("mymodal2");
    }

    // Cuando el usuario haga clic en Sí, confirmo, mostrar el mensaje de agradecimiento y redirigir a la página principal
    confirmarBtn.onclick = function () {
        alert("Hemos recibido su pedido. Muchas gracias.");
        window.location.href = "index.html"; // Redirigir a la página principal
    }

    // Cuando el usuario haga clic en No, quiero volver al formulario, cerrar el modal
    cancelarBtn.onclick = function () {
        const modal = document.getElementById("mymodal2");
        modal.style.display = "none";
    }
}

// Asignar evento onclick al botón "Agregar Pedido (s)"
document.addEventListener("DOMContentLoaded", function () {
    const agregarBtn = document.getElementById("button2");
    agregarBtn.addEventListener("click", submitPedido);
});

