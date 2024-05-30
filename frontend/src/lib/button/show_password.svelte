<script>
	import SVG from '$lib/svg.svelte';

	export let show_password = false;
</script>

<form on:submit|preventDefault>
	<button
		tabindex="-1"
		on:click={() => {
			show_password = !show_password;
		}}
	>
		<SVG icon={show_password ? 'hide_password' : 'show_password'} size="12" />
	</button>
</form>

<style>
	form {
		position: absolute;
		right: var(--sp1);
		top: 0;

		display: flex;
		align-items: center;

		height: 100%;
	}

	button {
		--size: 28px;
		display: flex;
		align-items: center;
		justify-content: center;
		flex-shrink: 0;

		width: var(--size);
		height: var(--size);
		padding: 0;
		border: none;
		border-radius: var(--size);

		background-color: var(--ac5);
		color: var(--ac2);
		fill: currentColor;
		cursor: pointer;
	}

	button:hover {
		background-color: var(--cl1_b);
		color: var(--ac6_);
	}
</style>
