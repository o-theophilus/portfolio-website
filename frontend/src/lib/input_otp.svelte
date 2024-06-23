<script>
	let inputs = [];
	export let value = '';

	const press = (e, i) => {
		if (
			!['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'Backspace', 'Delete'].includes(e.key)
		) {
			return;
		}

		if (e.key == 'Backspace') {
			e.target.value = '';
			if (i != 0) {
				inputs[i - 1].focus();
			}
		} else if (e.key == 'Delete') {
			e.target.value = '';
		} else {
			e.target.value = e.key;
			if (i < inputs.length - 1) {
				inputs[i + 1].focus();
			} else {
				inputs[i].blur();
			}
		}

		value = '';
		for (const x of inputs) {
			value += x.value;
		}
	};

	const paste = (e) => {
		let data = (e.clipboardData || window.clipboardData).getData('text');
		data = data.replace(/\D/g, '');

		value = data;
		for (const x in inputs) {
			if (x < data.length) {
				inputs[x].value = data[x];
			} else {
				inputs[x].value = '';
			}
		}
	};
</script>

<div class="line">
	{#each Array(6) as _, i}
		<input
			type="number"
			maxlength="1"
			bind:this={inputs[i]}
			on:keypress={(e) => {
				e.preventDefault();
			}}
			on:keydown={(e) => {
				press(e, i);
			}}
			on:paste={(e) => {
				e.preventDefault();
				paste(e);
			}}
		/>
	{/each}
</div>

<style>
	.line {
		display: flex;
		gap: var(--sp0);
	}

	input {
		--size: 56px;

		max-width: var(--size);
		width: 100%;
		height: var(--size);

		text-align: center;
		font-size: x-large;
		color: var(--ft1);
		background-color: var(--input);
		outline: 2px solid transparent;
		border: none;
		border-radius: var(--sp0);

		transition: outline-color var(--trans);
	}

	input:disabled,
	input:focus {
		outline-color: var(--ft1);
	}

	input:disabled {
		opacity: 0.4;
	}

	input[type='number']::-webkit-outer-spin-button,
	input[type='number']::-webkit-inner-spin-button {
		-webkit-appearance: none;
		margin: 0;
	}
</style>
