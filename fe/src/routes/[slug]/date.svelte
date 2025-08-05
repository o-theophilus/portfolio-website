<script>
	import { module, user } from '$lib/store_old.js';

	import Button from '$lib/button_old/button.svelte';
	import Icon from '$lib/icon.svelte';
	import Datetime from '$lib/datetime.svelte';
	import Edit from './date.edit.svelte';

	export let post;
	export let edit_mode;
	export let update;
</script>

{#if $user.access.includes('post:edit_date') && edit_mode}
	<Button
		size="small"
		on:click={() => {
			$module = {
				module: Edit,
				post,
				update
			};
		}}
	>
		<Icon icon="edit" size="1.4" />
		Edit Date
	</Button>
{/if}
<span class="date">
	<Datetime datetime={post.date} />
	<slot />
</span>

<style>
	.date {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: var(--sp1);
		flex-wrap: wrap;

		font-size: 0.8rem;
		margin-bottom: var(--sp3);
	}
</style>
