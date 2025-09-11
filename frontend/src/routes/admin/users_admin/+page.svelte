<script>
	import { flip } from 'svelte/animate';
	import { cubicInOut } from 'svelte/easing';
	import { page } from '$app/state';
	import { onMount } from 'svelte';
	import { page_state } from '$lib/store.svelte.js';

	import { Content } from '$lib/layout';
	import { Pagination, Dropdown, Search } from '$lib/input';
	import { BackButton } from '$lib/button';
	import { PageNote } from '$lib/info';
	import { Meta, Log, Icon } from '$lib/macro';
	import Item from '../users/item.svelte';

	let { data } = $props();
	let items = $derived(data.items);
	let total_page = $derived(data.total_page);
	let { search_query } = data;
	let { order_by } = data;
	let search = $state({
		entity_type: 'all',
		action: 'all',
		search: '',
		order: 'latest',
		page_no: 1
	});

	onMount(() => {
		if (page_state.searchParams.entity_type) {
			search.entity_type = page_state.searchParams.entity_type;
		}
		if (page_state.searchParams.action) {
			search.action = page_state.searchParams.action;
		}
		if (page_state.searchParams.search) {
			search.search = page_state.searchParams.search;
		}
		if (page_state.searchParams.order) {
			search.order = page_state.searchParams.order;
		}
		if (page_state.searchParams.page_no) {
			search.page_no = page_state.searchParams.page_no;
		}

		page.url.search = new URLSearchParams(page_state.searchParams);
		window.history.replaceState(history.state, '', page.url.href);
	});
</script>

<Log entity_type={'page'} />
<Meta title="Admin" description="Users with elevated Access" />

<Content>
	<div class="line">
		<BackButton />
		<div class="page_title">
			Admin{items.length > 1 ? 's' : ''}
		</div>
	</div>

	<br />
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
		bind:value={search.search}
		ondone={(v) => {
			page_state.set({ search: v });
		}}
	></Search>

	<Dropdown
		--select-height="10"
		--select-padding-x="0"
		--select-font-size="0.8rem"
		--select-background-color="transparent"
		--select-background-color-hover="transparent"
		--select-color-hover="var(--ft1)"
		--select-outline-color="transparent"
		list={order_by}
		icon="arrow-down-narrow-wide"
		icon2="chevron-down"
		bind:value={search.order}
		onchange={(v) => {
			search.page_no = 1;
			v = v == 'latest' ? '' : v;
			page_state.set({ order: v });
		}}
	/>

	{#each items as item (item.key)}
		<div animate:flip={{ delay: 0, duration: 250, easing: cubicInOut }}>
			<Item {item} />
		</div>
	{:else}
		<PageNote>
			<Icon icon="search" size="50" />
			No user found
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
