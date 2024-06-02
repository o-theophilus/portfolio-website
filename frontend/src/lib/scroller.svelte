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

		border: 2px solid var(--ac1);
		border-radius: 50%;
		width: var(--size);
		height: var(--size);

		fill: var(--ac1);
		color: var(--ac1);

		background-color: transparent;
	}
	.invert {
		fill: var(--ac8);
		border-color: var(--ac8);
	}
	button:hover {
		fill: var(--ac8_);
		color: var(--ac8_);
		border-color: transparent;
	}
	button:hover .highlight {
		width: var(--size);
		height: var(--size);

		background-color: var(--cl1);
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
