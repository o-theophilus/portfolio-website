<script>
	import { page } from '$app/stores';
	import Content from '$lib/comp/content.svelte';
	import ItemBox from '$lib/comp/item_box.svelte';
	import Meta from '$lib/comp/meta.svelte';
	import Tags from '$lib/comp/tags.svelte';

	export let data;
	$: blogs = data.blogs;
	$: projects = data.projects;
	let { tags } = data;
</script>

<Meta title="{$page.params.slug} - Tags" description="tags" image="/site/home.jpg" />

<Content>
	<br />
	<strong class="big">{$page.params.slug} - Tag</strong>
	<br />
	{#if blogs.length > 0}
		{@const post_type = 'blog'}
		<br />
		<strong class="big">{post_type}{blogs.length > 1 ? 's' : ''}</strong>
		<br /><br />
		<section>
			{#each blogs as post}
				<ItemBox {post} {post_type} />
			{/each}
		</section>
	{/if}
	<br /> <br />
	{#if projects.length > 0}
		{@const post_type = 'project'}
		<br />
		<strong class="big">{post_type}{projects.length > 1 ? 's' : ''}</strong>
		<br /><br />
		<section>
			{#each projects as post}
				<ItemBox {post} {post_type} />
			{/each}
		</section>
	{/if}

	{#if blogs.length + projects.length == 0}
		No post found
	{/if}
	<br /> <br /> <br />
	<Tags {tags} />
</Content>

<style>
	section {
		display: flex;
		flex-direction: column;

		gap: var(--gap4);
	}
	.big {
		text-transform: capitalize;
	}
</style>
