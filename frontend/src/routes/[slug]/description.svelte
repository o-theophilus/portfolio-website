<script>
	import { module, user } from '$lib/store.js';

	import Button from '$lib/button/button.svelte';
	import Icon from '$lib/icon.svelte';
	import Edit from './description.edit.svelte';

	export let post;
	export let edit_mode;
	export let update;
</script>

{#if $user.access.includes('post:edit_description') && edit_mode}
	<hr />
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
		Edit Description
	</Button>
	<div class="margin">
		{#if post.description}
			{post.description}
		{:else}
			No description
		{/if}
	</div>
{/if}

<style>
	.margin {
		margin: var(--sp2) 0;
	}

	hr {
		margin: var(--sp2) 0;
	}
</style>
