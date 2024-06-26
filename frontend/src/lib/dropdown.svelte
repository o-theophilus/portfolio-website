<script>
	import Icon from '$lib/icon.svelte';

	export let list = [];
	export let icon = '';
	export let wide = false;
	export let default_value = list[0] || '';
	let value = default_value;

	export const set = (x) => {
		value = x;
	};
</script>

{#if icon}
	<button>
		<div class="icon">
			<Icon {icon} />
		</div>
		<select bind:value class:wide on:change>
			{#each list as x}
				<option value={x}>
					{x}
				</option>
			{/each}
		</select>
	</button>
{:else}
	<select class="select" bind:value class:wide on:change>
		{#each list as x}
			<option value={x}>
				{x}
			</option>
		{/each}
	</select>
{/if}

<style>
	.select {
		padding: var(--sp2);
		width: 100%;
		border-radius: var(--sp0);
		outline: 2px solid transparent;

		border: none;
		background-color: var(--input);
		color: var(--ft2);
		cursor: pointer;

		transition: outline-color var(--trans);
	}
	.select:not(.wide) {
		max-width: fit-content;
	}

	.select:hover {
		outline-color: var(--ft1);
		color: var(--ft1);
	}

	button {
		position: relative;

		border-radius: var(--sp0);
		border: none;
		outline: 2px solid transparent;

		line-height: 0;
		background-color: var(--input);
		color: var(--ft2);

		transition: color var(--trans), outline-color var(--trans);
	}
	button:hover:not(:disabled) {
		color: var(--ft1);
		outline-color: var(--ft1);
	}

	.icon {
		position: absolute;
		inset: 0;

		display: flex;
		justify-content: center;
		align-items: center;
		pointer-events: none;
	}

	button select {
		--size: 50px;
		width: var(--size);
		height: var(--size);
		opacity: 0;
	}

	option {
		color: var(--ft1_d);
	}
</style>
