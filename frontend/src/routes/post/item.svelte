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
	<div class="ititle">
		<strong>
			{post.title}
		</strong>
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

		background-color: var(--bg1);
		color: var(--ft2);
		text-decoration: none;

		border-radius: var(--sp1);
		border: 2px solid transparent;

		transition: background-color var(--trans), border-color var(--trans);
	}
	a:hover {
		border-color: var(--ft2);
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
		background-color: var(--bg2);

		transition: transform var(--aTime);
		transition-timing-function: ease-in-out;
	}
	a:hover img {
		transform: scale(1.2);
	}
	.ititle {
		color: var(--cl1);
		margin: var(--sp2) 0;
	}

	.description {
		margin: var(--sp2) 0;
		color: var(--ft1);
		transition: color var(--trans);
	}

	.date {
		font-size: small;
		transition: color var(--trans);
	}
</style>
