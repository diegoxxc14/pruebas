$(document).ready(function () {
    var tabla;  //DataTable global
    var numRolesSel = 0;
    var filas, lista_pk;

    $.ajax({
        url: "/libros/roles_pago/load/",//url: "{% url 'cargar_rolesPago' %}",
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


    function quitarRolesPago(lista_pk, filas_delete){
        $.ajax({
            data: {'pks':JSON.stringify(lista_pk)}, //Paso el array de datos seleccionados como JSON
            url: "/libros/roles_pago/delete/",    //url: "{% url 'remover_rolesPago' %}",
            type: 'post',
            success: function () {  //Si _todo sale bien
                filas_delete.remove().draw(false);  //Eliminar las filas de la tabla
                $('#roles_sel').text("");
                $('#btnEliminarSel').attr('disabled','true');   //Desactivar le boton de eliminar
                verMensajeModal("Los Roles de Pago se han eliminado con éxito.", "alert alert-success");
            },
            error: function () {    //Si algo sale mal
                verMensajeModal("Ups, algo salió mal..", "alert alert-danger");
            }
        });
    }


    function guardarRolPago(newRolPago){
        $.ajax({
            data: {'rol_pago':JSON.stringify(newRolPago)}, //Paso el array de datos seleccionados como JSON
            url: "/libros/roles_pago/create/",    //url: "{% url 'crear_rolesPago' %}",
            type: 'post',
            success: function (data) {  //Si _todo sale bien
                tabla.rows.add(data).draw(false);   //Agrego la fila en la tabla
                verMensajeModal("Rol de Pago guardado con éxito.", "alert alert-success");
            },
            error: function () {    //Si algo sale mal
                verMensajeModal("Ups, algo salió mal..", "alert alert-danger");
            }
        });
    }


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


    $('#tabla_persona tbody').on('click', 'tr', function () {//Seleccionar la filas
        $(this).toggleClass('selected');
        numRolesSel = tabla.rows('.selected').data().length;
        if (numRolesSel != 0){
            $('#roles_sel').text(numRolesSel +' rol(es) seleccionado(s)');
            $('#btnEliminarSel').removeAttr('disabled');
        }else{
            $('#roles_sel').text('');
            $('#btnEliminarSel').attr('disabled','true');
        }
    });


    $("#btnEliminarSel").on("click", function(){
        if (numRolesSel != 0) {//Si se ha seleccionado algún registro
            filas = tabla.rows('.selected');//Tomo las filas que se han seleccionado
            var datos_json = filas.data();//obtengo sus datos como JSON
            lista_pk = $.makeArray();
            for (var i=0;i<datos_json.length;i++){//Guardo los pk en un arreglo para pasarlos por AJAX
                lista_pk.push(datos_json[i].pk);
            }

            $('#deleteRolPago').html(
                "<div class='alert alert-danger'>" +
                    "<h6 class='alert-heading'>Está seguro de eliminar los siguientes Roles de Pago?</h6>" + detalleRolesRemove() +
                "</div>"
            );

            function detalleRolesRemove () {
                var datosRoles="<ul>";
                for (var i=0;i<numRolesSel;i++){
                    datosRoles+="<li >" + datos_json[i].fields.apellidos + " " + datos_json[i].fields.nombres + "</li>";
                }
                return datosRoles+"</ul>";
            }

            $('#deleteRolPagoModal').modal('show');
        }else{
            verMensajeModal("Por favor, debe seleccionar al menos un Rol de Pago.", "alert alert-warning");
        }
    });


    $("#btnSiDelete").on("click", function(){
        $('#deleteRolPagoModal').modal('hide');
        quitarRolesPago(lista_pk, filas);
    });


    $('#btnGenerarRol').on("click", function () {
        $('#newRolPagoModal').modal('show');
    });


    $("#btnGuardarRolPago").on("click", function(){
        $('#newRolPagoModal').modal('hide');
        var newRolPago = $.makeArray();
        newRolPago.push($('#newCedula').val());
        newRolPago.push($('#newSueldo').val());
        newRolPago.push($('#newNombres').val());
        newRolPago.push($('#newApellidos').val());
        guardarRolPago(newRolPago);
        //Mejorar lo siguiente
        $('#newCedula').val("")
        $('#newSueldo').val(0)
        $('#newNombres').val("")
        $('#newApellidos').val("")
    });


    function verMensajeModal(info, tipo) {
        $('#infoRolPago').html(
            "<div class='"+tipo+"'>" +
                "<h6 class='alert-heading'>"+info+"</h6>" +
            "</div>"
        );
        $('#infoRolPagoModal').modal('show');
    }

});