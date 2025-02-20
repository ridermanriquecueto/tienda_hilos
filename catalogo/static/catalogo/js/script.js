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
    
    document.getElementById("metodoPago").addEventListener("change", mostrarCamposPago);
    
    document.getElementById("formCompra").addEventListener("submit", function (event) {
        if (!validarFormulario()) {
            event.preventDefault();
        }
    });
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
    const carrito = JSON.parse(localStorage.getItem("carrito")) || [];
    const total = carrito.reduce((sum, item) => sum + (item.precio * item.cantidad), 0);
    document.getElementById("totalCarrito").textContent = total.toFixed(2);
}

function mostrarCamposPago() {
    const metodo = document.getElementById("metodoPago").value;
    document.getElementById("datosTarjeta").style.display = metodo === "tarjeta" ? "block" : "none";
    document.getElementById("datosTransferencia").style.display = metodo === "transferencia" ? "block" : "none";
}

function validarFormulario() {
    const metodo = document.getElementById("metodoPago").value;
    if (metodo === "tarjeta") {
        return validarTarjeta();
    } else if (metodo === "transferencia") {
        return validarTransferencia();
    }
    return true;
}

function validarTarjeta() {
    const numero = document.getElementById("numeroTarjeta").value;
    const cvv = document.getElementById("cvv").value;
    if (numero.length !== 16 || isNaN(numero) || cvv.length !== 3 || isNaN(cvv)) {
        mostrarMensaje("Datos de tarjeta inválidos", "error");
        return false;
    }
    return true;
}

function validarTransferencia() {
    const comprobante = document.getElementById("comprobantePago").files.length;
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
