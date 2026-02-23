<script>
	import { Button } from '$lib/button';
	import { onMount } from 'svelte';
	import { slide } from 'svelte/transition';
	let { value = $bindable(), min = 1, total_page, ondone } = $props();
	let value_rt = $state(0);

	const set = (val) => {
		if (val == value && value_rt == val) return;

		if (val === 'increase') value += 1;
		else if (val === 'decrease') value -= 1;
		else {
			const num = Number(val);
			if (!Number.isNaN(num)) value = num;
			else value = 0;
		}

		const maxNum = Number(total_page);
		const minNum = Number(min);
		if (!Number.isNaN(maxNum) && value > maxNum) value = maxNum;
		if (!Number.isNaN(minNum) && value < minNum) value = minNum;

		value_rt = value;
		ondone?.(value);
	};
	onMount(() => (value_rt = value));
</script>

{#if total_page > 1}
	<section>
		<div class="block">
			<form onsubmit={(e) => e.preventDefault()}>
				<Button
					disabled={value <= min}
					--button-height="44px"
					--button-width="44px"
					icon="chevron-left"
					tabindex={-1}
					onclick={() => set('decrease')}
				></Button>
			</form>

			<div class="width_helper">
				<input
					type="number"
					bind:value={value_rt}
					onkeydown={(e) => {
						const allowedKeys = [
							'Backspace',
							'Delete',
							'Tab',
							'Escape',
							'Enter',
							'Home',
							'End',
							'ArrowLeft',
							'ArrowRight',
							'0',
							'1',
							'2',
							'3',
							'4',
							'5',
							'6',
							'7',
							'8',
							'9'
						];

						if (e.ctrlKey) {
							return;
						}

						if (!allowedKeys.includes(e.key)) {
							e.preventDefault();
							return;
						}

						if (e.key == 'Enter') {
							set(parseInt(value_rt));
						}
					}}
					onpaste={(e) => {
						e.preventDefault();
						let data = (e.clipboardData || window.clipboardData).getData('text');
						data = data.replace(/\D/g, '');
						set(parseInt(data));
					}}
				/>
				<div class="value">
					{value_rt}
				</div>
				&nbsp; / {total_page}
			</div>

			<form onsubmit={(e) => e.preventDefault()}>
				{#if value != value_rt}
					<div transition:slide={{ axis: 'x' }} onsubmit={(e) => e.preventDefault()}>
						<Button
							--button-height="44px"
							--button-width="44px"
							icon="chevrons-right"
							tabindex={-1}
							onclick={() => set(parseInt(value_rt))}
						></Button>
					</div>
				{/if}
				<Button
					disabled={value >= total_page}
					--button-height="44px"
					--button-width="44px"
					icon="chevron-right"
					tabindex={-1}
					onclick={() => set('increase')}
				></Button>
			</form>
		</div>
	</section>
{/if}

<style>
	section {
		margin-top: 24px;
		display: flex;
		justify-content: center;
	}

	.block {
		display: flex;
		align-items: center;

		padding: 2px;
		width: fit-content;
		border-radius: 4px;

		background-color: var(--input);
		outline: 1px solid var(--pagination-outline-color, var(--input));
		outline-offset: -1px;

		transition: outline-color 0.2s ease-in-out;

		&:hover,
		&:has(input:focus) {
			outline-color: var(--pagination-outline-color-hover, var(--ft1));
		}
	}

	.width_helper {
		position: relative;

		display: flex;

		padding: 0 16px;
		min-width: 60px;

		& .value {
			visibility: hidden;
		}
	}

	form {
		display: flex;
	}

	input {
		position: absolute;
		inset: 0;

		padding: 0 16px;
		border: none;

		font-size: var(--input-font-size, 1rem);
		background-color: transparent;
	}

	input[type='number']::-webkit-outer-spin-button,
	input[type='number']::-webkit-inner-spin-button {
		-webkit-appearance: none;
		margin: 0;
	}
</style>
