<script>
	let { active = false, state_1 = '', state_2 = '', disabled = false, onclick } = $props();

	let width_1 = $state(0);
	let width_2 = $state(0);
</script>

<button {onclick} class:active {disabled}>
	<div class="knob" style:--width_1="{width_1}px" style:--width_2="{width_2}px"></div>
	<div class="state state_1" class:empty={!state_1} bind:clientWidth={width_1}>{state_1}</div>
	<div class="state state_2" class:empty={!state_2} bind:clientWidth={width_2}>{state_2}</div>
</button>

<style>
	button {
		--size: 24px;

		position: relative;

		display: flex;
		align-items: center;
		flex-shrink: 0;

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
		position: relative;
		display: flex;
		align-items: center;
		justify-content: center;
		padding: 0 var(--sp1);
		transition: color var(--trans);
	}
	.state_1 {
		color: white;
	}
	.state_2 {
		color: var(--ft2);
	}
	.empty {
		width: var(--size);
		padding: 0;
	}

	.knob {
		position: absolute;
		left: 2px;

		width: calc(var(--width_1) - 4px);
		height: calc(var(--size) - 4px);
		border-radius: calc(var(--size) / 2);
		background-color: var(--cl1);

		transition:
			background-color var(--trans),
			left var(--trans),
			width var(--trans);
		/* box-shadow: 0 0 3px rgba(0, 0, 0, 0.857); */
	}
	button:not(:disabled):hover .knob {
		background-color: color-mix(in srgb, var(--cl1), black 30%);
	}

	.active .knob {
		width: calc(var(--width_2) - 4px);
		left: calc(100% - var(--width_2) + 2px);
	}
	.active .state_1 {
		color: var(--ft2);
	}
	.active .state_2 {
		color: white;
	}
</style>
