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
                $('#select-frame').empty();
                $('#select-frame').append($('<option value="" disabled selected>Тип короба</option>'));
                var width = 0;
                var height = 0;
                var frame = "";
                $.each(data, function (index, item) {
                    if (width != item.width) {
                        width = item.width;
                        $('#select-width').append('<option value="' + item.width + '">' + item.width + '</option>');
                    }
                    if (height != item.height) {
                        height = item.height;
                        $('#select-height').append('<option value="' + item.height + '">' + item.height + '</option>');
                    }
                    if (frame != item.frame) {
                        frame = item.frame;
                        $('#select-frame').append('<option value="' + item.frame + '">' + item.frame + '</option>');
                    }
                });
            }
        });
    });
    $('#add').click(function () {
        if ($('#select-model').val() && $('#select-opening').val() && $('#select-width').val() && $('#select-height').val() && $('#select-frame').val()) {
            var data = [];
            data.push($('#select-model').val());
            data.push($('#select-opening').val());
            data.push('');
            data.push('');

            ajax_data = {
                'width': $('#select-width').val(),
                'height': $('#select-height').val(),
                'frame': $('#select-frame').val(),
            }
            $.ajax({
                url: "/get_back_width/",
                data: ajax_data,
                dataType: "json",
                success: function (dimensions) {
                    console.log(data);
                    door_list[door_list.length - 1][2] = $('#select-width').val() + '\\' + dimensions.back_width;
                    door_list[door_list.length - 1][3] = $('#select-height').val() + '\\' + dimensions.back_height;
                    create_table();
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

            data.push($('#aperture-width').text());
            data.push($('#aperture-height').text());
            data.push($('#select-frame').val());
            data.push($('#frame-width').text());
            data.push($('#frame-height').text());
            data.push($('#price').text());

            door_list.push(data);
            create_table();
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
        if ($('#select-width').val() && $('#select-height').val() && $('#select-frame').val()) {
            var json_req = {
                'model': $('#select-model').val(),
                'width': $('#select-width').val(),
                'height': $('#select-height').val(),
                'frame': $('#select-frame').val(),
            };
            $.ajax({
                url: "/get_price/",
                data: json_req,
                dataType: "json",
                success: function (data) {
                    var price = $('#price');
                    price.empty();
                    price.append(data[0].price);
                }
            });

            // get_dimensions_aperture
            json_dimensions_aperture = {
                'width_door': $('#select-width').val(),
                'height_door': $('#select-height').val(),
                'frame': $('#select-frame').val(),
            }
            $.ajax({
                url: "/get_dimensions_aperture/",
                data: json_dimensions_aperture,
                dataType: "json",
                success: function (data) {
                    $('#aperture-width').empty().append(data.aperture_width);
                    $('#aperture-height').empty().append(data.aperture_height);
                }
            });

            // get_dimensions_frame

            $.ajax({
                url: "/get_dimensions_frame/",
                data: json_dimensions_aperture,
                dataType: "json",
                success: function (data) {
                    $('#frame-width').empty().append(data.frame_width);
                    $('#frame-height').empty().append(data.frame_height);
                }
            });
        }

    });





});
