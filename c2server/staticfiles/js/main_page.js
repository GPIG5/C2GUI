function SubForm (){
    $.ajax({
        url:'/send_search_coord/',
        type:'post',
        data:$('#coordForm').serialize(),
        success:function(){
            alert("submitte");
        }
    });
}

$( document ).ready(function() {
    SubForm();
});
