document.addEventListener('DOMContentLoaded', () => {
    let map = L.map('map').setView([51.5074, -0.1278], 13);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '© OpenStreetMap'
    }).addTo(map);

    const prefButtons = document.querySelectorAll('.pref-btn');
    const prefInput = document.querySelector('input[name="preferences"]');

    prefButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const pref = btn.getAttribute('data-pref');
            let currentPrefs = prefInput.value.trim() || '';
            let prefsArray = currentPrefs.split(',').map(p => p.trim()).filter(p => p);
            if (!prefsArray.includes(pref)) {
                prefsArray.push(pref);
                prefInput.value = prefsArray.join(', ');
                console.log(`Updated preferences: ${prefInput.value}`); // Debug
            }
        });
    });

    document.getElementById('recommendForm').addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(this);
        console.log("Form data being sent:", Object.fromEntries(formData)); // Debug
        fetch('/recommend', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            const resultDiv = document.getElementById('result');
            resultDiv.innerHTML = `
                <p><strong>Weather:</strong> ${data.weather || 'clear'}</p>
                <p><strong>Points:</strong> ${data.points} (Great Explorer!)</p>
                <p><strong>Total Time:</strong> ${data.total_time || 0} hrs</p>
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
            if (data.points >= 30) alert('Level Up! Elite Explorer!');
        })
        .catch(error => console.error('Error:', error));
    });

    document.getElementById('signupForm').addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(this);
        const email = formData.get('email');
        const password = formData.get('password');
        alert(`Signed up with Email: ${email} and Password: ${password}`);
        document.querySelector('.signup-form').style.display = 'none';
        document.querySelector('.recommend-form').style.display = 'block';
        document.querySelector('.preferences-section').style.display = 'block';
    });
});