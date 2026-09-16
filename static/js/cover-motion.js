(function () {
    "use strict";

    var prefersReduced = window.matchMedia(
        "(prefers-reduced-motion: reduce)"
    ).matches;

    var coverLight = document.getElementById("cover-light");
    var coverDark = document.getElementById("cover-dark");
    var coverDarkBg = document.getElementById("cover-dark-bg");
    var coverDarkText = document.getElementById("cover-dark-text");

    // Kalau halaman ini nggak punya elemen cover (Experience/Education/
    // Projects yang extend base.html tapi nggak punya cover), atau user
    // minta reduced motion, hentikan tanpa error.
    if (!coverLight || !coverDark || !coverDarkBg || !coverDarkText) {
        return;
    }
    if (prefersReduced) {
        coverDarkText.style.opacity = "1";
        return;
    }

    var ticking = false;

    function clamp(value, min, max) {
        return Math.min(Math.max(value, min), max);
    }

    function update() {
        var vh = window.innerHeight;

        // --- Cover terang: memudar & sedikit membesar begitu mulai discroll ---
        var rLight = coverLight.getBoundingClientRect();
        var pLight = clamp((vh - rLight.top) / (vh + rLight.height), 0, 1);
        var lightFade = clamp((pLight - 0.5) * 2.4, 0, 1);
        coverLight.style.opacity = String(1 - lightFade);
        coverLight.style.transform =
            "scale(" + (1 + clamp(pLight - 0.5, 0, 1) * 0.08) + ")";

        // --- Cover gelap: teks nama & background bergerak kontinu
        // mengikuti persis posisi section di layar (kurva sinus biar
        // halus di ujung-ujungnya, bukan linear kaku) ---
        var rDark = coverDark.getBoundingClientRect();
        var pDark = clamp((vh - rDark.top) / (vh + rDark.height), 0, 1);
        var visibility = Math.sin(pDark * Math.PI);

        coverDarkText.style.opacity = String(visibility);
        coverDarkText.style.transform =
            "translateY(calc(-50% + " +
            (0.5 - pDark) * 60 +
            "px)) scale(" +
            (0.75 + visibility * 0.3) +
            ")";
        coverDarkBg.style.transform =
            "translateY(" + (0.5 - pDark) * 80 + "px)";

        ticking = false;
    }

    function onScroll() {
        if (!ticking) {
            window.requestAnimationFrame(update);
            ticking = true;
        }
    }

    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", onScroll);
    update();
})();