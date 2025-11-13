<script>
	import { flip } from 'svelte/animate';
	import { cubicInOut } from 'svelte/easing';
	import { module, app, page_state } from '$lib/store.svelte.js';
	import { onMount } from 'svelte';
	import { page } from '$app/state';

	import { Content } from '$lib/layout';
	import { Button, Radio } from '$lib/button';
	import { Dropdown, Search, Pagination } from '$lib/input';
	import { PageNote } from '$lib/info';
	import { Meta, Icon, Log } from '$lib/macro';
	import Item from './item.svelte';

	import Add from './_add.svelte';
	import Tags from './tags.svelte';
	import FilterNote from './filter_note.svelte';

	let { data } = $props();
	let items = $derived(data.items);

	let total_page = $derived(data.total_page);
	let order_by = $derived(data.order_by);
	let _status = $derived(data._status);
	let search = $state({ order: 'latest', search: '', tag: '', status: 'active', page_no: 1 });

	const update = (a, b) => {
		items = a;
		total_page = b;
	};

	onMount(() => {
		if (page_state.searchParams.order) {
			search.order = page_state.searchParams.order;
		}
		if (page_state.searchParams.search) {
			search.search = page_state.searchParams.search;
		}
		if (page_state.searchParams.tag) {
			search.tag = page_state.searchParams.tag;
		}
		if (page_state.searchParams.status) {
			search.status = page_state.searchParams.status;
		}
		if (page_state.searchParams.page_no) {
			search.page_no = page_state.searchParams.page_no;
		}

		page.url.search = new URLSearchParams(page_state.searchParams);
		window.history.replaceState(history.state, '', page.url.href);
	});

	let tags = $state();
</script>

<Log entity_type={'page'} />
<Meta
	title="Posts"
	description="This page showcases a collection of interesting blogs and projects that I have worked on"
/>

<Content
	--content-background-color="var(--bg2)"
	--content-height="auto"
	--content-padding-bottom="0"
>
	<div class="line space">
		<div class="page_title">
			Post{items.length > 1 ? 's' : ''}
		</div>
		{#if app.user.access.includes('post:add')}
			<div class="line">
				<Radio
					--button-outline-color-hover="var(--ft1)"
					list={_status}
					bind:value={search.status}
					ondone={(v) => {
						search.page_no = 1;
						v = v == 'active' ? '' : v;
						page_state.set({ status: v });
					}}
				></Radio>
				<Button icon="plus" extra="outline" onclick={() => module.open(Add, { update })}>
					Add
				</Button>
			</div>
		{/if}
	</div>

	<div class="line nowrap">
		<Search
			bind:value={search.search}
			ondone={(v) => {
				search.page_no = 1;
				page_state.set({ search: v });
			}}
		></Search>

		<Tags
			bind:this={tags}
			bind:value={search.tag}
			ondone={(v) => {
				search.page_no = 1;
				page_state.set({ tag: v });
			}}
		/>
	</div>

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

	<FilterNote
		onclick={() => {
			search.page_no = 1;
			search.search = '';
			search.tag = '';
			tags.clear();
			page_state.set({ search: '', tag: '' });
		}}
	/>
</Content>

<Content --content-background-color="var(--bg2)" --content-padding-top="1px" --content-width="1500px">
	{#if items.length}
		<section class="items">
			{#each items as item (item.key)}
				<div animate:flip={{ delay: 0, duration: 500, easing: cubicInOut }}>
					<Item {item} />
				</div>
			{/each}
		</section>
	{:else}
		<PageNote>
			<Icon icon="search" size="50" />
			No post found
		</PageNote>
	{/if}

	<Pagination
		{total_page}
		bind:value={search.page_no}
		ondone={(v) => {
			if (v == 1) v = 0;
			page_state.set({ page_no: v });
		}}
	></Pagination>
</Content>

<style>
	.items {
		margin: var(--sp2) 0;
		display: grid;
		gap: var(--sp2);
	}

	@media screen and (min-width: 550px) {
		.items {
			grid-template-columns: repeat(2, 1fr);
		}
	}

	@media screen and (min-width: 850px) {
		.items {
			grid-template-columns: repeat(3, 1fr);
		}
	}

	@media screen and (min-width: 1200px) {
		.items {
			grid-template-columns: repeat(4, 1fr);
		}
	}
</style>
