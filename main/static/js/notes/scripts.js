selected_sorting_type = null;

function init()
{
    $.each($('#note_list .list-group a'), function() { this.onclick = function() { get_note_data($(this).attr('id')) } });
    document.getElementById('search_btn').onclick = search;
};

function get_note_data(id)
{
    $('#note_show').attr('hidden', '');
    $('#preloader').removeAttr('hidden');
    $.ajax({
        type: "POST",
        url: '/notes/get_note_data',
        data: {"id": id},
        success: function(response)
        {
            if (response['result'] == "100")
            {
                $.each($('#note_list .list-group a'), function() { $(this).removeClass('active') })
                $('#' + response['id']).addClass('active');
                init();
                document.getElementById(response['id']).onclick = null;
                set_note_show(response);
                $('#preloader').attr('hidden', '');
                $('#note_show').removeAttr('hidden');
            }
            else
            {
                voice_ajax_result(response['result']);
            }
        }
    });
};

function set_note_show(response)
{
    $('#note_show .note h3').html(' ' + response['title'] + ' ');
    $('#note_show .note .date').html(response['added_time']);
    $('#note_show .note .text').html(response['data']);
    $('#delete_btn').unbind('click');
    $('#delete_btn').click(function() { delete_note(response['id']); });
};

function delete_note(id)
{
    var should_delete = confirm('Вы уверены?');
    if (should_delete)
    {
        $.ajax({
            type: "POST",
            url: '/notes/delete',
            data: {"id": id},
            success: function(response)
            {
                if (response['result'] == "100")
                {
                    $('#note_show').attr('hidden', '');
                    $('#' + id).remove();
                    voice_text('Заметка удалена.');
                }
                else
                {
                    voice_ajax_result(response['result']);
                }
            }
        });
    }
};

function add_note_to_list(id, title)
{
    $('#note_list .list-group').append('<a id="' + id + '" class="list-group-item list-group-item-action list-group-item-warning">' + title + '</a>');
    $('#' + id).click(function() { get_note_data(id) } );
};

function search()
{
    if (selected_sorting_type)
    {
        sort_notes(selected_sorting_type);
    }
    else
    {
        $.ajax({
            type: "POST",
            url: '/notes/search',
            data: {"aim": $('input[name="aim"]').val()},
            success: function(response)
            {
                $('#note_list .list-group').html('');
                for (var i = 0; i < response['found_notes'].length; i++)
                {
                    add_note_to_list(response['found_notes'][i]['id'], response['found_notes'][i]['title']);
                }
            }
        });
    }
};

function sort_notes(sorting_type)
{
    selected_sorting_type = sorting_type;
    $.ajax({
        type: "POST",
        url: '/notes/sort',
        data: {"aim": $('input[name="aim"]').val(), "sorting_type": sorting_type},
        success: function(response)
        {
            $('#note_list .list-group').html('');
            for (var i = 0; i < response['found_notes'].length; i++)
            {
                add_note_to_list(response['found_notes'][i]['id'], response['found_notes'][i]['title']);
            }
        }
    });
};