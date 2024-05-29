<script>
	export let active = false;
	export let state_1 = 'off';
	export let state_2 = 'on';
	export let disabled = false;
</script>

<button on:click class:active {disabled}>
	<div class="state">{state_1}</div>
	<div class="state">{state_2}</div>
	<div class="switch">
		<div class="state knob">
			{active ? state_2 : state_1}
		</div>
	</div>
</button>

<style>
	button {
		--size: 24px;
		
		display: flex;
		align-items: center;
		
		position: relative;
		
		height: var(--size);
		border: none;
		border-radius: calc(var(--size) / 2);
		/* overflow: hidden; */

		font-size: x-small;
		cursor: pointer;
		background-color: var(--ac4);

		text-transform: capitalize;
		color: var(--ac1);
	}
	button:disabled {
		opacity: 0.4;
		cursor: unset;
	}

	.state {
		display: flex;
		align-items: center;
		justify-content: center;
		padding: 0 var(--sp2);
	}

	.switch {
		position: absolute;
		left: 0;

		transition: var(--trans1);
	}
	.active .switch {
		left: 100%;
	}
	.active .switch .knob {
		left: -100%;
	}

	.knob {
		position: relative;
		left: 0;

		font-size: small;
		height: var(--size);
		border-radius: calc(var(--size) / 2);
		background-color: var(--cl1);
		color: var(--ac5_);

		transition: var(--trans1);
	}
	button:not(:disabled) .knob:hover {
		background-color: var(--cl1_d);
	}
</style>
