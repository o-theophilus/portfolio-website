<script>
	import { flip } from 'svelte/animate';
	import { cubicInOut } from 'svelte/easing';
	import { onMount } from 'svelte';
	import { page } from '$app/state';
	import { app, page_state } from '$lib/store.svelte.js';

	import { Button } from '$lib/button';
	import { Dropdown, Pagination, Search } from '$lib/input';
	import { Content } from '$lib/layout';
	import { PageNote } from '$lib/info';
	import { Meta, Icon } from '$lib/macro';
	import Item from './item.svelte';

	let { data } = $props();
	let items = $derived(data.items);
	let total_page = $derived(data.total_page);
	let search_query = $derived(data.search_query);

	let search = $state({
		u_search: '',
		entity_type: 'all',
		action: 'all',
		e_search: '',
		page_no: 1
	});

	onMount(() => {
		if (page_state.searchParams.u_search) {
			search.u_search = page_state.searchParams.u_search;
		}
		if (page_state.searchParams.entity_type) {
			search.entity_type = page_state.searchParams.entity_type;
		}
		if (page_state.searchParams.action) {
			search.action = page_state.searchParams.action;
		}
		if (page_state.searchParams.e_search) {
			search.e_search = page_state.searchParams.e_search;
		}
		if (page_state.searchParams.page_no) {
			search.page_no = page_state.searchParams.page_no;
		}

		page.url.search = new URLSearchParams(page_state.searchParams);
		window.history.replaceState(history.state, '', page.url.href);
	});
</script>

<Meta title="Logs" />

<Content>
	<div class="page_title">Logs</div>

	<br />

	{#if app.user.access.includes('log:view')}
		<div class="line nowrap">
			<Search
				placeholder="Search for User"
				bind:value={search.u_search}
				ondone={(v) => {
					search.page_no = 1;
					page_state.set({ u_search: v });
				}}
			></Search>
			<Button onclick={() => (search.u_search = app.user.key)}>Me</Button>
		</div>
	{/if}

	<div class="line nowrap">
		<Dropdown
			icon2="chevron-down"
			list={Object.keys(search_query)}
			bind:value={search.entity_type}
			onchange={(v) => {
				v = v == 'all' ? '' : v;
				search.action = 'all';
				search.page_no = 1;
				page_state.set({ entity_type: v, action: '' });
			}}
			--select-width="100%"
		/>
		<Dropdown
			icon2="chevron-down"
			list={search_query[search.entity_type]}
			bind:value={search.action}
			onchange={(v) => {
				v = v == 'all' ? '' : v;
				search.page_no = 1;
				page_state.set({ action: v });
			}}
			--select-width="100%"
		/>
	</div>

	<Search
		placeholder="Search for {search.entity_type}"
		bind:value={search.e_search}
		ondone={(v) => {
			search.page_no = 1;
			page_state.set({ e_search: v });
		}}
	></Search>

	{#each items as item (item.key)}
		<div animate:flip={{ delay: 0, duration: 250, easing: cubicInOut }}>
			<Item {item} bind:search />
		</div>
	{:else}
		<PageNote>
			<Icon icon="search" size="50" />
			No log found
		</PageNote>
	{/each}

	<Pagination
		{total_page}
		bind:value={search.page_no}
		ondone={(v) => {
			if (v == 1) v = 0;
			page_state.set({ page_no: v });
		}}
	></Pagination>
</Content>
