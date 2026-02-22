<script>
	import { replaceState } from '$app/navigation';
	import { Button, Radio } from '$lib/button';
	import { PageNote } from '$lib/info';
	import { Dropdown, Pagination, Search } from '$lib/input';
	import { Content } from '$lib/layout';
	import { Icon, Log, Meta } from '$lib/macro';
	import { app, module, page_state } from '$lib/store.svelte.js';
	import { onMount } from 'svelte';
	import { flip } from 'svelte/animate';
	import { cubicInOut } from 'svelte/easing';
	import Add from './_add.svelte';
	import FilterNote from './filter_note.svelte';
	import Item from './item.svelte';
	import Tags from './tags.svelte';

	let { data } = $props();
	let posts = $derived(data.posts);
	let total_page = $derived(data.total_page);
	let order_by = $derived(data.order_by);
	let _status = $derived(data._status);
	let searchParams = $state({ ...data.searchParams });
	let defaultParams = $state(data.searchParams);

	const update = (a, b) => {
		posts = a;
		total_page = b;
	};

	onMount(() => {
		const sp = page_state.searchParams;
		if (Object.keys(sp).length) {
			queueMicrotask(() => replaceState(`?${new URLSearchParams(sp)}`));
			for (const key of Object.keys(searchParams)) {
				if (sp[key]) searchParams[key] = sp[key];
			}
		}
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
			Post{posts.length > 1 ? 's' : ''}
		</div>
		{#if app.user.access.includes('post:add')}
			<div class="line">
				<Radio
					--button-outline-color-hover="var(--ft1)"
					list={_status}
					bind:value={searchParams.status}
					ondone={(v) => {
						searchParams.page_no = 1;
						page_state.set({ status: v == defaultParams.status ? '' : v });
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
			bind:value={searchParams.search}
			ondone={(v) => {
				searchParams.page_no = 1;
				page_state.set({ search: v });
			}}
		></Search>

		<Tags
			bind:this={tags}
			bind:value={searchParams.tag}
			ondone={(v) => {
				searchParams.page_no = 1;
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
		bind:value={searchParams.order}
		onchange={(v) => {
			searchParams.page_no = 1;
			page_state.set({ order: v == defaultParams.order ? '' : v });
		}}
	/>

	<FilterNote
		onclick={() => {
			searchParams.page_no = 1;
			searchParams.search = '';
			searchParams.tag = '';
			tags.clear();
			page_state.set({ search: '', tag: '' });
		}}
	/>
</Content>

<Content
	--content-background-color="var(--bg2)"
	--content-padding-top="1px"
	--content-width="1500px"
>
	{#if posts.length}
		<section class="items">
			{#each posts as item (item.key)}
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
		bind:value={searchParams.page_no}
		ondone={(v) => {
			if (v == 1) v = 0;
			page_state.set({ page_no: v });
		}}
	></Pagination>
</Content>

<style>
	.items {
		margin: 16px 0;
		display: grid;
		gap: 16px;
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
