<script>
	import { flip } from 'svelte/animate';
	import { cubicInOut } from 'svelte/easing';

	import { Content } from '$lib/layout';
	import { BackButton } from '$lib/button';
	import { PageNote } from '$lib/info';
	import { Meta, Pagination, Dropdown, Log, Icon2 } from '$lib/macro';
	import One from '../users/one.svelte';
	import Search from './search.svelte';

	let { data } = $props();
	let users = $derived(data.users);
	let total_page = $derived(data.total_page);
	let { search_query } = data;
	let { order_by } = data;
	console.log(search_query);
	
</script>

<Log entity_type={'page'} />
<Meta title="Admin" description="Users with elevated Access" />

<Content>
	<div class="line space line1">
		<div class="line">
			<BackButton />
			<strong class="ititle">
				Admin{users.length > 1 ? 's' : ''}
			</strong>
		</div>
		<Dropdown name="order" list={order_by} novalue icon="arrow-down-narrow-wide" />
	</div>

	<Search {search_query} />

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

	.pagination {
		display: flex;
		justify-content: center;
		margin: 16px;
	}
</style>
