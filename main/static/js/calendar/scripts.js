var now_year = 0;
var now_month = 0;
var today_month = 0;
var today_year = 0;

function make_list_item(item){
    var list_item = '<a href="#" class="list-group-item list-group-item-light" data-toggle="modal" data-target="#Event-Card" onclick="get_event_data_ajax(' +
    item[2] + ')"><h7>' +
    item[0] + '</h7><div class="date-and-place"><small>' +
    item[1] + '</small>|<small><b>' +
    item[4] + '</b></small></div></a>';
    return list_item
};

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
        url: '/calendar/change_month',
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
        url: '/calendar/change_month',
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
        url: '/calendar/change_month',
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
                    savePlacemark(coords);
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


function ShowTable()
{
    $("#ViewList").hide("slow");
    $("#ViewTable").show("slow");
};

function ShowList()
{
    $("#ViewList").show("slow");
    $("#ViewTable").hide("slow");
};


function save_event_ajax()
{
    var id = $('#event_num').html();
    $("#id_todo_id").val(id);
    var form_data = $('#edit_event_form').serialize();
    $("#edit_event_form").find(':input').each(function(){
        $(this).attr('disabled', 'disabled');
    });
    $('#save_event_btn').attr('disabled', 'disabled');
    $.ajax({
        type: "POST",
        url: '/events/edit',
        data: form_data,
        success: function(response)
        {
            if (response['result'] == "Success")
            {
                alert('OK, Changes were saved');
                $('#event_title_' + id).html($('#id_event_edit_title').val());
                $('#event_date_' + id).html(response['deadline_date']);
                $('#event_title_show').html($('#id_event_edit_title').val());
            }
            else{
                alert(response['result']);
            }
            $("#edit_event_form").find(':input').each(function(){
                $(this).removeAttr('disabled');
            });
            $('#save_event_btn').removeAttr('disabled');
        }
    });
};

function sorting(sort_type, type){
    if (type == 'all'){
        for (var i = 1; i < $("#all_page_holder").length - 2; i++){
            $("#all_page_holder button:eq(" + i + ")").attr("onclick", "paginate(" + i + "," + type + "," + sort_type + ")");
        }
        paginate(1, type, sort_type);
    };
    if (type == 'my'){
        for (var i = 1; i < $("#user_page_holder").length - 2; i++){
            $("#user_page_holder button:eq(" + i + ")").attr("onclick", "paginate(" + i + "," + type + "," + sort_type + ")");
        }
        paginate(1, type, sort_type);
    };
    if (type == 'weekly'){
        for (var i = 1; i < $("#week_page_holder").length - 2; i++){
            $("#week_page_holder button:eq(" + i + ")").attr("onclick", "paginate(" + i + "," + type + "," + sort_type + ")");
        }
        paginate(1, type, sort_type)
    };
};

function paginate(page, type, sort_type){
    $.ajax({
        type: "POST",
        url: '/calendar',
        data: {"page": page, "type": type, "sort_type": sort_type},
        success: function(response){
            if (response['result'] == '100'){
                if (type == 'all'){
                    $("#ViewAll").html("");
                    for (var i = 0; i < response['events_list'].length; i++){
                        $("#ViewAll").append(make_list_item(response['events_list'][i]));
                    }
                };
                if (type == 'my'){
                    $("#ViewMy").html("");
                    for (var i = 0; i < response['events_list'].length; i++){
                        $("#ViewMy").append(make_list_item(response['events_list'][i]));
                    }
                };
                if (type == 'weekly'){
                    $("#ViewList").html("");
                    for (var i = 0; i < response['events_list'].length; i++){
                        $("#ViewList").append(make_list_item(response['events_list'][i]));
                    }
                };
            }
        }
    });
};