<script>
	import { notify } from '$lib/store.svelte.js';

	import { Icon } from '$lib/macro';
	import { Row } from '$lib/layout';

	let { one } = $props();

	let isDrawn = $state(false);
	const radius = 50;
	const circumference = 2 * Math.PI * radius;
	const time = 5;

	setTimeout(() => {
		notify.close(one.key);
	}, time * 1000);

	setTimeout(() => {
		isDrawn = true;
	});
</script>

<div class="notify" class:bad={one.status == 400} class:caution={one.status == 201}>
	<Row nowrap>
		<Icon
			size="2"
			icon={one.status == 201 ? 'error' : one.status == 400 ? 'cancel' : 'check_circle'}
		/>
		{one.message || 'no message'}

		<button onclick={() => notify.close(one.key)}>
			<Icon icon="close"></Icon>
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
	</Row>
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

		pointer-events: all;
		padding: var(--sp2);

		color: var(--green);
		border-left: 16px solid var(--green);
		background-color: color-mix(in srgb, var(--green), white 90%);
	}
	.bad {
		color: var(--red);
		border-left: 16px solid var(--red);
		background-color: color-mix(in srgb, var(--red), white 90%);
	}
	.caution {
		color: var(--yellow);
		border-left: 16px solid var(--yellow);
		background-color: color-mix(in srgb, var(--yellow), white 90%);
	}

	button {
		--size: 32px;

		position: relative;

		display: flex;
		align-items: center;
		justify-content: center;

		width: var(--size);
		height: var(--size);
		border-radius: 50%;

		border: none;
		background-color: var(--bg1);
		color: var(--ft1);

		transition:
			background-color var(--trans),
			color var(--trans);
	}
	button:hover {
		background-color: var(--cl1_d);
		color: var(--ft1_b);
	}

	svg {
		position: absolute;
		top: -2px;
		left: -2px;

		width: calc(var(--size) + 4px);
		height: calc(var(--size) + 4px);

		pointer-events: none;
	}

	circle {
		fill: none;
		stroke: rgb(183, 183, 183);
		stroke-width: 8px;
		transform: rotate(-90deg);
		transform-origin: 60px 60px;
		transition: stroke-dashoffset var(--time) ease-in-out;
	}
</style>
