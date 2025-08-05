<script>
	import { module, app } from '$lib/store.svelte.js';

	import { Button } from '$lib/button';
	import { Icon } from '$lib/macro';
	import Edit from './description.edit.svelte';

	let { post, edit_mode, update } = $props();
</script>

<div class="margin">
	{#if app.user.access.includes('post:edit_description') && edit_mode}
		<Button size="small" onclick={() => module.open(Edit, { post, update })}>
			<Icon icon="edit" size="1.4" />
			Edit Description
		</Button>
	{/if}

	{#if post.description}
		{post.description}
	{:else if edit_mode}
		No description
	{/if}
</div>

<style>
	.margin {
		margin: var(--sp2) 0;
	}
</style>
