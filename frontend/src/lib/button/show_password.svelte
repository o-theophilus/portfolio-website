<script>
	import Icon from '$lib/icon.svelte';

	export let show_password = false;
</script>

<form on:submit|preventDefault>
	<button
		tabindex="-1"
		on:click={() => {
			show_password = !show_password;
		}}
	>
		<Icon icon={show_password ? 'visibility_off' : 'Visibility'} size="12" />
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

		background-color: var(--ac8);
		color: var(--ac2);
		fill: currentColor;
		cursor: pointer;
	}

	button:hover {
		background-color: var(--cl1_d);
		color: var(--ac6_);
	}
</style>
