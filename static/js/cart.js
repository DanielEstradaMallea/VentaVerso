$('#buscarempleado').on('input', function () {
    var busqueda = $('#buscarempleado').val();
    if (busqueda === '') {
      $('#resultados').empty();
    } else {
      $.ajax({
        url: "{% url 'buscar_empleado' %}",
        data: {
          'busqueda': busqueda
        },
        dataType: 'json',
        success: function (data) {
          $('#resultados').empty();
          data.forEach(function (item) {
            var nombreCompleto = item.nombre + " " + item.apellidos;
            $('#resultados').append(new Option(nombreCompleto, item.id));
          });
        }
      });
    }
  });