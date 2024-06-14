<script>
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { set_state } from '$lib/store.js';

	import Search from '$lib/search.svelte';
	import Icon from '$lib/icon.svelte';
	import Button from '$lib/button/button.svelte';

	export let permissions;

	let user_key = '';
	let type = 'all';
	let action = 'all';
	let search = `${user_key}:${type}:${action}`;

	onMount(() => {
		if ($page.url.searchParams.has('search')) {
			let temp = $page.url.searchParams.get('search');
			temp = temp.split(':');
			if (temp.length == 3) {
				user_key = temp[0];
				type = temp[1];
				action = temp[2];
				search = `${user_key}:${type}:${action}`;
			}
		}
	});

	const submit = (clear = false) => {
		if (clear) {
			user_key = '';
			type = 'all';
			action = 'all';
		}

		let check = `${search}`;
		search = `${user_key}:${type || 'all'}:${action || 'all'}`;
		if (search != check) {
			set_state('search', search != ':all:all' ? search : '');
		}
	};
</script>

<section>
	<div class="row">
		<select
			class="wide"
			bind:value={type}
			on:input={() => {
				action = 'all';
			}}
		>
			{#each Object.entries(permissions) as [type, _]}
				<option value={type}>
					{type}
				</option>
			{/each}
		</select>
		<select class="wide" bind:value={action}>
			{#each permissions[type] as x}
				<option value={x}>
					{x}
				</option>
			{/each}
		</select>
	</div>

	<Search
		non_default
		placeholder="Search for User"
		bind:search={user_key}
		on:clear={() => {
			user_key = '';
		}}
	>
		<Button
			disabled={`${user_key}:${type}:${action}` == search}
			on:click={() => {
				submit();
			}}
		>
			<Icon icon="search" />
		</Button>
		<Button
			extra="hover_red"
			disabled={`${user_key}:${type}:${action}` == ':all:all'}
			on:click={() => {
				submit(true);
			}}
		>
			<Icon icon="close" />
		</Button>
	</Search>
</section>

<style>
	section {
		display: flex;
		flex-direction: column;
		gap: var(--sp1);
		margin: var(--sp2) 0;
	}

	.row {
		display: flex;
		gap: var(--sp1);
		align-items: center;
	}
</style>
