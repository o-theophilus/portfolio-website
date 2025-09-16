<script>
	import { module, app } from '$lib/store.svelte.js';

	import Button from '../button.svelte';
	import { Datetime } from '$lib/macro';
	import Edit from './edit.svelte';

	let { item, edit_mode, update } = $props();
</script>

<div class="kkk">
	{#if app.user.access.includes('post:edit_date') && edit_mode}
		<Button
			onclick={() =>
				module.open(Edit, {
					key: item.key,
					date_created: item.date_created,
					update
				})}
		>
			Edit Date
		</Button>
	{/if}
	<div class="date">
		<Datetime datetime={item.date_created} />
	</div>
</div>

<style>
	.kkk{
		align-self: flex-end;
	}
	.date {
		font-size: 0.8rem;
	}
</style>
