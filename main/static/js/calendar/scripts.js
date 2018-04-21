var now_year = 0;
var now_month = 0;
var today_month = 0;
var today_year = 0;

function setup_date(month, year)
{
    now_year = year;
    now_month = month;
    today_month = month;
    today_year = year;
};

function next_month()
{
    now_month += 1;
    if (now_month == 13)
    {
        now_month = 1;
        now_year += 1;
    }
    $.ajax({
        type: "POST",
        url: '/calendar/',
        data: {'now_date': String(now_year) + '_' + String(now_month)},
        success: function(response)
        {
            if (response['result'] == "100")
            {
                $("#month_holder").text(response['month_name']);
                $("#year_holder").text(response['now_year']);
                $("#month_calendar").find('tbody').each(
                    function()
                    {
                        var weeks = response['weeks'];
                        result_html = '';
                        weeks.forEach(function(week, i, weeks)
                        {
                            result_html += '<tr>\n<th>' + String(week['week_num']) + '</th>\n';
                            var week_days = week['week_days'];
                            week_days.forEach(function(day, i, week_days)
                            {
                                if (day['class'])
                                {
                                    result_html += '<td class="' + day['class'] + '">\n';
                                    if (day['event'])
                                    {
                                        result_html += '<div class="alert alert-primary event" data-toggle="modal"' +
                                            'data-target="#Event-Card" onclick="get_event_data_ajax(' + day['event']['id'] + ')">\n';
                                        result_html += day['event']['caption'];
                                        result_html += '\n</div>\n';
                                    }
                                    result_html += '<small class="date">' + String(day['day']) + '</small>\n';
                                    result_html += '</td>\n';
                                }
                                else
                                {
                                    result_html += '<td>\n';
                                    if (day['event'])
                                    {
                                        result_html += '<div class="alert alert-primary event" data-toggle="modal"' +
                                            'data-target="#Event-Card" onclick="get_event_data_ajax(' + day['event']['id'] + ')">\n';
                                        result_html += day['event']['caption'];
                                        result_html += '\n</div>\n';
                                    }
                                    result_html += '<small class="date">' + String(day['day']) + '</small>\n';
                                    result_html += '</td>\n';
                                }
                            });
                            result_html += '</tr>\n';
                        });
                        $(this).html(result_html);
                    }
                );
            }
            else
            {
                voice_ajax_result(response['result']);
            }
        }
    });
};

function go_to_now_month()
{
    now_month = today_month;
    now_year = today_year;
    $.ajax({
        type: "POST",
        url: '/calendar/',
        data: {'now_date': String(now_year) + '_' + String(now_month)},
        success: function(response)
        {
            if (response['result'] == "100")
            {
                $("#month_holder").text(response['month_name']);
                $("#year_holder").text(response['now_year']);
                $("#month_calendar").find('tbody').each(
                    function()
                    {
                        var weeks = response['weeks'];
                        result_html = '';
                        weeks.forEach(function(week, i, weeks)
                        {
                            result_html += '<tr>\n<th>' + String(week['week_num']) + '</th>\n';
                            var week_days = week['week_days'];
                            week_days.forEach(function(day, i, week_days)
                            {
                                if (day['class'])
                                {
                                    result_html += '<td class="' + day['class'] + '">\n';
                                    if (day['event'])
                                    {
                                        result_html += '<div class="alert alert-primary event" data-toggle="modal"' +
                                            'data-target="#Event-Card" onclick="get_event_data_ajax(' + day['event']['id'] + ')">\n';
                                        result_html += day['event']['caption'];
                                        result_html += '\n</div>\n';
                                    }
                                    result_html += '<small class="date">' + String(day['day']) + '</small>\n';
                                    result_html += '</td>\n';
                                }
                                else
                                {
                                    result_html += '<td>\n';
                                    if (day['event'])
                                    {
                                        result_html += '<div class="alert alert-primary event" data-toggle="modal"' +
                                            'data-target="#Event-Card" onclick="get_event_data_ajax(' + day['event']['id'] + ')">\n';
                                        result_html += day['event']['caption'];
                                        result_html += '\n</div>\n';
                                    }
                                    result_html += '<small class="date">' + String(day['day']) + '</small>\n';
                                    result_html += '</td>\n';
                                }
                            });
                            result_html += '</tr>\n';
                        });
                        $(this).html(result_html);
                    }
                );
            }
            else
            {
                voice_ajax_result(response['result']);
            }
        }
    });
};

