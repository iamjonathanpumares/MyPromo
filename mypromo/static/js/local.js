var $direccion = $('#direccion'),
	$latitud = $('#latitud'),
	$longitud = $('#longitud'),
	$fila = $('.TableBody-row').eq(0),
	$tabla = $('.TableBody');

var cont_local = 0;

//$tabla.hide();

// Funciones vinculadas con los eventos-----------------------------------------------------------------
function agregarLocal()
{
	//$tabla.show();
	var direccion = $direccion.val();
	var latitud = $latitud.val();
	var longitud = $longitud.val();
	var $clone = $fila.clone(true);
	$clone.removeClass('fila-base');

	$clone.find('.TableBody--direccion').text(direccion);
	$clone.find('.TableBody--latitud').text(latitud);
	$clone.find('.TableBody--longitud').text(longitud);
	//$clone.find('.TableBody--eliminar').attr("id", "boton-eliminar" + cont_local.toString());
	//$clone.hide();

	$clone.appendTo('.TableBody');
	$clone.fadeIn();
}

function eliminarLocal()
{
	var $parent = $(this).parents().get(0);
	$($parent).remove();
}

// Eventos ----------------------------------------------------------------------------------------------
$('#agregar-local').click(agregarLocal);
$('.TableBody--eliminar').click(eliminarLocal);