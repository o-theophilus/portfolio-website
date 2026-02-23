<script>
	import { RoundButton } from '$lib/button';
	import { Icon } from '$lib/macro';
	import Code from './code.svelte';
	import Number from './number.svelte';
	import Check from './password.checker.svelte';
	import Rating from './rating.svelte';

	let { value = $bindable(), show_password = $bindable(), type, icon, right, ...props } = $props();
	if (type == 'datetime') type = 'datetime-local';
</script>

{#if type == 'textarea'}
	<div class="input" class:disabled={props.disabled}>
		<textarea bind:value {...props}></textarea>
	</div>
{:else if type == 'code'}
	<div class="input" class:disabled={props.disabled}>
		<Code bind:value {...props}></Code>
	</div>
{:else if type == 'number'}
	<div class="input number" class:disabled={props.disabled}>
		<Number bind:value {...props}></Number>
	</div>
{:else if type == 'rating'}
	<div class="input rating" class:disabled={props.disabled}>
		<Rating bind:value {...props}></Rating>
	</div>
{:else if type?.startsWith('password')}
	<div class="input" class:disabled={props.disabled}>
		{#if icon}
			<div class="icon">
				<Icon {icon}></Icon>
			</div>
		{/if}
		{#if show_password}
			<input bind:value type="text" {...props} />
		{:else}
			<input bind:value type="password" {...props} />
		{/if}
		{#if type?.startsWith('password+')}
			<form onsubmit={(e) => e.preventDefault()}>
				<RoundButton
					icon={show_password ? 'eye' : 'eye-off'}
					extra="hover_red"
					tabindex="-1"
					onclick={() => (show_password = !show_password)}
				/>
			</form>
		{/if}
	</div>
	{#if type == 'password++'}
		<div class="password_check">
			<div><Check {value}></Check></div>
		</div>
	{/if}
{:else}
	<div class="input" class:disabled={props.disabled}>
		{#if icon}
			<div class="icon">
				<Icon {icon}></Icon>
			</div>
		{/if}
		<input bind:value {type} {...props} />
		{@render right?.()}
	</div>
{/if}

<style>
	.input {
		position: relative;

		display: flex;
		align-items: center;

		margin-top: var(--input-margin-top, 0);
		width: 100%;
		border-radius: 4px;
		outline: 1px solid var(--input);
		outline-offset: -1px;
		color: var(--ft2);
		fill: currentColor;

		background-color: var(--group-background-color, var(--input));
		transition: outline-color 0.2s ease-in-out;

		&:hover:not(.disabled),
		:global(&:has(:focus)) {
			outline-color: var(--ft1);
			color: var(--ft1);
		}

		&.number,
		&.rating {
			width: fit-content;
		}

		&.rating {
			background-color: transparent;
			outline-color: transparent;
			&:hover {
				outline-color: transparent;
			}
		}

		& .icon {
			line-height: 0;
			padding-left: 16px;
			flex-shrink: 0;
		}

		& form {
			padding-right: 8px;
		}
	}

	.password_check {
		margin-top: 0;
		display: grid;
		grid-template-rows: 0fr;

		transition:
			margin 0.2s ease-in-out,
			grid-template-rows 0.2s ease-in-out;
	}

	.password_check div {
		overflow: hidden;
	}

	.input:has(input:focus) + .password_check {
		margin-top: 4px;
		grid-template-rows: 1fr;
	}

	input,
	textarea {
		width: var(--input-width, 100%);
		height: var(--input-height, 48px);
		border: none;

		font-size: var(--input-font-size, 1rem);
		background-color: var(--input-background-color, transparent);
		color: var(--input-color, var(--ft1));
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

	::-webkit-calendar-picker-indicator {
		filter: invert(0.5);
	}
</style>
