document.addEventListener('DOMContentLoaded', function () {
  const input = document.getElementById('id_images');
  const preview = document.getElementById('image-preview');
  const mainInput = document.getElementById('id_main_image_index');
  if (!input) return;
  input.addEventListener('change', function () {
    preview.innerHTML = '';
    Array.from(input.files).forEach((file, idx) => {
      const reader = new FileReader();
      const col = document.createElement('div');
      col.className = 'col-md-3 text-center mb-3';
      const img = document.createElement('img');
      img.className = 'img-fluid mb-1';
      const radio = document.createElement('input');
      radio.type = 'radio';
      radio.name = 'main_choice';
      radio.value = idx;
      radio.className = 'form-check-input';
      radio.addEventListener('change', () => {
        mainInput.value = radio.value;
      });
      if (idx === 0) {
        radio.checked = true;
        mainInput.value = 0;
      }
      reader.onload = e => {
        img.src = e.target.result;
      };
      reader.readAsDataURL(file);
      col.appendChild(img);
      col.appendChild(radio);
      preview.appendChild(col);
    });
  });
});
