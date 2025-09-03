function volverArtistas() {
    if (window.history.length > 1) {
        history.back();
    } else {
        window.location.href = 'index.html';
    }
}