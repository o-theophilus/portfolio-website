<script>
	import { module, user, portal } from '$lib/store.js';

	import Content from '$lib/content.svelte';
	import ItemBox from '$lib/item_box.svelte';
	import Meta from '$lib/meta.svelte';
	import Button from '$lib/button.svelte';
	import Add from './_add.svelte';
	import Tags from '$lib/tags.svelte';
	import OrderBy from './order_by.svelte';
	import Pagination from './pagination.svelte';
	import UpdateUrl from './update_url.svelte';

	export let data;
	$: posts = data.posts;
	$: total_page = data.total_page;
	let { tags } = data;
	let { order_by } = data;
	let { post_status } = data;

	console.log(data);

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
		<br />

		<div class="title">
			<strong class="big">Post{posts.length > 1 ? 's' : ''}</strong>
			<OrderBy list={order_by} name="order" />
			<OrderBy list={post_status} name="status" />
		</div>

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

		<section class="block">
			{#each posts as post}
				<ItemBox {post} />
			{:else}
				No post found
			{/each}
		</section>

		<br />
		<Tags {tags} />
		<br />
	</Content>

	<Pagination {total_page} />
</section>

<style>
	.title {
		display: flex;
		justify-content: space-between;
		align-items: center;
	}
	.background {
		background-color: var(--ac4);
	}
	.block {
		display: grid;
		gap: var(--sp2);
	}
	.big {
		color: var(--ac1);
		text-transform: capitalize;
	}

	@media screen and (min-width: 600px) {
		.block {
			grid-template-columns: 1fr 1fr;
		}
	}
</style>
