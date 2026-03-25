<script>
	import { app, module } from '$lib/store.svelte.js';

	import Button from '../button.svelte';
	import Edit from './edit.svelte';

	let { post, update } = $props();
</script>

{#if app.user.access.includes('post.edit_status')}
	<Button
		onclick={() =>
			module.open(Edit, {
				key: post.key,
				status: post.status,
				photo: post.photo,
				update
			})}
	>
		Edit Status: <span class="status {post.status}">{post.status}</span>
	</Button>
{/if}

<style>
	.status {
		font-weight: 800;
	}
	.status.active {
		color: green;
	}
	.status.draft {
		color: red;
	}
</style>
