<script>
	import { Icon } from '$lib/macro';

	let { value = $bindable(), disabled } = $props();
	console.log(disabled);
</script>

<div class="stars" class:disabled>
	{#each Array(5) as _, i}
		<button class="star" class:active={i < value} onclick={() => (value = i + 1)}>
			<Icon icon="Star" size="28"></Icon>
		</button>
	{/each}
</div>

<style>
	.stars {
		display: flex;

		&.disabled {
			pointer-events: none;
			opacity: 0.6;
		}
	}

	.star {
		all: unset;
		--icon-stroke-width: 1;
		--icon-fill: var(--ft2);
		--icon-stroke: var(--ft2);

		cursor: pointer;
		line-height: 0;

		&.active {
			--icon-fill: goldenrod;
			--icon-stroke: goldenrod;
		}
		&:hover {
			--icon-fill: gold;
			--icon-stroke: gold;
		}
	}
</style>
