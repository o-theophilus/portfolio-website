<script>
	import { flip } from 'svelte/animate';
	import { cubicInOut } from 'svelte/easing';

	import { Content } from '$lib/layout';
	import { PageNote } from '$lib/info';
	import { Meta, Pagination, UpdateUrl, Icon2 } from '$lib/macro';
	import Search from './search.svelte';
	import Log from './log.svelte';

	let { data } = $props();
	let logs = $derived(data.logs);
	let total_page = $derived(data.total_page);
	let search_query = $derived(data.search_query);
	let search = $state({ user_key: '', entity_type: 'all', action: 'all', entity_key: '' });
</script>

<!-- <UpdateUrl /> -->
<Meta title="Logs" />

<Content>
	<strong class="ititle"> Logs </strong>
	<Search {search_query} bind:search />

	{#each logs as log (log.key)}
		<div animate:flip={{ delay: 0, duration: 250, easing: cubicInOut }}>
			<Log {log} bind:search />
		</div>
	{:else}
		<PageNote>
			<Icon2 icon="search" size="50" />
			No log found
		</PageNote>
	{/each}
	<div class="pagination">
		<Pagination {total_page} />
	</div>
</Content>

<style>
	.pagination {
		display: flex;
		justify-content: center;
		margin: 16px;
	}
</style>
