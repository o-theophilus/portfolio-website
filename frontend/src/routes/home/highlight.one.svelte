<script>
	import Tag from '$lib/button/tag.svelte';

	export let post;
</script>

<a href="/{post.slug}">
	<img src={post.photos[0] || '/no_photo.png'} alt={post.title} />
</a>

<div class="title">
	{post.title}
</div>
<div class="desc">
	{post.description}
</div>

{#each post.tags as tag}
	<Tag>
		{tag}
	</Tag>
{/each}

<style>
	a {
		display: block;
		position: relative;
		flex-shrink: 0;

		height: 30vh;
		width: min(calc(100vw - var(--sp2) * 2), 400px);

		border-radius: var(--sp1);
		overflow: hidden;

		transition: all var(--aTime);
		transition-timing-function: ease-in-out;

		border: 2px solid transparent;
	}

	img {
		display: block;
		width: 100%;
		height: 100%;

		object-fit: cover;
		background-color: var(--bg2);

		transition: transform var(--aTime);
		transition-timing-function: ease-in-out;
	}
</style>
