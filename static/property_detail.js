
document.addEventListener('DOMContentLoaded', function () {
    const scriptEl = document.getElementById('booked-dates');
    const calendar = document.getElementById('availability-calendar');
    if (typeof $ === 'undefined' || !scriptEl || !calendar) return;
    const booked = JSON.parse(scriptEl.textContent);
    $(calendar).datepicker({
        minDate: new Date(calendar.dataset.min),
        maxDate: new Date(calendar.dataset.max),
        beforeShowDay: function(date) {
            const d = $.datepicker.formatDate('yy-mm-dd', date);
            if (booked.indexOf(d) !== -1) {
                return [false, 'booked', 'Booked'];
            }
            return [true, '', 'Available'];
        }
    });
});

