$(document).ready(function () {
  $('form').submit(function () {
    $('form').hide();
    $('.loader').fadeIn();
    var form = this;
    setTimeout(function () {
      form.submit();
    }, 500);
    return false;
  });
});
