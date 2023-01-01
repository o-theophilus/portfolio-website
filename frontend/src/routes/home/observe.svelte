<script>
	import IntersectionObserver from 'svelte-intersection-observer';

	let element;
</script>

<IntersectionObserver {element} let:intersecting once threshold="0" rootMargin="-20%">
	<div bind:this={element}>
		<slot {intersecting} />
	</div>
</IntersectionObserver>

<style>
</style>
