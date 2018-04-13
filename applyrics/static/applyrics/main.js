$(document).ready(function(){
	$('.item').click(function(){
        var a = $(this).find('a')[0];
        window.location.assign($(a).attr('href'));
	});
	$('#submit_correction').click(function(){
	    $('#correctModal').slideDown();
	    var title = $('#song_title').text();
	    var writers = $('#writers').html();
	    var lyrics = $('#lyrics').text();
	    var correct = $('#correct');
	    correct.text(title + ' - ' + writers + '\n\n' + lyrics);
	});
});
