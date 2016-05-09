$( document ).ready(function() {
    $('#postBtn').click(function() {
        var str = $('#coordForm').serialize();
        $.post('send_search_coord',
            str,
            function(data){
                alert(str);
                return false;
            });
    });
});
