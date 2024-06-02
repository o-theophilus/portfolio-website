<script>
	import IntersectionObserver from '$lib/observe.svelte';

	export let num;
</script>

<IntersectionObserver let:intersecting>
	<div class="block">
		<div class="filler" class:intersecting style:--width="{num}%">
			<!-- {num} -->
		</div>
	</div>
</IntersectionObserver>

<style>
	.block {
		width: 100%;
	}
	.filler {
		width: 0;

		margin: 2px;
		height: 12px;
		border-radius: var(--sp0);

		background-color: var(--ac4);
		/* background-color: var(--cl1); */

		transition: width 2000ms;
		transition-timing-function: cubic-bezier(0.47, 1.64, 0.41, 0.8);
	}

	.intersecting {
		width: var(--width);
	}
</style>
