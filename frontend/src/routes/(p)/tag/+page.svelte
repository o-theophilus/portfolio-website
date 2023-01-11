<script>
	import Content from '$lib/comp/content.svelte';
	import Tags from '$lib/comp/tags.svelte';
	import Meta from '$lib/comp/meta.svelte';

	export let data;
	let { tags } = data;
</script>

<Meta title="Tags" description="tags" image="/site/home.jpg" />

<Content>
	<br />
	<strong class="big">Tag{tags.length > 1 && 's'}</strong>
	<br /><br />

	<Tags {tags} />
</Content>

<style>
	strong {
		text-transform: capitalize;
	}
	.big {
		text-transform: uppercase;
	}
</style>
