<script>
	import { app, module } from '$lib/store.svelte.js';

	import { Datetime } from '$lib/macro';
	import Button from '../button.svelte';
	import Edit from './edit.svelte';

	let { post, edit_mode, update } = $props();
</script>

<div class="kkk">
	{#if app.user.access.includes('post:edit_date') && edit_mode}
		<Button
			onclick={() =>
				module.open(Edit, {
					key: post.key,
					date_created: post.date_created,
					update
				})}
		>
			Edit Date
		</Button>
	{/if}
	<div class="date">
		<Datetime datetime={post.date_created} />
	</div>
</div>

<style>
	.kkk {
		align-self: flex-end;
	}
	.date {
		font-size: 0.8rem;
	}
</style>
