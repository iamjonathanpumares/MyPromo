var $direccion = $('#direccion'),
$latitud = $('#latitud'),
$longitud = $('#longitud'),
$fila = $('.TableBody-row').eq(0),
$tabla = $('.TableBody');
$('#enviar-locales').attr("disabled", true);

var csrftoken = $.cookie('csrftoken');
var url_afiliado = location.href;

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
	if ($('.TableBody').children().size() > 1)
	{
		$('#enviar-locales').attr("disabled", false);
	}
	else
	{
		$('#enviar-locales').attr("disabled", true);
	}
}

function eliminarLocal()
{
	var $parent = $(this).parents().get(0);
	$($parent).remove();
	if ($('.TableBody').children().size() > 1)
	{
		$('#enviar-locales').attr("disabled", false);
	}
	else
	{
		$('#enviar-locales').attr("disabled", true);
	}
}

function convertirJSON()
{
	var numFilas = $('.TableBody').children().length - 1;
	var direccion = "";
	var latidud = 0;
	var longitud = 0;
	var direcciones = [], latitudes = [], longitudes = [];
	for(var i = 1; i <= numFilas; i++)
	{
		direccion = $('.TableBody').children().eq(i).find('.TableBody--direccion').text();
		latitud = $('.TableBody').children().eq(i).find('.TableBody--latitud').text();
		longitud = $('.TableBody').children().eq(i).find('.TableBody--longitud').text();
		direcciones.push(direccion);
		latitudes.push(latitud);
		longitudes.push(longitud);
	}
	var locales = { 
		direcciones: direcciones,
		latitudes: latitudes,
		longitudes: longitudes 
	};
	var json_locales = JSON.stringify(locales);

	$.post(url_afiliado, json_locales, function (url_redirect) {
		document.location.href = url_redirect;
	});

	/*$.ajax({
	    url: url_afiliado,
	    type: 'POST',
	    data: json_locales,
	    success: function (msg) {
	    	alert(msg);
	        //document.location.href = msg;
	    }
	    contentType: 'application/json; charset=utf-8',
	    dataType: 'json',
	    async: false

	});*/

	//return json_locales;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

// Eventos ----------------------------------------------------------------------------------------------
$('#agregar-local').click(agregarLocal);
$('.TableBody--eliminar').click(eliminarLocal);
$('#enviar-locales').click(convertirJSON);
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});