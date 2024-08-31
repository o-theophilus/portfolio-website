<script>
	export let disabled = false;
</script>

<button on:click {disabled}>
	<slot />
</button>

<style>
	button {
		--size: 24px;

		border: none;
		height: var(--size);
		border-radius: calc(var(--size) / 2);
		padding: 0 var(--sp2);

		font-size: 0.8rem;
		background-color: color-mix(in srgb, var(--cl1), transparent 80%);

		text-transform: capitalize;
		color: var(--ft2);

		transition: color var(--trans), background-color var(--trans);
	}

	button:hover {
		cursor: pointer;
		background-color: color-mix(in srgb, var(--cl1), black 30%);
		color: var(--clb);
	}

	:disabled {
		background-color: var(--bg2);
		pointer-events: none;
	}
</style>
