const CLIENT_ID = "264328433017-eeodnelnjtm51t1hj6gg9j6d43qngipq.apps.googleusercontent.com"; 
const SCOPES = "https://www.googleapis.com/auth/drive.file";

// Esta función carga el cliente de gapi y maneja la autenticación.
// Retorna una Promesa que resuelve cuando gapi está listo y autenticado (o rechazado).
function loadGoogleAPIandAuth() {
    return new Promise((resolve, reject) => {
        gapi.load('client:auth2', () => { // Asegura que gapi.client y gapi.auth2 estén disponibles
            gapi.client.init({
                clientId: CLIENT_ID,
                discoveryDocs: ["https://www.googleapis.com/discovery/v1/apis/drive/v3/rest"],
                scope: SCOPES
            }).then(() => {
                const authInstance = gapi.auth2.getAuthInstance();
                if (!authInstance.isSignedIn.get()) {
                    // Si no está firmado, pide al usuario que inicie sesión
                    authInstance.signIn().then(() => {
                        console.log("Usuario autenticado en Google Drive.");
                        resolve();
                    }).catch(err => {
                        console.error("Error al autenticar en Google Drive (signIn):", err);
                        // No usar alert aquí para no interrumpir el flujo si falla
                        reject(err);
                    });
                } else {
                    console.log("Usuario ya autenticado en Google Drive.");
                    resolve();
                }
            }).catch(err => {
                console.error("Error al inicializar el cliente de Google Drive (gapi.client.init):", err);
                // No usar alert aquí
                reject(err);
            });
        });
    });
}
// Esta función es global y será llamada desde video.html