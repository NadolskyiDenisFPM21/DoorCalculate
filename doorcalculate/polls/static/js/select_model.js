

function isStringInOptions(selectId, searchString) {
    var selectElement = $(selectId);
    var options = selectElement.children();

    for (var i = 0; i < options.length; i++) {
        if (options[i].text.includes(searchString)) {
            return true; // Найдено совпадение
        }
    }

    return false; // Совпадение не найдено
}


export function attachChangeEvent() {
    //change model
    $('#select-model').change(function () {
        $('#price').text('');
        var selectedModel = $(this).val();
        $.ajax({
            url: '/get_filtered_data/',
            data: { 'selected_model': selectedModel },
            dataType: "json",
            success: function (data) {
                $('#select-width').empty();
                $('#select-width').append($('<option value="" disabled selected>Ширина мм</option>'));
                $('#select-height').empty();
                $('#select-height').append($('<option value="" disabled selected>Высота мм</option>'));
                $('#select-frame').empty();
                $('#select-frame').append($('<option value="" disabled selected>Тип короба</option>'));
                $.each(data, function (index, item) {
                    if (!isStringInOptions('#select-width', item.width)) {
                        $('#select-width').append('<option value="' + item.width + '">' + item.width + '</option>');
                    }
                    if (!isStringInOptions('#select-height', item.height)) {
                        $('#select-height').append('<option value="' + item.height + '">' + item.height + '</option>');
                    }
                    if (!isStringInOptions('#select-frame', item.frame)) {
                        $('#select-frame').append('<option value="' + item.frame + '">' + item.frame + '</option>');
                    }
                });
            }
        });
    });


    //change width
    $('#select-width').change(function (e) {
        var selectedModel = $('#select-model').val();
        var selectedWidth = $(this).val();
        $.ajax({
            url: '/get_filtered_data/',
            data: {
                'selected_model': selectedModel,
                'selected_width': selectedWidth,
            },
            dataType: "json",
            success: function (data) {
                $('#select-height').empty();
                $('#select-height').append($('<option value="" disabled selected>Высота мм</option>'));
                $('#select-frame').empty();
                $('#select-frame').append($('<option value="" disabled selected>Тип короба</option>'));
                $.each(data, function (index, item) {
                    if (!isStringInOptions('#select-height', item.height)) {
                        $('#select-height').append('<option value="' + item.height + '">' + item.height + '</option>');
                    }
                    if (!isStringInOptions('#select-frame', item.frame)) {
                        $('#select-frame').append('<option value="' + item.frame + '">' + item.frame + '</option>');
                    }
                });
            }
        });
    });


    $('#loop').change(function (e) {
        var inputValue = $('#loop').val();
        var maxValue = 2;  // Задайте ваше максимальное значение

        if (inputValue > maxValue) {
            $('#loop').val(maxValue);
        }
    });
}



$(document).ready(function () {
    attachChangeEvent();
});