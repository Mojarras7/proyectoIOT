document.addEventListener('DOMContentLoaded', function () {

    // Elementos de las páginas
    const loginForm = document.getElementById('login-form');
    const loginError = document.getElementById('login-error');
    const sendNumberBtn = document.getElementById('send-number-btn');
    const activateModeBtn = document.getElementById('activate-mode-btn');
    const numberOutput = document.getElementById('number-output');
    const modeStatusOutput = document.getElementById('mode-status-output');
    const inventorySelectBtn = document.getElementById('inventory-select-btn');
    const loadInventoryBtn = document.getElementById('load-inventory-btn');
    const inventoryList = document.getElementById('inventory-table-body'); // Cambié aquí

    // APEX API Base URL
    const APEX_HOST = "apex.oracle.com";
    const BASE_PATH = "https://apex.oracle.com/pls/apex/iot_project/api/products/api/products";

    // Evento de inicio de sesión
    if (loginForm) {
        loginForm.addEventListener('submit', function (e) {
            e.preventDefault(); // Prevenir el envío del formulario

            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;

            // Validación de las credenciales
            if (username === "admin" && password === "1234") {
                // Si las credenciales son correctas, redirige a la página de selección de inventario
                window.location.href = "/inventory-select";
            } else {
                // Si las credenciales son incorrectas, muestra un mensaje de error
                loginError.textContent = "Usuario o contraseña incorrectos";
            }
        });
    }

    // Evento de enviar número a la Raspberry Pi (si existe el botón)
    if (sendNumberBtn) {
        sendNumberBtn.addEventListener('click', async function() {
            const numberToSend = "123"; // Número de ejemplo
            numberOutput.textContent = `Número enviado: ${numberToSend}`;

            try {
                const response = await fetch("http://10.43.117.121:5000/enviar_numero", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ numero: numberToSend })
                });

                const result = await response.json();

                if (response.ok) {
                    numberOutput.textContent += ` | Número recibido: ${result.numero}`;
                } else {
                    numberOutput.textContent = "Error al recibir el número";
                }
            } catch (error) {
                numberOutput.textContent = "Error de conexión";
            }
        });
    }

    // Activar modo lectura (si existe el botón)
    if (activateModeBtn) {
        activateModeBtn.addEventListener('click', async function() {
            try {
                const response = await fetch("http://10.43.117.121:5000/activar_lectura", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ activar: true })
                });

                const result = await response.json();

                if (response.ok) {
                    modeStatusOutput.textContent = `Modo Lectura: ${result.message}`;
                } else {
                    modeStatusOutput.textContent = `Error: ${result.message}`;
                }
            } catch (error) {
                modeStatusOutput.textContent = "Error de conexión";
            }
        });
    }

    // Evento para seleccionar inventario (si existe el botón)
    if (inventorySelectBtn) {
        inventorySelectBtn.addEventListener('click', function() {
            window.location.href = "/inventory"; // Redirigir a la página de inventario
        });
    }

    // Evento para cargar los datos del inventario desde la base de datos de APEX
    if (loadInventoryBtn) {
        loadInventoryBtn.addEventListener('click', async function() {
            try {
                // Construir la URL completa de la API de APEX
                const apiUrl = `https://apex.oracle.com/pls/apex/iot_project/api/products/getStatus`;

                const response = await fetch(apiUrl, {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                    }
                });

                const data = await response.json();
                console.log(data); // Para revisar la respuesta en consola

                if (response.ok) {
                    // Limpiar el contenedor antes de agregar nuevos elementos
                    inventoryList.innerHTML = "";

                    // Verificar si los productos fueron devueltos y agregarlos a la tabla
                    if (data.length > 0) {
                        data.forEach(product => {
                            const row = document.createElement("tr");

                            const productCell = document.createElement("td");
                            productCell.textContent = product.nombre; // Nombre del producto
                            row.appendChild(productCell);

                            const quantityCell = document.createElement("td");
                            quantityCell.textContent = product.cantidad; // Cantidad del producto
                            row.appendChild(quantityCell);

                            const categoryCell = document.createElement("td");
                            categoryCell.textContent = product.categoria; // Categoría del producto
                            row.appendChild(categoryCell);

                            // Agregar la fila a la tabla
                            inventoryList.appendChild(row);
                        });
                    } else {
                        inventoryList.innerHTML = "<tr><td colspan='3'>No hay productos disponibles</td></tr>";
                    }
                } else {
                    inventoryList.innerHTML = "<tr><td colspan='3'>Error al cargar el inventario</td></tr>";
                }
            } catch (error) {
                inventoryList.innerHTML = "<tr><td colspan='3'>Error de conexión</td></tr>";
            }
        });
    }
    
    const pesoOutput = document.getElementById('peso');

        async function getWeight() {
            try {
                const response = await fetch('http://10.43.117.121:5000/get_weight');
                const data = await response.json();

                if (response.ok) {
                    pesoOutput.textContent = `Peso: ${data.peso} gramos`;
                } else {
                    pesoOutput.textContent = "Error al obtener el peso";
                }
            } catch (error) {
                pesoOutput.textContent = "Error de conexión";
            }
        }

        // Llamar al obtener el peso
        getWeight();
        setInterval(getWeight, 2000);

});
