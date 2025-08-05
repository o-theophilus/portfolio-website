<script>
	import { browser } from '$app/environment';
	import { onMount } from 'svelte';

	let element;
	let intersecting;
	onMount(() => {
		let op = {
			threshold: 0,
			rootMargin: '-20% 0px'
		};
		let cb = (elements, ob) => {
			if (elements[0].isIntersecting) {
				intersecting = true;
				ob.unobserve(element);
			}
		};
		if (browser) {
			let ob = new IntersectionObserver(cb, op);
			ob.observe(element);
		}
	});
</script>

<div bind:this={element}>
	<slot {intersecting}  />
</div>

<style>
</style>
