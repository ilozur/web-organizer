onpopstate = function(event) {
    var page = get_key("page");
    var sort_type = get_key("sort_type");
    paginate(page, false, sort_type);
}

function add_note_to_list(notes_data){
    $("#list_id").append('<div onclick="get_note_data_ajax('
        + notes_data[2] + ');"><a href="#" class="list-group-item list-group-item-action list-group-item-warning" data-toggle="modal" data-target="#Note-Card"><h7 id="note_title_'
        + notes_data[2] + '">'
        + notes_data[0] + '</h7><div class="date"><small id="note_date_'
        + notes_data[2] + '">'
        + notes_data[1] + '</small></div></a></div>'
    );
}

function add_note_to_cards(notes_data){
    $("#cards_id").append('<div id="note_card_'
        + notes_data[2] + '" onclick="get_note_data_ajax('
        + notes_data[2] + ')" class="col-4" data-toggle="modal" data-target="#Note-Card"><div class="card"><div class="card-body"><h3 id="card_note_title_'
        + notes_data[2] + '">'
        + notes_data[0] + '</h3><small class="date">' + notes_data[1] + '</small><hr/><p id="card_note_description_'
        + notes_data[2] + '">'
        + notes_data[3] + '</p></div></div></div>'
    );
}

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
    $('#list_id').hide('slow');
    $('#cards_id').show('slow');
};

function show_list(){
    $('#cards_id').hide('slow');
    $('#list_id').show('slow');
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
            if (response['result'] == "100")
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
                $('#card_note_title_' + id).html($('#id_note_title_edit').val());
                $('#card_note_description_' + id).html(response['data_part']);
                close_note_edit_mode();
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
            if (response['result'] == "100")
            {
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
                $('#note_' + response['id']).show(duration='slow');
                $('#note_card_' + response['id']).show(duration='slow');
                $("#close_note_btn").trigger("click");
                voice_text('Заметка добавлена.');
            }
            else
            {
                voice_ajax_result(response['result']);
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
                if (response['result'] == "100")
                {
                    $('#note_' + id).hide(duration='slow', complete=function(){$('#note_' + id).remove()});
                    $('#note_card_' + id).hide(duration='slow', complete=function(){$('#note_card' + id).remove()});
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

function sort_notes_ajax(sort_type){
    var page = get_key("page");
    paginate(page, true, sort_type);
};

function paginate(page, push_state=true, sort_type=false){
    if (!sort_type)
    {
        sort_type = get_key("sort_type");
    }
    if (!page)
    {
        page = 1;
    }
    var url = "";
    if (sort_type)
    {
        url = "/notes?page=" + page + "&sort_type=" + sort_type;
    }
    else
    {
        url = "/notes?page=" + page;
    }
    if (push_state)
    {
        history.pushState(null,null, url);
    }
    $.ajax({
        type: "POST",
        url: url,
        success: function(response)
        {
            if (response['result'] == 100) {
                for (var i = 1; i <= $('#paginate_btn_holder a').length - 2; i++)
                {
                    $('#paginate_btn_' + i).removeAttr('disabled');
                }
                $('#paginate_btn_' + response['normal_page']).attr('disabled', 'disabled');
                if (response['buttons'][0]) {
                    $("#PrevPage").removeAttr('disabled');
                    $("#PrevPage").attr('onclick', 'paginate(' + (response['normal_page'] - 1) + ')');
                } else {
                    $("#PrevPage").attr('disabled', 'disabled');
                    $('#PrevPage').removeAttr('onclick');
                }
                if (response['buttons'][1]) {
                    $("#NextPage").removeAttr('disabled');
                    $("#NextPage").attr('onclick', 'paginate(' + (response['normal_page'] + 1) + ')');
                }  else {
                    $("#NextPage").attr('disabled', 'disabled');
                    $('#NextPage').removeAttr('onclick');
                }
                $("#list_id").html('');
                $("#cards_id").html('');
                for (var i = 0; i < response['notes_list'].length; i++) {
                    add_note_to_list(response['notes_list'][i]);
                    add_note_to_cards(response['notes_list'][i]);
                }
            }
        }
    });
};

function get_key(key) {
    var p = window.location.search;
    p = p.match(new RegExp(key + '=([^&=]+)'));
    return p ? p[1] : false;
};