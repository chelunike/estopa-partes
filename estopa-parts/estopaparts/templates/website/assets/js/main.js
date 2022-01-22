
$('[id^="quantity_"]').change(function (e){
    var id = $(e.target).attr('id').replace("quantity_", '');
    $('#cantidad_'+id).val($(this).val()); // <-- reverse your selectors here
    $('#producto_id_'+id).val($(this).val()); // <-- reverse your selectors here
});
$('[id^="cantidad_"]').change(function (e){
    var id = $(e.target).attr('id').replace("cantidad_", '');
    $('#quantity_'+id).val($(this).val()); // <-- reverse your selectors here
    $('#producto_id_'+id).val($(this).val()); // <-- reverse your selectors here
});
$('[id^="producto_id_"]').change(function (e){
    var id = $(e.target).attr('id').replace("cantidad_", '');
    $('#quantity_'+id).val($(this).val()); // <-- reverse your selectors here
    $('#cantidad_'+id).val($(this).val()); // <-- reverse your selectors here
});


