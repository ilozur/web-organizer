var cur_coordinates;

ymaps.ready(function () {
    var placemark,
    myMap = new ymaps.Map('map', {
        center: [55.753994, 37.622093],
        zoom: 10
    }, {
        searchControlProvider: 'yandex#search'
    });

    // Слушаем клик на карте.
    myMap.events.add('click', function (e) {
        var coords = e.get('coords');

        // Если метка уже создана – просто передвигаем ее.
        if (placemark) {
            placemark.geometry.setCoordinates(coords);
        }
        // Если нет – создаем.
        else {
            placemark = createPlacemark(coords);
            myMap.geoObjects.add(placemark);
            // Слушаем событие окончания перетаскивания на метке.
            placemark.events.add('dragend', function () {
                getAddress(placemark.geometry.getCoordinates());
            });
        }
        getAddress(coords);
        console.log(placemark.geometry.getCoordinates()[0]);
        $('#id_place').val(placemark.geometry.getCoordinates()[0] + "|" + placemark.geometry.getCoordinates()[1]);
    });

    // Создание метки.
    function createPlacemark(coords) {
        return new ymaps.Placemark(coords, {
            iconCaption: 'поиск...'
        }, {
            preset: 'islands#violetDotIconWithCaption',
            draggable: true
        });
    }

    // Определяем адрес по координатам (обратное геокодирование).
    function getAddress(coords) {
        placemark.properties.set('iconCaption', 'поиск...');
        ymaps.geocode(coords).then(function (res) {
            var firstGeoObject = res.geoObjects.get(0);

            placemark.properties
                .set({
                    // Формируем строку с данными об объекте.
                    iconCaption: [
                        // Название населенного пункта или вышестоящее административно-территориальное образование.
                        firstGeoObject.getLocalities().length ? firstGeoObject.getLocalities() : firstGeoObject.getAdministrativeAreas(),
                        // Получаем путь до топонима, если метод вернул null, запрашиваем наименование здания.
                        firstGeoObject.getThoroughfare() || firstGeoObject.getPremise()
                    ].filter(Boolean).join(', '),
                    // В качестве контента балуна задаем строку с адресом объекта.
                    balloonContent: firstGeoObject.getAddressLine()
                });
            $('#placemark').html(firstGeoObject.getAddressLine());
        });
    }
    
    showMap = new ymaps.Map('show_map', {
        center: [55.753994, 37.622093],
        zoom: 10
    }, {
        searchControlProvider: 'yandex#search'
    });


});
