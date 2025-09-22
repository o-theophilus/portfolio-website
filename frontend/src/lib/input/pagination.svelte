<script>
	import { Icon } from '$lib/macro';

	let { value = $bindable(), total_page = 1, ondone } = $props();
	let value_rt = $derived(value);
	let width = $state();

	const submit = (val) => {
		if (val == value) return;

		value = val;
		if (value < 1 || !value) value = 1;
		else if (value > total_page) value = total_page;
		ondone?.(value);
	};
</script>

{#if total_page > 1}
	<section>
		{#if value > 1}
			<button onclick={() => submit(parseInt(value) - 1)}>
				<Icon icon="chevron-left" />
			</button>
		{/if}

		<div class="input">
			<input
				style:width="calc({width}px + 4px)"
				type="text"
				oninput={(e) => (e.target.value = e.target.value.replace(/[^0-9]/g, ''))}
				bind:value={value_rt}
				onkeypress={(e) => {
					if (e.key == 'Enter') submit(value_rt);
				}}
			/>
			<div class="total">
				/ {total_page}
			</div>
		</div>

		<div class="width_helper" bind:clientWidth={width}>
			<span>
				{#if value_rt}
					{value_rt}
				{:else}
					0
				{/if}
			</span>
			/ {total_page}
		</div>

		{#if value_rt != value}
			<button onclick={() => submit(value_rt)}>
				<Icon icon="chevrons-right" />
			</button>
		{/if}

		{#if value < total_page}
			<button onclick={() => submit(parseInt(value) + 1)}>
				<Icon icon="chevron-right" />
			</button>
		{/if}
	</section>
{/if}

<style>
	section {
		--size: var(--sp3);

		display: flex;
		align-items: center;
		padding: 0 4px;

		width: fit-content;
		border-radius: 4px;
		background-color: var(--pagination-background-color, hsl(0, 0%, 90%));
		outline: 2px solid var(--pagination-outline-color, transparent);
		outline-offset: -2px;

		transition: outline-color var(--trans);
	}
	section:hover,
	section:has(input:focus) {
		outline-color: var(--pagination-outline-color-hover, transparent);
	}

	.input {
		position: relative;
		display: flex;
		align-items: center;
		justify-content: center;
	}
	input {
		padding: var(--size);
		height: 48px;
		border: none;

		color: var(--ft1);
		background-color: transparent;
	}

	.total {
		position: absolute;
		right: var(--size);
		pointer-events: none;
		color: var(--ft2);
	}

	.width_helper {
		position: absolute;
		visibility: hidden;
		padding: var(--size);
		display: inline-block;
	}

	button {
		display: flex;
		justify-content: center;
		align-items: center;

		height: 40px;
		aspect-ratio: 1/1;

		border-radius: var(--sp0);
		background-color: var(--button);
		color: var(--ft2);
		border: none;
		font-weight: 700;

		transition:
			color var(--trans),
			background-color var(--trans);
	}

	button:hover {
		background-color: var(--cl1);
		color: white;
	}
</style>
