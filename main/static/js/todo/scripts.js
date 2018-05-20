function add_todo_to_cards(item){
    $("#CardList").append('<div id="todo_card_' + item[2] + '" onclick="get_todo_data_ajax(' + item[2] + ')"' +
                          'class="col-4" data-toggle="modal" data-target="#Open-Todo"><div class="card">' +
                          '<div class="card-body"><h3>' + item[0] + '</h3><small class="date" id="card_date_' +
                          item[2] + '">' + item[1] + '</small></div><div class="card-footer"><div class="priorities"' +
                          'id="card_priorities_' + item[2] +'"></div><button type="button"' +
                          'onclick="status_change(' + item[2] + ', ' + "'done'" + ')" class="btn btn-light">&#10003;' +
                          '</button></div></div></div>'
    );
    get_priorities(item[3], item[2]);
};

function add_todo_to_list(item){
    $("#ViewList").append('<div id="todo_' + item[2] + '" onclick="get_todo_data_ajax(' + item[2] + ');">' +
                          '<a href="#" class="list-group-item list-group-item-primary" data-toggle="modal" data-target="#Open-Todo">' +
                          '<button type="button" class="btn btn-primary" onclick="status_change(' + item[2] + ', ' + "'done'" + ')">' +
                          '&#10003;</button><h7 id="todo_title_' + item[2] + '">' + item[0] + '</h7><div class="priorities">' +
                          '<div class="priorities" id="list_priorities_' + item[2] + '"></div><div class="date">' +
                          '<small id="todo_date_' + item[2] + '">' + item[1] + '</small></div></div></a></div>'
    );
    get_priorities(item[3], item[2]);
};

function update_done_todos(item){
    var str = "'in progress'";
    tmp = '<a href="#" id="todo_' + item[2] + '" class="list-group-item list-group-item-light" data-toggle="modal" data-target="#Open">' +
              '<h7>' + item[0] + '</h7>' +
              '<div class="priorities">' +
                  '<button  type="button" class="btn btn-info" onclick="status_change(' + item[2] + ', ' + str + ')">&#10007;</button>' +
                  '<div class="date"><small>' + item[1] + '</small></div>' +
              '</div>' +
          '</a>';
    $("#Complete").find(".list-group").html(tmp + $("#Complete").find(".list-group").html());
    get_priorities(item[3], item[2]);
}

function get_priorities(value, id){
    $("#list_priorities_" + id).html('');
    for (var i = 0; i < value; i++){
        $("#list_priorities_" + id).html("<span class='badge badge-pill priority-list'>!</span>" + $("#list_priorities_" + id).html());
    }
    $("#card_priorities_" + id).html('');
    for (var i = 0; i < value; i++){
        $("#card_priorities_" + id).html($("#card_priorities_" + id).html() + "<span class='badge badge-pill priority'>!</span>");
    }
};

function clean_add_todo_fields()
{
    $("#id_todo_title").val("");
    $("#id_todo_deadline").val("");
    $("#id_todo_time").val("");
};

