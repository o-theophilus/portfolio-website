<script>
	import Input from './input.svelte';
	import { Icon } from '$lib/macro';
	import Check from './password.checker.svelte';
	import Show from './password.show.svelte';
	import { slide } from 'svelte/transition';

	let {
		value = $bindable(),
		show_password = $bindable(),

		name = '',
		icon = null,
		error = '',
		no_pad = false,
		required = false,

		label,
		input,

		right,
		type: props_type,
		onblur,
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

	let _value = $state();
	let show_check = $state(false);
</script>

<div class="inputGroup" class:no_pad>
	{#if label}
		{@render label()}
	{:else if name}
		<div class="label">
			<label for={id}>
				{name}
				{#if required}
					<span class="required">*</span>
				{/if}
			</label>
		</div>
	{/if}

	{#if error}
		<div class="error" transition:slide>
			{error}
		</div>
	{/if}

	{#if input}
		{@render input(id)}
	{:else}
		<div class="input" class:left_pad={icon} class:disabled={props.disabled}>
			{#if icon}
				<Icon {icon}></Icon>
			{/if}
			<Input
				bind:value
				{type}
				{id}
				{...props}
				oninput={(e) => {
					if (props_type.startsWith('password++')) {
						_value = e.target.value;
					}
				}}
				onfocus={(e) => {
					if (props_type.startsWith('password++')) {
						show_check = true;
					}
				}}
				onblur={(e) => {
					if (props_type.startsWith('password++')) {
						show_check = false;
					}
					onblur?.();
				}}
			/>
			{#if props_type?.startsWith('password+') && !props.disabled}
				<div class="show_password">
					<Show bind:show_password></Show>
				</div>
			{/if}
			{@render right?.()}
		</div>
		{#if props_type == 'password++' && show_check && !props.disabled}
			<div class="password" transition:slide>
				<Check value={_value}></Check>
			</div>
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
		outline-offset: -2px;
		color: var(--ft2);
		fill: currentColor;

		background-color: var(--group-background-color, transparent);
		transition: outline-color var(--trans);
	}

	.input.disabled {
		opacity: 0.4;
	}

	.input:hover:not(.disabled),
	:global(.input:has(:focus)) {
		outline-color: var(--ft1);
		color: var(--ft1);
	}

	.label {
		font-size: 0.8rem;
		transition: color var(--trans);
	}
	:global(.inputGroup:has(.input:hover:not(.disabled))),
	:global(.inputGroup:has(:focus) .label) {
		color: var(--ft1);
	}

	.required {
		color: red;
		font-weight: 1000;
	}

	.error {
		color: red;
		font-size: 0.8rem;
	}

	.left_pad {
		padding-left: var(--sp2);
	}

	.show_password {
		padding-right: 8px;
	}
</style>
