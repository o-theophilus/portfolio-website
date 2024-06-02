<script>
	import Icon from '$lib/icon.svelte';

	export let name;
	export let error;
	export let icon = '';
	let id = name.split(' ').join('_');
</script>

<div class="inputGroup" class:svgi={!!icon}>
	<slot name="label" />
	{#if !$$slots.label}
		<label for={id}>{name}</label>
	{/if}
	{#if error}
		<span class="error">
			{error}
		</span>
	{/if}
	<slot {id} />
	{#if icon}
		<div class="svg">
			<Icon {icon} size="20" />
		</div>
	{/if}
</div>
