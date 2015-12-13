function updateFooter() {
  var footer = $('footer');
  footer.removeClass('fixed');
  if (footer.offset().top < $(document).height() - footer.height() - 20) {
    footer.addClass('fixed');
  }
}

$(document).ready(function() {
  // setTimeout(updateFooter, 0); // ? Doesn't work without setTimeout...?
  updateFooter(); // ? Works now? Who knows.
  $(window).resize(updateFooter);

  $('.dropdown').click(function () {
    $(this).toggleClass('open');
  });

  setTimeout(function () {
    $('.messages p').fadeOut();
  }, 2000);
});
