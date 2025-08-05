<script>
	import { goto } from '$app/navigation';
	import { scroll } from '$lib/store_old.js';

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
	<div class="outline" />
	<div class="content">
		<slot />
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
		color: var(--clb);
	}

	.invert .content {
		color: var(--clb);
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
		border-color: var(--clb);
	}

	.highlight {
		position: absolute;
		top: 0;
		left: 0;

		width: var(--size);
		height: var(--size);

		background-color: transparent;
		border-radius: 50%;

		transition: width var(--trans), height var(--trans), background-color var(--trans),
			top var(--trans), left var(--trans);
	}

	button:hover .highlight {
		top: -8px;
		left: -8px;
		background-color: var(--cl1);
	}
</style>
