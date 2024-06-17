<script>
	import Avatar from '$lib/avatar.svelte';

	export let post;
</script>

<class class="block">
	<Avatar name={post.author_name} photo={post.author_photo} />

	{post.author_name} | Author
</class>

<style>
	.block {
		display: flex;
		gap: var(--sp2);
		align-items: center;
	}
</style>