function back_month()
{
    now_month -= 1;
    if (now_month == 0)
    {
        now_month = 12;
        now_year -= 1;
    }
    $.ajax({
        type: "POST",
        url: '/calendar/',
        data: {'now_date': String(now_year) + '_' + String(now_month)},
        success: function(response)
        {
            if (response['result'] == "100")
            {
                $("#month_holder").text(response['month_name']);
                $("#year_holder").text(response['now_year']);
                $("#month_calendar").find('tbody').each(
                    function()
                    {
                        var weeks = response['weeks'];
                        result_html = '';
                        weeks.forEach(function(week, i, weeks)
                        {
                            result_html += '<tr>\n<th>' + String(week['week_num']) + '</th>\n';
                            var week_days = week['week_days'];
                            week_days.forEach(function(day, i, week_days)
                            {
                                if (day['class'])
                                {
                                    result_html += '<td class="' + day['class'] + '">\n';
                                    if (day['event'])
                                    {
                                        result_html += '<div class="alert alert-primary event" data-toggle="modal"' +
                                            'data-target="#Event-Card" onclick="get_event_data_ajax(' + day['event']['id'] + ')">\n';
                                        result_html += day['event']['caption'];
                                        result_html += '\n</div>\n';
                                    }
                                    result_html += '<small class="date">' + String(day['day']) + '</small>\n';
                                    result_html += '</td>\n';
                                }
                                else
                                {
                                    result_html += '<td>\n';
                                    if (day['event'])
                                    {
                                        result_html += '<div class="alert alert-primary event" data-toggle="modal"' +
                                            'data-target="#Event-Card" onclick="get_event_data_ajax(' + day['event']['id'] + ')">\n';
                                        result_html += day['event']['caption'];
                                        result_html += '\n</div>\n';
                                    }
                                    result_html += '<small class="date">' + String(day['day']) + '</small>\n';
                                    result_html += '</td>\n';
                                }
                            });
                            result_html += '</tr>\n';
                        });
                        $(this).html(result_html);
                    }
                );
            }
            else
            {
                voice_ajax_result(response['result']);
            }
        }
    });
};

function add_event_ajax()
{
    for (instance in CKEDITOR.instances) {
        CKEDITOR.instances[instance].updateElement();
    }
    var data = CKEDITOR.instances.id_description.getData();
    form_data = $('#add_event_form').serialize();
    form_data['data'] = data;
    $.ajax({
        type: "POST",
        url: '/calendar/events/add',
        data: form_data,
        success: function(response)
        {
            if (response['result'] == "100")
            {
                $("#close_calendar_btn").trigger("click");
                voice_text('Событие добавлено.');
                go_to_now_month();
            }
            else
            {
                voice_ajax_result(response['result']);
            }
        }
    });
};

function get_event_data_ajax(id){
    $('#event_num').html(id);
    $('#event_title_show').html('loading');
    $('#event_date_show').html('loading');
    $('#event_description_show').html('loading');
    $.ajax({
        type: "POST",
        url: '/calendar/events/get_event_data',
        data: {"id": id},
        success: function(response)
        {
            if (response['result'] == "100")
            {
                $('#event_title_show').html(response['title']);
                $('#event_date_show').html(response['date']);
                $('#event_description_show').html(response['description']);
                if(response['map_coordinates'] != 'none'){
                    coords = response['map_coordinates'].split('|')
                    show_placemark = createPlacemark(coords);
                    myMap.geoObjects.add(show_placemark);
                    show_placemark.events.add('dragend', function () {
                        getAddress(show_placemark.geometry.getCoordinates());
                    });
                    getAddress(coords);
                }
            }
            else
            {
                voice_ajax_result(response['result']);
            }

        }
    });
};

function delete_event_ajax()
{
    var id = $('#event_num').html();
    var should_delete = confirm('Вы уверены?');
    if (should_delete)
    {
        $.ajax({
            type: "POST",
            url: '/calendar/events/delete',
            data: {"id": id},
            success: function(response)
            {
                if (response['result'] == "100")
                {
                    voice_text('Событие удалено.');
                    go_to_now_month();
                }
                else
                {
                    voice_ajax_result(response['result']);
                }
            }
        });
    }
};
