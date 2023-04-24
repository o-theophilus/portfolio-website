<script>
	import Content from '$lib/content.svelte';
	import Tags from '$lib/tags.svelte';
	import Meta from '$lib/meta.svelte';

	export let data;
	let { tags } = data;
</script>

<Meta title="Tags" description="tags" image="/favicon.png" />

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
