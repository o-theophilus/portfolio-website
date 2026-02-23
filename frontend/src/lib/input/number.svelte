<script>
	import { Button } from '$lib/button';
	import { onMount } from 'svelte';
	let { value = $bindable(), disabled, min = 0, max = undefined, ondone } = $props();

	let ready = false;

	const set = (val) => {
		if (val === 'increase') {
			value += 1;
		} else if (val === 'decrease') {
			value -= 1;
		} else {
			const num = Number(val);

			if (!Number.isNaN(num)) {
				value = num;
			} else {
				value = 0;
			}
		}

		const maxNum = Number(max);
		const minNum = Number(min);

		if (!Number.isNaN(maxNum) && value > maxNum) {
			value = maxNum;
		}

		if (!Number.isNaN(minNum) && value < minNum) {
			value = minNum;
		}

		if (ready) ondone?.(value);
		ready = true;
	};
	onMount(() => set(value));
</script>

<div class="block">
	<form onsubmit={(e) => e.preventDefault()}>
		<Button {disabled} icon="minus" tabindex={-1} onclick={() => set('decrease')}></Button>
	</form>

	<input
		type="number"
		bind:value
		{disabled}
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
		}}
		onpaste={(e) => {
			e.preventDefault();
			let data = (e.clipboardData || window.clipboardData).getData('text');
			data = data.replace(/\D/g, '');
			set(parseInt(data));
		}}
		onblur={() => set(value)}
	/>

	<div class="width_helper">
		{value}
	</div>

	<form onsubmit={(e) => e.preventDefault()}>
		<Button {disabled} icon="plus" tabindex={-1} onclick={() => set('increase')}></Button>
	</form>
</div>

<style>
	.block {
		position: relative;

		display: flex;
		align-items: center;
		padding: 2px;

		width: fit-content;

		--button-height: var(--number-height, 44px);
		--button-width: var(--number-width, 44px);
	}

	.width_helper {
		visibility: hidden;
		padding: 0 var(--number-pading-x, 16px);
		min-width: var(--input-min-width, 60px);
	}

	input {
		position: absolute;
		top: 0;
		bottom: 0;
		right: var(--button-width);
		left: var(--button-width);

		border: none;

		font-size: var(--input-font-size, 1rem);
		text-align: center;
		background-color: transparent;
	}

	input[type='number']::-webkit-outer-spin-button,
	input[type='number']::-webkit-inner-spin-button {
		-webkit-appearance: none;
		margin: 0;
	}

	form {
		line-height: 0;
	}
</style>
