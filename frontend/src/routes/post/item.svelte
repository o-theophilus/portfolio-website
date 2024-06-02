<script>
	import { timeAgo } from '$lib/store.js';
	import { onMount } from 'svelte';

	export let post;

	let time = timeAgo(post.date);
	onMount(() => {
		const intervalId = setInterval(() => {
			time = timeAgo(post.date);
		}, 1000);

		return () => clearInterval(intervalId);
	});
</script>

<a href="/{post.slug}" data-sveltekit-preload-data>
	<div class="img">
		<img src={post.photos[0] || ''} alt={post.title} onerror="this.src='/site/no_photo.png'" />
	</div>
	<div class="title">
		{post.title}
	</div>
	<div class="description">
		{post.description}
	</div>
	<div class="date">
		{time}
	</div>
</a>

<style>
	a {
		padding: var(--sp3);

		background-color: var(--ac8);
		color: var(--ac2);
		text-decoration: none;

		border-radius: var(--sp1);
		border: 2px solid transparent;

		transition: background-color var(--trans1), border-color var(--trans1);
	}
	a:hover {
		border-color: var(--ac2);
	}

	.img {
		border-radius: var(--sp1);
		overflow: hidden;
	}
	img {
		display: block;

		width: 100%;
		object-fit: cover;
		aspect-ratio: 1 / 1;
		background-color: var(--ac7);

		transition: transform var(--animTime3);
		transition-timing-function: ease-in-out;
	}
	a:hover img {
		transform: scale(1.2);
	}
	.title {
		margin: var(--sp2) 0;
		color: var(--cl1);
		font-size: large;
		font-weight: 800;
	}

	.description {
		margin: var(--sp2) 0;
		color: var(--ac1);
		transition: color var(--trans1);
	}
	
	.date {
		font-size: small;
		transition: color var(--trans1);
	}
</style>
