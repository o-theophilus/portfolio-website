<script>
	import { onMount } from 'svelte';
	import { app, page_state } from '$lib/store.svelte.js';

	import { Button } from '$lib/button';
	import { Dropdown, Search } from '$lib/input';
	import { Icon2 } from '$lib/macro';
	import { Row } from '$lib/layout';

	let { search = $bindable(), search_query } = $props();
	let subbmited = $state({ user_key: '', entity_type: 'all', action: 'all', entity_key: '' });
	let empty = $state({ user_key: '', entity_type: 'all', action: 'all', entity_key: '' });

	onMount(() => {
		if (!page_state.searchParams.search) {
			search = { ...empty };
			subbmited = { ...empty };
			return;
		}
		let temp = page_state.searchParams.search.split(':');
		if (temp.length != 4) {
			search = { ...empty };
			subbmited = { ...empty };
			return;
		}
		search = {
			user_key: temp[0],
			entity_type: temp[1],
			action: temp[2],
			entity_key: temp[3]
		};
		subbmited = { ...search };
	});

	const to_string = (x) =>
		`${x.user_key}:${x.entity_type || 'all'}:${x.action || 'all'}:${x.entity_key}`;

	const submit = () => {
		subbmited = { ...search };
		let ss = to_string(search);
		page_state.set({ search: ss == to_string(empty) ? '' : ss });
	};
</script>

<section class="search">
	{#if app.user.access.includes('log:view')}
		<Search
			non_default
			placeholder="Search for User"
			bind:value={search.user_key}
			onclear={() => {
				search.user_key = null;
			}}
		>
			<Button onclick={() => (search.user_key = app.user.key)}>Me</Button>
		</Search>
	{/if}

	<Row nowrap --row-gap="8px">
		<Dropdown
			icon="chevron-down"
			list={Object.keys(search_query)}
			bind:value={search.entity_type}
			onchange={() => {
				search.action = 'all';
			}}
			--select-width="100%"
		/>
		<Dropdown
			icon="chevron-down"
			list={search_query[search.entity_type]}
			bind:value={search.action}
			--select-width="100%"
		/>
	</Row>

	<Row nowrap --row-gap="8px">
		<Search
			non_default
			placeholder="Search for {search.entity_type}"
			bind:value={search.entity_key}
			onclear={() => {
				search.entity_key = null;
			}}
		></Search>
		<Button disabled={to_string(search) == to_string(subbmited)} onclick={submit}>
			<Icon2 icon="search" />
		</Button>
		<Button
			disabled={to_string(search) == to_string(empty) && to_string(subbmited) == to_string(empty)}
			extra="hover_red"
			onclick={() => {
				search.user_key = '';
				search.entity_type = 'all';
				search.action = 'all';
				search.entity_key = '';
				submit();
			}}
		>
			<Icon2 icon="x" />
		</Button>
	</Row>
</section>

<style>
	section {
		display: flex;
		flex-direction: column;
		margin: var(--sp2) 0;
	}
</style>
