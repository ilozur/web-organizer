var notes_link;

function setup_link(link)
{
    notes_link = link;
};

function clean_add_note_fields()
{
    for (instance in CKEDITOR.instances) {
        CKEDITOR.instances[instance].updateElement();
    }
    CKEDITOR.instances.id_note_data.setData("");
    $("#id_note_title").val("");
};

function get_note_data_ajax(id){
    $('#note_num').html(id);
    $('#Edit-Note-Modal').attr('hidden', '');
    $('#Show-Note-Modal').removeAttr('hidden');
    $('#note_title_show').html('loading');
    $('#note_data_show').html('loading');
    $.ajax({
        type: "POST",
        url: '/notes/get_note_data',
        data: {"id": id},
        success: function(response)
        {
            if (response['result'] == "100")
            {
                $('#note_title_show').html(response['title']);
                $('#note_data_show').html(response['data']);
                $('#note_added_time').html(response['added_time']);
                if ('last_edit_time' in response)
                {
                    $('#note_last_edit').html(response['last_edit_time'] + '(edited)');
                }
            }
            else
            {
                voice_ajax_result(response['result']);
            }
        }
    });
};

function open_note_edit_mode()
{
    $('#Show-Note-Modal').attr('hidden', '');
    $('#Edit-Note-Modal').removeAttr('hidden');
    for (instance in CKEDITOR.instances) {
        CKEDITOR.instances[instance].updateElement();
    }
    CKEDITOR.instances.id_note_data_edit.setData($('#note_data_show').html());
    $('#id_note_title_edit').val($('#note_title_show').html());
};

function close_note_edit_mode()
{
    $('#Edit-Note-Modal').attr('hidden', '');
    $('#Show-Note-Modal').removeAttr('hidden');
};

function add_note_ajax()
{
    for (instance in CKEDITOR.instances) {
        CKEDITOR.instances[instance].updateElement();
    }
    var clean_text = $('#cke_id_note_data iframe').contents().find('body').text();
    $('#id_note_data_part').val(clean_text.substr(0, 128));
    var data = CKEDITOR.instances.id_note_data.getData();
    form_data = $('#add_note_form').serialize();
    form_data['data'] = data;
    $.ajax({
        type: "POST",
        url: '/notes/add',
        data: form_data,
        success: function(response)
        {
            if (response['result'] == "100")
            {
                var now_notes_count = $("#last_notes_holder").find('div').length;
                if (now_notes_count == 0)
                {
                    $("#last_notes_holder").html('<p class="lead"><small><a href="' + notes_link + '">Показать все</a></small></p></div>');
                    $("#last_notes_holder").parent().find('h5').remove();
                    $("#last_note_title").attr('href', '');
                    $("#last_note_title").attr('data-toggle', 'modal');
                    $("#last_note_title").attr('data-target', '#Note-Card');
                }
                var new_note_html = '<div style="display: none" id="note_' + response['id'] + '"><p class="lead"><a href="#" data-toggle="modal" data-target="#Note-Card"' +
                    'onclick="get_note_data_ajax(' + response['id'] + ')" id="note_title_' + response['id'] +
                    '">' + response['name'] + '</a></p></div>';
                $("#last_notes_holder").html(new_note_html + $("#last_notes_holder").html());
                if (now_notes_count >= 3)
                {
                    var id = $("#last_notes_holder div:last").attr('id');
                    $('#' + id).slideUp(duration='slow', complete=function(){$('#' + id).remove()});
                }
                $('#note_' + response['id']).slideDown('slow');
                $("#close_note_btn").trigger("click");
                $("#last_note_title").html(response['name']);
                $("#last_note_title").attr('onclick', 'get_note_data_ajax(' + response['id'] + ')');
                voice_text('Заметка добавлена.');
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
            }
            else
            {
                voice_ajax_result(response['result']);
            }
        }
    });
};

