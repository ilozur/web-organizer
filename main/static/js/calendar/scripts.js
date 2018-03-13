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
            if (response['result'] == "success")
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
                            result_html += '<tr>\n<th class="bg-danger">' + String(week['week_num']) + '</th>\n';
                            var week_days = week['week_days'];
                            week_days.forEach(function(day, i, week_days)
                            {
                                if (day['class'])
                                {
                                    result_html += '<td class="' + day['class'] + '"><small class="date">' + String(day['day']) + '</small></td>\n';
                                }
                                else
                                {
                                    result_html += '<td><small class="date">' + String(day['day']) + '</small></td>\n';
                                }
                            });
                            result_html += '</tr>\n';
                        });
                        $(this).html(result_html);
                    }
                );
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
            if (response['result'] == "success")
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
                            result_html += '<tr>\n<th class="bg-danger">' + String(week['week_num']) + '</th>\n';
                            var week_days = week['week_days'];
                            week_days.forEach(function(day, i, week_days)
                            {
                                if (day['class'])
                                {
                                    result_html += '<td class="' + day['class'] + '"><small class="date">' + String(day['day']) + '</small></td>\n';
                                }
                                else
                                {
                                    result_html += '<td><small class="date">' + String(day['day']) + '</small></td>\n';
                                }
                            });
                            result_html += '</tr>\n';
                        });
                        $(this).html(result_html);
                    }
                );
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
            if (response['result'] == "success")
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
                            result_html += '<tr>\n<th class="bg-danger">' + String(week['week_num']) + '</th>\n';
                            var week_days = week['week_days'];
                            week_days.forEach(function(day, i, week_days)
                            {
                                if (day['class'])
                                {
                                    result_html += '<td class="' + day['class'] + '"><small class="date">' + String(day['day']) + '</small></td>\n';
                                }
                                else
                                {
                                    result_html += '<td><small class="date">' + String(day['day']) + '</small></td>\n';
                                }
                            });
                            result_html += '</tr>\n';
                        });
                        $(this).html(result_html);
                    }
                );
            }
        }
    });
};

function add_event_ajax()
{
    for (instance in CKEDITOR.instances) {
        CKEDITOR.instances[instance].updateElement();
    }
    var description = CKEDITOR.instances.id_description.getData();
    form_data = $('#add_event_form').serialize();
    form_data['description'] = description;
    $.ajax({
        type: "POST",
        url: '/calendar/event/add',
        data: form_data,
        success: function(response)
        {
            alert(response['result']);
            if (response['result'] == "success")
            {
                window.location.href = '/calendar';
            }
        }
    });
};