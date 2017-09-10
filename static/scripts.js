$(function(){
  $('form').find('input').keyup(function(e){
    var changed = e.target.id;

    if ( $('#' + changed).val() === "" ) {
      $('label[for="' + changed + '"]').fadeOut("fast");
    } else {
      $('label[for="' + changed + '"]').fadeIn("fast");
    }
  });
});