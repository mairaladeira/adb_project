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
                callback(data);
            });
        }
    });

}