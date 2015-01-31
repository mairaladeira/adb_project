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

function inSchema(table_name, schemaTables) {
    $.each(schemaTables, function(key, val){
        if (val['name'] == table_name) return true;
    });
    return false;
}

function inFds(fd, fds) {

    var equal = false;
    $.each(fds, function(key,val){
        var equal_lhs = val.lhs.join() == fd.lhs.join();
        var equal_rhs = val.rhs.join() == fd.rhs.join();
        if(equal_lhs && equal_rhs) {
            equal =  true;
            return false;

        }
    });

    return equal;
}

function insertDataManually(domIdButton, callback) {
    var data = {
        Schema:'',
        Tables: []
    };
    var table = {}
    var attrs = []
    var fds = []
    $("#"+domIdButton).on("click", function(){
        var box_content = $('#insertManually');
        var step = $(this).attr('data-id');
        switch (step) {
            case 'step1':
                var schema = $('#insertmanual-schema-name').val();
                if(schema != '') {
                    $('#insertmanual-warning').html('');
                    data['Schema'] = schema;
                    box_content.find('.step1').addClass('hidden');
                    box_content.find('.step2').removeClass('hidden');
                    $(this).attr('data-id', 'step2');
                } else {
                    $('#insertmanual-warning').html('Our schema must have a name!');
                }
                break;
            case 'step2':
                var table_name = $('#insertmanual-table-name').val();
                if(table_name != '' && !inSchema(table_name, data['Tables'])) {
                    $('#insertmanual-warning').html('');
                    table = {
                        name: table_name
                    };
                    var attr_list = $('#insetmanual-attr-box');
                    $('.insertmanual-attr-name').each(function(key) {
                        var val= $(this).val();
                        if($.inArray(val, attrs) === -1) {
                            if (val != ''){
                                attrs.push(val);
                                var a = newHTMLElement('li', {class: 'attr-elem', 'data-id': 'attr-' + key, text: val});
                                attr_list.append(a);
                            }
                        }
                        else
                            $('#insertmanual-warning').html('Some attributes were removed for being repeated!');
                    });
                    table['attributes'] = attrs;
                    fds = [];
                    $('#added-fds').html('');
                    box_content.find('.step2').addClass('hidden');
                    box_content.find('.step3').removeClass('hidden');
                    $(this).attr('data-id', 'step3');
                } else {
                    if (table_name == ''){
                        $('#insertmanual-warning').html('Our table must have a name!');
                    } else {
                        $('#insertmanual-warning').html('Table already on the schema, please change table name!');
                    }
                }

                break;
            case 'step3':
                if(!table['fds']) {
                    table['fds'] = fds;
                    data['Tables'].push(table);
                };
                $.post("/"+domIdButton, {data: JSON.stringify(data)}).done(function(schema) {
                    schema = JSON.parse(schema);
                    $('.modal').removeClass('in').fadeOut(250);
                    displayTables(schema);
                    connectionType = 'manual';
                });
                break;
        }
    });
    $('#add-attr').on("click", function(){
        //<input type="text" class="form-control insertmanual-attr-name" name="insertmanual-attr-name" data-id="0" placeholder="Attribute Name" aria-describedby="basic-addon1">

        var new_attr = newHTMLElement('input', {type:'text', class:'form-control insertmanual-attr-name', placeholder:'Attribute Name', 'aria-describedby':'basic-addon1'});
        $('#attrs-inputs-wrap').append(new_attr);
    });

    $('#addNewTable').on("click", function(){
        var box_content = $('#insertManually');
        table['fds'] = fds;
        data['Tables'].push(table);
        table = {};
        attrs = [];
        fds = [];
        $('#insertmanual-warning').html('');
        $('#insertmanual-table-name').val('');
        var new_attr = newHTMLElement('input', {type:'text', class:'form-control insertmanual-attr-name', placeholder:'Attribute Name', 'aria-describedby':'basic-addon1'});
        $('#attrs-inputs-wrap').html(new_attr);
        box_content.find('.step2').removeClass('hidden');
        box_content.find('.step3').addClass('hidden');
        $("#"+domIdButton).attr('data-id', 'step2');
        $('#added-fds').html('');
        $('#insetmanual-attr-box').html('');
    });

    $('#addFd').on("click", function(){
        var lhs_div = $("#insetmanual-lhs");
        var rhs_div = $("#insetmanua-rhs");
        var attr_list = $('#insetmanual-attr-box');
        var warning = $('#insertmanual-warning');
        attr_list.html('');
        $.each(attrs, function(key, attr){
           var a = newHTMLElement('li', {class:'attr-elem', 'data-id': 'attr-'+key, text:attr});
           attr_list.append(a);
        })
        var lhs = [];
        lhs_div.find('li').each(function(){
           lhs.push($(this).html());
        });
        var rhs = [];
        rhs_div.find('li').each( function(){
           rhs.push($(this).html());
        });
        if(lhs.length > 0 && rhs.length > 0){
            warning.html('');
            var fd = {lhs: lhs, rhs: rhs};
            if(!inFds(fd, fds)){
                fds.push(fd);
                var fd_html = newHTMLElement('div', {text:fd.lhs.join()+'->'+fd.rhs.join()});
                $('#added-fds').append(fd_html);
            }
            else {
                warning.html('The repeated fd was not added!');
            }
        } else {
            warning.html('Our fds must have lhs and rhs!');
        }

        lhs_div.html(' ');
        rhs_div.html(' ');
    });

    $(function() {
        $( "#insetmanual-attr-box, #insetmanual-lhs, #insetmanua-rhs" ).sortable({
          connectWith: ".sortable-box"
        }).disableSelection();
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
                $('#normalization-content').addClass('hidden');
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
                $('.modal').removeClass('in').fadeOut(250);
                $('#attr-box-edit-fd').html('');
                $('#attr-lhs-edit-fd').html('');
                $('#attr-rhs-edit-fd').html('');
                var fd_elem = createFdsElement(fd, table, id, false);
                $('.fd-elem[data-id='+id+']').replaceWith(fd_elem);
                edit_button_unbind_click()
                edit_button_bind_click();
                $('#normalization-content').addClass('hidden');
            }
         });
     });
}

