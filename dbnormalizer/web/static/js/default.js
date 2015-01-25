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
                console.log(data);
                displayTables(data);
                //callback(data);
            });
        }
    });

}

function createTableElement(table_name, table_key){
    var t = document.createElement('li');
    t.setAttribute('id', 'table-'+table_key);
    t.setAttribute('class', 'table-elem');
    var tn_elem = document.createElement('div');
    tn_elem.setAttribute('class', 'table-name');
    var tn = document.createTextNode(table_name)
    var expand_arrow = document.createElement('span');
    expand_arrow.setAttribute('class', 'glyphicon glyphicon-chevron-down');
    tn_elem.appendChild(tn)
    tn_elem.appendChild(expand_arrow)
    t.appendChild(tn_elem);
    return t;

}

function createTableContentElements(table){
    var content = document.createElement('div');
    content.setAttribute('class', 'table-content');
    var attr_list = document.createElement('ul');
    attr_list.setAttribute('class', 'attr-list');
    $.each(table['attributes'], function(k, attr){
        var a = createTableAttributeElement(attr);
        attr_list.appendChild(a);
    });
    content.appendChild(attr_list);
    var fds = document.createElement('ol');
    fds.setAttribute('class', 'fds-list');
    $.each(table['fds'], function(i, val){
        var fd = createFdsElement(val);
        fds.appendChild(fd);
    });
    var fds_elem = document.createElement('h6');
    var fdst = document.createTextNode('Functional dependencies:');
    fds_elem.appendChild(fdst);
    content.appendChild(fds_elem);
    content.appendChild(fds);
    return content;
}

function createTableAttributeElement(attr) {
    var a = document.createElement('li');
    a.setAttribute('class', 'attr-elem');
    var attr_name = document.createTextNode(attr);
    a.appendChild(attr_name);
    return a;
}

function createFdsElement(fds) {
    var fd = document.createElement('li');
    fd.setAttribute('class', 'fd-elem');
    var fd_lhs = document.createElement('div');
    fd_lhs.setAttribute('class', 'fds fds_lhs');
    var fd_rhs = document.createElement('div');
    fd_rhs.setAttribute('class', 'fds fds_rhs');
    $.each(fds['lhs'], function(j,lhs){
        var l = document.createElement('span');
        l.setAttribute('class', 'fd lhs');
        var l_name = document.createTextNode(lhs);
        l.appendChild(l_name);
        fd_lhs.appendChild(l);
    });
    var gives = document.createElement('span');
    gives.setAttribute('class', 'glyphicon glyphicon-arrow-right');
    $.each(fds['rhs'], function(j,rhs){
        var r = document.createElement('span');
        r.setAttribute('class', 'fd rhs');
        var r_name = document.createTextNode(rhs);
        r.appendChild(r_name);
        fd_rhs.appendChild(r);
    });
    fd.appendChild(fd_lhs);
    fd.appendChild(gives);
    fd.appendChild(fd_rhs);
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
        $('.table-elem').bind('click', function(e){
            var c = $(this).find('.table-content');
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
    }, 1000);
}