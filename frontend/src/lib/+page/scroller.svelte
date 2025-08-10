<script>
	import { goto } from '$app/navigation';
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
	<div class="highlight"></div>
	<div class="outline"></div>
	<div class="content">
		{@render children()}
	</div>
</button>

<style>
	button {
		--size: 100px;

		position: relative;

		display: flex;
		justify-content: center;
		align-items: center;

		width: var(--size);
		height: var(--size);
		border: none;

		background-color: transparent;

		cursor: pointer;
	}

	.content {
		position: absolute;
		display: flex;
		justify-content: center;
		align-items: center;

		color: var(--ft1);
		transition: color var(--trans);
	}
	button:hover .content {
		color: white;
	}

	.invert .content {
		color: white;
	}

	.outline {
		position: absolute;

		width: var(--size);
		height: var(--size);

		border-radius: 50%;
		border: 2px solid var(--ft1);
		border-radius: 50%;

		background-color: transparent;

		transition: border-color var(--trans);
	}
	.invert .outline {
		border-color: white;
	}

	.highlight {
		position: absolute;
		top: 0;
		left: 0;

		width: var(--size);
		height: var(--size);

		background-color: transparent;
		border-radius: 50%;

		transition:
			width var(--trans),
			height var(--trans),
			background-color var(--trans),
			top var(--trans),
			left var(--trans);
	}

	button:hover .highlight {
		top: -8px;
		left: -8px;
		background-color: var(--cl1);
	}
</style>
