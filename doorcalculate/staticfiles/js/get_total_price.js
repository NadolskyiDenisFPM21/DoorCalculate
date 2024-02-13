$(document).change(function () {
    $('#count').change(function (e) {
        if ($('#count').val() && $('#price').text()) {
            var total_price = $('#count').val() * $('#price').text()
            $('#total-price').text(total_price);
        }
    });
});