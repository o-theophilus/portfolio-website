<script>
	import { Icon } from '$lib/macro';

	let { value = $bindable(), total_page = 1, ondone } = $props();
	let _value = $state(value);
	let width = $state();

	const normalize = (x) => {
		if (x < 1 || !x) {
			x = 1;
		} else if (x > total_page) {
			x = total_page;
		}
		return x;
	};

	const submit = (x) => {
		if (x == value) {
			return;
		}
		value = _value = normalize(x);
		ondone?.(value);
	};

	export const reset = (n = 1) => {
		value = _value = n;
	};

	value = normalize(value);
</script>

{#if total_page > 1}
	<section>
		{#if value > 1}
			<button
				onclick={() => {
					submit(value - 1);
				}}
			>
				<Icon icon="arrow_back" size="1.5" />
			</button>
		{/if}

		<div class="input">
			<input
				style:width="calc({width}px + 4px)"
				type="text"
				oninput={(e) => (e.target.value = e.target.value.replace(/[^0-9]/g, ''))}
				bind:value={_value}
				onkeypress={(e) => {
					if (e.key == 'Enter') {
						submit(_value);
					}
				}}
			/>
			<div class="total">
				/ {total_page}
			</div>
		</div>

		<div class="width_helper" bind:clientWidth={width}>
			<span>
				{#if _value}
					{_value}
				{:else}
					0
				{/if}
			</span>
			/ {total_page}
		</div>

		{#if _value != value}
			<button
				onclick={() => {
					submit(_value);
				}}
			>
				<Icon icon="keyboard_double_arrow_right" size="1.5" />
			</button>
		{/if}

		{#if value < total_page}
			<button
				onclick={() => {
					submit(value + 1);
				}}
			>
				<Icon icon="arrow_forward" size="1.5" />
			</button>
		{/if}
	</section>
{/if}

<style>
	section {
		--size: var(--sp3);
		--height: 48px;

		display: flex;
		gap: var(--sp0);

		width: fit-content;
		border-radius: var(--sp0);

		outline: 2px solid transparent;
		background-color: var(--input);

		transition: outline-color var(--trans);
	}
	section:hover,
	section:has(input:focus) {
		outline-color: var(--ft1);
	}

	.input {
		position: relative;
		display: flex;
		align-items: center;
		justify-content: center;
	}
	input {
		padding: var(--size);
		height: var(--height);
		border: none;

		color: var(--ft1);
		background-color: transparent;
	}

	.total {
		position: absolute;
		right: var(--size);
		pointer-events: none;
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

		height: var(--height);
		aspect-ratio: 1/1;

		border-radius: var(--sp0);
		background-color: var(--button);
		fill: var(--ft2_b);
		border: none;
		font-weight: 700;

		transition:
			color var(--trans),
			background-color var(--trans);
	}

	button:hover {
		background-color: var(--cl1);
		fill: var(--ft1_b);
	}
</style>
