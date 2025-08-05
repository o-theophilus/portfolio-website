<script>
	import { flip } from 'svelte/animate';
	import { cubicInOut } from 'svelte/easing';

	import { Content } from '$lib/layout';
	import { BackButton } from '$lib/button';
	import { UpdateUrl, Meta, Pagination, Dropdown, Log } from '$lib/macro';
	import Search from '$lib/search.svelte';
	import User from './user.svelte';

let { data } = $props();
	users = data.users;
	total_page = data.total_page;
	let { order_by } = data;
	let { _status } = data;
</script>

<Log entity_type={'page'} />
<UpdateUrl />
<Meta title="All Users" />

<Content>
	<div class="title">
		<div class="left">
			<BackButton />
			<strong class="ititle">
				User{users.length > 1 ? 's' : ''}
			</strong>
		</div>

		<Dropdown name="status" list={['all', ..._status]} default_value="all" />
	</div>

	<div class="search_bar">
		<Search />
		<Dropdown name="order" list={order_by} icon="sort" />
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
