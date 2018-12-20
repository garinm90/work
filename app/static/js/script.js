$(document).ready(function () {
    $('#order_table').DataTable({

        "columnDefs": [{
                "orderable": false,
                "targets": [5, 6],
            },
            {
                type: "natural",
                "targets": [0, 3],
            }
        ]
    });
    $('#customer_jobs').DataTable({
        "columnDefs": [{
                "orderable": false,
                "targets": [ 3, 4, 6, 7, 8, 9],
            },
            {
                type: "natural",
                "targets": [0, 4]
            }
        ]
    });
    $('#controller_list').DataTable({
        'columnDefs': [{
            "orderable": false,
            "targets": [5]
        }
        ]
    });
    $('#customer_list').DataTable({
        'columnDefs': [{
            "orderable": false,
            "targets": [1, 2, 3, 4]
        }]
    })
});