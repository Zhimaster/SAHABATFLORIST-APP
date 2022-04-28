$(document).ready(function() {
    $(".alert").fadeTo(3500, 0).slideUp(500, function(){
        $(this).remove(); 
    });

    $('#tablemaster').DataTable();
})