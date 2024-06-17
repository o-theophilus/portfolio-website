<script>
	import { flip } from 'svelte/animate';
	import { cubicInOut } from 'svelte/easing';

	import UpdateUrl from '$lib/update_url.svelte';
	import Content from '$lib/content.svelte';
	import Back from '$lib/button/back.svelte';
	import Meta from '$lib/meta.svelte';
	import Pagination from '$lib/pagination.svelte';
	import DropPlus from '$lib/dropdown_plus.svelte';
	import Search from '$lib/search.svelte';
	import Log from '$lib/log.svelte';
	import One from './one.svelte';

	export let data;
	$: reports = data.reports;
	$: total_page = data.total_page;
	let { order_by } = data;
	let { _status } = data;
	let { _type } = data;
</script>

<Log entity_type={'page'} />
<UpdateUrl />
<Meta title="All Users" />

<Content>
	<div class="title">
		<Back />
		<strong class="ititle">
			Report{reports.length > 1 ? 's' : ''}
		</strong>
	</div>

	<div class="line">
		<DropPlus name="status" list={_status} default_value={_status[0]} />
		<DropPlus name="type" list={['all', ..._type]} default_value="all" />
	</div>
	<div class="line">
		<Search />
		<DropPlus name="order" list={order_by} icon="sort" />
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
