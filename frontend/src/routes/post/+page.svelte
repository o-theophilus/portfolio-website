<script>
	import { module, user, portal } from '$lib/store.js';

	import Content from '$lib/content.svelte';
	import ItemBox from '$lib/item_box.svelte';
	import Meta from '$lib/meta.svelte';
	import Button from '$lib/button.svelte';

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
			Post{posts.length > 1 ? 's' : ''}
		</div>

		<Search />
		<OrderBy list={order_by} name="order" />
		<OrderBy list={post_status} name="status" />

		<br />
		{#if $user.permissions.includes('post:add')}
			<Button
				on:click={() => {
					$module = {
						module: Add
					};
				}}
			>
				Add
			</Button>
			<br /><br />
		{/if}

		<Note />
		<section class="block">
			{#each posts as post}
				<ItemBox {post} />
			{:else}
				No post found
			{/each}
		</section>

		<br />
		<Tags />
		<br />
	</Content>

	<Pagination {total_page} />
</section>

<style>
	.background {
		background-color: var(--ac4);
		padding-top: 1px;
	}

	.title {
		display: flex;
		justify-content: space-between;
		align-items: center;

		margin-top: var(--sp3);

		font-size: x-large;
		font-weight: 800;
		color: var(--ac1);
	}

	.block {
		display: grid;
		gap: var(--sp2);
	}

	@media screen and (min-width: 600px) {
		.block {
			grid-template-columns: 1fr 1fr;
		}
	}
</style>
