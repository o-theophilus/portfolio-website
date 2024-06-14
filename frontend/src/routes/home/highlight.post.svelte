<script>
	import { browser } from '$app/environment';
	import { onMount, createEventDispatcher } from 'svelte';

	export let post;
	export let active_post = {};

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
	href="/{post.slug}"
	data-sveltekit-preload-data
	bind:this={element}
	class:active={post.key == active_post.key}
	on:mouseenter
	on:mouseleave
>
	<img src={post.photos[0] || ''} alt={post.title} onerror="this.src='/site/no_photo.png'" />
</a>

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

		/* box-shadow: 0 0 10px 2px rgba(0, 0, 0, 0.131); */
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

	a.active {
		/* transform: scale(1.05); */
		border-color: var(--cl1);
	}
	a.active img {
		transform: scale(1.2);
	}
</style>
