import { setCookie } from './cookies.js';
import { getCookie } from './cookies.js';
import { attachChangeEvent } from './select_model.js'


function full_price() {
    var fullPrice = 0.0;
    var discountVal = parseFloat($('#discount-value').val());
    $("#table tbody tr .total-price").each(function (index, element) {
        var price = $(element).find('span');
        fullPrice += parseFloat(price.text());
    });
    $('#full-price-value').text(fullPrice.toFixed(2));
    fullPrice = parseFloat((fullPrice * (1 - discountVal / 100)).toFixed(2));
    $('#full-price-discount-value').text(fullPrice.toFixed(2));
    fullPrice += parseFloat($('#delivery-value').val()) + parseFloat($('#instal-value').val()) + parseFloat($('#zamery-value').val());
    $('#total-ex-vat-value').text(fullPrice.toFixed(2));
    fullPrice -= parseFloat($('#prepayment-value').val());
    $('#remainder-value').text(fullPrice.toFixed(2));
}


function removeDoor() {
    var tr = $(this).parent().parent();
    tr.next().remove();
    tr.remove();
    setCookie();
}



$(document).ready(function () {
    var remove_buttons = $('.remove-button');
    remove_buttons.each(function () {
        $(this).click(removeDoor);
    });
    full_price();

    $('.info-value').change(function () {
        full_price();
    });


    $('#add').click(function (e) {
        if ($('#select-model').val() && $('#select-opening').val() && $('#select-opening-2').val() && $('#select-width').val() && $('#select-height').val() && $('#select-frame').val() && $('#count').val()) {
            var html_data = $("#form-table tbody").children();
            var base = $("#form-table tbody").children().clone();
            html_data.children().each(function () {
                $(this).find('span').each(function () {
                    $(this).replaceWith('<span>' + $(this).text() + '</span>');
                });
                // Find select and input elements within the cell
                $(this).find('select, input').each(function () {
                    // Replace select or input with span
                    $(this).replaceWith('<span>' + $(this).val() + '</span>');
                });
            });
            $(html_data[0]).append('<td rowspan="2"><button type="button" class="remove-button">Удалить дверь</button></td>');
            var remove_buttons = $('.remove-button');
            console.log(remove_buttons.length);
            $(remove_buttons[remove_buttons.length - 1]).click(removeDoor);
            var rem = $($("#table thead").children()[0]).find('.remove');
            if (rem.length == 0) {
                $($("#table thead").children()[0]).append('<th class="cell remove" rowspan="3">Удалить</th>');
            }
            base.children().each(function () {
                $(this).find('input').each(function () {
                    $(this).val(0);
                });
            });
            $('#table tbody').append(html_data);

            $('#form-table tbody').append(base);

        }
        attachChangeEvent();
        setCookie();
        full_price();
    });

});