function deleteFDButton(domIdButton, domIdTable, callback){
    $("#"+domIdButton).bind("click", function(){
        var table = $("#"+domIdTable).html();
        var id = $(this).attr('data-id');
        $.post("/"+domIdButton, {table: table, id: id}).done(function(data){
            $('.modal').removeClass('in').fadeOut(250);
            if(data == "success") {
                $('#table-'+table).find('.fd-elem').each(function(){
                    var data_id = $(this).data('id');
                    if(data_id == id)
                        $(this).remove()
                    else if(data_id > id) {
                        var new_data_id = data_id - 1;
                        $(this).attr('data-id', new_data_id);
                    }
                });
                $('#normalization-content').addClass('hidden');
            }
        });
    });
}

function getMinimalCover(domIdButton, callback){
    $("#"+domIdButton).on("click", function(){
        $('#action-content').html('');
        $('#normalization-content').addClass('hidden');
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
        $('#normalization-content').addClass('hidden');
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
        $('#normalization-content').addClass('hidden');
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
        $('#normalization-content').addClass('hidden');
        var table = $("#table-detail-name").attr('data-id');
        $('.nav>li>a').removeClass('selected');
        $("#"+domIdButton).addClass('selected');
        $.post("/"+domIdButton, {table:table}).done(function(data){
            data = JSON.parse(data);
            var element = newHTMLElement('h5', {class:'nf', text:'The table '+table+' is on: '});
            var nf = newHTMLElement('b', {text: data['nf']});
            element.appendChild(nf);
            var violation_title = newHTMLElement('h6', {text: 'Functional dependencies that violate the normal form:'})
            var fds_list = newHTMLElement('ul', {class:'fds-list', id:'check-fd-list'})
            $.each(data['violated_fds'], function(key, val){
                var fd = createFdsElement(val, table, key, true);
                fds_list.appendChild(fd);
            });
            $('#action-content').append(element).append(violation_title).append(fds_list);
        });
    });
}

