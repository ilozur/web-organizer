function sorting(type){
    $.ajax({
        type: "POST",
        url: '/todo/sort',
        data: {"data": type},
        success: function(response)
        {
            if (response['result'] == "Success")
            {
                $("#ViewList > #todo_body").each(function(index) {
                    $(this).attr("onclick", 'get_todo_data_ajax(' + response['todo_list'][index][2] + ')');
                    $($(".date > small").get(index)).html(response['todo_list'][index][1]);
                    $($("a.list-group-item > #todo_title").get(index)).html(response['todo_list'][index][0]);
                });
                $("#ViewCard > div.row").each(function(index) {
                    $($(".card-body > h3").get(index)).html(response['todo_list'][index][0]);
                    $($(".card-body > .date").get(index)).html(response['todo_list'][index][1]);
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
                $("#Open").find("h2").html(response['title']);
                $("#Open").find("p:first").html(response['text']);
                $("#Open").find("small").html(response['added_date_and_time']);
                $("#Open").find("p:eq(1)").html(response['status']);
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
                alert('OK, todo was deleted');
                $('#todo_' + id).slideUp("Slow");
            }
            $('#delete_btn').removeAttr('disabled');
        }
    });
};