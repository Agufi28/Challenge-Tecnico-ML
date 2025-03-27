$(document).ready(function () {
    function fetchScanResults() {
		const urlParams = new URLSearchParams(window.location.search);
        const databaseId = urlParams.get('databaseId');

        if (!databaseId) {
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: 'You must provide a database ID.',
            }).then(() => {
                window.location = '/databases';
            });
            return;
        }

        $.ajax({
            type: 'GET',
            url: `/api/v1/databases/${databaseId}/scans/last`,
            success: function (response) {
				$("#scannedOn").text(response.executed_on);
                populateTable(response.schemas);
            },
            error: function (response) {
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: response.responseJSON?.detail || 'Error while fetching the scan data.',
                }).then(() => {
                    if (response.status === 401) {
                        window.location = '/login';
                    }
                });
            }
        });
    }

    function populateTable(scanResult) {
		const tbody = $("table tbody");
		tbody.empty();
	
		scanResult.forEach(schema => {
			const row = `
				<tr>
					<td>${schema.id}</td>
					<td>${schema.name}</td>
					<td>
						<button class="btn btn-primary btn-sm view-tables" data-schema-id="${schema.id}" data-schema-name="${schema.name}">View Tables</button>
					</td>
				</tr>
			`;
			tbody.append(row);
		});

		$(".view-tables").click(function () {
			const schemaId = $(this).data("schema-id");
	
			const schema = scanResult.find(s => s.id === schemaId);
			if (schema) {
				const modalBody = $("#tablesModal .modal-body tbody");
				modalBody.empty();
	
				schema.tables.forEach(table => {
					const tableRow = `
						<tr>
							<td>${table.id}</td>
							<td>${table.name}</td>
							<td>
								<button class="btn btn-info btn-sm view-fields" data-table-id="${table.id}" data-table-name="${table.name}">View Fields</button>
							</td>
						</tr>
					`;
					modalBody.append(tableRow);
				});
	
				$(".view-fields").click(function () {
					const tableId = $(this).data("table-id");
	
					const table = schema.tables.find(t => t.id === tableId);
					if (table) {
						const fieldsModalBody = $("#fieldsModal .modal-body tbody");
						fieldsModalBody.empty();
	
						table.fields.forEach(field => {
							const tags = field.tags.length > 0 
								? `<ul>${field.tags.map(tag => `<li>${tag.tag.name} (${tag.certanty_score})</li>`).join("")}</ul>` 
								: "No Tags";
							const fieldRow = `
								<tr>
									<td>${field.id}</td>
									<td>${field.name}</td>
									<td>${tags || "No Tags"}</td>
								</tr>
							`;
							fieldsModalBody.append(fieldRow);
						});
	
						$("#fieldsModal").modal("show");
					} else {
						Swal.fire({
							icon: 'error',
							title: 'Error',
							text: 'No fields where found for this table.',
						});
					}
				});

				$("#tablesModal").modal("show");
			} else {
				Swal.fire({
					icon: 'error',
					title: 'Error',
					text: 'No tables where found for this scheme.',
				});
			}
		});
	}

    fetchScanResults();
});