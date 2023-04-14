<script>
	import SVG from '$lib/comp/svg.svelte';

	export let name;
	export let error;
	export let svg = '';
	let id = name.split(' ').join('_');
</script>

<div class="inputGroup" class:svgi={!!svg}>
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
	{#if svg}
		<div class="svg">
			<SVG type={svg} size="25" />
		</div>
	{/if}
</div>
