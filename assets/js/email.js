const emailDecoded = atob("bWVAcmFmYWVsb3N0ZXJ0YWcucGhvdG8=");

window.addEventListener('load', (event) => {
    const emailAnchors = document.querySelectorAll("a.my-email");
    for (const emailAnchor of emailAnchors) {
        emailAnchor.href = "mailto:" + emailDecoded;
    }
});
