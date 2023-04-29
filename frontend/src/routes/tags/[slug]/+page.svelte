<script>
	import { page } from '$app/stores';
	import Content from '$lib/content.svelte';
	import ItemBox from '$lib/item_box.svelte';
	import Meta from '$lib/meta.svelte';
	import Tags from '$lib/tags.svelte';

	export let data;
	$: posts = data.posts;
	let { tags } = data;
</script>

<Meta
	title="{$page.params.slug} - Tags"
	description="This page displays posts that are relevant to the selected tag: {$page.params.slug}"
/>

<section class="background">
	<Content>
		<br />
		<strong class="big">Tag: <span class="color1"> {$page.params.slug}</span></strong>
		<br /><br />
		{#if posts.length > 0}
			<section class="block">
				{#each posts as post}
					<ItemBox {post} />
				{/each}
			</section>
		{:else}
			No post found
			<br />
		{/if}
		<br />
		<Tags {tags} />
		<br />
	</Content>
</section>

<style>
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
