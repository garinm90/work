$(document).ready( function () {
    $('#order_table').DataTable({
        "columnDefs": [
            { "orderable": false, "targets": [5, 6], }
        ]
    });
} );