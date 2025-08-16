<script>
	import { onMount } from 'svelte';
	import { app, page_state } from '$lib/store.svelte.js';

	import { Button } from '$lib/button';
	import { Dropdown, Search } from '$lib/input';
	import { Icon2 } from '$lib/macro';
	import { Row } from '$lib/layout';

	let { search_query = {} } = $props();

	let empty = $state({ user_key: '', entity_type: 'all', action: 'all' });
	let search = $state({ ...empty });
	let subbmited = $state({ ...empty });

	onMount(() => {
		if (!page_state.searchParams.search) {
			search = { ...empty };
			subbmited = { ...empty };
			return;
		}
		let temp = page_state.searchParams.search.split(':');
		if (temp.length != 3) {
			search = { ...empty };
			subbmited = { ...empty };
			return;
		}
		search = {
			user_key: temp[0],
			entity_type: temp[1],
			action: temp[2]
		};
		subbmited = { ...search };
	});

	const submit = () => {
		subbmited = { ...search };

		let ss = `${search.user_key}:${search.entity_type || 'all'}:${search.action || 'all'}`;
		if (JSON.stringify(search) == JSON.stringify(empty)) ss = '';
		page_state.set({ search: ss });
	};
</script>

<section class="search">
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
			bind:value={search.user_key}
			onclear={() => {
				search.user_key = null;
			}}
		></Search>
		<Button
			icon="search"
			disabled={JSON.stringify(search) == JSON.stringify(subbmited)}
			onclick={submit}
		></Button>
		<Button
			icon="x"
			--button-background-color-hover="red"
			disabled={JSON.stringify(search) == JSON.stringify(empty) &&
				JSON.stringify(subbmited) == JSON.stringify(empty)}
			onclick={() => {
				search.user_key = '';
				search.entity_type = 'all';
				search.action = 'all';
				if (JSON.stringify(subbmited) != JSON.stringify(empty)) submit();
			}}
		></Button>
	</Row>
</section>

<style>
	section {
		display: flex;
		flex-direction: column;
		margin: var(--sp2) 0;
	}
</style>
