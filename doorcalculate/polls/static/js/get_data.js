$(document).change(function () {

    $('.get-data').change(function () {
        if ($('#select-width').val() && $('#select-height').val() && $('#select-frame').val()) {
            var json_req = {
                'model': $('#select-model').val(),
                'width': $('#select-width').val(),
                'height': $('#select-height').val(),
                'frame': $('#select-frame').val(),
            };
            $.ajax({
                url: "/get_door_info/",
                data: json_req,
                dataType: "json",
                success: function (data) {
                    var price = $('#price');
                    price.empty();
                    price.append(data[0].price);

                    var al_band_canv = $('#al-band-canvas');
                    al_band_canv.empty();
                    al_band_canv.append(data[0].al_banding_canvas ? '+' : '-');
                    var profile_frame_color = $('#profile-frame-color');
                    profile_frame_color.empty();
                    profile_frame_color.append(data[0].profile_frame_color);
                    var seal_color = $('#seal-color');
                    seal_color.empty();
                    seal_color.append(data[0].seal_color);
                    var is_primed = $('#is-primed');
                    is_primed.empty();
                    is_primed.append(data[0].is_primed);
                }
            });

            // get_dimensions_aperture
            var json_dimensions_aperture = {
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


            var ajax_data = {
                'width': $('#select-width').val(),
                'height': $('#select-height').val(),
                'frame': $('#select-frame').val(),
            }
            $.ajax({
                url: "/get_back_width/",
                data: ajax_data,
                dataType: "json",
                success: function (dimensions) {
                    $('#back-width').empty().text(dimensions.back_width);
                    $('#back-height').empty().text(dimensions.back_height);
                    // $.ajax({
                    //     url: "/set_table_cookies/",
                    //     data: { 'door_table': js_table },
                    //     dataType: "json",
                    //     success: function (response) {
                    //     }
                    // });
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

        if ($('#count').val() && $('#price').text()) {
            var total_price = $('#count').val() * $('#price').text()
            $('#total-price').text(total_price);
        }
    });

});