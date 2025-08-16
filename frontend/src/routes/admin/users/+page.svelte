<script>
	import { flip } from 'svelte/animate';
	import { cubicInOut } from 'svelte/easing';

	import { Content } from '$lib/layout';
	import { BackButton } from '$lib/button';
	import { Meta, Pagination, Dropdown, Search, Radio, Log, Icon2 } from '$lib/macro';
	import { PageNote } from '$lib/info';
	import One from './one.svelte';

	let { data } = $props();
	let users = $derived(data.users);
	let total_page = $derived(data.total_page);
	let { order_by } = data;
	let { _status } = data;
</script>

<Log entity_type={'page'} />
<Meta title="All Users" />

<Content>
	<div class="line space line1">
		<div class="line">
			<BackButton />
			<div class="page_title">
				User{users.length > 1 ? 's' : ''}
			</div>
		</div>
		<Dropdown name="status" list={['all', ..._status]} icon="arrow-down-narrow-wide" />
	</div>

	<div class="search_bar">
		<Search />
		<Dropdown name="order" list={order_by} novalue icon="arrow-down-narrow-wide" />
	</div>

	{#each users as x (x.key)}
		<div animate:flip={{ delay: 0, duration: 250, easing: cubicInOut }}>
			<One user={x} />
		</div>
	{:else}
		<PageNote>
			<Icon2 icon="search" size="50" />
			No user found
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

	.search_bar {
		margin: var(--sp2) 0;
		display: flex;
		gap: var(--sp1);
		align-items: center;
	}

	.pagination {
		display: flex;
		justify-content: center;
		margin: 16px;
	}
</style>
