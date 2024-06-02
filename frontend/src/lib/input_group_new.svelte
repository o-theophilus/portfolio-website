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
</script>

<div class="inputGroup">
	<slot name="label">
		<label for={id}>{label || name}</label>
	</slot>

	{#if error}
		<div class="error">
			{error}
		</div>
	{/if}

	<slot {id}>
		<div class="line">
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
	.inputGroup {
		margin: var(--sp3) 0;
	}

	.line {
		display: flex;
		gap: var(--sp2);
		align-items: center;
	}

	label {
		text-transform: capitalize;
	}
</style>
