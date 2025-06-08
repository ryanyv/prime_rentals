document.addEventListener('DOMContentLoaded', function () {
  const form = document.getElementById('filter-form');
  if (form) {
    form.addEventListener('submit', function () {
      const fields = form.querySelectorAll('input, select');
      fields.forEach(function (field) {
        if (!field.value) {
          field.removeAttribute('name');
        }
      });
    });
  }
  const params = new URLSearchParams(window.location.search);
  let changed = false;
  for (const [key, value] of params.entries()) {
    if (!value) {
      params.delete(key);
      changed = true;
    }
  }
  if (changed) {
    const newUrl = params.toString()
      ? `${window.location.pathname}?${params.toString()}`
      : window.location.pathname;
    history.replaceState(null, '', newUrl);
  }
});
