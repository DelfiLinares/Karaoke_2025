function mostrarDetallesArtista(artista) {
    document.querySelector('.nombre-artista').textContent = artista.nombre;
    document.querySelector('.fotoArtista').src = artista.imagen;

    const contenedor = document.querySelector('.contenedorCanciones');
    contenedor.innerHTML = "";
    artista.canciones.forEach(cancion => {
        const row = document.createElement('div');
        row.className = "row itemCancion";
        row.innerHTML = `
            <h3>${cancion.titulo}</h3>
            <h5>${cancion.duracion}</h5>
        `;
        contenedor.appendChild(row);
    });
}

async function cargarDatosArtista(artistaId) {
    try {
        const response = await fetch('artistas.json');
        const artistas = await response.json();
        const artistaEncontrado = artistas.find(artista => artista.id == artistaId);

        if (artistaEncontrado) { mostrarDetallesArtista(artistaEncontrado); } 
        else { console.error(`No se encontró el artista con ID: ${artistaId}`); }
    } 
    catch (error) { console.error("Error al cargar o parsear el JSON de artistas:", error);}
}

document.addEventListener('DOMContentLoaded', () => {
    const urlParams = new URLSearchParams(window.location.search);
    const artistaId = urlParams.get('id');

    if (artistaId) { cargarDatosArtista(artistaId); } 
    else { console.error("No se encontró el ID del artista en la URL."); }
});