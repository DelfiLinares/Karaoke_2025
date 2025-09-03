const divisor = document.querySelector('div#image-track');
let artistasGlobal = [];

function mostrarArtistas(artistas) {
    divisor.innerHTML = ""; 
    if (artistas.length > 0) {
        artistas.forEach(artista => {
            divisor.insertAdjacentHTML('beforeend', 
                `<a href="artista.html?id=${artista.id}">
                    <img class="image" src="${artista.imagen}" draggable="false" />
                </a>`
            );
        });
    }}

fetch('artistas.json')
    .then(res => res.json())
    .then(data => {
        artistas = data;
        const popArtistas = artistas.filter(a => a.genero.toLowerCase() === "pop");
        mostrarArtistas(popArtistas);
        
        document.querySelectorAll('.generosLista a[data-genero]').forEach(enlace => {
            enlace.addEventListener('click', e => {
                e.preventDefault();
                const genero = enlace.getAttribute('data-genero');
                const filtrados = artistas.filter(a => a.genero.toLowerCase() === genero.toLowerCase());
                mostrarArtistas(filtrados);
            });
        });
    });


