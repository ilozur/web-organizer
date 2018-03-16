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
            if (response['result'] == "Success")
            {
                $('#note_title_show').html(response['title']);
                $('#note_data_show').html(response['data']);
                $('#note_added_time').html(response['added_time']);
                if ('last_edit_time' in response)
                {
                    $('#note_last_edit').html(response['last_edit_time'] + '(edited)');
                }
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
    var data = CKEDITOR.instances.id_note_data.getData();
    form_data = $('#add_note_form').serialize();
    form_data['data'] = data;
    $.ajax({
        type: "POST",
        url: '/notes/add',
        data: form_data,
        success: function(response)
        {
            if (response['result'] == "Success")
            {
                alert('OK, note was added');
                var now_notes_count = $("#last_notes_holder").find('p').length - 1;
                if (now_notes_count == -1)
                {
                    $("#last_notes_holder").html('<p class="lead"> <small><a href="' + notes_link + '">Показать все</a></small></p>');
                    $("#last_notes_holder").parent().find('h5').remove();
                }
                if (now_notes_count >= 3)
                {
                    $("#last_notes_holder").find('p')[2].remove();
                }
                var new_note_html = '<p class="lead"><a href="#" data-toggle="modal" data-target="#Note-Card"' +
                    'onclick="get_note_data_ajax(' + response['id'] + ')" id="note_title_' + response['id'] +
                    '">' + response['name'] + '</a></p>';
                $("#last_notes_holder").html(new_note_html + $("#last_notes_holder").html());
                $("#close_note_btn").trigger("click");
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
            if (response['result'] == "success")
            {
                alert('OK, event was added');
                $("#close_calendar_btn").trigger("click");
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
            if (response['result'] == "success")
            {
                alert('OK, Changes were saved');
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
            }
            $("#save_note_form").find(':input').each(function(){
                $(this).removeAttr('disabled');
            });
            $('#save_note_btn').removeAttr('disabled');
        }
    });
};