$(document).ready( function () {
    $('.crud-table').DataTable({
        language:{
            zeroRecords:'No hay coincidencias',
            info:'Mostrando _END_ resultados de _MAX_',
            infoEmpty:'No hay datos disponibles',
            infoFiltered:'(Filtrado de _MAX_ registros totales)',
            search:'Buscar',
            emptyTable:     "No existen registros",
            paginate: {
                first:      "Primero",
                previous:   "Anterior",
                next:       "Siguiente",
                last:       "Anterior"
            },
        },
        responsive: true,
        dom: 'Bfrtip',
        buttons: [
            { extend: 'csv', text:'Excel' },
            { extend: 'print', text: 'Imprimir'},
        ],
    } );
} );