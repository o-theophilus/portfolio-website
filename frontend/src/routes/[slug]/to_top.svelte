<script>
	import { scroll } from '$lib/store.svelte.js';

	import { Icon } from '$lib/macro';

	let percent = $state(0);
	let scrollTop = $state(0);
	const radius = 50;
	const circumference = 2 * Math.PI * radius;
</script>

<svelte:window
	onscroll={() => {
		scrollTop = window.scrollY;
		percent = Math.round((scrollTop / (document.body.offsetHeight - window.innerHeight)) * 100);
	}}
/>

<div
	class="circle"
	class:show={scrollTop > 160}
	role="presentation"
	onclick={() => {
		scroll('#top_nav');
	}}
>
	<svg viewBox="0 0 120 120">
		<circle
			cx="60"
			cy="60"
			r={radius}
			stroke-dasharray={circumference}
			stroke-dashoffset={circumference - circumference * percent * 0.01}
		/>
	</svg>

	<div class="center">
		<Icon icon="arrow-up"></Icon>
		<!-- {percent} -->
	</div>
</div>

<style>
	.circle {
		--size: 40px;
		--stroke_width: 10px;

		position: fixed;
		bottom: var(--sp3);
		right: var(--sp3);
		z-index: 1;

		display: flex;
		justify-content: center;
		align-items: center;

		width: var(--size);
		height: var(--size);
		border-radius: 50%;

		background-color: var(--bg2);
		opacity: 0;
		pointer-events: none;

		transition: opacity var(--trans);
	}
	.show {
		opacity: 0.5;
		cursor: pointer;
		pointer-events: all;
	}
	.show:hover {
		opacity: 1;
	}

	svg {
		position: absolute;
		width: calc(var(--size) + var(--stroke_width) / 2);
		height: calc(var(--size) + var(--stroke_width) / 2);
	}

	circle {
		fill: none;
		stroke: var(--cl1);
		stroke-width: var(--stroke_width);
		stroke-linecap: round;
		transform: rotate(-90deg);
		transform-origin: 60px 60px;
	}

	.center {
		display: flex;
		justify-content: center;
		align-items: center;

		width: calc(var(--size) - (var(--stroke_width) / 2));
		height: calc(var(--size) - (var(--stroke_width) / 2));

		border-radius: 50%;
		background-color: var(--bg1);
	}
</style>
