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

		border: 2px solid var(--ft1);
		border-radius: 50%;
		width: var(--size);
		height: var(--size);

		background-color: transparent;
		transition: border-color var(--trans);

		cursor: pointer;
	}
	button:hover {
		border-color: transparent;
	}
	.invert {
		border-color: var(--ft1_b);
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
		color: var(--ft1_b);
	}

	.invert .content {
		color: var(--ft1_b);
	}

	.highlight {
		position: absolute;
		width: 0%;
		height: 0%;

		background-color: transparent;
		border-radius: 50%;

		transition: width var(--trans), height var(--trans), background-color var(--trans);
	}

	button:hover .highlight {
		width: var(--size);
		height: var(--size);
		background-color: var(--cl1);
	}
</style>
