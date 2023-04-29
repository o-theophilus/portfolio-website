<script>
	import Content from '$lib/content.svelte';
	import Tags from '$lib/tags.svelte';
	import Meta from '$lib/meta.svelte';

	export let data;
	let { tags } = data;
</script>

<Meta
	title="Tags"
	description="This page features tags that allow for easy filtering of similar and related posts"
/>

<Content>
	<br />
	<strong class="big">Tag{tags.length > 1 && 's'}</strong>
	<br /><br />

	<Tags {tags} />
	<br />
</Content>

<style>
	.big {
		text-transform: capitalize;
		color: var(--accent1);
	}
</style>
