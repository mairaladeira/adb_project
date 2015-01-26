var connectionType = 'none';
function simpleButton(domId, callback, server) {
    var shouldUseServer = server || false;
    $("#" + domId).on("click", function(){
        if (shouldUseServer) {
            var request = new XMLHttpRequest();
            request.onload = function() {
                callback(request.responseText);
            };
            request.open("GET", "/" + domId, true);
            request.send();
        } else {
            callback.call();
        }
    });
}

function postButton(domIdButton, domIdsInput, callback) {
    $("#" + domIdButton).on("click", function(){
        var data = {
            url: $('#'+domIdsInput[0]).val(),
            user: $('#'+domIdsInput[1]).val(),
            pwd: $('#'+domIdsInput[2]).val(),
            dbName: $('#'+domIdsInput[3]).val(),
            schema: $('#'+domIdsInput[4]).val()
        };
        $.ajax({
            type: "POST",
            url: "/"+domIdButton,
            data: data,
            success: function(data){
                try {
                    data = JSON.parse(data);
                    $('.modal').removeClass('in');
                    displayTables(data);
                    connectionType = 'database';
                } catch(e) {
                    $('#db-connection-error').html(data)
                }
            }
        });
    });
}

function insertFDButton(domIdButton, data, callback){
    $("#" + domIdButton).on("click", function(){
        var table = $("#"+data[0]).html();
        var lhs = [];
        $.each($("#"+data[1]).find('li'), function(){
            lhs.push($(this).html());
        });
        var rhs = [];
        $.each($("#"+data[2]).find('li'), function(){
            rhs.push($(this).html());
        });
        var fd = {lhs: lhs, rhs: rhs};
        $.post("/"+domIdButton, {table: table, lhs: lhs.toString(), rhs: rhs.toString()}).done(function(data){
            if(data == "success"){
                $('.modal').removeClass('in');
                $('#attr-box').html('');
                $('#attr-lhs').html('');
                $('#attr-rhs').html('');
                var data_id = parseInt($('.fd-elem:last-child').data('id')) + 1;
                var fd_elem = createFdsElement(fd, table, data_id, false);
                $('#table-'+table).find('.fds-list').append(fd_elem);
                edit_button_unbind_click();
                edit_button_bind_click();
            }

        });
    });
}

function editFDButton(domIdButton, data, callback){
     $("#" + domIdButton).on("click", function(){

         var table = $("#"+data[0]).html();
         var lhs = [];
         $.each($("#"+data[1]).find('li'), function(){
            lhs.push($(this).html());
         });
         var rhs = [];
         $.each($("#"+data[2]).find('li'), function(){
            rhs.push($(this).html());
         });
         var id = $(this).data('id');
         var fd = {lhs: lhs, rhs: rhs};
         $.post("/"+domIdButton, {table: table, lhs: lhs.toString(), rhs: rhs.toString(), id: id}).done(function(data){
            if(data == "success"){
                $('.modal').removeClass('in');
                $('#attr-box-edit-fd').html('');
                $('#attr-lhs-edit-fd').html('');
                $('#attr-rhs-edit-fd').html('');
                var fd_elem = createFdsElement(fd, table, id, false);
                $('.fd-elem[data-id='+id+']').replaceWith(fd_elem);
                edit_button_unbind_click()
                edit_button_bind_click();
            }
         });
     });
}

function getMinimalCover(domIdButton, table, callback){
    $("#"+domIdButton).on("click", function(){
        table = $("#"+table).data('id');
        $('.nav>li>a').removeClass('selected');
        $("#"+domIdButton).addClass('selected');
        $.post("/"+domIdButton, {table:table}).done(function(data){
            data = JSON.parse(data);
            getFDsListElement(data, table);
        });
    });
}

