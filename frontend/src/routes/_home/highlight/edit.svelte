<script>
	import Add from './edit.add.svelte';
	import Order from './edit.order.svelte';

	let order;
</script>

<div class="comp">
	<div class="page_title">Add Highlights</div>
	<Add ondone={() => order.reset()} />
	<hr />
	<div class="page_title">Change Order</div>
	<Order bind:this={order} />
</div>

<style>
	.comp {
		padding: 24px;
	}
</style>
