<script>
	import Input from '$lib/input.svelte';
	import Icon from '$lib/icon.svelte';

	export let name = '';
	export let label = '';
	export let icon = '';
	export let error = '';
	let id = name.split(' ').join('_').toLowerCase();

	export let value = '';
	export let type = '';
	export let placeholder = '';
	export let min = '';
	export let disabled = false;

	export let no_pad = false;
</script>

<div class="inputGroup" class:no_pad>
	<slot name="label">
		<label for={id}>{label || name}</label>
	</slot>

	{#if error}
		<div class="error">
			{error}
		</div>
	{/if}

	<slot {id}>
		<div class="input" class:left_pad={icon} class:right_pad={$$slots.right} class:disabled>
			{#if icon}
				<Icon {icon} />
			{/if}
			<Input bind:value {id} {type} {placeholder} {min} {disabled} on:blur on:input />
			<slot name="right" />
		</div>
		<slot name="down" />
	</slot>
</div>

<style>
	.inputGroup:not(.no_pad) {
		margin: var(--sp3) 0;
	}

	label {
		text-transform: capitalize;
	}

	.input {
		display: flex;
		align-items: center;

		width: 100%;

		border-radius: var(--sp0);
		border: none;

		outline: 2px solid transparent;
		background-color: var(--ac4);
		color: var(--ac2);

		transition: outline-color var(--trans);
	}

	.input.disabled {
		opacity: 0.4;
	}

	.input:hover:not(.disabled),
	.input:has(:focus) {
		outline-color: var(--ac1);
	}

	.left_pad {
		padding-left: var(--sp2);
	}
	.right_pad {
		padding-right: var(--sp2);
	}
</style>