var textfiles = {}
function uploadTextfileButton(domIdButton, domIdInput, callback) {
    if (domIdButton in textfiles) throw new Error("nop.. already done! {" + domIdButton + "}");

    $("#" + domIdInput).on("change", function(e){
        var reader = new FileReader();
        reader.onload = function(file){
            textfiles[domIdButton] = file.target.result;
        }
        reader.readAsText(e.target.files[0]);
    });

    $("#" + domIdButton).on("click", function(){
        if (domIdButton in textfiles) {
            $.post("/" + domIdButton, {data: textfiles[domIdButton]}).done(
            function( data ) {
                $('.modal').removeClass('in');
                data = JSON.parse(data);
                displayTables(data);
                connectionType = 'xml';
            });
        }
    });

}

function newHTMLElement(type, data){
    var e = document.createElement(type);
    if(data['text']){
        var e_text = document.createTextNode(data['text']);
        e.appendChild(e_text)
    }
    $.each(data, function(key, val){
        if(key != 'text'){
            e.setAttribute(key, val);
        }
    });
    return e;
}

function appendChildes(elem, childes){
    $.each(childes, function(key, val){
       elem.appendChild(val);
    });
    return elem;
}

function createTableElement(table_name, table_key){
    var t = newHTMLElement('li', {'id':'table-'+table_name, class:'table-elem', 'data-id': table_key});
    var tn_elem = newHTMLElement('div', {class:'table-name', text:table_name, 'data-id':table_name});
    var expand_arrow = newHTMLElement('span',{class:'glyphicon glyphicon-chevron-down'});
    tn_elem.appendChild(expand_arrow);
    t.appendChild(tn_elem);
    return t;

}

function createTableContentElements(table){
    var content = newHTMLElement('div', {class:'table-content'});
    var attr_list = newHTMLElement('ul', {class:'attr-list'});
    $.each(table['attributes'], function(k, attr){
        var a = createTableAttributeElement(attr);
        attr_list.appendChild(a);
    });
    content.appendChild(attr_list);
    var fds = newHTMLElement('ol', {class:'fds-list'});
    $.each(table['fds'], function(i, val){
        var fd = createFdsElement(val, table['name'], i, false);
        fds.appendChild(fd);
    });
    var fds_title_elem = newHTMLElement('div', {class:'fds-title'});
    var fds_elem = newHTMLElement('h6', {text:'Functional Dependencies:'});
    var fds_add = newHTMLElement('a', {
                        class:'glyphicon glyphicon-plus fds_add_icon',
                        id:'add-fd-'+table['name'],
                        'data-id': table['name'],
                        title: 'Add FDs',
                        role: 'button',
                        'data-toggle':'modal',
                        href:'#insertFD'
                    });
    fds_title_elem = appendChildes(fds_title_elem, [fds_elem, fds_add]);
    content = appendChildes(content, [fds_title_elem, fds]);
    return content;
}

function createTableAttributeElement(attr) {
    return newHTMLElement('li', {class: 'attr-elem', text:attr});
}

function createFdsElement(fds,table_name, key, remove_edit_link) {
    var fd = newHTMLElement('li', {class:'fd-elem', 'data-id': key});
    var fd_lhs = newHTMLElement('div', {class:'fds fds_lhs'});
    var fd_rhs = newHTMLElement('div', {class:'fds fds_rhs'});
    $.each(fds['lhs'], function(j,lhs){
        var l = newHTMLElement('span', {class:'fd lhs', text: lhs});
        fd_lhs.appendChild(l);
    });
    var gives = newHTMLElement('span', {class:'glyphicon glyphicon-arrow-right'});
    $.each(fds['rhs'], function(j,rhs){
        var r = newHTMLElement('span', {class:'fd rhs', text:rhs});
        fd_rhs.appendChild(r);
    });
    fd = appendChildes(fd, [fd_lhs, gives]);
    if(!remove_edit_link) {
        var fds_edit = newHTMLElement('a', {
                        class:'glyphicon glyphicon-edit fds_edit_icon',
                        title: 'Edit FDs',
                        'data-id': table_name,
                        role: 'button',
                        'data-toggle':'modal',
                        href:'#editFD'
        });
        fd.appendChild(fds_edit);
    }
    fd.appendChild(fd_rhs);
    return fd;
}

