<script>
	import IntersectionObserver from './observe.svelte';

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
		border-radius: var(--gap0);

		background-color: var(--accent3);
		/* background-color: var(--color1); */

		transition: width 2000ms;
		transition-timing-function: cubic-bezier(0.47, 1.64, 0.41, 0.8);
	}

	.intersecting {
		width: var(--width);
	}
</style>
