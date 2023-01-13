<script>
	import { api_url, is_admin } from '$lib/store.js';

	export let post;
	export let post_type;

	let href = `/${post_type}/${post.slug}`;
	let target = '';
	if (post.format == 'url' && !$is_admin) {
		href = post.content;
		target = '_blank';
	}
</script>

<a {href} {target} data-sveltekit-preload-data on:mouseenter on:mouseleave>
	<img
		src="{api_url}/{post.photos[0] || ''}"
		alt={post.title}
		onerror="this.src='/site/no_photo.png'"
	/>
</a>

<style>
	a {
		display: block;
		position: relative;
		flex-shrink: 0;

		height: 30vh;
		width: 400px;

		/* text-decoration: none; */

		border-radius: var(--gap1);
		overflow: hidden;

		transition: all var(--animTime1);
		transition-timing-function: ease-in-out;
	}
	a:hover {
		transform: scale(1.2);
	}

	img {
		display: block;
		width: 100%;
		height: 100%;

		object-fit: cover;
		background-color: var(--foreground);
	}
</style>
