<script>
	let { data, headers } = $props();
</script>

<div class="table-wrapper">
	<table>
		<thead>
			<tr>
				{#each headers as head}
					<th>{head}</th>
				{/each}
			</tr>
		</thead>

		<tbody>
			{#each data as row}
				<tr>
					{#each headers as head}
						<td>{row[head]}</td>
					{/each}
				</tr>
			{/each}
		</tbody>
	</table>
</div>

<style>
	.table-wrapper {
		width: 100%;
		overflow-x: auto;
	}

	table {
		width: 100%;
		border-collapse: collapse;
		font-size: 0.7rem;
	}

	thead {
		background-color: var(--bg2);

		th {
			text-align: left;
			padding: 4px 8px;
			font-weight: 800;
			text-transform: capitalize;
		}
	}

	tbody {
		tr:hover {
			background-color: var(--bg2);
		}
		td {
			padding: 2px 8px;
		}
	}

	tr {
		border-bottom: 1px solid var(--ol);
		&:last-child {
			border-bottom: none;
		}
	}
</style>
