<script>
	import { page } from '$app/state';
	import { onMount } from 'svelte';

	import { page_state } from '$lib/store.svelte.js';

	import Search from '$lib/search.svelte';
	import { Icon } from '$lib/macro';
	import { Button } from '$lib/button';
	import { Dropdown } from '$lib/input';

	let { access } = $props();

	let user_key = $state('');
	let type = $state('all');
	let action = $state('all');
	let search = $derived(`${user_key}:${type}:${action}`);
	let drop_1;
	let drop_2;

	onMount(() => {
		if (page.url.searchParams.has('search')) {
			let temp = page.url.searchParams.get('search');
			temp = temp.split(':');
			if (temp.length == 3) {
				user_key = temp[0];
				type = temp[1];
				action = temp[2];
				search = `${user_key}:${type}:${action}`;
				drop_1.set(type);
				drop_2.set(action);
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
			page_state.set('search', search != ':all:all' ? search : '');
		}
	};
</script>

<section>
	<div class="row">
		<Dropdown
			wide
			list={Object.keys(access)}
			default_value="all"
			bind:this={drop_1}
			on:change={(e) => {
				type = e.target.value;
				action = 'all';
				drop_2.set(action);
			}}
		/>

		<Dropdown
			wide
			list={access[type]}
			default_value="all"
			bind:this={drop_2}
			on:change={(e) => {
				action = e.target.value;
			}}
		/>
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
			onclick={() => {
				submit();
			}}
		>
			<Icon icon="search" />
		</Button>
		<Button
			extra="hover_red"
			disabled={`${user_key}:${type}:${action}` == ':all:all'}
			onclick={() => {
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
