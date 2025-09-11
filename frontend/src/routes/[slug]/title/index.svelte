<script>
	import { module, app } from '$lib/store.svelte.js';
	import Button from '../button.svelte';
	import Edit from './edit.svelte';

	let { item, edit_mode, update } = $props();
</script>

<div class="comp">
	{#if app.user.access.includes('post:edit_title') && edit_mode}
		<Button
			onclick={() =>
				module.open(Edit, {
					key: item.key,
					title: item.title,
					update
				})}
		>
			Edit Title
		</Button>
	{/if}
	<div class="page_title">
		{item.title}
	</div>
</div>

<style>
	.comp {
		margin-top: var(--sp3);
	}
</style>
