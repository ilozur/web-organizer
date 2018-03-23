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

function clean_add_note_fields()
{
    for (instance in CKEDITOR.instances) {
        CKEDITOR.instances[instance].updateElement();
    }
    CKEDITOR.instances.id_note_data.setData("");
    $("#id_note_title").val("");
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

function show_cards(){
    if ($('#cards_id').attr('hidden'))
    {
        $('#list_id').attr('hidden', '');
        $('#list_id').attr('style', 'display: none');
        $('#cards_id').removeAttr('hidden');
        if ($('#cards_id div').length == 0)
        {
            $('#cards_id').removeAttr('style');
        }
        else
        {
            $('#cards_id').slideDown('slow');
        }
    }
};

function show_list(){
    if ($('#list_id').attr('hidden'))
    {
        $('#cards_id').attr('hidden', '');
        $('#cards_id').attr('style', 'display: none');
        $('#list_id').removeAttr('hidden');
        if ($('#list_id div').length == 0)
        {
            $('#list_id').removeAttr('style');
        }
        else
        {
            $('#list_id').slideDown('slow');
        }
    }
};

function search_notes_ajax()
{
    form_data = $('#search_note_form').serialize();
    $("#search_note_form").find(':input').each(function(){
        $(this).attr('disabled', 'disabled');
    });
    $('#sign_up_btn').attr('disabled', 'disabled');
    $.ajax({
        type: "POST",
        url: '/notes/search',
        data: form_data,
        success: function(response)
        {
            if (response['result'] == "Success")
            {
                $("#list_id").html('');
                for (var i = 0; i < response['notes_list'].length; i++) {
                    $("#list_id").append('<div onclick="get_note_data_ajax('+ response['notes_list'][i][2] + ');"><a href="#" class="list-group-item list-group-item-action list-group-item-warning" data-toggle="modal" data-target="#Note-Card"><h7 id="note_title_'
                    + response['notes_list'][i][2] + '">' + response['notes_list'][i][0]
                    + '</h7><div class="date"> <small id="note_date_'
                    + response['notes_list'][i][2] + '">' + response['notes_list'][i][1]
                    + '</small></div></a></div>');
                }
                $("#search_note_form").find(':input').each(function(){
                    $(this).removeAttr('disabled');
                });
                $('#sign_up_btn').removeAttr('disabled');
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
            if (response['result'] == "success")
            {
                alert('OK, Changes were saved');
                $('#note_title_' + id).html($('#id_note_title_edit').val());
                $('#card_note_title_' + id).html($('#id_note_title_edit').val());
                $('#card_note_description_' + id).html(response['data_part']);
                close_note_edit_mode();
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

function add_note_ajax()
{
    for (instance in CKEDITOR.instances) {
        CKEDITOR.instances[instance].updateElement();
    }
    var clean_text = $('#cke_id_note_data iframe').contents().find('body').text();
    $('#id_note_data_part').val(clean_text.substr(0, 128));
    form_data = $('#add_note_form').serialize();
    form_data['data'] = CKEDITOR.instances.id_note_data.getData();;
    $.ajax({
        type: "POST",
        url: '/notes/add',
        data: form_data,
        success: function(response)
        {
            if (response['result'] == "Success")
            {
                alert('OK, note was added');
                var result_html_list = '<div id="note_' + response['id'] + '" style="display: none" onclick="get_note_data_ajax(' + response['id'] + ');">' +
                    '<a href="#" class="list-group-item list-group-item-action list-group-item-warning"' +
                    'data-toggle="modal" data-target="#Note-Card"> <h7 id="note_title_' + response['id'] + '">' +
                    response['name'] + '</h7><div class="date"> <small>' +
                    response['datetime'] + '</small></div></a></div>';
                var result_html_card = '<div style="display: none" id="note_card_' + response['id'] + '" onclick="get_note_data_ajax(' +
                    response['id'] + ');" class="col-md-4" data-toggle="modal" data-target="#Note-Card"><div class="card">' +
                    '<div class="card-body"><h3 id="card_note_title_' + response['id'] + '">' + response['name'] + '</h3><small class="date">' + response['datetime'] +
                    '</small><hr/><p id="card_note_description_' + response['id'] + '">' + response['data_part'] + '</p></div></div></div>';
                $("#list_id").html(result_html_list + $("#list_id").html());
                $("#cards_id").html(result_html_card + $("#cards_id").html());
                $('#note_' + response['id']).slideDown(duration='slow');
                $('#note_card_' + response['id']).slideDown(duration='slow');
                $("#close_note_btn").trigger("click");
            }
        }
    });
};

function sort_notes_ajax(type){
    $.ajax({
        type: "POST",
        url: '/notes/sort',
        data: {"data": type},
        success: function(response)
        {
            if (response['result'] == "Success")
            {
                $("#list_id").html('');
                for (var i = 0; i < response['notes_list'].length; i++) {
                    $("#list_id").append('<div onclick="get_note_data_ajax('+ response['notes_list'][i][2] + ');"><a href="#" class="list-group-item list-group-item-action list-group-item-warning" data-toggle="modal" data-target="#Note-Card"><h7 id="note_title_'
                    + response['notes_list'][i][2] + '">' + response['notes_list'][i][0]
                    + '</h7><div class="date"> <small id="note_date_'
                    + response['notes_list'][i][2] + '">' + response['notes_list'][i][1]
                    + '</small></div></a></div>');
                }
                $("#search_note_form").find(':input').each(function(){
                    $(this).removeAttr('disabled');
                });
                $('#sign_up_btn').removeAttr('disabled');
            }
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
            data: {"id": id, 'return_last_note': false},
            success: function(response)
            {
                if (response['result'] == "success")
                {
                    alert('OK, note was deleted');
                    $('#note_' + id).slideUp(duration='slow', complete=function(){$('#note_' + id).remove()});
                    $('#note_card_' + id).slideUp(duration='slow', complete=function(){$('#note_card' + id).remove()});
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