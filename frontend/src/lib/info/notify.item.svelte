<script>
	import { notify } from '$lib/store.svelte.js';

	import { Icon } from '$lib/macro';

	let { item } = $props();

	let isDrawn = $state(false);
	const radius = 50;
	const circumference = 2 * Math.PI * radius;
	const time = 5;

	setTimeout(() => {
		notify.close(item.key);
	}, time * 1000);

	setTimeout(() => {
		isDrawn = true;
	});
</script>

<div class="notify" class:bad={item.status == 400} class:caution={item.status == 201}>
	<div class="line nowrap">
		<Icon
			size="24"
			icon={item.status == 201
				? 'triangle-alert'
				: item.status == 400
					? 'circle-x'
					: 'square-check'}
		/>
		{item.message || 'no message'}

		<button onclick={() => notify.close(item.key)}>
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

		display: flex;
		flex-direction: column;
		align-items: end;

		border-radius: var(--sp0);
		fill: currentColor;
		font-size: 0.8rem;

		pointer-events: all;
		padding: var(--sp2);

		color: green;
		border-left: 8px solid green;
		background-color: color-mix(in srgb, green, white 90%);
	}
	.bad {
		color: red;
		border-color: red;
		background-color: color-mix(in srgb, red, white 90%);
	}
	.caution {
		color: var(--yellow);
		border-color: var(--yellow);
		background-color: color-mix(in srgb, var(--yellow), white 90%);
	}

	button {
		--size: 24px;

		position: relative;

		display: flex;
		align-items: center;
		justify-content: center;

		width: var(--size);
		height: var(--size);
		border-radius: 50%;

		border: none;
		background-color: transparent;
		color: var(--ft2);

		transition:
			background-color var(--trans),
			color var(--trans);
	}
	button:hover {
		background-color: red;
		color: white;
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
