<script>
	import { module, app, memory } from '$lib/store.svelte.js';
	import { goto } from '$app/navigation';

	import { Button } from '$lib/button';
	import { Icon } from '$lib/macro';
	import { Tags } from '$lib/layout';
	import Edit from './tags.edit.svelte';

	let { post, edit_mode, update } = $props();
</script>

{#if post.tags.length > 0 || (app.user.access.includes('post:edit_tags') && edit_mode)}
	<hr />
{/if}

{#if app.user.access.includes('post:edit_tags') && edit_mode}
	<Button size="small" onclick={() => module.open(Edit, { post, update })}>
		<Icon icon="edit" size="1.4" />
		Edit Tags
	</Button>
{/if}

{#if post.tags.length > 0}
	<Tags
		style="1"
		tags={post.tags}
		onclick={(e) => {
			let pn = 'post';
			let i = $memory.findIndex((x) => x.name == pn);
			if (i != -1) {
				$memory.splice(i, 1);
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
