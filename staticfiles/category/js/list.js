$(function () {
    $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'searchdata'
            }, // parametros
            dataSrc: ""
        },
        columns: [
            {"data": "id"},
            {"data": "name"},
            {"data": "desc"},
            {"data": "desc"},
        ],
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    let buttons = '<a href="/erp/category/update/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit fa-2x"></i></a> ';
                    buttons += '<a href="/erp/category/delete/' + row.id + '/" type="button" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt fa-2x"></i></a>';
                    return buttons;
                }
            },
        ],
        initComplete: function(settings, json) {
        
          }
        });
});