<script>
	import Add from './add.svelte';
	import Order from './order.svelte';

	let reset;
</script>

<div class="comp">
	<strong class="ititle"> Add Highlights </strong>
	<Add on:ok={reset} />
	<hr />
	<strong class="ititle"> Change Order </strong>
	<Order bind:reset />
</div>

<style>
	.comp {
		padding: var(--sp3);
	}

	hr {
		margin: var(--sp2) 0;
	}
</style>
