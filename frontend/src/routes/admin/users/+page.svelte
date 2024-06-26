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
	import User from './user.svelte';

	export let data;
	$: users = data.users;
	$: total_page = data.total_page;
	let { order_by } = data;
	let { _status } = data;
</script>

<Log entity_type={'page'} />
<UpdateUrl />
<Meta title="All Users" />

<Content>
	<div class="title">
		<div class="left">
			<Back />
			<strong class="ititle">
				User{users.length > 1 ? 's' : ''}
			</strong>
		</div>

		<DropPlus name="status" list={['all', ..._status]} default_value="all" />
	</div>

	<div class="search_bar">
		<Search />
		<DropPlus name="order" list={order_by} icon="sort" />
	</div>

	{#each users as x (x.key)}
		<div animate:flip={{ delay: 0, duration: 250, easing: cubicInOut }}>
			<User user={x} />
		</div>
	{:else}
		no item here
	{/each}

	<Pagination {total_page} />
</Content>

<style>
	.title {
		display: flex;
		justify-content: space-between;
		align-items: center;
	}
	.left {
		display: flex;
		align-items: center;
		gap: var(--sp2);
	}

	.search_bar {
		margin: var(--sp2) 0;
		display: flex;
		gap: var(--sp1);
		align-items: center;
	}
</style>
