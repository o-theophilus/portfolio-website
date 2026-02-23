<script>
	import { Icon } from '$lib/macro';
	import { notify } from '$lib/store.svelte.js';
	import { onDestroy } from 'svelte';

	let { one } = $props();

	let isDrawn = $state(false);
	const radius = 50;
	const circumference = 2 * Math.PI * radius;
	const time = 5;

	let closeTimer = setTimeout(() => {
		notify.close(one.key);
	}, time * 1000);

	let drawTimer = setTimeout(() => {
		isDrawn = true;
	});

	onDestroy(() => {
		clearTimeout(closeTimer);
		clearTimeout(drawTimer);
	});
</script>

<div class="notify" class:bad={one.status == 400} class:caution={one.status == 201}>
	<div class="block">
		<Icon
			size="24"
			icon={one.status == 201 ? 'triangle-alert' : one.status == 400 ? 'circle-x' : 'square-check'}
		/>

		{one.message || 'no message'}

		<button onclick={() => notify.close(one.key)}>
			<Icon icon="x" size="16"></Icon>
			<svg viewBox="0 0 120 120">
				<circle
					cx="60"
					cy="60"
					r={radius}
					stroke-dasharray={circumference}
					stroke-dashoffset={isDrawn ? 0 : circumference}
					style:--time="{time}s"
				/>
			</svg>
		</button>
	</div>
</div>

<style>
	.notify {
		width: fit-content;
		max-width: 300px;

		border-radius: 4px;
		fill: currentColor;

		pointer-events: all;

		color: green;
		background-color: color-mix(in srgb, green, var(--bg) 90%);
		outline: 1px solid color-mix(in srgb, green, transparent 70%);
		outline-offset: -1px;

		&.bad {
			color: red;
			background-color: color-mix(in srgb, red, var(--bg) 90%);
			outline-color: color-mix(in srgb, red, transparent 70%);
		}

		&.caution {
			color: var(--yellow);
			background-color: color-mix(in srgb, var(--yellow), var(--bg) 90%);
			outline-color: color-mix(in srgb, var(--yellow), transparent 70%);
		}
	}

	.block {
		display: flex;
		gap: 16px;
		align-items: center;

		padding: 16px;
		font-size: 0.9rem;
	}

	button {
		--size: 24px;

		position: relative;

		display: flex;
		align-items: center;
		justify-content: center;
		flex-shrink: 0;

		width: var(--size);
		height: var(--size);
		border-radius: 50%;

		border: none;
		background-color: transparent;
		color: var(--ft2);

		transition:
			background-color 0.2s ease-in-out,
			color 0.2s ease-in-out;

		&:hover {
			background-color: red;
			color: white;
		}
	}

	svg {
		position: absolute;
		top: -5px;
		left: -5px;

		width: calc(var(--size) + 10px);
		height: calc(var(--size) + 10px);

		pointer-events: none;
	}

	circle {
		fill: none;
		stroke: var(--ft2);
		stroke-width: 5px;
		transform: rotate(-90deg);
		transform-origin: 60px 60px;
		transition: stroke-dashoffset var(--time) ease-in-out;
	}
</style>
