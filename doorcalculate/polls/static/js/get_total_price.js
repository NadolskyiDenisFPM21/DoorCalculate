$(document).change(function () {
    var total_price = $('#count').val() * $('#price').text()
    $('#total-price').text(total_price);
});