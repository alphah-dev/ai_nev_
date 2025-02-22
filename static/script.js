let map = L.map('map').setView([51.5074, -0.1278], 13);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '© OpenStreetMap'
}).addTo(map);

document.getElementById('recommendForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const formData = new FormData(this);
    fetch('/recommend', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        const resultDiv = document.getElementById('result');
        resultDiv.innerHTML = `
            <p><strong>Weather:</strong> ${data.weather}</p>
            <p><strong>Points:</strong> ${data.points}</p>
            <p><strong>Total Time:</strong> ${data.total_time} hrs</p>
            <h3>Itinerary:</h3>
        `;
        map.eachLayer(layer => layer instanceof L.Marker ? map.removeLayer(layer) : null);
        data.itinerary.forEach(poi => {
            resultDiv.innerHTML += `<p>${poi.name} (${poi.type}, ${poi.time} hrs) - ${poi.desc}</p>`;
            L.marker([poi.lat, poi.lon]).addTo(map).bindPopup(`<b>${poi.name}</b><br>${poi.desc}`);
        });
        if (data.itinerary.length) {
            map.fitBounds(data.itinerary.map(poi => [poi.lat, poi.lon]));
        }
        if (data.points >= 30) alert('Level Up! Great Explorer!');
    });
});