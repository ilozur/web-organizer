$(document).ready(function() {
	$('.btn_change').click(function(event) {
		$('.table').removeClass('active')
		var num = $(this).attr('data-num');
		$('#table'+num).addClass('active')
	});
});