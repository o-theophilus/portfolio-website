<script>
	import Input from '$lib/input.svelte';

	export let name = '';
	export let label = '';
	export let error = {};
	let id = name.split(' ').join('_').toLowerCase();

	export let value = '';
	export let type = '';
	export let placeholder = '';
	export let min = '';
	export let disabled = false;
</script>

<div class="inputGroup">
	<slot name="label">
		<label for={id}>{label || name.replace(/_/g, ' ')}</label>
	</slot>

	<!-- {#if !$$slots.label}
		{/if} -->
	{#if error[id]}
		<span class="error">
			{error[id]}
		</span>
	{/if}

	<slot {id}>
		<div class="position">
			<Input bind:value {id} {type} {placeholder} {min} {disabled} on:blur />
			<slot name="pos_1" />
		</div>
		<slot name="pos_2" />
	</slot>
</div>
<br />

<style>
	.inputGroup {
		display: flex;
		flex-direction: column;
		gap: var(--sp1);
	}

	.position {
		position: relative;
	}
</style>
