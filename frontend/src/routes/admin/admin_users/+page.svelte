<script>
	import { flip } from 'svelte/animate';
	import { cubicInOut } from 'svelte/easing';

	import { Content } from '$lib/layout';
	import { BackButton } from '$lib/button';
	import User from '../users/user.svelte';
	import Search from './search.svelte';
	import { Meta, Pagination, Dropdown, UpdateUrl, Log } from '$lib/macro';

	let { data } = $props();
	users = data.users;
	total_page = data.total_page;
	let { access } = data;
	let { order_by } = data;
</script>

<Log entity_type={'page'} />
<UpdateUrl />
<Meta title="Admin" description="Users with elevated Access" />

<Content>
	<div class="title">
		<div class="left">
			<BackButton />
			<strong class="ititle">
				Admin{users.length > 1 ? 's' : ''}
			</strong>
		</div>
		<Dropdown name="order" list={order_by} />
	</div>

	<Search {access} />

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
</style>
