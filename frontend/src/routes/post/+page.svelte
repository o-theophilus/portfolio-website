<script>
	import { module, _user, _portal } from '$lib/store.js';

	import Content from '$lib/content.svelte';
	import ItemBox from '$lib/item_box.svelte';
	import Meta from '$lib/meta.svelte';
	import Button from '$lib/button.svelte';
	import Add from './__add__.svelte';
	import Sort from './sort.svelte';
	import Tags from '$lib/tags.svelte';

	export let data;
	let { posts } = data;
	let { tags } = data;

	$: if ($_portal) {
		if ($_portal.for == 'posts') {
			posts = $_portal.data;
		}

		$_portal = {};
	}
</script>

<Meta
	title="Posts"
	description="This page showcases a collection of interesting blogs and projects that I have worked on"
/>

<section class="background">
	<Content>
		<br />

		<div class="title">
			<strong class="big">Post{posts.length > 1 ? 's' : ''}</strong>
			<Sort />
		</div>

		<br />
		{#if $_user.roles.includes('admin')}
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
</section>

<style>
	.title {
		display: flex;
		justify-content: space-between;
		align-items: center;
	}
	.background {
		background-color: var(--accent4);
	}
	.block {
		display: grid;
		gap: var(--gap2);
	}
	.big {
		color: var(--accent1);
		text-transform: capitalize;
	}

	@media screen and (min-width: 600px) {
		.block {
			grid-template-columns: 1fr 1fr;
		}
	}
</style>