function save_note_ajax()
{
    var id = $('#note_num').html();
    $("#id_note_id").val(id)
    for (instance in CKEDITOR.instances) {
        CKEDITOR.instances[instance].updateElement();
    }
    var clean_text = $('#cke_id_note_data_edit iframe').contents().find('body').text();
    $('#id_note_data_part_edit').val(clean_text.substr(0, 128));
    var form_data = $('#save_note_form').serialize();
    form_data['note_data_edit'] = CKEDITOR.instances.id_note_data_edit.getData();
    $("#save_note_form").find(':input').each(function(){
        $(this).attr('disabled', 'disabled');
    });
    $('#save_note_btn').attr('disabled', 'disabled');
    $.ajax({
        type: "POST",
        url: '/notes/save',
        data: form_data,
        success: function(response)
        {
            if (response['result'] == "100")
            {
                $('#note_title_' + id).html($('#id_note_title_edit').val());
                close_note_edit_mode();
                for (instance in CKEDITOR.instances) {
                    CKEDITOR.instances[instance].updateElement();
                }
                $('#note_data_show').html(CKEDITOR.instances.id_note_data_edit.getData());
                $('#note_title_show').html($('#id_note_title_edit').val());
                for (instance in CKEDITOR.instances) {
                    CKEDITOR.instances[instance].updateElement();
                }
                $('#note_data_show').html(CKEDITOR.instances.id_note_data_edit.getData());
                $('#note_title_show').html($('#id_note_title_edit').val());
                $('#note_last_edit').html(response['edited_time']);
                voice_text('Заметка сохранена.');
            }
            else
            {
                voice_ajax_result(response['result']);
            }
            $("#save_note_form").find(':input').each(function(){
                $(this).removeAttr('disabled');
            });
            $('#save_note_btn').removeAttr('disabled');
        }
    });
};

function delete_note_ajax()
{
    var id = $('#note_num').html();
    var should_delete = confirm('Вы уверены?');
    if (should_delete)
    {
        $.ajax({
            type: "POST",
            url: '/notes/delete',
            data: {"id": id, "return_last_note": true},
            success: function(response)
            {
                if (response['result'] == "100")
                {
                    var now_notes_count = $("#last_notes_holder").find('div').length;
                    if (now_notes_count == 1)
                    {
                        $("#last_notes_holder p:last").remove();
                        $("#last_notes_holder").append('<h5>Нет заметок</h5>');
                        $('#last_note_title').html('Нет заметок');
                        $("#last_note_title").removeAttr('onclick');
                        $("#last_note_title").removeAttr('href');
                        $("#last_note_title").removeAttr('data-toggle');
                        $("#last_note_title").removeAttr('data-target');
                    }
                    else
                    {
                        if ($('#last_notes_holder div')[0].id == 'note_' + id)
                        {
                            $('#last_note_title').html($('#last_notes_holder div p a')[1].text);
                            $("#last_note_title").attr('onclick', $('#last_notes_holder div p a').attr('onclick'));
                        }
                    }
                    if (response['id'])
                    {
                        var new_note_html = '<div style="display: none" id="note_' + response['id'] + '"><p class="lead"><a href="#" data-toggle="modal" data-target="#Note-Card"' +
                            'onclick="get_note_data_ajax(' + response['id'] + ')" id="note_title_' + response['id'] +
                            '">' + response['name'] + '</a></p></div>';
                        var show_all_label = '<p class="lead"><small><a href="' + notes_link + '">Показать все</a></small></p></div>';
                        $("#last_notes_holder p:last").remove();
                        $("#last_notes_holder").html($("#last_notes_holder").html() + new_note_html);
                        $("#last_notes_holder").html($("#last_notes_holder").html() + show_all_label);
                        $('#note_' + response['id']).slideDown('slow');
                    }
                    $('#note_' + id).slideUp(duration='slow', complete=function(){$('#note_' + id).remove()});

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

function voice_note()
{
    var clean_text = $('#note_data_show').text();
    voice_text(clean_text);
};

function listen_note(param)
{
    $('#New-Note').find('img').attr('src', '/static/icons/listening_icon.png');
    voice_to_text(function (text) {
        for (instance in CKEDITOR.instances) {
            CKEDITOR.instances[instance].updateElement();
        }
        if (param == "add")
        {
            CKEDITOR.instances.id_note_data.setData(text);
        }
        else if (param == 'edit')
        {
            CKEDITOR.instances.id_note_data_edit.setData(text);
        }
        $('#New-Note').find('img').attr('src', '/static/icons/micro_icon.png');
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
            }
            else
            {
                voice_ajax_result(response['result']);
            }

        }
    });
};