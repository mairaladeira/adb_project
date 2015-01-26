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
                var fd_elem = createFdsElement(fd, table);
                $('#table-'+table).find('.fds-list').append(fd_elem);
            }

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
    var tn_elem = newHTMLElement('div', {class:'table-name', text:table_name});
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
        var fd = createFdsElement(val, table['name']);
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

function createFdsElement(fds,table_name) {
    var fd = newHTMLElement('li', {class:'fd-elem'});
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
    var fds_edit = newHTMLElement('a', {
                        class:'glyphicon glyphicon-edit fds_edit_icon',
                        id:'edit-fd-'+table_name,
                        title: 'Edit FDs',
                        'data-id': table_name,
                        role: 'button',
                        'data-toggle':'modal',
                        href:'#editFD'
                    });
    fd = appendChildes(fd, [fd_lhs, gives,fds_edit, fd_rhs]);
    return fd;
}

function displayTables(data) {
    var tables = document.createElement('ul');
    $.each(data,function(key, table){
        var table_name = table['name'];
        var t = createTableElement(table_name, key);
        var content = createTableContentElements(table);
        t.appendChild(content);
        $('#tables-list').append(t);
    });
    setTimeout(function(){
        $('.table-elem').find('.table-name').bind('click', function(e){
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
            $.post("/requestAddFD", {table: table}).done(function(data){
                data = JSON.parse(data);
                create_addFd_attr_list(data);
            });
        });
    }, 1000);
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