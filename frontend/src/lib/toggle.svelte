<script>
	export let active = false;
	export let state_1 = '';
	export let state_2 = '';
	export let disabled = false;
	let width_1;
	let width_2;
</script>

<button on:click class:active {disabled}>
	<div class="knob" style:--width_1="{width_1}px" style:--width_2="{width_2}px" />
	<div class="state" class:sq={!state_1} bind:clientWidth={width_1}>{state_1}</div>
	<div class="state" class:sq={!state_2} bind:clientWidth={width_2}>{state_2}</div>
</button>

<style>
	button {
		--size: 24px;
		
		display: flex;
		align-items: center;
		flex-shrink: 0;
		
		position: relative;
		
		height: var(--size);
		border: none;
		border-radius: calc(var(--size) / 2);
		
		font-size: 0.8rem;
		cursor: pointer;
		background-color: var(--bg2);
		text-transform: capitalize;
		box-shadow: 0 0 3px color-mix(in srgb, var(--ft2), transparent 50%) inset;
		
		transition: background-color var(--trans);
	}
	button:disabled {
		opacity: 0.4;
		cursor: unset;
	}

	.state {
		display: flex;
		align-items: center;
		justify-content: center;
		padding: 0 var(--sp1);
		transition: color var(--trans);
	}
	.sq {
		width: var(--size);
		padding: 0;
	}
	.state:nth-child(2) {
		color: var(--clb);
	}
	.state:last-of-type {
		color: var(--ft2);
	}

	.knob {
		position: absolute;
		left: 2px;

		width: calc(var(--width_1) - 4px);
		height: calc(var(--size) - 4px);
		border-radius: calc(var(--size) / 2);
		background-color: var(--cl1);

		transition: background-color var(--trans), left var(--trans), width var(--trans);
		/* box-shadow: 0 0 3px rgba(0, 0, 0, 0.857); */
	}
	button:not(:disabled):hover .knob {
		background-color: color-mix(in srgb, var(--cl1), black 30%);
	}

	.active .knob {
		width: calc(var(--width_2) - 4px);
		left: calc(100% - var(--width_2) + 2px);
	}
	.active .state:nth-child(2) {
		color: var(--ft2);
	}
	.active .state:last-of-type {
		color: var(--clb);
	}
</style>
