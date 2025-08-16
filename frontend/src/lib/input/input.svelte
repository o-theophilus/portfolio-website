<script>
	import Code from './code.svelte';
	let { value = $bindable(), type, ...props } = $props();
	if (type == 'datetime') type = 'datetime-local';
</script>

{#if type == 'textarea'}
	<textarea bind:value {...props}></textarea>
{:else if type == 'code'}
	<Code bind:value {...props}></Code>
{:else}
	<input bind:value {type} {...props} />
{/if}

<style>
	input,
	textarea {
		width: var(--input-width, 100%);
		height: var(--input-height, 48px);
		border: none;

		font-size: var(--input-font-size, 1rem);
		background-color: var(--input-background-color, transparent);
		color: var(--input-color, hsl(0, 0%, 0%));
	}
	input {
		padding: 0 var(--input-padding-x, 16px);
	}

	textarea {
		display: block;
		resize: none;
		height: 160px;
		padding: var(--input-padding, 16px);
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
