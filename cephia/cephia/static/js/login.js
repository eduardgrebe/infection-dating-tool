$(document).ready(function() {
    $('.homeBtn').on('click', function() {
        $('.nonBlur').toggleClass('blur');
        $('.blur_login').slideToggle(500);
    });
});


