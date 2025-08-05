<script>
	import { module, user } from '$lib/store_old.js';

	import Button from '$lib/button_old/button.svelte';
	import Icon from '$lib/icon.svelte';
	import Edit from './title.edit.svelte';

	export let post;
	export let edit_mode;
	export let update;
</script>

<div class="comp">
	{#if $user.access.includes('post:edit_title') && edit_mode}
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
