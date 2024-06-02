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
>
	<div class="highlight" />
	<div class="content">
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

		background-color: transparent;
		transition: border-color var(--animTime1) ease-in-out;
	}
	.invert {
		border-color: var(--ac8_);
	}
	button:hover {
		border-color: transparent;
	}
	button:hover .content {
		color: var(--ac8_);
	}

	.content {
		position: absolute;
		display: flex;
		justify-content: center;
		align-items: center;

		color: var(--ac1);
		transition: color var(--animTime1) ease-in-out;
	}
	.invert .content {
		color: var(--ac8_);
	}

	.highlight {
		position: absolute;
		width: 0%;
		height: 0%;

		opacity: 0;

		background-color: transparent;
		border-radius: 50%;

		transition-property: width, height, background-color, opacity;
		transition-duration: var(--animTime1);
		transition-timing-function: ease-in-out;
	}

	button:hover .highlight {
		width: var(--size);
		height: var(--size);

		background-color: var(--cl1);
		opacity: 1;
	}
</style>
