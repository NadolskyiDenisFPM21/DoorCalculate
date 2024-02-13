$(document).ready(function () {
    $('#gen-pdf').click(function () {
        var preHtml = $('#form-pdf').html();
        preHtml = preHtml.replace('<input placeholder="0-100" type="number" id="discount-value" class="info-value" name="" min="0" max="100" value="0">', '<span>' + $('#discount-value').val() + '</span>');
        preHtml = preHtml.replace('<input placeholder="0-100" type="number" id="delivery-value" class="info-value" name="" min="0" value="0">', '<span>' + $('#delivery-value').val() + '</span>');
        preHtml = preHtml.replace('<input placeholder="0-100" type="number" id="instal-value" class="info-value" name="" min="0" value="0">', '<span>' + $('#instal-value').val() + '</span>');
        preHtml = preHtml.replace('<input placeholder="0-100" type="number" id="zamery-value" class="info-value" name="" min="0" value="0">', '<span>' + $('#zamery-value').val() + '</span>');
        preHtml = preHtml.replace('<input placeholder="0-100" type="number" id="prepayment-value" class="info-value" name="" min="0" value="0">', '<span>' + $('#prepayment-value').val() + '</span>');
        console.log(preHtml);
        var data = {
            'html': preHtml,
        }
        $.ajax({
            type: "GET",
            url: "/create_pdf_specification/",
            data: data,
            dataType: "json",

        });
    });
});