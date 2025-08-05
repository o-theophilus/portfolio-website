<script>
	import { module, user } from '$lib/store_old.js';

	import Button from '$lib/button_old/button.svelte';
	import Icon from '$lib/icon.svelte';
	import Edit from './description.edit.svelte';

	export let post;
	export let edit_mode;
	export let update;
</script>

<div class="margin">
	{#if $user.access.includes('post:edit_description') && edit_mode}
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
