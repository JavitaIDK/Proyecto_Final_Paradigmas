
// Esta función se ejecuta cuando el botón "Filtrar" es presionado.
async function filtrar() {
    const origin = document.getElementById('origin').value;
    const type = document.getElementById('type').value;
    const friendlyRating = document.getElementById('friendly-rating').value;
    const size = document.getElementById('size').value;
    const groomingNeeds = document.getElementById('grooming-needs').value;
    const goodChildren = document.getElementById('good-children').value;
    const intelligence = document.getElementById('intelligence').value;
    const sheddingLevel = document.getElementById('shedding-level').value;
    const trainingDifficulty = document.getElementById('training-difficulty').value;

    // Construir la URL de filtros
    const url = new URL('http://127.0.0.1:5000/api/dogs');
    if (origin) url.searchParams.append('Origin', origin);
    if (type) url.searchParams.append('Type', type);
    if (friendlyRating) url.searchParams.append('Friendly Rating (1-10)', friendlyRating);
    if (size) url.searchParams.append('Size', size);
    if (groomingNeeds) url.searchParams.append('Grooming Needs', groomingNeeds);
    if (goodChildren) url.searchParams.append('Good with Children', goodChildren);
    if (intelligence) url.searchParams.append('Intelligence Rating (1-10)', intelligence);
    if (sheddingLevel) url.searchParams.append('Shedding Level', sheddingLevel);
    if (trainingDifficulty) url.searchParams.append('Training Difficulty (1-10)', trainingDifficulty);

    // Llamar al backend
    const response = await fetch(url);
    const data = await response.json();

    // Mostrar resultados
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = '';
    if (data.length === 0) {
        resultsDiv.innerHTML = '<p>No se encontraron resultados.</p>';
        return;
    }
    data.forEach(dog => {
        const dogCard = document.createElement('div');
        dogCard.classList.add('dog-card');
        dogCard.innerHTML = `
            <div style="display: flex; align-items: flex-start; gap: 20px;">
                <!-- Información del perro -->
                <div>
                    <h2>${dog.Name}</h2>
                    <p><strong>Origen:</strong> ${dog.Origin}</p>
                    <p><strong>Tipo:</strong> ${dog.Type}</p>
                    <p><strong>Amabilidad:</strong> ${dog["Friendly Rating (1-10)"]}</p>
                    <p><strong>Tamaño:</strong> ${dog["Size"]}</p>
                    <p><strong>Cuidado del pelaje:</strong> ${dog["Grooming Needs"]}</p>
                    <p><strong>Bueno con Niños:</strong> ${dog["Good with Children"]}</p>
                    <p><strong>Inteligencia (1-10):</strong> ${dog["Intelligence Rating (1-10)"]}</p>
                    <p><strong>Nivel de mudanza:</strong> ${dog["Shedding Level"]}</p>
                    <p><strong>Dificultad de entrenamiento (1-10):</strong> ${dog["Training Difficulty (1-10)"]}</p>
                </div>
                <!-- Imagen del perro -->
                <img src="${dog.Image}" alt="${dog.Name}" style="max-width: 200px; border-radius: 10px;">
            </div>
        `;
        resultsDiv.appendChild(dogCard);
    });
}

// Esto asegura que el evento de hacer clic en el botón "Filtrar" ejecute la función 'filtrar'.
document.querySelector("button").addEventListener("click", filtrar);
