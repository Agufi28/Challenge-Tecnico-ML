$(function () {
    function fetchDatabases() {
        $.ajax({
            type: 'GET',
            url: '/api/v1/databases',
            success: function (response) {
                populateTable(response);
            },
            error: function (response) {
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: response.responseJSON?.detail || 'Error fetching the databases data.',
                }).then(() => {
                    if (response.status === 401) {
                        window.location = '/login';
                    }
                });
            }
        });
    }

    function populateTable(databases) {
        const tbody = $("table tbody");
        tbody.empty();

        databases.forEach(database => {
            const row = `
                <tr>
                    <td>${database.id}</td>
                    <td>${database.type}</td>
                    <td>
                        <button class="btn btn-success btn-sm scan-database" data-id="${database.id}">Scan</button>
                        <button class="btn btn-info btn-sm view-last-results" data-id="${database.id}">View Last Results</button>
                    </td>
                </tr>
            `;
            tbody.append(row);
        });

        $(".scan-database").click(function () {
            const databaseId = $(this).data("id");

            $.ajax({
                type: 'POST',
                url: `/api/v1/databases/${databaseId}/scans`,
                success: function () {
                    Swal.fire({
                        icon: 'success',
                        title: 'Success',
                        text: `The database with ID ${databaseId} has been successfully scanned.`,
                    });
                },
                error: function (response) {
                    Swal.fire({
                        icon: 'error',
                        title: 'Error',
                        text: response.responseJSON?.detail || 'An unexpected error has occurred while scanning the database. Please try again later.',
                    });
                }
            });
        });

        $(".view-last-results").click(function () {
            const databaseId = $(this).data("id");
			window.location = `/results?databaseId=${databaseId}`;
        });
    }

    fetchDatabases();
});