(() => {
  const debounce = (fn, wait) => {
    let t = null;
    return (...args) => {
      if (t) window.clearTimeout(t);
      t = window.setTimeout(() => fn(...args), wait);
    };
  };

  const init = () => {
    const inputs = document.querySelectorAll("[data-search-input]");
    if (!inputs.length) return;

    inputs.forEach((input) => {
      const datalistId = input.getAttribute("list");
      const datalist = datalistId ? document.getElementById(datalistId) : null;
      const url = input.getAttribute("data-suggest-url");
      if (!datalist || !url) return;

      const update = async () => {
        const q = (input.value || "").trim();
        if (q.length < 2) {
          datalist.innerHTML = "";
          return;
        }

        try {
          const res = await fetch(`${url}?q=${encodeURIComponent(q)}`, {
            headers: { "X-Requested-With": "XMLHttpRequest" },
          });
          if (!res.ok) return;
          const data = await res.json();
          const suggestions = Array.isArray(data.suggestions) ? data.suggestions : [];

          datalist.innerHTML = suggestions
            .slice(0, 12)
            .map((s) => `<option value="${String(s).replace(/"/g, "&quot;")}"></option>`)
            .join("");
        } catch {
          // Silent fail: suggestions should never block search.
        }
      };

      input.addEventListener("input", debounce(update, 120));
      input.addEventListener("focus", debounce(update, 0));
    });
  };

  document.addEventListener("DOMContentLoaded", init);
})();

