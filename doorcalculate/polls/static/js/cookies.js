
export function getCookie(cookieName) {
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

function getKilobyteSize(str) {
    // Переводим строку в байты, учитывая кодировку UTF-8
    var byteSize = new TextEncoder().encode(str).length;

    // Конвертируем байты в килобайты
    var kilobyteSize = byteSize / 1024;

    return kilobyteSize.toFixed(2); // Округляем до двух знаков после запятой
}


export function setCookie() {
    var tableHtml = document.getElementById('table').outerHTML;


    var formData = {
        'html': tableHtml,
        'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
        'csrftoken': getCookie('csrftoken')
    };

    $.ajax({
        type: 'POST',
        url: '/set_table/',
        data: formData,
    });
}

