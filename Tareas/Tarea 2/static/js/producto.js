// Diccionarios de Frutas y Verduras, inicializados con su valores en 0

let frutas = {
    "Arándano": 0,
    "Frambuesa": 0,
    "Frutilla": 0,
    "Grosella": 0,
    "Mora": 0,
    "Limón": 0,
    "Mandarina": 0,
    "Naranja": 0,
    "Pomelo": 0,
    "Melón": 0,
    "Sandía": 0,
    "Palta": 0,
    "Chirimoya": 0,
    "Coco": 0,
    "Dátil": 0,
    "Kiwi": 0,
    "Mango": 0,
    "Papaya": 0,
    "Piña": 0,
    "Plátano": 0,
    "Damasco": 0,
    "Cereza": 0,
    "Ciruela": 0,
    "Higo": 0,
    "Kaki": 0,
    "Manzana": 0,
    "Durazno": 0,
    "Nectarin": 0,
    "Níspero": 0,
    "Pera": 0,
    "Uva": 0,
    "Almendra": 0,
    "Avellana": 0,
    "Maní": 0,
    "Castaña": 0,
    "Nuez": 0,
    "Pistacho": 0
};

let verduras = {
    "Brócoli": 0,
    "Repollo": 0,
    "Coliflor": 0,
    "Rábano": 0,
    "Alcachofa": 0,
    "Lechuga": 0,
    "Zapallo": 0,
    "Pepino": 0,
    "Haba": 0,
    "Maíz": 0,
    "Champiñón": 0,
    "Acelga": 0,
    "Apio": 0,
    "Espinaca": 0,
    "Perejil": 0,
    "Ajo": 0,
    "Cebolla": 0,
    "Espárrago": 0,
    "Puerro": 0,
    "Acelga": 0,
    "Espinaca": 0,
    "Remolacha": 0,
    "Berenjena": 0,
    "Papa": 0,
    "Pimiento": 0,
    "Tomate": 0,
    "Zanahoria": 0
};


// La funcion show toma el tipo de alimento que se selecciono en el primer formulario
// Luego cambia dinamicamente las opciones del formulario productos dependiendo de si respondio Fruta o Verdura 
const showProducts = () => {
    const tipoSeleccionado = document.getElementById("tipo").value;
    let Productos = document.getElementById("productos");

    // Obtener el diccionario correspondiente según el tipo seleccionado
    let diccionario = (tipoSeleccionado === "fruta") ? frutas : verduras;

    // Limpiar las opciones actuales del select
    Productos.innerHTML = "";

    // Agregar las opciones al menú desplegable
    for (let producto in diccionario) {
        let opcion = document.createElement("option");
        opcion.text = producto;
        opcion.value = producto;
        Productos.appendChild(opcion);
    }
}

// Llamar a la función showProducts cuando se cargue la página
window.onload = showProducts;
// Llamar a la función showProductos cuando se selecciona un tipo de alimento
document.getElementById("tipo").addEventListener("change", showProducts);

