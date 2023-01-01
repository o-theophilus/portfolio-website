<script>
	import SVG from '$lib/comp/svg.svelte';
	import { scroll } from '$lib/store.js';

	export let query = '';
</script>

<button
	on:click|stopPropagation={() => {
		scroll(query);
	}}
	on:keypress
>
	<div class="highlight" />
	<div class="icon">
		<slot>
			<SVG type="down" size="20" />
		</slot>
	</div>
</button>

<style>
	button {
		--size: 100px;

		display: flex;
		justify-content: center;
		align-items: center;

		/* border: 2px solid var(--color1); */
		border: 2px solid var(--font);
		border-radius: 50%;
		width: var(--size);
		height: var(--size);

		fill: var(--font);
		color: var(--font);

		background-color: transparent;
	}
	button:hover {
		fill: var(--light_color);
		color: var(--light_color);
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
