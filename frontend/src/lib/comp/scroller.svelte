<script>
	import { goto } from '$app/navigation';
	import { scroll } from '$lib/store.js';

	export let query = '';
	export let href = '';
	export let invert = false;
</script>

<button
	class:invert
	on:click|stopPropagation={() => {
		if (query) {
			scroll(query);
		} else if (href) {
			goto(href);
		}
	}}
	on:keypress
>
	<div class="highlight" />
	<div class="icon">
		<slot />
	</div>
</button>

<style>
	button {
		--size: 100px;

		display: flex;
		justify-content: center;
		align-items: center;

		border: 2px solid var(--accent1);
		border-radius: 50%;
		width: var(--size);
		height: var(--size);

		fill: var(--accent1);
		color: var(--accent1);

		background-color: transparent;
	}
	.invert {
		fill: var(--accent5);
		border-color: var(--accent5);
	}
	button:hover {
		fill: var(--accent5_);
		color: var(--accent5_);
		border-color: transparent;
	}
	button:hover .highlight {
		width: var(--size);
		height: var(--size);

		background-color: var(--color1);
		opacity: 1;
	}
	.icon {
		position: absolute;
		display: flex;
		justify-content: center;
		align-items: center;
	}
	.highlight {
		position: absolute;
		width: 0%;
		height: 0%;

		opacity: 0;

		background-color: transparent;
		border-radius: 50%;

		transition: all var(--animTime1);
		transition-timing-function: ease-in-out;
	}
</style>
