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
	import { Meta, Icon2, Log } from '$lib/macro';
	import One from './one.svelte';

	import Add from './_add.svelte';
	import Tags from './tags.svelte';
	import FilterNote from './filter_note.svelte';

	let { data } = $props();
	let posts = $derived(data.posts);
	let total_page = $derived(data.total_page);
	let order_by = $derived(data.order_by);
	let _status = $derived(data._status);
	let search = $state({ order: 'latest', search: '', status: 'active', page_no: 1 });

	const update = (a, b) => {
		posts = a;
		total_page = b;
	};

	onMount(() => {
		if (page_state.searchParams.order) {
			search.order = page_state.searchParams.order;
		}
		if (page_state.searchParams.search) {
			search.search = page_state.searchParams.search;
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
</script>

<Log entity_type={'page'} />
<Meta
	title="Posts"
	description="This page showcases a collection of interesting blogs and projects that I have worked on"
/>

<section class="background">
	<Content>
		<div class="line space">
			<div class="page_title">
				Post{posts.length > 1 ? 's' : ''}
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

		<Search
			bind:value={search.search}
			ondone={(v) => {
				search.page_no = 1;
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

		<FilterNote />

		{#if posts.length}
			<section class="items">
				{#each posts as post (post.key)}
					<div animate:flip={{ delay: 0, duration: 500, easing: cubicInOut }}>
						<One {post} />
					</div>
				{/each}
			</section>
		{:else}
			<PageNote>
				<Icon2 icon="search" size="50" />
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
		<Tags />
	</Content>
</section>

<style>
	.background {
		background-color: var(--bg2);
		padding: 1px 0;
	}

	.items {
		margin: var(--sp2) 0;
		display: grid;
		gap: var(--sp2);
	}

	@media screen and (min-width: 550px) {
		.items {
			grid-template-columns: 1fr 1fr;
		}
	}
</style>
