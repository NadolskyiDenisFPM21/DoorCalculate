$(document).ready(function () {
    $('#gen-pdf').click(function () {
        var preHtml = $('#form-pdf').html();
        preHtml = preHtml.replace('<input placeholder="0-100" type="number" id="discount-value" class="info-value" name="" min="0" max="100" value="0">', '<span>' + $('#discount-value').val() + '</span>');
        preHtml = preHtml.replace('<input placeholder="0-100" type="number" id="delivery-value" class="info-value" name="" min="0" value="0">', '<span>' + $('#delivery-value').val() + '</span>');
        preHtml = preHtml.replace('<input placeholder="0-100" type="number" id="instal-value" class="info-value" name="" min="0" value="0">', '<span>' + $('#instal-value').val() + '</span>');
        preHtml = preHtml.replace('<input placeholder="0-100" type="number" id="zamery-value" class="info-value" name="" min="0" value="0">', '<span>' + $('#zamery-value').val() + '</span>');
        preHtml = preHtml.replace('<input placeholder="0-100" type="number" id="prepayment-value" class="info-value" name="" min="0" value="0">', '<span>' + $('#prepayment-value').val() + '</span>');
        //
        preHtml = preHtml.replace(/<input.*?>/g, '')
        preHtml = preHtml.replace('<form method="post" action="/new_order/">', '')
        preHtml = preHtml.replace('<button type="submit" id="new">Новый заказ</button>', '')
        preHtml = preHtml.replace('</form>', '')
        preHtml = preHtml.replace('<th class="cell remove" rowspan="3">Удалить</th>', '')
        // Экранируем специальные символы в подстроке
        let substringToReplace = '<td rowspan="2"><button type="button" class="remove-button">Удалить дверь</button></td>';
        let escapedSubstring = substringToReplace.replace(/[-\/\\^$*+?.()|[\]{}]/g, '\\$&');

        // Используем регулярное выражение с экранированной подстрокой
        preHtml = preHtml.replace(new RegExp(escapedSubstring, 'g'), '');
        preHtml = preHtml.replace(/<\/br>/g, '');

        console.log(preHtml);
        var data = {
            'html': preHtml,
        }
        $.ajax({
            type: "GET",
            url: "/create_pdf_specification/",
            data: data,
            xhrFields: {
                responseType: 'blob'
            },
            success: function (xhr) {
                const blob = new Blob([xhr], { type: 'application/pdf' });
                const tempLink = document.createElement('a');
                tempLink.href = URL.createObjectURL(blob);
                tempLink.target = '_blank';
                tempLink.download = 'specification-' + (new Date()).toLocaleString() + '.pdf';

                document.body.appendChild(tempLink);
                tempLink.click();
                document.body.removeChild(tempLink);
            },
            error: function (error) {
                console.error('Ошибка при скачивании файла:', error);
            }
        });

    });
});