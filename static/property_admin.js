document.addEventListener('DOMContentLoaded', function () {
  const input = document.getElementById('id_images');
  const preview = document.getElementById('image-preview');
  const mainInput = document.getElementById('id_main_image_index');
  if (!input) return;
  const rentalType = document.getElementById('id_rental_type');
  const nightlyDiv = document.getElementById('div_id_price_nightly');
  const monthlyDiv = document.getElementById('div_id_price_monthly');

  function togglePrices() {
    if (!rentalType) return;
    const val = rentalType.value;
    if (val === 'short') {
      nightlyDiv.style.display = '';
      monthlyDiv.style.display = 'none';
    } else if (val === 'long') {
      nightlyDiv.style.display = 'none';
      monthlyDiv.style.display = '';
    } else {
      nightlyDiv.style.display = '';
      monthlyDiv.style.display = '';
    }
  }

  if (rentalType) {
    rentalType.addEventListener('change', togglePrices);
    togglePrices();
  }
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
