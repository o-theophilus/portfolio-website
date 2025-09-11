<script>
	import { module, app } from '$lib/store.svelte.js';
	import Button from '../button.svelte';
	import Edit from './edit.svelte';

	let { item, edit_mode, update } = $props();
</script>

<div class="margin">
	{#if app.user.access.includes('post:edit_description') && edit_mode}
		<Button
			onclick={() =>
				module.open(Edit, {
					key: item.key,
					description: item.description,
					update
				})}>Edit Description</Button
		>
	{/if}

	{#if item.description}
		{item.description}
	{:else if edit_mode}
		No description
	{/if}
</div>

<style>
	.margin {
		margin: var(--sp2) 0;
	}
</style>