function displayTables(data) {
    var table_list = $('#tables-list');
    table_list.html('');
    var tables = document.createElement('ul');
    $.each(data,function(key, table){
        var table_name = table['name'];
        var t = createTableElement(table_name, key);
        var content = createTableContentElements(table);
        t.appendChild(content);
        table_list.append(t);
    });
    setTimeout(function(){
        $('.table-elem').find('.table-name').bind('click', function(e){
            var rightContent = $('#rightContent');
            rightContent.removeClass('hidden');
            $('#table-detail-name').html($(this).data('id')).attr('data-id', $(this).data('id'));
            if(connectionType == 'database')
                rightContent.find('#checkfds_link').removeClass('disabled');
            var c = $(this).parent().find('.table-content');
            var t_arrow = $(this).find('.table-name .glyphicon');
            if(c.hasClass('visible')) {
                c.removeClass('visible');
                t_arrow.removeClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down')
                c.fadeOut(250);
            } else {
                c.addClass('visible');
                t_arrow.removeClass('glyphicon-chevron-down').addClass('glyphicon-chevron-up')
                c.fadeIn(250);
            }
        });
        $('.fds_add_icon').bind('click', function(e){
            var table = $(this).data('id');
            $(".modal-title #add-fd-table-name").html( table );
            $.post("/requestFD", {table: table}).done(function(data){
                data = JSON.parse(data);
                create_addFd_attr_list(data);
            });
        });
        edit_button_bind_click();
    }, 1000);
}

function generate_fd_list_elem(parent) {
    var list_attr = []
    parent.find('.lhs').each(function(){
        list_attr.push($(this).html());
        var fd = newHTMLElement('li', {class:'attr-elem', text: $(this).html()});
        $('#attr-lhs-edit-fd').append(fd);
    })
    parent.find('.rhs').each(function(){
        list_attr.push($(this).html());
        var fd = newHTMLElement('li', {class:'attr-elem', text: $(this).html()});
        $('#attr-rhs-edit-fd').append(fd);
    })
    return list_attr;
}

function create_addFd_attr_list(attributes) {
    var attr_list = $('#attr-box')
    $.each(attributes, function(key, attr){
        var a = newHTMLElement('li', {class:'attr-elem', 'data-id': 'attr-'+key, text:attr});
        attr_list.append(a);
    })
    $(function() {
        $( "#attr-box, #attr-lhs, #attr-rhs" ).sortable({
          connectWith: ".sortable-box"
        }).disableSelection();
    });
}

function create_editFD_lists(data, list_of_attr) {
    $.each(data, function(key, val){
        if(list_of_attr.indexOf(val) == -1){
            var fd = newHTMLElement('li', {class:'attr-elem', text: val});
            $('#attr-box-edit-fd').append(fd);
        }
        $(function() {
            $( "#attr-box-edit-fd, #attr-lhs-edit-fd, #attr-rhs-edit-fd" ).sortable({
              connectWith: ".sortable-box"
            }).disableSelection();
        });
    });
}

function edit_button_bind_click(){
    $('.fds_edit_icon').bind('click', function(e){
        $('#attr-box-edit-fd').html('');
        $('#attr-lhs-edit-fd').html('');
        $('#attr-rhs-edit-fd').html('');
        var table = $(this).data('id');
        var parent = $(this).parent();
        var id = parent.data('id');
        $('#editFDButton').attr('data-id', id);
        $(".modal-title #edit-fd-table-name").html( table );
        var list_of_attr = generate_fd_list_elem(parent);
        $.post("/requestFD", {table: table}).done(function(data){
            data = JSON.parse(data);
            create_editFD_lists(data, list_of_attr);
        });
    });
}

function edit_button_unbind_click() {
    $('.fds_edit_icon').unbind('click');
}

function getFDsListElement(fds,table) {
    var fds_list = newHTMLElement('ul', {class:'fds-list'});
    $.each(fds, function(key,val){
        var fd = createFdsElement(val, table, key, true);
        fds_list.appendChild(fd);
    });
    $('#action-content').append(fds_list);
}