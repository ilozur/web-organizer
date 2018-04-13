function sorting(type){
    $.ajax({
        type: "POST",
        url: '/todo/sort',
        data: {"data": type},
        success: function(response)
        {
            if (response['result'] == "Success")
            {
                $("#ViewList").find("a.list-group-item").each(function(index) {
                    $(this).attr("onclick", 'get_todo_data_ajax(' + response['todo_list'][index][2] + ')');
                    $(this).find("h7").html(response['todo_list'][index][0]);
                    $(this).find("small").html(response['todo_list'][index][1]);
                });
                $("#ViewCard").find("a.col-md-4").each(function(index) {
                    $(this).find("h3").html(response['todo_list'][index][0]);
                    $(this).find("small").html(response['todo_list'][index][1]);
                });
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
            if (response['result'] == 'Success')
            {
                $("#todo_" + id).remove();
                $("#card_" + id).remove();
                $("#amounts small:eq(1)").html(response['amount_of_todos'][0]);
                $("#amounts small:eq(3)").html(response['amount_of_todos'][1]);
                $("#amounts small:eq(5)").html(response['amount_of_todos'][2]);
            };
        }
    });
};


function get_todo_data_ajax(id){
    $.ajax({
        type: "POST",
        url: '/todo/show_todo',
        data: {"id": id},
        success: function(response)
        {
            if (response['result'] == "Success")
            {
                $("#Open").find("#todo_title_show").html(response['title']);
                $("#Open").find("#todo_text_show").html(response['text']);
                $("#Open").find("#todo_added_time").html(response['added_date_and_time']);
                $("#Open").find("p:first").html(response['status']);
                $("#Open").find("button.btn-light").attr("onclick", "status_change(" + id + ", " + response['current_status'] + ")");
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

function open_todo_edit_mode()
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

function ShowCard()
{
    $("#ViewList").hide("slow");
    $("#ViewCard").show("slow");
};

function ShowList()
{
    $("#ViewList").show("slow");
    $("#ViewCard").hide("slow");
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
                var result_html_list = '<div id="todo_' + response['id'] + '" style="display: none" onclick="get_todo_data_ajax(' + response['id'] + ');">' +
                    '<a href="#" class="list-group-item list-group-item-action list-group-item-warning"' +
                    'data-toggle="modal" data-target="#Open-Todo"> <h7 id="todo_title_' + response['id'] + '">' +
                    response['title'] + '</h7><div class="date"> <small>' +
                    response['datetime'] + '</small></div></a></div>';
                var result_html_card = '<div style="display: none" id="todo_card_' + response['id'] + '" onclick="get_todo_data_ajax(' +
                    response['id'] + ');" class="col-md-4" data-toggle="modal" data-target="#Open-Todo"><div class="card">' +
                    '<div class="card-body"><h3 id="card_todo_title_' + response['id'] + '">' + response['title'] + '</h3><small class="date">' + response['datetime'] +
                    '</small><hr/></div></div></div>';
                $("#list_id").html(result_html_list + $("#list_id").html());
                $("#cards_id").html(result_html_card + $("#cards_id").html());
                $('#todo_' + response['id']).slideDown(duration='slow');
                $('#todo_card_' + response['id']).slideDown(duration='slow');
                $("#close_todo_btn").trigger("click");
            }
        }
    });
};


function delete_todo_ajax(id)
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
                $('#todo_' + id).slideUp(duration='slow', complete=function(){$('#todo_' + id).remove()});
                    $('#todo_card_' + id).slideUp(duration='slow', complete=function(){$('#todo_card' + id).remove()});
            }
            $('#delete_btn').removeAttr('disabled');
        }
    });
};