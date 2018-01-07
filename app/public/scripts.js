$(document).ready(function(){
    $('.catalog-object').click(function(event){
        var obj_id = $(event.currentTarget).attr('object_id')
       window.location.href = '/detail?obj_id='+obj_id;
    });

    var $grid = $('.img-grid').packery({
        itemSelector: '.grid-img',
        stagger: 30,
        gutter: 10
    }).on( 'click', '.grid-img', function( event ) {
        var current = $(event.currentTarget)
        if(current.hasClass('grid-img--4')) {
            current.toggleClass('grid-img--4');
            current.toggleClass('grid-img--2');
        }
        else if(current.hasClass('grid-img--2')) {
            current.toggleClass('grid-img--2');
            current.toggleClass('grid-img--1');
        }
        else if(current.hasClass('grid-img--1')) {
            current.toggleClass('grid-img--1');
            current.toggleClass('grid-img--4');
        }
        $grid.packery('layout');
    });

    $('.tree-toggler').click(function () {
		$(this).parent().children('.tree').toggle(300);
	});
  $('.tree-toggler').parent().children('.tree').toggle(1000);
});
