<script>
	import Icon from '$lib/icon.svelte';
	export let wide = false;
	export let icon = '';
	export let list = [];
	export let default_value = list[0] || '';
	let value = default_value;

	export const set = (x) => {
		value = x;
	};
</script>

<div class="select" class:wide={!$$slots.default && !icon && wide}>
	<select
		bind:value
		on:change
		class:no_slot={!$$slots.default && !icon}
		class:has_slot={$$slots.default || icon}
	>
		{#each list as x}
			<option value={x}>
				{x}
			</option>
		{/each}
	</select>
	<slot>
		{#if icon}
			<button class="btn">
				<Icon {icon} />
			</button>
		{/if}
	</slot>
</div>

<style>
	.select {
		position: relative;

		width: fit-content;
		line-height: 0;
	}
	.select.wide {
		width: 100%;
	}

	.no_slot {
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
	.no_slot:hover {
		outline-color: var(--ft1);
		color: var(--ft1);
	}

	.has_slot {
		position: absolute;
		inset: 0;

		background-color: transparent;
		border: none;
		appearance: none;

		font-size: 0;
		line-height: 0;
		cursor: pointer;
	}

	option {
		font-size: 1rem;
		color: var(--cld);
	}

	.btn {
		--size: 50px;

		display: flex;
		align-items: center;
		justify-content: center;

		width: var(--size);
		height: var(--size);
		border-radius: var(--sp0);
		outline: 2px solid transparent;

		border: none;
		background-color: var(--input);
		color: var(--ft2);

		transition: outline-color var(--trans);
	}

	.has_slot:hover + .btn {
		outline-color: var(--ft1);
		color: var(--ft1);
	}
</style>
