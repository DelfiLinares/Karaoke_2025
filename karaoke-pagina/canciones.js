fetch("./artistas.json")
  .then(response => response.json())
  .then(data => {
    const infoDeTay = data.find(artista => artista.nombre === "Taylor Swift");
    if (infoDeTay) {
        document.querySelector('.nombre-artista').textContent = infoDeTay.nombre;

        const fotoArtistaElem = document.querySelector('.fotoArtista');
        fotoArtistaElem.src = infoDeTay.imagen;

        const contenedor = document.querySelector('.contenedorCanciones');
        contenedor.innerHTML = ""; 
        infoDeTay.canciones.forEach(cancion => {
            const row = document.createElement('div');
            row.className = "row itemCancion";
            row.innerHTML = `
                <h3>${cancion.titulo}</h3>
                <h5>${cancion.duracion}</h5>
            `;
            contenedor.appendChild(row);
        });
    } 
  }).catch(error => {
    console.error('Error al cargar las canciones:', error);
  });