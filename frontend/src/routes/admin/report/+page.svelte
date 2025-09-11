<script>
	import { flip } from 'svelte/animate';
	import { cubicInOut } from 'svelte/easing';
	import { page } from '$app/state';
	import { onMount } from 'svelte';
	import { page_state } from '$lib/store.svelte.js';

	import { Content } from '$lib/layout';
	import { BackButton } from '$lib/button';
	import { Pagination, Dropdown, Search } from '$lib/input';
	import { PageNote } from '$lib/info';
	import { Meta, Log, Icon } from '$lib/macro';
	import Item from './item.svelte';

	let { data } = $props();
	let items = $derived(data.items);
	let total_page = $derived(data.total_page);
	let { order_by } = data;
	let { _type } = data;
	let { _status } = data;
	let search = $state({
		type: '',
		status: '',
		search: '',
		order: 'latest',
		page_no: 1
	});

	onMount(() => {
		if (page_state.searchParams.type) {
			search.type = page_state.searchParams.type;
		}
		if (page_state.searchParams.status) {
			search.status = page_state.searchParams.status;
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

	const update = (key) => {
		let temp = [];
		for (const x of items) {
			if (x.user.key == key) continue;
			temp.push(x);
		}
		items = temp;
		page_state.refresh();
	};
</script>

<Log entity_type={'page'} />
<Meta title="All Users" />

<Content --content-background-color="var(--bg2)">
	<div class="line space">
		<div class="line">
			<BackButton />
			<div class="page_title">
				Report{items.length > 1 ? 's' : ''}
			</div>
		</div>

		<Dropdown
			icon2="chevron-down"
			list={['all', ..._type]}
			bind:value={search.type}
			onchange={(v) => {
				v = v == 'all' ? '' : v;

				search.page_no = 1;
				page_state.set({ type: v });
			}}
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
			<Item {item} {update} />
		</div>
	{:else}
		<PageNote>
			<Icon icon="search" size="50" />
			No report found
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
