<script>
	import Add from './highlight.mod.add.svelte';
	import Order from './highlight.mod.order.svelte';

	let reset;
</script>

<div class="comp">
	<div class="title">Add Highlights</div>
	<Add on:ok={reset} />
	<hr />
	<div class="title">Change Order</div>
	<Order bind:reset />
</div>

<style>
	.title {
		font-weight: 800;
	}

	.comp {
		padding: var(--sp3);
	}

	hr {
		margin: var(--sp2) 0;
	}
</style>
