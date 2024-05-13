// Funciones de validación

// Chequea formato del input de email es correcto
const validateEmail = (email) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

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

// Chequea input del teléfono, debe tener código chileno 569XXXXXXXX
const validateTelefono = (input) => {
    const regexTelefono = /^569\d{8}$/;
    return regexTelefono.test(input);
}

// Valida que se hayan seleccionado al menos 1 archivo y máximo 3
const validateArchivos = () => {
    const files = document.querySelectorAll('input[type="file"]');
    let archivosSeleccionados = 0;

    // Contamos cuántos archivos se seleccionaron
    for (let i = 0; i < files.length; i++) {
        if (files[i].files.length > 0) {
            archivosSeleccionados++;
        }
    }

    // Verificar que sean máximo 3 y al menos 1 
    return archivosSeleccionados >= 1 && archivosSeleccionados <= 3;
}

// Función para abrir el modal
function abrirModal() {
    // Obtener el modal
    const modal = document.getElementById("myModal");
    // Mostrar el modal en pantalla
    modal.style.display = "block";
}

// --- Form Submission Function ---

function submitProducto() {
    console.log("Submitting form...");

    // Obtener los botones
    const confirmarBtn = document.getElementById("confirmarBtn");
    const cancelarBtn = document.getElementById("cancelarBtn");

    // Get form elements by ID
    const regionInput = document.getElementById("regiones");
    const comunaInput = document.getElementById("comunas");
    const emailInput = document.getElementById("email");
    const nombreInput = document.getElementById("name");
    const phoneInput = document.getElementById("phone");

    let isValid = true;
    let errorMessage = "";
    
    // Reset input borders to default
    const inputs = [regionInput,comunaInput, emailInput, nombreInput, phoneInput];
    inputs.forEach((input) => {
        input.style.borderColor = "";
    });
    
    // Validate Productos
    if (!validateProducto()) {
        isValid = false;
        errorMessage += "Por favor, selecciona al menos 1 producto y máximo 5\n";
    }
    // Validate region 
    if (!validateGeneralInput(regionInput.value)) {
        isValid = false;
        errorMessage += "Por favor, Selecciona una Region \n";
        emailInput.style.borderColor = "red";
    }
    // Validate Comuna 
    if (!validateGeneralInput(comunaInput.value)) {
        isValid = false;
        errorMessage += "Por favor, selecciona una Comuna \n";
        emailInput.style.borderColor = "red";
    }
    // Validate Archivos
    if (!validateArchivos()) {
        isValid = false;
        errorMessage += "Por favor, ingresa al menos una fotografía\n";
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
        abrirModal();
    }

    // Cuando el usuario haga clic en Sí, confirmo, mostrar el mensaje de agradecimiento y redirigir a la página principal
    confirmarBtn.onclick = function () {
        alert("Hemos recibido el registro de producto. Muchas gracias.");
        window.location.href = "index.html"; // Redirigir a la página principal
    }

    // Cuando el usuario haga clic en No, quiero volver al formulario, cerrar el modal
    cancelarBtn.onclick = function () {
        const modal = document.getElementById("myModal");
        modal.style.display = "none";
    }
}

// Asignar evento onclick al botón "Agregar Producto (s)"
document.addEventListener("DOMContentLoaded", function () {
    const agregarBtn = document.getElementById("button1");
    agregarBtn.addEventListener("click", submitProducto);
});
