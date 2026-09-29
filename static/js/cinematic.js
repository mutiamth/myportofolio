(function () {
    "use strict";

    var prefersReduced = window.matchMedia(
        "(prefers-reduced-motion: reduce)"
    ).matches;

    var header = document.querySelector(".site-header");

    // Navbar scroll state
    function updateHeader() {
        if (!header) return;

        if (window.scrollY > 24) {
            header.classList.add("is-scrolled");
        } else {
            header.classList.remove("is-scrolled");
        }
    }

    window.addEventListener("scroll", updateHeader, { passive: true });
    updateHeader();

    // Jangan jalankan cursor effect kalau user minta reduced motion
    // atau perangkatnya touch/mobile.
    if (
        prefersReduced ||
        !window.matchMedia("(pointer: fine)").matches
    ) {
        return;
    }

    var glow = document.querySelector(".cursor-glow");

    if (!glow) return;

    var mouseX = window.innerWidth / 2;
    var mouseY = window.innerHeight / 2;
    var glowX = mouseX;
    var glowY = mouseY;

    document.addEventListener("mousemove", function (event) {
        mouseX = event.clientX;
        mouseY = event.clientY;
        document.body.classList.add("has-pointer");
    });

    function animate() {
        glowX += (mouseX - glowX) * 0.08;
        glowY += (mouseY - glowY) * 0.08;

        glow.style.transform =
            "translate3d(" +
            glowX +
            "px, " +
            glowY +
            "px, 0) translate(-50%, -50%)";

        requestAnimationFrame(animate);
    }

    animate();
})();