function search_todo_ajax()
{
    form_data = $('#search_todo_form').serialize();
    $("#search_todo_form").find(':input').each(function(){
        $(this).attr('disabled', 'disabled');
    });
    $('#search_todo_btn').attr('disabled', 'disabled');
    $.ajax({
        type: "POST",
        url: '/todo/search',
        data: form_data,
        success: function(response)
        {
            if (response['result'] == "Success")
            {
                alert(response['result']);
                $("#ViewList").html('');
                for(var i = 0; i < response['todo_list'].length; i++){
                    add_todo_to_list(response['todo_list'][i]);
                }
		        $("#CardList").html('');
		        for(var i = 0; i < response['todo_list'].length; i++){
                    add_todo_to_cards(response['todo_list'][i]);
                }
                $("#search_todo_form").find(':input').each(function(){
                    $(this).removeAttr('disabled');
                });
                $('#search_todo_btn').removeAttr('disabled');
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
		        sorting('new');
		        if (type == 'done'){
		            update_done_todos(response['current']);
		        } else {
		            $("#todo_" + id).remove();
		        }
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
                $("#todo_id").html(id);
                $("#Open-Todo").find("#todo_title_show").html(response['title']);
		        $("#Open-Todo").find("#todo_id").html(response['id']);
                $("#Open-Todo").find("#todo_added_time").html(response['added_date_and_time']);
                $("#Open-Todo").find("p:first").html(response['status']);
                $("#Open-Todo").find("button.btn-light").attr("onclick", "status_change(" + id + ", " + response['current_status'] + ")");
		        $("#Open-Todo").find("#todo_deadline").html(response['deadline']);
		        $("#Open-Todo").find("#todo_num").html(response['id']);
		        $("#Open-Todo").find("#todo_priority").html('');
		        for (var i = 0; i < response['priority']; i++){
		            $("#Open-Todo").find("#todo_priority").html($("#Open-Todo").find("#todo_priority").html() + '<span class="badge badge-pill priority">!</span>');
		            $('#id_todo_edit_time').val(response['time'][0] + ':' + response['time'][1]);
		            $('#id_todo_edit_deadline').val(response['date'][0] + '-' + response['date'][1] + '-' + response['date'][2]);
		        }
            }
        }
    });
};

function save_todo_ajax()
{
    var id = $('#todo_num').html();
    $("#id_todo_id").val(id);
    var form_data = $('#edit_todo_form').serialize();
    $("#edit_todo_form").find(':input').each(function(){
        $(this).attr('disabled', 'disabled');
    });
    $('#save_todo_btn').attr('disabled', 'disabled');
    $.ajax({
        type: "POST",
        url: '/todo/edit',
        data: form_data,
        success: function(response)
        {
            if (response['result'] == "Success")
            {
                alert('OK, Changes were saved');
                $('#todo_title_' + id).html($('#id_todo_edit_title').val());
                $('#todo_card_' + id).html($('#id_todo_edit_title').val());
                get_priorities(response['priority'], id);
                $('#todo_date_' + id).html(response['deadline_date']);
                close_todo_edit_mode();
                $('#todo_title_show').html($('#id_todo_edit_title').val());
		        set_priority_edit($('#id_todo_edit_priority').val());
                $('#todo_last_edit').html(response['edited_time']);
            }
            else{
                alert(response['result']);
            }
            $("#edit_todo_form").find(':input').each(function(){
                $(this).removeAttr('disabled');
            });
            $('#save_todo_btn').removeAttr('disabled');
        }
    });
};

function set_priority(value){
    $("#id_todo_priority").val(value);
};

function set_priority_edit(value){
    $("#id_todo_edit_priority").val(value);
};

