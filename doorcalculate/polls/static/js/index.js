$(document).ready(function () {

    var door_list = [];
    const myCookieValue = getCookie('door_table');
    if (myCookieValue) {
        const replacedCommas = myCookieValue.replace(/\\054/g, ',');
        // Преобразуем строку в двумерный массив
        door_list = JSON.parse(decodeURIComponent(replacedCommas));
        create_table();
    }


    function create_table() {
        var table = $('#table tbody');
        table.empty();
        for (let i = 0; i < door_list.length; i++) {
            var tr = document.createElement('tr');
            for (let j = 0; j < door_list[i].length; j++) {
                var td = document.createElement('td');
                td.innerHTML = door_list[i][j];
                tr.appendChild(td);
            }
            table.append(tr);
        }
    }

    function getCookie(cookieName) {
        // Разделяем все cookie по точке с запятой в массив
        const cookies = document.cookie.split(';');

        // Ищем cookie с заданным именем
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();

            // Проверяем, начинается ли cookie с искомого имени
            if (cookie.startsWith(cookieName + '=')) {
                // Если да, возвращаем значение cookie
                return cookie.substring(cookieName.length + 1);
            }
        }

        // Если cookie с указанным именем не найдено, возвращаем null
        return null;
    }

    // Пример использования


    $('#select-model').change(function () {
        $('#price').text('');
        var selectedModel = $(this).val();
        $.ajax({
            url: '/get_filtered_data/',
            data: { 'selected_model': selectedModel },
            dataType: "json",
            success: function (data) {
                $('#select-width').empty();
                $('#select-width').append($('<option value="" disabled selected>Ширина</option>'));
                $('#select-height').empty();
                $('#select-height').append($('<option value="" disabled selected>Высота</option>'));
                var width = 0;
                var height = 0;
                $.each(data, function (index, item) {
                    if (width != item.width) {
                        width = item.width;
                        $('#select-width').append('<option value="' + item.width + '">' + item.width + '</option>');
                    }
                    if (height != item.height) {
                        height = item.height;
                        $('#select-height').append('<option value="' + item.height + '">' + item.height + '</option>');
                    }
                });
            }
        });
    });
    $('#add').click(function () {
        if ($('#select-model').val() && $('#select-opening').val() && $('#select-width').val() && $('#select-height').val()) {
            var data = [];
            data.push($('#select-model').val());
            data.push($('#select-opening').val());
            data.push($('#select-width').val());
            data.push($('#select-height').val());
            //
            // TODO: Заглушка, изменить!!!
            data.push($('#select-width').val());
            data.push($('#select-height').val());
            data.push($('#select-width').val());
            data.push($('#select-height').val());
            data.push($('#price').text());
            //
            //
            door_list.push(data);
            create_table()
            var js_table = JSON.stringify(door_list);
            $.ajax({
                url: "/set_table_cookies/",
                data: { 'door_table': js_table },
                dataType: "json",
                success: function (response) {
                }
            });
        }
    });

    $('.get-price').change(function () {
        if ($('#select-width').val() && $('#select-height').val()) {
            var json_req = {
                'model': $('#select-model').val(),
                'width': $('#select-width').val(),
                'height': $('#select-height').val(),
            };
            $.ajax({
                url: "/get_price/",
                data: json_req,
                dataType: "json",
                success: function (data) {
                    console.log(data[0].price);
                    var price = $('#price');
                    price.empty();
                    price.append(data[0].price);
                }
            });
        }

    });

});
