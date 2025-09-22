<script>
	import { module, app, page_state } from '$lib/store.svelte.js';
	import { goto } from '$app/navigation';

	import Button from '../button.svelte';
	import { Tag } from '$lib/button';
	import Edit from './edit.svelte';

	let { item, edit_mode, update } = $props();
</script>

{#if item.tags.length > 0 || (app.user.access.includes('post:edit_tags') && edit_mode)}
	<hr />
{/if}

{#if app.user.access.includes('post:edit_tags') && edit_mode}
	<Button
		onclick={() =>
			module.open(Edit, {
				key: item.key,
				title: item.title,
				tags: item.tags,
				update
			})}>Edit Tags</Button
	>
{/if}

{#if item.tags.length > 0}
	<div class="line">
		{#each item.tags as x}
			<Tag onclick={() => page_state.goto('post', { tag: x })}>
				{x}
			</Tag>
		{/each}
	</div>
{:else if edit_mode}
	<div class="notag">No tag</div>
{/if}

<style>
	.notag {
		font-size: 0.8rem;
	}

	.line {
		margin-top: 8px;
		gap: 4px;
	}

	hr {
		margin: var(--sp2) 0;
	}
</style>
