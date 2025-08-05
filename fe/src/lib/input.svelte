<script>
	export let value = '';
	export let id = '';
	export let type = '';
	export let placeholder = '';
	export let min = '';
	export let disabled = false;
</script>

{#if type == 'text'}
	<input bind:value {id} type="text" {placeholder} {disabled} />
{:else if type == 'email'}
	<input bind:value {id} type="email" {placeholder} {disabled} />
{:else if type == 'password'}
	<input bind:value {id} type="password" {placeholder} {disabled} />
{:else if type == 'number'}
	<input bind:value {id} type="number" {placeholder} {disabled} />
{:else if type == 'tel'}
	<input bind:value {id} type="tel" {placeholder} {disabled} />
{:else if type == 'date'}
	<input bind:value {id} type="date" {placeholder} {min} {disabled} />
{:else if type == 'time'}
	<input bind:value {id} type="time" {placeholder} {min} {disabled} />
{:else if type == 'datetime'}
	<input bind:value {id} type="datetime-local" {placeholder} {min} {disabled} />
{:else if type == 'textarea'}
	<textarea bind:value {id} {placeholder} on:blur on:input {disabled} />
{/if}

<style>
	input,
	textarea {
		width: 100%;

		padding: var(--sp2);
		border: none;

		background-color: transparent;
		color: var(--ft1);
	}

	textarea {
		display: block;
		resize: none;
		height: 160px;
	}

	input[type='number']::-webkit-outer-spin-button,
	input[type='number']::-webkit-inner-spin-button {
		-webkit-appearance: none;
		margin: 0;
	}
	::-webkit-calendar-picker-indicator {
		filter: invert(0.5);
	}
</style>
