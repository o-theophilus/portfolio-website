<script>
	import { Icon } from '$lib/macro';

	let { show_password: show = $bindable() } = $props();
</script>

<form onsubmit={(e) => e.preventDefault()}>
	<button
		tabindex="-1"
		onclick={() => {
			show = !show;
		}}
	>
		<Icon icon={show ? 'visibility' : 'visibility_off'} />
	</button>
</form>

<style>
	form {
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

		background-color: var(--bg1);
		color: var(--ft2);
		fill: currentColor;

		transition:
			color var(--trans),
			background-color var(--trans);
	}

	button:hover {
		background-color: var(--cl1);
		color: var(--ft1_b);
	}
</style>
