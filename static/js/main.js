document.addEventListener("DOMContentLoaded", () => {
    const body = document.body;
    const navToggle = document.querySelector(".nav-toggle");
    const navMenu = document.querySelector(".nav-menu");
    const themeToggle = document.querySelector("[data-theme-toggle]");

    const savedTheme = localStorage.getItem("cv-theme");
    if (savedTheme === "dark") {
        body.setAttribute("data-theme", "dark");
        if (themeToggle) {
            themeToggle.textContent = "🌙";
        }
    }

    if (navToggle && navMenu) {
        navToggle.addEventListener("click", () => {
            const isOpen = navMenu.classList.toggle("is-open");
            navToggle.setAttribute("aria-expanded", String(isOpen));
        });

        navMenu.querySelectorAll("a").forEach((link) => {
            link.addEventListener("click", () => {
                navMenu.classList.remove("is-open");
                navToggle.setAttribute("aria-expanded", "false");
            });
        });
    }

    if (themeToggle) {
        themeToggle.addEventListener("click", () => {
            const isDark = body.getAttribute("data-theme") === "dark";
            body.setAttribute("data-theme", isDark ? "light" : "dark");
            localStorage.setItem("cv-theme", isDark ? "light" : "dark");
            themeToggle.textContent = isDark ? "☀️" : "🌙";
        });
    }

    const revealItems = document.querySelectorAll(
        ".timeline-item, .feature-card, .tool-card, .project-card, .contact-card, .about-grid > *"
    );

    const revealObserver = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add("is-visible");
                    revealObserver.unobserve(entry.target);
                }
            });
        },
        { threshold: 0.15 }
    );

    revealItems.forEach((item) => {
        item.classList.add("reveal");
        revealObserver.observe(item);
    });
});
