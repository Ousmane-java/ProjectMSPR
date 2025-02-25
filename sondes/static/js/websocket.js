const socket = new WebSocket("ws://127.0.0.1:8080/ws/sondes/");

socket.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log("Mise à jour reçue:", data);

    const row = document.getElementById(`franchise-${data.franchise_id}`);
    if (row) {
        const statusCell = row.cells[3];  // 4ème colonne (Statut)
        if (data.status === "connected") {
            statusCell.className = "online";
            statusCell.innerHTML = "🟢 En ligne";
        } else {
            statusCell.className = "offline";
            statusCell.innerHTML = "🔴 Hors ligne";
        }
    }
};

socket.onopen = function() {
    console.log("WebSocket connecté !");
};

socket.onerror = function(error) {
    console.error("Erreur WebSocket:", error);
};
