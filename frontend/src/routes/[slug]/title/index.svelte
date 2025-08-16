<script>
	import { module, app } from '$lib/store.svelte.js';
	import Button from '../button.svelte';
	import Edit from './edit.svelte';

	let { post, edit_mode, update } = $props();
</script>

<div class="comp">
	{#if app.user.access.includes('post:edit_title') && edit_mode}
		<Button
			onclick={() =>
				module.open(Edit, {
					key: post.key,
					title: post.title,
					update
				})}>Edit Title</Button
		>
	{/if}
	<strong class="ititle">
		{post.title}
	</strong>
</div>

<style>
	.comp {
		margin-top: var(--sp3);
	}
</style>
