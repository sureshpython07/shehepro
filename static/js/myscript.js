$(document).ready(function () {
    $('.dropdown').hover(function () {
        $(this).find('.dropdown-menu')
           .stop(true, true).delay(100).fadeIn(200);
    }, function () {
        $(this).find('.dropdown-menu')
          .stop(true, true).delay(100).fadeOut(200);
    });
});
