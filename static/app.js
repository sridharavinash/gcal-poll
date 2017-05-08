$(document).ready(function(){
  $("input[name ^= 'checkbox_']").click(function() {
    $(this).toggle(this.checked);
    var split = $(this).attr('name').split('_');
    var player_id = split[1];
    var event_name = split[2];
    $.ajax({
      method: "POST",
      url: "/_update_poll",
      data: { event_name: event_name, player_id: player_id }
    })
    .done(function( msg ) {
    });
  });
});
