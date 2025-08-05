<script>
	import { module, user, state } from '$lib/store_old.js';
	import { goto } from '$app/navigation';

	import Button from '$lib/button_old/button.svelte';
	import Icon from '$lib/icon.svelte';
	import Tags from '$lib/tags.svelte';
	import Edit from './tags.edit.svelte';

	export let post;
	export let edit_mode;
	export let update;
</script>

{#if post.tags.length > 0 || ($user.access.includes('post:edit_tags') && edit_mode)}
	<hr />
{/if}

{#if $user.access.includes('post:edit_tags') && edit_mode}
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
		Edit Tags
	</Button>
{/if}

{#if post.tags.length > 0}
	<Tags
		style="1"
		tags={post.tags}
		on:click={(e) => {
			let pn = 'post';
			let i = $state.findIndex((x) => x.name == pn);
			if (i != -1) {
				$state.splice(i, 1);
			}

			goto(`post?${new URLSearchParams({ tag: e.detail }).toString()}`);
		}}
	/>
{:else if edit_mode}
	<div class="margin">No tag</div>
{/if}

<style>
	.margin {
		margin: var(--sp2) 0;
	}

	hr {
		margin: var(--sp2) 0;
	}
</style>
