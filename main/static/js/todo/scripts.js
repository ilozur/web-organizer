function sorting(type){
    $.ajax({
        type: "POST",
        url: '/todo/sort',
        data: {"data": type},
        success: function(response)
        {
            if (response['result'] == "Success")
            {
                $("#list_id").html('');
                for (var i = 0; i < response['todo_list'].length; i++) {
                    $("#list_id").append('<div onclick="get_todo_data_ajax('+ response['todo_list'][i][2] + ');"><a
                    href="#" class="list-group-item list-group-item-action list-group-item-warning" data-toggle="modal"
                     data-target="#Open-Todo"><h7 id="todo_title_'
                    + response['todo_list'][i][2] + '">' + response['notes_list'][i][0]
                    + '</h7><div class="date"> <small id="todo_date_'
                    + response['todo_list'][i][2] + '">' + response['todo_list'][i][1]
                    + '</small></div></a></div>');
                }
                $("#search_todo_form").find(':input').each(function(){
                    $(this).removeAttr('disabled');
                });
                $('#sign_up_btn').removeAttr('disabled');
            }
        }
    });
};

function status_change(id, type){
    $.ajax({
        type: "POST",
        url: '/todo/change',
        data: {'id': id, 'type': type},
        success: function(response){

        }
    });
};


function get_todo_data_ajax(id){
    $('#note_num').html(id);
    $('#Edit-Todo-Modal').attr('hidden', '');
    $('#Show-Todo-Modal').removeAttr('hidden');
    $('#todo_title_show').html('loading');
    $('#todo_text_show').html('loading');
    $.ajax({
        type: "POST",
        url: '/todo/show_todo',
        data: {"id": id},
        success: function(response)
        {
            if (response['result'] == "Success")
            {
                $('#todo_title_show').html(response['title']);
                $('#todo_text_show').html(response['text']);
                $('#todo_added_time').html(response['added_date_and_time']);
                if ('last_edit_time' in response)
                {
                    $('#todo_last_edit').html(response['last_edit_time'] + '(edited)');
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
    $('#Show-Todo-Modal').attr('hidden', '');
    $('#Edit-Todo-Modal').removeAttr('hidden');
    for (instance in CKEDITOR.instances) {
        CKEDITOR.instances[instance].updateElement();
    }
    CKEDITOR.instances.id_todo_data_edit.setData($('#todo_text_show').html());
    $('#id_todo_title_edit').val($('#todo_title_show').html());
};

function close_todo_edit_mode()
{
    $('#Edit-Todo-Modal').attr('hidden', '');
    $('#Show-Todo-Modal').removeAttr('hidden');
};

function show_cards(){
    $('.list-view').hide();
    $('.card-view').hide();
    $('.card-view').removeAttr('hidden');
    $('.card-view').show('slow');
};

function show_list(){
    $('.card-view').hide();
    $('.list-view').hide();
    $('.list-view').removeAttr('hidden');
    $('.list-view').slideDown('slow');
};

function search_notes_ajax()
{
    form_data = $('#search_todo_form').serialize();
    $("#search_todo_form").find(':input').each(function(){
        $(this).attr('disabled', 'disabled');
    });
    $('#sign_up_btn').attr('disabled', 'disabled');
    $.ajax({
        type: "POST",
        url: '/todo/search',
        data: form_data,
        success: function(response)
        {
            if (response['result'] == "Success")
            {
                $("#list_id").html('');
                for (var i = 0; i < response['todo_list'].length; i++) {
                    $("#list_id").append('<div onclick="get_todo_data_ajax('+ response['todo_list'][i][2] + ');
                    "><a href="#" class="list-group-item list-group-item-action list-group-item-warning"
                    data-toggle="modal" data-target="#Opne_Todo"><h7 id="todo_title_'
                    + response['todo_list'][i][2] + '">' + response['todo_list'][i][0]
                    + '</h7><div class="date"> <small id="todo_date_'
                    + response['todo_list'][i][2] + '">' + response['todo_list'][i][1]
                    + '</small></div></a></div>');
                }
                $("#search_todo_form").find(':input').each(function(){
                    $(this).removeAttr('disabled');
                });
                $('#sign_up_btn').removeAttr('disabled');
            }
        }
    });
};

function save_todo_ajax()
{
    var id = $('#todo_num').html();
    $("#id_todo_id").val(id)
    for (instance in CKEDITOR.instances) {
        CKEDITOR.instances[instance].updateElement();
    }
    var form_data = $('#save_todo_form').serialize();
    form_data['todo_text_edit'] = CKEDITOR.instances.id_todo_data_edit.getData();
    $("#save_todo_form").find(':input').each(function(){
        $(this).attr('disabled', 'disabled');
    });
    $('#save_todo_btn').attr('disabled', 'disabled');
    $.ajax({
        type: "POST",
        url: '/todo/edit',
        data: form_data,
        success: function(response)
        {
            if (response['result'] == "success")
            {
                alert('OK, Changes were saved');
                $('#todo_title_' + id).html($('#id_todo_title_edit').val());
                close_todo_edit_mode();
                for (instance in CKEDITOR.instances) {
                    CKEDITOR.instances[instance].updateElement();
                }
                $('#todo_text_show').html(CKEDITOR.instances.id_todo_data_edit.getData());
                $('#todo_title_show').html($('#id_todo_title_edit').val());
                $('#todo_last_edit').html(response['edited_time']);
            }
            $("#save_todo_form").find(':input').each(function(){
                $(this).removeAttr('disabled');
            });
            $('#save_todo_btn').removeAttr('disabled');
        }
    });
};

function add_todo_ajax()
{
    for (instance in CKEDITOR.instances) {
        CKEDITOR.instances[instance].updateElement();
    }
    form_data = $('#add_todo_form').serialize();
    form_data['data'] = CKEDITOR.instances.id_todo_data.getData();;
    $.ajax({
        type: "POST",
        url: '/todo/add',
        data: form_data,
        success: function(response)
        {
            if (response['result'] == "Success")
            {
                alert('OK, todo was added');
                result_html = '<div id="todo_' + response['id'] + '" onclick="get_todo_data_ajax(' + response['id'] + ');">' +
                    '<a href="#" class="list-group-item list-group-item-action list-group-item-warning"' +
                    'data-toggle="modal" data-target="#Open-Todo"> <h7 id="todo_title_' + response['id'] + '">' +
                    response['title'] + '</h7><div class="date"> <small>' +
                    response['datetime'] + '</small></div></a></div>';
                $("#list_id").html(result_html + $("#list_id").html());
                $("#close_todo_btn").trigger("click");
            }
        }
    });
};


function delete_note_ajax(id)
{
    $('#delete_btn').attr('disabled', 'disabled');
    $.ajax({
        type: "POST",
        url: '/todo/delete',
        data: {"id": id},
        success: function(response)
        {
            if (response['result'] == "Success")
            {
                alert('OK, todo was deleted');
                $('#todo_' + id).slideUp("Slow");
            }
            $('#delete_btn').removeAttr('disabled');
        }
    });
};