$(function(){
	$('#button-to-click').click(function(){
		e1 = $('#first-child');
        e1.addClass('animate');
        e1.one('webkitAnimationEnd oanimationend msAnimationEnd animationend',
        function (e) {
            e1.removeClass('animate');
        });
	});
});