<script>
	import Input from './input.svelte';
	import { Icon } from '$lib/macro';
	import Check from './password.checker.svelte';
	import Show from './password.show.svelte';
	import Error from '../layout/error.svelte';

	let {
		value = $bindable(),
		show_password = $bindable(),

		name = '',
		icon = '',
		icon_size = 1.2,
		error = '',
		no_pad = false,
		required = false,

		label,
		input,

		type: props_type,
		...props
	} = $props();

	let type = $state(props_type);
	$effect(() => {
		if (props_type?.startsWith('password')) {
			if (show_password) {
				type = 'text';
			} else {
				type = 'password';
			}
		}
	});

	let id = $derived.by(() => {
		let temp = '';
		if (name) {
			temp = name.split(' ').join('_').toLowerCase();
		}
		return temp;
	});
</script>

<div class="inputGroup" class:no_pad>
	{#if label}
		{@render label()}
	{:else if name}
		<div class="label">
			<label for={id}>
				{name}
				{#if required}
					<span class="error">*</span>
				{/if}
			</label>
		</div>
	{/if}

	<Error {error}></Error>

	{#if input}
		{@render input(id)}
	{:else}
		<div class="input" class:left_pad={icon} class:disabled={props.disabled}>
			{#if icon}
				<Icon {icon} size={icon_size} />
			{/if}
			<Input bind:value {type} {id} {...props} />
			{#if props_type?.startsWith('password+') && !props.disabled}
				<div class="show_password">
					<Show bind:show_password></Show>
				</div>
			{/if}
		</div>
		{#if props_type == 'password++' && !props.disabled}
			<Check {value}></Check>
		{/if}
	{/if}
</div>

<style>
	.inputGroup {
		width: 100%;
	}
	.inputGroup:not(.no_pad) {
		margin: var(--sp2) 0;
	}

	.input {
		position: relative;
		display: flex;
		align-items: center;

		width: 100%;

		border-radius: var(--sp0);
		border: none;
		margin: var(--sp1) 0;

		outline: 2px solid var(--input);
		color: var(--ft2);
		fill: currentColor;

		transition: outline-color var(--trans);
	}

	.input.disabled {
		opacity: 0.4;
	}

	.input:hover:not(.disabled),
	:global(.input:has(:focus)) {
		outline-color: var(--cl1);
	}

	.left_pad {
		padding-left: var(--sp2);
	}

	.label {
		font-size: 0.8rem;
	}

	.show_password {
		padding-right: var(--sp2);
	}
	.error {
		color: red;
		font-weight: 1000;
	}
</style>
