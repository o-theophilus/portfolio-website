<script>
	import { slide } from 'svelte/transition';
	import Input from './input.svelte';

	let {
		value = $bindable(),
		show_password = $bindable(),

		name = '',
		icon = null,
		required = false,

		error = '',
		label,
		input,

		...props
	} = $props();

	let id = $derived.by(() => {
		let temp = '';
		if (name) {
			temp = name.split(' ').join('_').toLowerCase();
		}
		return temp;
	});
</script>

<div class="inputGroup">
	{#if label}
		{@render label()}
	{:else if name}
		<label for={id}>
			{name}
			{#if required}
				<span class="required">*</span>
			{/if}
		</label>
	{/if}

	{#if error}
		<div class="error" transition:slide>
			{error}
		</div>
	{/if}

	{#if input}
		<div class="input">
			{@render input(id)}
		</div>
	{:else}
		<div class="input">
			<Input bind:value bind:show_password {id} {...props} />
		</div>
	{/if}
</div>

<style>
	.inputGroup {
		width: 100%;
		margin-top: var(--group-margin-top, 16px);
		margin-bottom: var(--group-margin-bottom, 16px);
		line-height: 100%;
	}

	label {
		font-size: 0.8rem;
		transition: color 0.2s ease-in-out;

		&:hover {
			color: var(--ft1);
		}

		& .required {
			color: red;
			font-weight: 1000;
		}
	}
	.error {
		color: red;
		font-size: 0.8rem;
	}

	.input {
		margin-top: 4px;
	}

	:global(.inputGroup:has(input:hover, textarea:hover, input:focus, textarea:focus)) label {
		color: var(--ft1);
	}
</style>
