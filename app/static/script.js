// Tab Switching
document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.dashboard').forEach(d => d.classList.remove('active'));

        btn.classList.add('active');
        const target = btn.dataset.tab === 'manual' ? 'manual-dashboard' : 'bulk-dashboard';
        document.getElementById(target).classList.add('active');
    });
});

document.getElementById('prediction-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const btn = document.getElementById('predict-btn');
    const resultCard = document.getElementById('result-card');
    const initContent = resultCard.querySelector('.init-state');
    const predContent = resultCard.querySelector('.prediction-state');
    const priceEl = document.getElementById('predicted-price');

    // Loading state
    btn.disabled = true;
    btn.querySelector('.btn-text').textContent = 'Analyzing Market Data...';

    // Collect Data
    const formData = {
        Area_sqft: parseFloat(document.getElementById('Area_sqft').value),
        Neighborhood: document.getElementById('Neighborhood').value,
        Bedrooms: parseInt(document.getElementById('Bedrooms').value),
        Bathrooms: parseInt(document.getElementById('Bathrooms').value),
        Age_years: parseInt(document.getElementById('Age_years').value),
        Distance_to_Center: parseFloat(document.getElementById('Distance_to_Center').value),
        Condition: document.getElementById('Condition').value,
        Garage_size: parseInt(document.getElementById('Garage_size').value),
        Has_Garden: document.getElementById('Has_Garden').checked ? 1 : 0
    };

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });

        if (!response.ok) throw new Error('Prediction service error');

        const result = await response.json();

        // UI transitions
        initContent.style.display = 'none';
        predContent.style.display = 'block';

        // Counter animation for price
        animatePrice(0, result.prediction_usd, priceEl);

        // Scroll to result on mobile
        if (window.innerWidth < 850) {
            resultCard.scrollIntoView({ behavior: 'smooth' });
        }

    } catch (error) {
        alert('Error: ' + error.message);
    } finally {
        btn.disabled = false;
        btn.querySelector('.btn-text').textContent = 'Generate Prediction';
    }
});

// Bulk Upload Logic
const dropzone = document.getElementById('dropzone');
const fileInput = document.getElementById('file-input');

dropzone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropzone.classList.add('dragover');
});

dropzone.addEventListener('dragleave', () => dropzone.classList.remove('dragover'));

dropzone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropzone.classList.remove('dragover');
    if (e.dataTransfer.files.length) handleFileUpload(e.dataTransfer.files[0]);
});

fileInput.addEventListener('change', () => {
    if (fileInput.files.length) handleFileUpload(fileInput.files[0]);
});

async function handleFileUpload(file) {
    const status = document.getElementById('upload-status');
    const tableBody = document.querySelector('#results-table tbody');

    status.innerHTML = `<p style="color: var(--accent)">Processing ${file.name}...</p>`;

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('/predict-bulk', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const err = await response.json();
            throw new Error(err.detail || 'Upload failed');
        }

        const data = await response.json();
        renderTable(data.results);
        status.innerHTML = `<p style="color: #00ff88">✅ Successfully processed ${data.results.length} records</p>`;

    } catch (error) {
        status.innerHTML = `<p style="color: #ff5d5d">❌ Error: ${error.message}</p>`;
    }
}

function renderTable(results) {
    const tableBody = document.querySelector('#results-table tbody');
    tableBody.innerHTML = '';

    results.forEach(row => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${Math.round(row.Area_sqft)} sqft</td>
            <td>${row.Neighborhood}</td>
            <td>${row.Bedrooms}</td>
            <td>${row.Bathrooms}</td>
            <td class="res-price">$${row.Predicted_Price_USD.toLocaleString()}</td>
        `;
        tableBody.appendChild(tr);
    });
}

function animatePrice(start, end, element) {
    let current = start;
    const range = end - start;
    const increment = range / 50;
    const duration = 1000;
    const stepTime = Math.abs(Math.floor(duration / 50));

    const timer = setInterval(() => {
        current += increment;
        if ((increment > 0 && current >= end) || (increment < 0 && current <= end)) {
            clearInterval(timer);
            current = end;
        }
        element.textContent = '$' + Math.round(current).toLocaleString();
    }, stepTime);
}
