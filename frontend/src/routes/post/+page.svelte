<script>
	import { module, user, portal } from '$lib/store.js';

	import Content from '$lib/content.svelte';
	import Item from './item.svelte';
	import Meta from '$lib/meta.svelte';
	import Button from '$lib/button/button.svelte';
	import Icon from '$lib/icon.svelte';

	import Add from './_add.svelte';
	import Tags from './tags.svelte';
	import Note from './filter_note.svelte';

	import OrderBy from './order_by.svelte';
	import Pagination from './pagination.svelte';
	import Search from './search.svelte';

	import UpdateUrl from './update_url.svelte';

	export let data;
	$: posts = data.posts;
	$: total_page = data.total_page;
	let { order_by } = data;
	let { post_status } = data;

	$: if ($portal) {
		if ($portal.for == 'posts') {
			posts = $portal.data;
		}

		$portal = {};
	}
</script>

<UpdateUrl />
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
			{#if $user.permissions.includes('post:add')}
				<div class="line">
					<OrderBy list={post_status} name="status" />

					<Button
						extra="outline"
						on:click={() => {
							$module = {
								module: Add
							};
						}}
					>
						<Icon icon="add" />
						Add
					</Button>
				</div>
			{/if}
		</div>

		<div class="search_bar">
			<Search />
			<OrderBy list={order_by} name="order" button />
		</div>

		<Note />

		<section class="items">
			{#each posts as post}
				<Item {post} />
			{:else}
				No post found
			{/each}
		</section>

		<Pagination {total_page} />
		<Tags />
	</Content>
</section>

<style>
	.background {
		background-color: var(--ac4);
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
	@media screen and (min-width: 600px) {
		.items {
			grid-template-columns: 1fr 1fr;
		}
	}
</style>
