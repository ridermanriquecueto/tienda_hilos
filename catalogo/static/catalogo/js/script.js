document.addEventListener("DOMContentLoaded", function () {
    actualizarTotalCarrito();
    manejarEventos();
});

function manejarEventos() {
    document.querySelectorAll(".agregar-carrito").forEach(boton => {
        boton.addEventListener("click", function () {
            agregarAlCarrito(this);
        });
    });
    
    const metodoPagoElem = document.getElementById("metodoPago");
    if (metodoPagoElem) {
        metodoPagoElem.addEventListener("change", mostrarCamposPago);
    }

    const formCompra = document.getElementById("formCompra");
    if (formCompra) {
        formCompra.addEventListener("submit", function (event) {
            if (!validarFormulario()) {
                event.preventDefault();
            }
        });
    }
}

function agregarAlCarrito(boton) {
    const id = boton.getAttribute("data-id");
    const nombre = boton.getAttribute("data-nombre");
    const precio = parseFloat(boton.getAttribute("data-precio"));
    const cantidad = parseInt(document.getElementById("cantidad-" + id).value) || 1;
    const carrito = JSON.parse(localStorage.getItem("carrito")) || [];
    
    let producto = carrito.find(item => item.id === id);
    if (producto) {
        producto.cantidad += cantidad;
    } else {
        carrito.push({ id, nombre, precio, cantidad });
    }
    
    localStorage.setItem("carrito", JSON.stringify(carrito));
    actualizarTotalCarrito();
    mostrarMensaje("Producto agregado al carrito", "success");
}

function actualizarTotalCarrito() {
    const totalElem = document.getElementById("totalCarrito");
    if (!totalElem) {
        return;
    }

    const carrito = JSON.parse(localStorage.getItem("carrito")) || [];
    const total = carrito.reduce((sum, item) => sum + (item.precio * item.cantidad), 0);
    totalElem.textContent = total.toFixed(2);
}

function mostrarCamposPago() {
    const metodoElem = document.getElementById("metodoPago");
    if (!metodoElem) {
        return;
    }

    const metodo = metodoElem.value;
    const datosTarjeta = document.getElementById("datosTarjeta");
    const datosTransferencia = document.getElementById("datosTransferencia");

    if (datosTarjeta) {
        datosTarjeta.style.display = metodo === "tarjeta" ? "block" : "none";
    }
    if (datosTransferencia) {
        datosTransferencia.style.display = metodo === "transferencia" ? "block" : "none";
    }
}

function validarFormulario() {
    const metodoElem = document.getElementById("metodoPago");
    if (!metodoElem) {
        return true;
    }

    const metodo = metodoElem.value;
    if (metodo === "tarjeta") {
        return validarTarjeta();
    } else if (metodo === "transferencia") {
        return validarTransferencia();
    }
    return true;
}

function validarTarjeta() {
    const numeroElem = document.getElementById("numeroTarjeta");
    const cvvElem = document.getElementById("cvv");
    if (!numeroElem || !cvvElem) {
        return true;
    }

    const numero = numeroElem.value;
    const cvv = cvvElem.value;
    if (numero.length !== 16 || isNaN(numero) || cvv.length !== 3 || isNaN(cvv)) {
        mostrarMensaje("Datos de tarjeta inválidos", "error");
        return false;
    }
    return true;
}

function validarTransferencia() {
    const comprobanteElem = document.getElementById("comprobantePago");
    if (!comprobanteElem) {
        return true;
    }

    const comprobante = comprobanteElem.files.length;
    if (comprobante === 0) {
        mostrarMensaje("Debe subir el comprobante de pago", "error");
        return false;
    }
    return true;
}

function mostrarMensaje(mensaje, tipo) {
    const alerta = document.createElement("div");
    alerta.className = `alerta alerta-${tipo}`;
    alerta.textContent = mensaje;
    document.body.appendChild(alerta);
    setTimeout(() => alerta.remove(), 3000);
}

// Animations: staggered fade-in for lists
function runStaggeredAnimations() {
    document.querySelectorAll('.animate-list').forEach(function(list){
        const items = list.querySelectorAll('.animate-item');
        const baseDelay = window.innerWidth <= 768 ? 40 : 70;
        items.forEach(function(item, i){
            setTimeout(function(){
                item.classList.add('fade-in-up','show');
            }, i * baseDelay);
        });
    });
}

document.addEventListener('DOMContentLoaded', function(){
    // run after other handlers; use smaller initial delay on mobile
    const initialDelay = window.innerWidth <= 768 ? 60 : 120;
    setTimeout(runStaggeredAnimations, initialDelay);
});
