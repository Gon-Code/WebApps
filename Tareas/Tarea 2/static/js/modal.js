// Obtén el modal
var modal = document.getElementById("myModal");

// Obtén los botones de confirmar y cancelar
var confirmarBtn = document.getElementById("confirmarBtn");
var cancelarBtn = document.getElementById("cancelarBtn");

// Obtén el mensaje del modal
var modalMessage = document.getElementById("modalMessage");

// Cuando el usuario hace clic en el botón de confirmar, envía el formulario
confirmarBtn.onclick = function() {
    document.getElementById("form_add_producto").submit();
}

// Cuando el usuario hace clic en el botón de cancelar, cierra el modal
cancelarBtn.onclick = function() {
    modal.style.display = "none";
}

// Cuando el usuario hace clic fuera del modal, cierra el modal
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

// Cuando el formulario se envía, muestra el modal si es necesario
document.getElementById("form_add_producto").addEventListener("submit", function(event) {
    // Realiza la validación del formulario en el servidor (Python)
    // Si la validación es exitosa, el formulario se enviará normalmente y el modal se mostrará después
    // Si la validación falla, el formulario no se enviará y el modal no se mostrará

    // Mostrar el modal solo si la validación es exitosa
    modalMessage.innerText = "¿Confirma el registro de este producto?";
    modal.style.display = "block";

    // Detener el envío del formulario normalmente
    event.preventDefault();
});