function checkFDs(domIdButton, callback){
    $("#"+domIdButton).on("click", function() {
        if(!$(this).parent().hasClass('disabled')){
            $('#action-content').html('');
            $('#normalization-content').addClass('hidden');
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

function normalizeTable(domIdButton, callback){
    $("#"+domIdButton).on("click", function() {
        if (!$(this).hasClass('disabled')) {
            $('#action-content').html('');
            $('#normalization-content').addClass('hidden');
            var table = $("#table-detail-name").attr('data-id');
            $('.nav>li>a').removeClass('selected');
            $.post("/"+domIdButton, {table:table}).done(function(data){
                if (data == 'false') {
                    var message = newHTMLElement('h6', {text: 'No normalization needed, the schema is already on BCNF', id:"no-normalization"});
                    $('#normalization-content').removeClass('hidden').append(message);
                    $('#getBCNF').addClass('hidden');
                    return;
                } else {
                    $('#no-normalization').remove();
                }
                data = JSON.parse(data);
                console.log(data);
                getNormalizationHTML(data);
            });
        }
    });
}

function downloadXML(domIdButton, callback){
    $("#"+domIdButton).on("click", function() {
        if(!$("#"+domIdButton).hasClass('disabled')){
            window.open("/"+domIdButton);
        }
    });
}

var textfiles = {};
function uploadTextfileButton(domIdButton, domIdInput, callback) {
    if (domIdButton in textfiles) throw new Error("nop.. already done! {" + domIdButton + "}");

    $("#" + domIdInput).on("change", function(e){
        var reader = new FileReader();
        reader.onload = function(file){
            textfiles[domIdButton] = file.target.result;
        };
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

function createFdsElement(fds,table_name, key, remove_edition_link) {
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
    if(!remove_edition_link) {
        var fds_edit = newHTMLElement('a', {
                        class:'glyphicon glyphicon-edit fds_edit_icon',
                        title: 'Edit FD',
                        'data-id': table_name,
                        role: 'button',
                        'data-toggle':'modal',
                        href:'#editFD'
        });
        fd.appendChild(fds_edit);
        var fds_remove = newHTMLElement('a', {
                        class:'glyphicon glyphicon-remove fds_remove_icon',
                        title: 'Remove FD',
                        'data-id': table_name,
                        role: 'button',
                        'data-toggle':'modal',
                        href:'#deleteFD'
        });
        fd.appendChild(fds_remove);
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
    $('#XMLDownload').removeClass('disabled');
    setTimeout(function(){
        $('.table-elem').find('.table-name').bind('click', function(e){
            var rightContent = $('#rightContent');
            $('#action-content').html('');
            $('#normalization-content').addClass('hidden');
            $('#table-menu li a').removeClass('selected');
            var c = $(this).parent().find('.table-content');
            var t_arrow = $(this).find('.table-name .glyphicon');
            if(c.hasClass('visible')) {
                rightContent.addClass('hidden');
                c.removeClass('visible');
                $('#normalizer').addClass('disabled');
                t_arrow.removeClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down');
                c.fadeOut(250);
            } else {
                rightContent.removeClass('hidden');
                $('#table-detail-name').html($(this).data('id')).attr('data-id', $(this).data('id'));
                if(connectionType == 'database')
                    rightContent.find('#checkfds_link').removeClass('disabled');
                $('#normalizer').removeClass('disabled');
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
    $('.fds_remove_icon').bind('click', function(e){
        var table = $(this).data('id');
        var parent = $(this).parent();
        var id = parent.data('id');
        $('#removeFDButton').attr('data-id', id);
        $(".modal-title #remove-fd-table-name").html( table );
        var delete_fd_confirm = $('#delete-fd-confirm');
        delete_fd_confirm.find('.fds_lhs').html(parent.find('.fds_lhs').html());
        delete_fd_confirm.find('.fds_rhs').html(parent.find('.fds_rhs').html());
    });
}

function edit_button_unbind_click() {
    $('.fds_edit_icon').unbind('click');
    $('.fds_remove_icon').unbind('click');
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

function getNormalizationHTML(data){
    var bcnf_button = $('#getBCNF');
    var sql_download_button = $('#getSQL');
    $('#action-content').html('');
    $('#normalization-content').removeClass('hidden');
    var title = 'BCNF';
    $('#bcnfWarning').html('');

    if(data['bcnf']){
        title = '3NF';
        bcnf_button.removeClass('hidden');
    } else {
        bcnf_button.addClass('hidden');
    }
    if (connectionType == 'database'){
        sql_download_button.removeClass('hidden');
    } else {
        sql_download_button.addClass('hidden');
    }
    $('#normalization-tables').find('ul.tables').html('');
    $('#normalization-nf').html(title);
    $.each(data['3nf'], function(key, val){
        var table = getNormalizedTableHTML(val);
        $('#normalization-tables').find('ul.tables').append(table);
    });
    bcnf_button.unbind('click');
    sql_download_button.unbind('click');
    bcnf_button.bind('click', function(){
        var tables = $('#normalization-tables').find('ul.tables');
        tables.html('');
        var warning = newHTMLElement('h6', {class:'error-message clear', text:'It is important to remember that some FDs are dropped with the BCNF decomposition of this table!'});
        $('#bcnfWarning').html('').append(warning);
        title = 'BCNF';
        console.log(data);
        $('#normalization-nf').html(title);
        $.each(data['bcnf'], function(key, val){
            var table = getNormalizedTableHTML(val);
            tables.append(table);
        });
    });

    sql_download_button.on('click', function(){
        var table = $('#table-detail-name').attr('data-id');
        window.open("/downloadSQL?table="+table+"&type="+title+"");

    });
}

function getNormalizedTableHTML(table_data) {
    var table_html = newHTMLElement('li', {class:'normalized-table', id:'table-'+table_data['name']});
    var tableTitle = newHTMLElement('h5', {class:'normalized-table-title', text: table_data['name']});
    var attr_html = getNormalizedTableAttrHTML(table_data['attributes']);
    var fds_html = getNormalizedTableFdsHTML(table_data['fds'], table_data['name']);
    var ck_html = getNormalizedTableCKHTML(table_data['candidate_keys']);
    var fk_html = getNormalizedTableFKHTML(table_data['f_key']);
    table_html = appendChildes(table_html, [tableTitle, attr_html, fds_html, ck_html, fk_html]);
    return table_html;
}

function getNormalizedTableAttrHTML(attributes) {
    var attrs = newHTMLElement('ul', {class:'normalized-table-attributes'});
    $.each(attributes, function(key, val){
        var attr = newHTMLElement('li', {class:'attr', text: val});
        attrs.appendChild(attr);
    });
    return attrs;
}

function getNormalizedTableFdsHTML(fds, table) {
    var fdsWrap = newHTMLElement('div', {class:'normalized-table-fds'});
    if(fds.length > 0) {
        var title = newHTMLElement('h6', {text:'Functional Dependencies:'});
        var fds_list = newHTMLElement('ul', {class:'normalized-table-fds-list'});
        $.each(fds, function(key, val){
            var fd = createFdsElement(val, table, key, true);
            fds_list.appendChild(fd);
        });
        fdsWrap = appendChildes(fdsWrap, [title, fds_list]);
    }
    return fdsWrap;
}

function getNormalizedTableCKHTML(cks) {
    var ckWrap = newHTMLElement('div', {class:'normalized-table-ck'});
    var title = newHTMLElement('h6', {text:'Candidate keys:'});
    var ck_list = newHTMLElement('ul', {class:'normalized-table-ck-list'});
    $.each(cks, function(key, attributes){
        var text = '';
        $.each(attributes, function(k, attr){
            if (k == 0)
                text += attr;
            else
                text += ', '+attr;
        });
        var key_elem = newHTMLElement('li', {class:'key-elem', 'data-id':'key-'+key, text: text});
        ck_list.appendChild(key_elem);
    })
    ckWrap = appendChildes(ckWrap, [title, ck_list]);
    return ckWrap
}

function getNormalizedTableFKHTML(f_keys) {
    var fkWrap = newHTMLElement('div', {class:'normalized-table-fk'});
    if(f_keys.length > 0) {
        var title = newHTMLElement('h6', {text:'Foreign keys:'});
        var fk_list = newHTMLElement('table', {class:'normalized-table-fk-list'});
        var fk_titles = newHTMLElement('tr', {class:'fk-elem title'});
        var fk_titles_attr = newHTMLElement('td', {class:'fk-attr', text: 'Attribute'});
        var fk_titles_referenced_table = newHTMLElement('td', {class:'fk-rt', text:'Referenced Table'});
        var fk_titles_referenced_attr = newHTMLElement('td', {class:'fk-rattr', text:'Referenced Attribute'});
        fk_titles = appendChildes(fk_titles, [fk_titles_attr,fk_titles_referenced_table,fk_titles_referenced_attr]);
        fk_list.appendChild(fk_titles);
        $.each(f_keys, function(key, val){
            var fk_elem = newHTMLElement('tr', {class:'fk-elem'});
            var attr_text = '';
            $.each(val['attr'], function(k, v){
                if (k == 0)
                    attr_text += v;
                else
                    attr_text += ', '+v;
            });
            var attr = newHTMLElement('td', {class:'fk-attr', text: attr_text});
            var referenced_table = newHTMLElement('td', {class:'fk-rt', text:val['referenced_table']});
            var referenced_attr_text = '';
            $.each(val['referenced_attribute'], function(k, v){
                if (k == 0)
                    referenced_attr_text += v;
                else
                    referenced_attr_text += ', '+v;
            });
            var referenced_attr = newHTMLElement('td', {class:'fk-rattr', text: referenced_attr_text});
            fk_elem = appendChildes(fk_elem, [attr, referenced_table, referenced_attr]);
            fk_list.appendChild(fk_elem);
        });
        fkWrap = appendChildes(fkWrap, [title, fk_list]);
    }
    return fkWrap;
}