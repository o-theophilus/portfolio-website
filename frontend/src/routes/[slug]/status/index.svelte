<script>
	import { module, app } from '$lib/store.svelte.js';

	import Button from '../button.svelte';
	import Edit from './edit.svelte';

	let { item, update } = $props();
</script>

{#if app.user.access.includes('post:edit_status')}
	<Button
		onclick={() =>
			module.open(Edit, {
				key: item.key,
				status: item.status,
				photo: item.photo,
				update
			})}
	>
		Edit Status: <span class="status {item.status}">{item.status}</span>
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
