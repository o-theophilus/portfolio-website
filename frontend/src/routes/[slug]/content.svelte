<script>
	import { module, user } from '$lib/store.js';

	import Button from '$lib/button/button.svelte';
	import Icon from '$lib/icon.svelte';
	import Marked from '$lib/marked.svelte';
	import Edit_Content from './content.edit.svelte';

	export let post;
	export let edit_mode;
	export let update;
	let content = '';

	// TODO: @[youtube](http://www.youtube.com/embed/dQw4w9WgXcQ)
	const process_content = (content) => {
		if (!content) {
			content = '';
		}

		let i = 0;

		let exist = content.search(/{#photo}/) >= 0;
		while (exist) {
			i++;
			content = content.replace(
				/{#photo}/,
				`![${post.title}](${post.photos[i] ? post.photos[i] : '/no_photo.png'})`
			);
			exist = content.search(/{#photo}/) >= 0;
		}

		return content;
	};

	export const refresh = () => {
		content = process_content(post.content);
	};

	refresh();
</script>

<hr />

{#if $user.access.includes('post:edit_content') && edit_mode}
	<Button
		size="small"
		on:click={() => {
			$module = {
				module: Edit_Content,
				post,
				update,
				process_content,
				refresh
			};
		}}
	>
		<Icon icon="edit" size="1.4" />
		Edit Content
	</Button>
{/if}
{#if post.content}
	<br />
	<Marked {content} />
	<br />
{:else if edit_mode}
	<div class="margin">No content</div>
{/if}

<style>
	.margin {
		margin: var(--sp2) 0;
	}

	hr {
		margin: var(--sp2) 0;
	}
</style>
