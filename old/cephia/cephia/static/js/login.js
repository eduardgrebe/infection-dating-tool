$(document).ready(function() {
    $('.homeBtn').on('click', function() {
        $('.nonBlur').toggleClass('blur');
        $('.blur_login').slideToggle(500);
    });
    $("#id_username").attr('placeholder', 'Username');
    $("#id_password").attr('placeholder', 'Password');
    
});
