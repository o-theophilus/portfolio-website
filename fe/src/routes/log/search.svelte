<script>
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { user, set_state } from '$lib/store_old.js';

	import Search from '$lib/search.svelte';
	import Button from '$lib/button_old/button.svelte';
	import Drop from '$lib/dropdown.svelte';
	import Icon from '$lib/icon.svelte';

	export let search_query;

	let user_key = '';
	let entity_type = 'all';
	let action = 'all';
	let entity_key = '';
	let search = `${user_key}:${entity_type}:${action}:${entity_key}`;
	let drop_1;
	let drop_2;

	export const set_value = ({ u = '', e = '' }) => {
		user_key = u || user_key;
		entity_key = e || entity_key;
	};

	onMount(() => {
		if ($page.url.searchParams.has('search')) {
			let temp = $page.url.searchParams.get('search');
			temp = temp.split(':');
			if (temp.length == 4) {
				user_key = temp[0];
				entity_type = temp[1];
				action = temp[2];
				entity_key = temp[3];
				search = `${user_key}:${entity_type}:${action}:${entity_key}`;
				drop_1.set(entity_type);
				drop_2.set(action);
			}
		}
	});

	const submit = (clear = false) => {
		if (clear) {
			user_key = '';
			entity_type = 'all';
			action = 'all';
			entity_key = '';
		}

		let check = `${search}`;
		search = `${user_key}:${entity_type || 'all'}:${action || 'all'}:${entity_key}`;
		if (search != check) {
			set_state('search', search != ':all:all:' ? search : '');
		}
	};
</script>

<section>
	{#if $user.access.includes('log:view')}
		<Search
			non_default
			placeholder="Search for User"
			bind:search={user_key}
			on:clear={() => {
				user_key = '';
			}}
		>
			<Button
				on:click={() => {
					set_value({ u: $user.key });
				}}
			>
				Me
			</Button>
		</Search>
	{/if}

	<div class="line">
		<Drop
			wide
			list={Object.keys(search_query)}
			default_value="all"
			bind:this={drop_1}
			on:change={(e) => {
				entity_type = e.target.value;
				action = 'all';
				drop_2.set(action);
			}}
		/>
		<Drop
			wide
			list={search_query[entity_type]}
			default_value="all"
			bind:this={drop_2}
			on:change={(e) => {
				action = e.target.value;
			}}
		/>
	</div>
	<div class="line">
		<Search
			non_default
			placeholder="Search for {entity_type}"
			bind:search={entity_key}
			on:clear={() => {
				entity_key = '';
			}}
		>
			<Button
				disabled={`${user_key}:${entity_type}:${action}:${entity_key}` == search}
				on:click={() => {
					submit();
				}}
			>
				<Icon icon="search" />
			</Button>
			<Button
				extra="hover_red"
				disabled={`${user_key}:${entity_type}:${action}:${entity_key}` == ':all:all:'}
				on:click={() => {
					submit(true);
				}}
			>
				<Icon icon="close" />
			</Button>
		</Search>
	</div>
</section>

<style>
	section {
		display: flex;
		flex-direction: column;
		gap: var(--sp1);
	}
	.line {
		display: flex;
		gap: var(--sp1);
		align-items: center;
	}
</style>
