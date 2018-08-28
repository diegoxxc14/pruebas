
$(document).ready(function () {
    var tabla;//DataTable global

    $.ajax({
        url: "/libros/personas/load/",//url: "{% url 'ver_personas' %}",
        success: function (data) {
            tabla = $('#tabla_persona').DataTable({
                "processing":true,
                "data": data,
                "columnDefs":[
                    {
                        "targets": -1,
                        "data": null,
                        "defaultContent": "<div class='btn-group'><button class='btn btn-warning btnEditar'>Editar</button>" +
                            "<button class='btn btn-primary btnVerRol'>Ver Rol</button>" +
                            "<button class='btn btn-default btnImprimir'>Imprimir</button></div>",
                    },
                ],
                "columns":[
                    { "data": null},
                    { "data": "fields.cedula" },
                    { "data": "fields.nombres" },
                    { "data": "fields.sueldo" },
                    { "data": null },

                ],
                "order": [[ 1, 'asc' ]],
                "language":{
                    "url":"//cdn.datatables.net/plug-ins/1.10.19/i18n/Spanish.json"
                },
            });

            tabla.on( 'order.dt search.dt', function () {   //Para enumerar las filas
                tabla.column(0, {search:'applied', order:'applied'}).nodes().each( function (cell, i) {
                    cell.innerHTML = i+1;
                } );
            } ).draw();

        }
    });


    function deletePer(pk, fila_delete){
        $.ajax({
            data: {'id':pk},
            url: "/libros/persona/delete/",//url: "{% url 'del_persona' %}",
            type: 'get',
            success: function (data) {//Si se elimina correctamente, lo quitamos de la tabla
                fila_delete.remove().draw( false );
                $('#roles_sel').text("")
            },
            error: function () {
                alert("Algo salió mal.. Ups")
            }
        });
    }

    function deletePersonas(lista_pk, filas_delete){
        $.ajax({
            data: {'pks':JSON.stringify(lista_pk)},//Paso el array de datos seleccionados como JSON
            url: "/libros/personas/delete/",//url: "{% url 'del_personas' %}",
            type: 'get',
            success: function () {//Si se eliminan correctamente, los quitamos de la tabla
                filas_delete.remove().draw(false);
                $('#roles_sel').text("");
            },
            error: function () {
                alert("Algo salió mal.. Ups");
            }
        });
    }

    // $('#tabla_persona tbody').on( 'click', 'button', function () {
    //     var fila = tabla.row($(this).parents('tr'));
    //     var dato_json = fila.data();
    //     deletePer(dato_json.pk, fila);
    // });

    $('#tabla_persona tbody').on( 'click', '.btnEditar', function () {
        var fila = tabla.row($(this).parents('tr'));
        var dato_json = fila.data();

        $('#editRolPago').html(
            "<form class='form-row'>" +
            "  <div class='col'>" +
            "    <label for='formGroupExampleInput'>Cédula:</label>" +
            "    <input type='text' class='form-control' id='formGroupExampleInput' value="+dato_json.fields.cedula+" readonly>"+
            "  </div>" +
            "  <div class='col'>" +
            "    <label for='formGroupExampleInput2'>Nombres:</label>" +
            "    <input type='text' class='form-control' id='formGroupExampleInput2' value="+dato_json.fields.nombres+" readonly>"+
            "  </div>" +
            "  <div class='form-group'>" +
            "    <label for='formGroupExampleInput3'>Sueldo:</label>" +
            "    <input type='number' class='form-control' id='formGroupExampleInput3' value="+dato_json.fields.sueldo+">"+
            "  </div>" +
            "  <div class='form-group'>" +
            "    <label for='formGroupExampleInput4'>Tipo:</label>" +
            "    <input type='text' class='form-control' id='formGroupExampleInput4' placeholder='Tipo' value="+dato_json.fields.tipo+">"+
            "  </div>" +
            "</form>"
        );

        $('#editRolPagoModal').modal('show');


    });


    var numRolesSel;

    $('#tabla_persona tbody').on('click', 'tr', function () {//Seleccionar la filas
        $(this).toggleClass('selected');
        numRolesSel = tabla.rows('.selected').data().length;
        if (numRolesSel!=0){
            $('#roles_sel').text(numRolesSel +' rol(es) seleccionado(s)');
        }else{
            $('#roles_sel').text("")
        }
    });

    var filas, lista_pk, datos_json;

    $("#btnEliminarSel").on("click", function(){
        filas = tabla.rows('.selected');//Tomo las filas que se han seleccionado
        console.log(filas);
        datos_json = filas.data();//obtengo sus datos como JSON
        lista_pk = $.makeArray();
        for (var i=0;i<datos_json.length;i++){//Guardo los pk en un arreglo para pasarlos por AJAX
            lista_pk.push(datos_json[i].pk)
        }

        $('#deleteRolPago').html(
            "<h6 class='alert-heading'>Está seguro de eliminar los siguientes Roles de Pago?</h6>" + detalleRolesDelete()
        );

        function detalleRolesDelete () {
            var datosRoles="<ul>";
            for (var i=0;i<numRolesSel;i++){
                datosRoles+="<li >" + datos_json[i].fields.apellidos + " " + datos_json[i].fields.nombres + "</li>";
            }
            return datosRoles+"</ul>";
        }

        $('#deleteRolPagoModal').modal('show');
    });

    $("#btnSiDelete").on("click", function(){
        $('#deleteRolPagoModal').modal('hide');
        deletePersonas(lista_pk, filas);
        verMensajeInfo("Los Roles de Pago se han eliminado con éxito.");
    });

    function verMensajeInfo(info) {
        $('#infoRolPago').html(
            "<h6 class='alert-heading'>"+info+"</h6>"
        );
        $('#infoRolPagoModal').modal('show');
    }

});