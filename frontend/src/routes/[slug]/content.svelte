<script>
	import { module, user } from '$lib/store.js';

	import Button from '$lib/button/button.svelte';
	import Icon from '$lib/icon.svelte';
	import Marked from '$lib/marked.svelte';
	import Edit from './content.edit.svelte';

	export let post;
	export let edit_mode;
	export let update;
	let content = '';

	const process_content = (text) => {
		text = text ? text : '';

		let i = 0;
		let exist = text.search(/@\[file\]/) >= 0;
		while (exist) {
			i++;

			let sub = `![${post.title}](/no_photo.png)`;
			if (post.files[i]) {
				if (post.files[i].slice(-4) == '.jpg') {
					sub = `![${post.title}](${post.files[i]})`;
				} else if (post.files[i].slice(-4) == '.pdf') {
					sub = `<embed src="${post.files[1]}#toolbar=0" width="100%" height="400" type="application/pdf" />`;
				}
			}

			text = text.replace(/@\[file\]/, sub);
			exist = text.search(/@\[file\]/) >= 0;
		}
		return text;
	};

	const refresh = (text) => {
		content = process_content(text);
	};

	refresh(post.content);
</script>

<hr />

{#if $user.access.includes('post:edit_content') && edit_mode}
	<Button
		size="small"
		on:click={() => {
			$module = {
				module: Edit,
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
