(() => {
  function clamp(n, min, max) {
    return Math.max(min, Math.min(max, n));
  }

  function initCarousel(root) {
    const viewport = root.querySelector("[data-carousel-viewport]");
    const track = root.querySelector("[data-carousel-track]");
    const prevBtn = root.querySelector("[data-carousel-prev]");
    const nextBtn = root.querySelector("[data-carousel-next]");

    if (!viewport || !track) return;

    const getStep = () => {
      const card = track.querySelector(".book-card");
      if (!card) return viewport.clientWidth;

      // Use real layout width (includes CSS width and padding/border).
      const step = card.offsetWidth;
      const styles = window.getComputedStyle(track);
      const gap = parseFloat(styles.columnGap || styles.gap || "0") || 0;

      // Move about a "page" (visible cards), but never less than 1 card.
      const visible = clamp(Math.floor(viewport.clientWidth / (step + gap)), 1, 10);
      return visible * (step + gap);
    };

    const updateButtons = () => {
      if (!prevBtn && !nextBtn) return;
      const maxScrollLeft = viewport.scrollWidth - viewport.clientWidth;
      const atStart = viewport.scrollLeft <= 1;
      const atEnd = viewport.scrollLeft >= maxScrollLeft - 1;
      if (prevBtn) prevBtn.disabled = atStart;
      if (nextBtn) nextBtn.disabled = atEnd;
    };

    const scrollByStep = (dir) => {
      viewport.scrollBy({ left: dir * getStep(), behavior: "smooth" });
    };

    if (prevBtn) prevBtn.addEventListener("click", () => scrollByStep(-1));
    if (nextBtn) nextBtn.addEventListener("click", () => scrollByStep(1));

    viewport.addEventListener("scroll", updateButtons, { passive: true });
    window.addEventListener("resize", updateButtons);

    // Touch + mouse drag (doesn't block native touch scrolling)
    let isDown = false;
    let startX = 0;
    let startScrollLeft = 0;

    const onPointerDown = (e) => {
      // Only primary button for mouse.
      if (e.pointerType === "mouse" && e.button !== 0) return;
      // Don't hijack interactions on clickable/form elements inside cards.
      if (e.target && e.target.closest && e.target.closest("a,button,input,select,textarea,label,form")) {
        return;
      }
      isDown = true;
      startX = e.clientX;
      startScrollLeft = viewport.scrollLeft;
      viewport.setPointerCapture?.(e.pointerId);
      viewport.classList.add("is-dragging");
    };

    const onPointerMove = (e) => {
      if (!isDown) return;
      const dx = e.clientX - startX;
      viewport.scrollLeft = startScrollLeft - dx;
    };

    const endDrag = () => {
      if (!isDown) return;
      isDown = false;
      viewport.classList.remove("is-dragging");
    };

    viewport.addEventListener("pointerdown", onPointerDown);
    viewport.addEventListener("pointermove", onPointerMove);
    viewport.addEventListener("pointerup", endDrag);
    viewport.addEventListener("pointercancel", endDrag);
    viewport.addEventListener("pointerleave", endDrag);

    updateButtons();
  }

  document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll("[data-carousel]").forEach(initCarousel);
  });
})();

