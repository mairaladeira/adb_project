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
            pwd: $('#'+domIdsInput[2]).val()
        };
        console.log(callback)
        $.ajax({
            type: "POST",
            url: "/"+domIdButton,
            data: data,
            success: function(data){
                if(data == "success") {
                    callback(data);
                    $('.modal').removeClass('in');
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

function displayTables(data) {
    var tables = document.createElement('ul');
    $.each(data,function(key, table){
        console.log(table);
        var t = document.createElement('li');
        var table_name = table['name'];
        console.log(table_name);
        t.setAttribute('id', 'table-'+key);
        t.setAttribute('class', 'table-elem');
        var tn = document.createTextNode(table_name)
        t.appendChild(tn);
        var attr_list = document.createElement('ul');
        attr_list.setAttribute('class', 'attr-list');
        $.each(table['attributes'], function(k, attr){
            var a = document.createElement('li');
            a.setAttribute('class', 'attr-elem');
            var attr_name = document.createTextNode(attr);
            a.appendChild(attr_name);
            attr_list.appendChild(a);
        });
        var at_elem = document.createElement('h6');
        var at = document.createTextNode('Attributes:');
        at_elem.appendChild(at);
        t.appendChild(at_elem);
        t.appendChild(attr_list);
        var fds = document.createElement('ul');
        fds.setAttribute('class', 'fds-list');
        $.each(table['fds'], function(i, val){
            var fd = document.createElement('li');
            fd.setAttribute('class', 'fd-elem');
            var lhst_elem = document.createElement('h6');
            var lhst = document.createTextNode('LHS:');
            lhst_elem.appendChild(lhst);
            fd.appendChild(lhst_elem);
            $.each(val['lhs'], function(j,lhs){
                var l = document.createElement('div');
                l.setAttribute('class', 'fds lhs');
                var l_name = document.createTextNode(lhs);
                l.appendChild(l_name);
                fd.appendChild(l);
            });
            var rhst_elem = document.createElement('h6');
            var rhst = document.createTextNode('RHS:');
            rhst_elem.appendChild(rhst);
            fd.appendChild(rhst_elem);
            $.each(val['rhs'], function(j,rhs){
                var r = document.createElement('div');
                r.setAttribute('class', 'fds rhs');
                var r_name = document.createTextNode(rhs);
                r.appendChild(r_name);
                fd.appendChild(r);
            });
            fds.appendChild(fd);
        });
        var fds_elem = document.createElement('h6');
        var fdst = document.createTextNode('Functional dependencies:');
        fds_elem.appendChild(fdst);
        t.appendChild(fds_elem);
        t.appendChild(fds);
        $('#tables-list').append(t);
    });

}