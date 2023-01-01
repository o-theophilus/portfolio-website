<script>
	// import { tweened } from 'svelte/motion';
	// import { backOut } from 'svelte/easing';
	// import IntersectionObserver from 'svelte-intersection-observer';
	import IntersectionObserver from './observe.svelte';

	export let num;
	// let element;

	// const progress = tweened(0, {
	// 	duration: 2000,
	// 	easing: backOut
	// });
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

		background-color: var(--mid_color);

		transition: width 2000ms;
		transition-timing-function: cubic-bezier(.47,1.64,.41,.8);
	}

	.intersecting {
		width: var(--width);
	}
</style>
