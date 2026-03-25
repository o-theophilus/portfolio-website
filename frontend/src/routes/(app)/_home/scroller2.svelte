<script>
	import { goto } from '$app/navigation';
	import { Icon } from '$lib/macro';
	import { scroll } from '$lib/store.svelte.js';

	let { query = '', href = '', invert = false, children } = $props();
</script>

<button
	class:invert
	onclick={() => {
		if (query) {
			scroll(query);
		} else if (href) {
			goto(href);
		}
	}}
>
	{@render children()}
	<Icon icon="corner-right-down" size="24"></Icon>
</button>

<style>
	button {
		all: unset;

		display: flex;
		gap: 8px;
		justify-content: center;
		align-items: center;

		width: 100px;
		aspect-ratio: 1;

		color: var(--ft1);
		border: 2px solid var(--ft1);
		border-radius: 50%;
		cursor: pointer;
		transform: rotate(15deg);

		box-shadow: inset 0 0 10px 0 var(--ft2);

		transition:
			color 0.2s ease-in-out,
			box-shadow 0.2s ease-in-out,
			background-color 0.2s ease-in-out;
	}

	button:hover {
		background-color: var(--ft1);
		color: var(--bg1);
		box-shadow: none;
	}

	@media screen and (min-width: 480px) {
		button {
			width: 120px;
		}
	}
</style>
