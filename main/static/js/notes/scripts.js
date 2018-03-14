function get_note_data_ajax(id){
    $('#note_num').html(id);
    for (instance in CKEDITOR.instances) {
                    CKEDITOR.instances[instance].updateElement();
                }
    CKEDITOR.instances.id_data_show.setData('loading');
    $.ajax({
        type: "POST",
        url: '/notes/get_note_data',
        data: {"id": id},
        success: function(response)
        {
            if (response['result'] == "Success")
            {
                $('#id_title_show').val(response['title']);
                for (instance in CKEDITOR.instances) {
                    CKEDITOR.instances[instance].updateElement();
                }
                CKEDITOR.instances.id_data_show.setData(response['data']);
            }
        }
    });
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
                    $("#list_id").append('<div onclick="get_note_data_ajax('+ response['notes_list'][i][2] + ');"><a href="#" class="list-group-item list-group-item-action list-group-item-warning" data-toggle="modal" data-target="#Open-Note"><h7 id="note_title_'
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
    for (instance in CKEDITOR.instances) {
        CKEDITOR.instances[instance].updateElement();
    }
    var data = CKEDITOR.instances.id_data_show.getData();
    var id = $('#note_num').html();
    $("#save_note_form").find(':input').each(function(){
        $(this).attr('disabled', 'disabled');
    });
    $('#save_btn').attr('disabled', 'disabled');
    $.ajax({
        type: "POST",
        url: '/notes/save',
        data: {"id": id, "title": $('#id_title_show').val(), "data": data},
        success: function(response)
        {
            if (response['result'] == "Success")
            {
                alert('OK, Changes were saved');
                $('#note_title_' + id).html($('#id_title_show').val());
                $('#note_data_' + id).html(data);
                CKEDITOR.instances.id_data_show.setData(data);
            }
            $("#save_note_form").find(':input').each(function(){
                $(this).removeAttr('disabled');
            });
            $('#save_btn').removeAttr('disabled');
        }
    });
};

function add_note_ajax()
{
    for (instance in CKEDITOR.instances) {
        CKEDITOR.instances[instance].updateElement();
    }
    var data = CKEDITOR.instances.id_data.getData();
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
                result_html = '<div onclick="get_note_data_ajax('+ response['id'] + ');"><a href="#" class="list-group-item list-group-item-action list-group-item-warning" data-toggle="modal" data-target="#Open-Note"><h7 id="note_title_'
                    + response['id'] + '">' + $('#id_title').val()
                    + '</h7><div class="date"> <small id="note_date_'
                    + response['id'] + '">' + '03.11.18'
                    + '</small></div></a></div>'
                $("#list_id").html(result_html + $("#list_id").html());
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
                    $("#list_id").append('<div onclick="get_note_data_ajax('+ response['notes_list'][i][2] + ');"><a href="#" class="list-group-item list-group-item-action list-group-item-warning" data-toggle="modal" data-target="#Open-Note"><h7 id="note_title_'
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

function delete_note_ajax(id)
{
    $('#delete_btn').attr('disabled', 'disabled');
    $.ajax({
        type: "POST",
        url: '/notes/delete',
        data: {"id": id},
        success: function(response)
        {
            if (response['result'] == "Success")
            {
                alert('OK, note was deleted');
                $('#note_' + id).slideUp("Slow");
            }
            $('#delete_btn').removeAttr('disabled');
        }
    });
};