function updateFooter() {
  var footer = $('footer');
  footer.removeClass('fixed');
  if (footer.offset().top < $(document).height() - footer.height() - 20) {
    footer.addClass('fixed');
  }
}

$(document).ready(function() {
  setTimeout(updateFooter, 0); // ? Doesn't work without setTimeout
  $(window).resize(updateFooter);

  $('.dropdown').click(function () {
    $(this).toggleClass('open');
  });
});
