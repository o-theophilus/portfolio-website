<script>
	import { flip } from 'svelte/animate';
	import { cubicInOut } from 'svelte/easing';

	import { Content } from '$lib/layout';
	import { BackButton } from '$lib/button';
	import { PageNote } from '$lib/info';
	import { Meta, Pagination, Dropdown, Log, Icon2 } from '$lib/macro';
	import { Search } from '$lib/input';
	import One from './one.svelte';

	let { data } = $props();
	let reports = $derived(data.reports);
	let total_page = $derived(data.total_page);
	let { order_by } = data;
	let { _type } = data;
	let { _status } = data;
</script>

<Log entity_type={'page'} />
<Meta title="All Users" />

<Content>
	<div class="line line1">
		<BackButton />
		<div class="page_title">
			Report{reports.length > 1 ? 's' : ''}
		</div>
	</div>

	<div class="line nowrap">
		<Dropdown
			icon="chevron-down"
			name="type"
			list={['all', ..._type]}
			default_value="all"
			--select-width="100%"
		/>
		<Dropdown
			icon="chevron-down"
			name="status"
			list={_status}
			default_value={_status[0]}
			--select-width="100%"
		/>
	</div>
	<div class="line">
		<Search />
		<Dropdown name="order" list={order_by} icon="arrow-down-narrow-wide" />
	</div>

	{#each reports as x (x.key)}
		<div animate:flip={{ delay: 0, duration: 250, easing: cubicInOut }}>
			<One one={x} />
		</div>
	{:else}
		<PageNote>
			<Icon2 icon="search" size="50" />
			No report found
		</PageNote>
	{/each}

	<div class="pagination">
		<Pagination {total_page} />
	</div>
</Content>

<style>
	.line1 {
		margin-top: 16px;
	}

	.pagination {
		display: flex;
		justify-content: center;
		margin: 16px;
	}
</style>
