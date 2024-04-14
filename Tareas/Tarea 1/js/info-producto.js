// Funcion que redirige al clickear la fila de una tabla

const redirect = (url) => {
    window.location.href = url; 

}

// Funcion que muestra la imagen mas grande al clickearla

const showImage = (src) => {
    let modal = document.getElementById('modal');
    let imagenModal = document.getElementById('imagenModal');
    imagenModal.src = src;
    modal.style.display = "block";
    
}

// Funcion para cerrar el modal

const hideImage = () => {
    let modal = document.getElementById('modal');
    modal.style.display = "none";

}