function open_todo_edit_mode()
{
    $('#Show-Todo-Modal').attr('hidden', '');
    $('#Edit-Todo-Modal').removeAttr('hidden');
    $('#id_todo_edit_title').val($('#todo_title_show').html());
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

function add_todo_ajax()
{
    form_data = $('#add_todo_form').serialize();
    $.ajax({
        type: "POST",
        url: '/todo/add',
        data: form_data,
        success: function(response)
        {
            if (response['result'] == "Success")
            {
		        var item = [response['title'], response['datetime'], response['id'], response['priority']];
		        var tmp = '<div style="display: none" id="todo_card_' + item[2] + '" onclick="get_todo_data_ajax(' + item[2] + ')"' +
                          'class="col-4" data-toggle="modal" data-target="#Open-Todo"><div class="card">' +
                          '<div class="card-body"><h3>' + item[0] + '</h3><small class="date" id="card_date_' +
                          item[2] + '">' + item[1] + '</small></div><div class="card-footer"><div class="priorities"' +
                          'id="card_priorities_' + item[2] +'"></div><button type="button"' +
                          'onclick="status_change(' + item[2] + ', ' + "'done'" + ')" class="btn btn-light">&#10003;' +
                          '</button></div></div></div>';
                $('#CardList').html(tmp + $('#CardList').html());
                tmp = '<div style="display: none" id="todo_' + item[2] + '" onclick="get_todo_data_ajax(' + item[2] + ');">' +
                      '<a href="#" class="list-group-item list-group-item-primary" data-toggle="modal" data-target="#Open-Todo">' +
                      '<button type="button" class="btn btn-primary" onclick="status_change(' + item[2] + ', ' + "'done'" + ')">' +
                      '&#10003;</button><h7 id="todo_title_' + item[2] + '">' + item[0] + '</h7><div class="priorities">' +
                      '<div class="priorities" id="list_priorities_' + item[2] + '"></div><div class="date">' +
                      '<small id="todo_date_' + item[2] + '">' + item[1] + '</small></div></div></a></div>';
                $('#ViewList').html(tmp + $('#ViewList').html());
                get_priorities(item[3], item[2]);
                $('#todo_' + response['id']).show(duration='slow');
                $('#todo_card_' + response['id']).show(duration='slow');
                $("#close_todo_btn").trigger("click");
            }
            else{
                alert(response['result']);
            }
        }
    });
};


function delete_todo_ajax()
{
    var should_delete = confirm('Вы уверены?');
    var id =  $('#todo_id').html()
    if (should_delete)
    {
        $.ajax({
            type: "POST",
            url: '/todo/delete',
            data: {"id": id},
            success: function(response)
            {
                if (response['result'] == "Success")
                {
                    $('#todo_' + id).hide("slow", complete=function(){$('#todo_' + id).remove()});
                    $('#todo_card_' + id).hide("slow", complete=function(){$('#todo_card_' + id).remove()});
                }
            }
        });
    }
};

function sort_todo_ajax(sort_type){
    var page = get_key("page");
    paginate(page, "in progress", true, sort_type);
};

function paginate(page, status, push_state=true, sort_type=false){
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
        url = "/todo?page=" + page + "&sort_type=" + sort_type;
    }
    else
    {
        url = "/todo?page=" + page;
    }
    if (push_state)
    {
        history.pushState(null,null, url);
    }
    $.ajax({
        type: "POST",
        url: url,
        data: status,
        success: function(response)
        {
            if (response['result'] == 100) {
                for (var i = 1; i <= $('#paginate_btn_holder a').length - 2; i++)
                {
                    $('#paginate_btn_' + i).removeAttr('disabled');
                }
                $('#paginate_btn_' + response['normal_page']).attr('disabled', 'disabled');
                if (response['buttons'][0]) {
                    $("#PrevPage_Progress").removeAttr('disabled');
                    $("#PrevPage_Progress").attr('onclick', 'paginate(' + (response['normal_page'] - 1) + ', "in progress")');
                } else {
                    $("#PrevPage_Progress").attr('disabled', 'disabled');
                    $('#PrevPage_Progress').removeAttr('onclick');
                }
                if (response['buttons'][1]) {
                    $("#NextPage_Progress").removeAttr('disabled');
                    $("#NextPage_Progress").attr('onclick', 'paginate(' + (response['normal_page'] + 1) + ', "in progress")');
                }  else {
                    $("#NextPage_Progress").attr('disabled', 'disabled');
                    $('#NextPage_Progress').removeAttr('onclick');
                }
                $("#ViewList").html('');
                $("#CardList").html('');
                for (var i = 0; i < response['todo_list'].length; i++) {
                    add_todo_to_list(response['todo_list'][i]);
                    add_todo_to_cards(response['todo_list'][i]);
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

onpopstate = function(event) {
    var page = get_key("page");
    var sort_type = get_key("sort_type");
    paginate(page, 'in progress', false, sort_type);
}