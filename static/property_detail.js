$(function() {
    const booked = JSON.parse(document.getElementById('booked-dates').textContent);
    $('#availability-calendar').datepicker({
        minDate: new Date($('#availability-calendar').data('min')),
        maxDate: new Date($('#availability-calendar').data('max')),
        beforeShowDay: function(date) {
            const d = $.datepicker.formatDate('yy-mm-dd', date);
            if (booked.indexOf(d) !== -1) {
                return [false, 'booked', 'Booked'];
            }
            return [true, '', 'Available'];
        }
    });
});

