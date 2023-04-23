<script>
	import { browser } from '$app/environment';
	import { onMount, createEventDispatcher } from 'svelte';

	import { api_url, _user } from '$lib/store.js';

	export let post;
	export let active_post = {};

	let href = `/${post.type}/${post.slug}`;
	let target = '';
	if (post.format == 'url' && !$_user.roles.includes('admin')) {
		href = post.content;
		target = '_blank';
	}

	let emit = createEventDispatcher();
	let element;
	export let parent;
	onMount(() => {
		let op = {
			root: parent,
			threshold: 0,
			rootMargin: '0px -49%'
		};
		let cb = (elements, ob) => {
			if (elements[0].isIntersecting) {
				emit('active');
			}
		};
		if (browser) {
			let ob = new IntersectionObserver(cb, op);
			ob.observe(element);
		}
	});
</script>

<a
	{href}
	{target}
	data-sveltekit-preload-data
	bind:this={element}
	class:active={post.key == active_post.key}
	on:mouseenter
	on:mouseleave
>
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
		width: min(calc(100vw - var(--gap2) * 2), 400px);

		border-radius: var(--gap1);
		overflow: hidden;

		transition: all var(--animTime3);
		transition-timing-function: ease-in-out;

		box-shadow: 0 0 10px 2px rgba(0, 0, 0, 0.131);
		border: 0 solid transparent;
	}

	img {
		display: block;
		width: 100%;
		height: 100%;

		object-fit: cover;
		background-color: var(--accent4);

		transition: transform var(--animTime3);
		transition-timing-function: ease-in-out;
	}

	a.active {
		transform: scale(1.05);
		border: 2px solid var(--color1);
	}
	a.active img {
		transform: scale(1.2);
	}
</style>
