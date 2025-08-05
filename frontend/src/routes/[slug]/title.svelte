<script>
	import { module, app } from '$lib/store.svelte.js';

	import { Button } from '$lib/button';
	import { Icon } from '$lib/macro';
	import Edit from './title.edit.svelte';

	let { post, edit_mode, update } = $props();
</script>

<div class="comp">
	{#if app.user.access.includes('post:edit_title') && edit_mode}
		<Button size="small" onclick={() => module.open(Edit, post, update)}>
			<Icon icon="edit" size="1.4" />
			Edit Title
		</Button>
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
