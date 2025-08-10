<script>
	import { flip } from 'svelte/animate';
	import { cubicInOut } from 'svelte/easing';
	import { module, app } from '$lib/store.svelte.js';

	import { Content } from '$lib/layout';
	import One from './one.svelte';
	import { Button } from '$lib/button';
	import { Meta, Icon2, Log, Dropdown, Pagination, Search, UpdateUrl } from '$lib/macro';

	import Add from './_add.svelte';

	import Tags from './tags.svelte';
	import FilterNote from './filter_note.svelte';

	import { PageNote } from '$lib/info';

	let { data } = $props();
	let posts = $derived(data.posts);
	let total_page = $derived(data.total_page);
	let order_by = $derived(data.order_by);
	let _status = $derived(data._status);

	const update = (a, b) => {
		posts = a;
		total_page = b;
	};

	let man = '';

	import { page } from '$app/state';
</script>

<Log entity_type={'page'} />
<!-- <UpdateUrl /> -->
<Meta
	title="Posts"
	description="This page showcases a collection of interesting blogs and projects that I have worked on"
/>

<section class="background">
	<Content>
		<div class="title">
			<strong class="ititle">
				Post{posts.length > 1 ? 's' : ''}
			</strong>
			{#if app.user.access.includes('post:add')}
				<div class="line">
					<Dropdown list={_status} name="status" />

					<Button extra="outline" onclick={() => module.open(Add, { update })}>
						<Icon2 icon="add" />
						Add
					</Button>
				</div>
			{/if}
		</div>

		<div class="search_bar">
			<Search />
			<Dropdown list={order_by} name="order" icon="sort" novalue />
		</div>

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

		<Pagination {total_page} />
		<Tags />
	</Content>
</section>

<style>
	.background {
		background-color: var(--bg2);
		padding: 1px 0;
	}

	.title {
		display: flex;
		justify-content: space-between;
		align-items: center;

		margin-top: var(--sp3);
	}

	.search_bar {
		margin: var(--sp2) 0;
		display: flex;
		gap: var(--sp1);
		align-items: center;
	}

	.items {
		margin: var(--sp2) 0;
		display: grid;
		gap: var(--sp2);
	}

	.line {
		display: flex;
		gap: var(--sp1);
		align-items: center;
	}
	@media screen and (min-width: 550px) {
		.items {
			grid-template-columns: 1fr 1fr;
		}
	}
</style>
