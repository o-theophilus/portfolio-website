<script>
	export let disabled = false;
	export let active = false;
	export let no_grow = false;
</script>

<button class:active class:grow={!no_grow} on:click {disabled}>
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
		cursor: pointer;
		background-color: color-mix(in srgb, var(--cl1), transparent 80%);

		text-transform: capitalize;
		color: var(--ft2);

		transition: color var(--trans), background-color var(--trans);
	}
	.grow {
		flex-grow: 1;
	}

	:disabled {
		background-color: color-mix(in srgb, var(--cl1), transparent 70%);
		color: var(--ft2);
		cursor: unset;
		opacity: 0.4;
	}

	:not(:disabled).active {
		background-color: var(--cl1);
		color: var(--clb);
	}
	:not(:disabled):hover {
		background-color: color-mix(in srgb, var(--cl1), black 30%);
		color: var(--clb);
	}
</style>
