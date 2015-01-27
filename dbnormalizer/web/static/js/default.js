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
                    $('.modal').removeClass('in').fadeOut(250);
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
                $('.modal').removeClass('in').fadeOut(250);
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
         console.log(data);
         $.each($("#"+data[1]).find('li'), function(){
            lhs.push($(this).html());
         });
         var rhs = [];
         $.each($("#"+data[2]).find('li'), function(){
            rhs.push($(this).html());
         });
         var id = $(this).data('id');
         var fd = {lhs: lhs, rhs: rhs};
         console.log(fd);
         $.post("/"+domIdButton, {table: table, lhs: lhs.toString(), rhs: rhs.toString(), id: id}).done(function(data){
            if(data == "success"){
                $('.modal').removeClass('in').fadeOut(250);
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

function getMinimalCover(domIdButton, callback){
    $("#"+domIdButton).on("click", function(){
        $('#action-content').html('');
        var table = $("#table-detail-name").attr('data-id');
        $('.nav>li>a').removeClass('selected');
        $("#"+domIdButton).addClass('selected');
        $.post("/"+domIdButton, {table:table}).done(function(data){
            data = JSON.parse(data);
            getFDsListElement(data, table);
        });
    });
}

function getAttributeClosure(domIdButton, callback){
    $("#"+domIdButton).on("click", function(){
        $('#action-content').html('');
        var table = $("#table-detail-name").attr('data-id');
        $('.nav>li>a').removeClass('selected');
        $("#"+domIdButton).addClass('selected');
        $.post("/"+domIdButton, {table:table}).done(function(data){
            data = JSON.parse(data);
            getAttributeSelector(data, table);
        });
    });
}

function getCandidateKeys(domIdButton, callback){
    $("#"+domIdButton).on("click", function(){
        $('#action-content').html('');
        var table = $("#table-detail-name").attr('data-id');
        $('.nav>li>a').removeClass('selected');
        $("#"+domIdButton).addClass('selected');
        $.post("/"+domIdButton, {table:table}).done(function(data){
            data = JSON.parse(data);
            getCandidateKeysHTML(data);
        });
    });
}

function detectNormalForm(domIdButton, callback){
    $("#"+domIdButton).on("click", function(){
        $('#action-content').html('');
        var table = $("#table-detail-name").attr('data-id');
        $('.nav>li>a').removeClass('selected');
        $("#"+domIdButton).addClass('selected');
        $.post("/"+domIdButton, {table:table}).done(function(data){
            var element = newHTMLElement('h6', {class:'nf', text:'The table '+table+' is on: '});
            var nf = newHTMLElement('b', {text: data});
            element.appendChild(nf);
            $('#action-content').append(element);
        });
    });
}

function checkFDs(domIdButton, callback){
    $("#"+domIdButton).on("click", function() {
        if(!$(this).parent().hasClass('disabled')){
            $('#action-content').html('');
            var table = $("#table-detail-name").attr('data-id');
            $('.nav>li>a').removeClass('selected');
            $("#" + domIdButton).addClass('selected');
            $.post("/"+domIdButton, {table:table}).done(function(data){
                data = JSON.parse(data);
                get_checkFDs_HTML(data, table)
            });
        }
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
                $('.modal').removeClass('in').fadeOut(250);
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
    $('#rightContent').addClass('hidden');
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
            $('#action-content').html('');
            $('#table-menu li a').removeClass('selected');
            var c = $(this).parent().find('.table-content');
            var t_arrow = $(this).find('.table-name .glyphicon');
            if(c.hasClass('visible')) {
                rightContent.addClass('hidden');
                c.removeClass('visible');
                t_arrow.removeClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down');
                c.fadeOut(250);
            } else {
                rightContent.removeClass('hidden');
                $('#table-detail-name').html($(this).data('id')).attr('data-id', $(this).data('id'));
                if(connectionType == 'database')
                    rightContent.find('#checkfds_link').removeClass('disabled');
                $('.table-content').removeClass('visible').css('display', 'none');
                $('.table-name .glyphicon').removeClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down');
                c.addClass('visible');
                t_arrow.removeClass('glyphicon-chevron-down').addClass('glyphicon-chevron-up');
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
    var attr_list = $('#attr-box');
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

function getAttributeSelector(attributes, table){
    var selector = newHTMLElement('select', {class:'form-control', id:"attr-selector"});
    var option = newHTMLElement('option', {value:'none', text:'Select Attribute'});
    selector.appendChild(option);
    var attr_list_elem = newHTMLElement('div', {class:'elem-list'});
    var attr_list = newHTMLElement('ul', {class:'sortable-box', id:'av-attr-box'});
    var attr_list_title = newHTMLElement('h6', {text:'Available attributes'});
    $.each(attributes, function(key,attr){
        var a = newHTMLElement('li', {class:'attr-elem', 'data-id': 'attr-'+key, text:attr});
        attr_list.appendChild(a);
    });
    attr_list_elem = appendChildes(attr_list_elem, [attr_list_title, attr_list]);

    var selected_attr_list_elem = newHTMLElement('div', {class:'elem-list last'});
    var selected_attr_list_title = newHTMLElement('h6', {text:'Selected attributes'});
    var selected_attr_list = newHTMLElement('ul', {class:'sortable-box', id:'sl-attr-box'});
    var confirmation_button = newHTMLElement('button', {type:'button', class:'btn btn-primary', id:'attr-selector',text:'Calculate closure'})
    selected_attr_list_elem = appendChildes(selected_attr_list_elem, [selected_attr_list_title, selected_attr_list]);
    $('#action-content').append(attr_list_elem).append(selected_attr_list_elem).append(confirmation_button);
    $(function() {
        $( "#av-attr-box, #sl-attr-box" ).sortable({
          connectWith: ".sortable-box"
        }).disableSelection();
    });
    setTimeout(function(){
        $("#attr-selector").bind("click",function(){
            var attrs = [];
            $('#attr-list-wrap').remove();
            $.each($("#sl-attr-box").find('li'), function(){
                attrs.push($(this).html());
            });
            $.post("/getAttributeClosure", {table: table, attributes: attrs.toString()}).done(function(data){
                data = JSON.parse(data);
                var wrap = newHTMLElement('div', {id:'attr-list-wrap'});
                var title = newHTMLElement('h6', {text:'Attribute Closure for attributes: '+attrs.toString()});
                var attr_l = newHTMLElement('ul', {class:'attr-list'});
                $.each(data, function(key, val){
                    var attr = newHTMLElement('li', {class:'attr-elem', text:val, 'data-id':key});
                    attr_l.appendChild(attr);
                });
                wrap = appendChildes(wrap, [title, attr_l]);
                $('#action-content').append(wrap);
            })

        });
    }, 1000);
}

function getCandidateKeysHTML(keys) {
    var title = newHTMLElement('h6', {text:'Candidate keys: '});
    var list = newHTMLElement('ul', {class:'candidate-keys-list'});
    $.each(keys, function(key, attributes){
        var text = '';
        $.each(attributes, function(k, attr){
            if (k == 0)
                text += attr;
            else
                text += ', '+attr;
        });
        var key_elem = newHTMLElement('li', {class:'key-elem', 'data-id':'key-'+key, text: text});
        list.appendChild(key_elem)
    });
    $('#action-content').append(title).append(list);
}


function get_checkFDs_HTML(checked_fds, table) {
    var holdTitle = newHTMLElement('h6', {text: 'Functional dependencies:'})
    var fds_list = newHTMLElement('ul', {class:'fds-list', id:'check-fd-list'})
    $.each(checked_fds['hold'], function(key, val){
        var fd = createFdsElement(val, table, key, true);
        fd.className = fd.className + ' satisfied';
        var icon = newHTMLElement('span', {class:'glyphicon glyphicon-ok'});
        fd.appendChild(icon);
        fds_list.appendChild(fd);
    });
    $.each(checked_fds['not_hold'], function(key, val){
        var fd = createFdsElement(val, table, key, true);
        var icon = newHTMLElement('span', {class:'glyphicon glyphicon-remove'});
        fd.appendChild(icon);
        fd.className = fd.className + ' not-satisfied';
        fds_list.appendChild(fd);
    });
    $('#action-content').append(holdTitle).append(fds_list);
}