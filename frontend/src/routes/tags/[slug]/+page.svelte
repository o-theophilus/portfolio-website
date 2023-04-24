<script>
	import { page } from '$app/stores';
	import Content from '$lib/content.svelte';
	import ItemBox from '$lib/item_box.svelte';
	import Meta from '$lib/meta.svelte';
	import Tags from '$lib/tags.svelte';

	export let data;
	$: blogs = data.blogs;
	$: projects = data.projects;
	let { tags } = data;
</script>

<Meta title="{$page.params.slug} - Tags" description="tags" image="/favicon.png" />

<section class="background">
	<Content>
		<br />
		<strong class="big">Tag: <span class="color1"> {$page.params.slug}</span></strong>
		<br />
		{#if blogs.length > 0}
			<br /><br />
			<strong class="big">Blog{blogs.length > 1 ? 's' : ''}</strong>
			<br /><br />
			<section class="block">
				{#each blogs as post}
					<ItemBox {post} />
				{/each}
			</section>
		{/if}
		{#if projects.length > 0}
			<br /><br />
			<strong class="big">Project{projects.length > 1 ? 's' : ''}</strong>
			<br /><br />
			<section class="block">
				{#each projects as post}
					<ItemBox {post} />
				{/each}
			</section>
		{/if}

		{#if blogs.length + projects.length == 0}
			<br />
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
