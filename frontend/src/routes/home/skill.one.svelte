<script>
	import IntersectionObserver from '$lib/observe.svelte';

	export let one;
</script>

<IntersectionObserver let:intersecting>
	<div class="comp">
		<div class="line">
			<span class="name">
				{one.name}
			</span>
			<span class="value">
				{one.value}
			</span>
		</div>

		<div class="filler_area">
			<div class="filler" class:intersecting style:--width="{one.value}%" />
		</div>
	</div>
</IntersectionObserver>

<style>
	.comp {
		margin: var(--sp2) 0;
	}
	.line {
		display: flex;
		gap: var(--sp2);
		justify-content: space-between;
	}

	.name,
	.value {
		line-height: 1;
	}

	.value {
		font-size: 0.8rem;
	}

	.filler_area {
		width: 100%;
		background-color: var(--bg2);
	}

	.filler {
		width: 0;

		height: 2px;
		border-radius: var(--sp0);

		background-color: var(--cl1);

		transition: width 2000ms;
		transition-timing-function: cubic-bezier(0.47, 1.64, 0.41, 0.8);
	}

	.intersecting {
		width: var(--width);
	}
</style>
