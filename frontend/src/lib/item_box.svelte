<script>
	import { api_url, _user, timeAgo } from '$lib/store.js';
	import { onMount } from 'svelte';

	export let post;

	let time = timeAgo(post.created_at);
	onMount(() => {
		const intervalId = setInterval(() => {
			time = timeAgo(post.created_at);
		}, 1000);

		return () => clearInterval(intervalId);
	});
</script>

<a href="/{post.slug}" data-sveltekit-preload-data class:draft={post.status == 'draft'}>
	<div class="img">
		<img
			src="{api_url}/{post.photos[0] || ''}"
			alt={post.title}
			onerror="this.src='/site/no_photo.png'"
		/>
	</div>
	<div class="details">
		<strong class="big color1">
			{post.title}
		</strong>
		{#if post.description}
			<br />
			<div class="description">
				{post.description}
			</div>
		{:else}
			<br />
		{/if}
		<br />
		<div class="date">
			{time}
		</div>
	</div>
</a>

<style>
	a {
		padding: var(--gap3);

		background-color: var(--accent5);
		color: var(--accent2);
		text-decoration: none;

		border-radius: var(--gap1);
		border: 2px solid transparent;

		transition: all var(--animTime1);
		transition-timing-function: ease-in-out;
	}
	a.draft {
		border: 2px solid var(--color2);
	}
	a:hover {
		border-color: var(--accent2);
	}

	.img {
		border-radius: var(--gap1);
		overflow: hidden;
	}
	img {
		display: block;

		object-fit: cover;
		aspect-ratio: 1 / 1;
		background-color: var(--accent4);

		transition: transform var(--animTime3);
		transition-timing-function: ease-in-out;
	}
	a:hover img {
		transform: scale(1.2);
	}

	.details {
		padding-top: var(--gap3);
	}
	strong {
		font-size: large;
	}
</style>
