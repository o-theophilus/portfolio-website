<script>
	import { flip } from 'svelte/animate';
	import { cubicInOut } from 'svelte/easing';

	import { Content } from '$lib/layout';
	import { BackButton } from '$lib/button';
	import { UpdateUrl, Meta, Pagination, Dropdown, Log } from '$lib/macro';
	import { Search } from '$lib/input';
	import One from './one.svelte';

	let { data } = $props();
	reports = data.reports;
	total_page = data.total_page;
	let { order_by } = data;
	let { _status } = data;
	let { _type } = data;
</script>

<Log entity_type={'page'} />
<UpdateUrl />
<Meta title="All Users" />

<Content>
	<div class="title">
		<BackButton />
		<strong class="ititle">
			Report{reports.length > 1 ? 's' : ''}
		</strong>
	</div>

	<div class="line">
		<Dropdown name="status" list={_status} default_value={_status[0]} wide />
		<Dropdown name="type" list={['all', ..._type]} default_value="all" wide />
	</div>
	<div class="line">
		<Search />
		<Dropdown name="order" list={order_by} icon="sort" />
	</div>

	{#each reports as x (x.key)}
		<div animate:flip={{ delay: 0, duration: 250, easing: cubicInOut }}>
			<One one={x} />
		</div>
	{:else}
		<div class="item">no item here</div>
	{/each}

	<Pagination {total_page} />
</Content>

<style>
	.title {
		display: flex;
		align-items: center;
		gap: var(--sp2);

		margin: var(--sp2) 0;
	}

	.line {
		display: flex;
		gap: var(--sp1);
		align-items: center;
		margin: var(--sp2) 0;
	}

	.item {
		margin: var(--sp2) 0;
	}
</style>
