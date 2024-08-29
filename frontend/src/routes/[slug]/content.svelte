<script>
	import { module, user } from '$lib/store.js';

	import Button from '$lib/button/button.svelte';
	import Icon from '$lib/icon.svelte';
	import Marked from '$lib/marked.svelte';
	import Edit from './content.edit.svelte';
	import File from './content.file.svelte';

	export let post;
	export let edit_mode;
	export let update;
	let content = '';

	const process_content = (text) => {
		text = text ? text : '';
		let exist = text.search(/@\[file\]/) >= 0;
		let i = 0;

		while (exist) {
			let sub = `![${post.title}](/no_photo.png)`;
			if (post.files[i]) {
				if (post.files[i].slice(-4) == '.jpg') {
					sub = `![${post.title}](${post.files[i]})`;
				} else if (post.files[i].slice(-4) == '.pdf') {
					sub = `
<div class="embed">
	<embed src="${post.files[i]}#toolbar=0" width="100%" height="400" type="application/pdf" />
	<a href="${post.files[i]}#toolbar=0" target="_blank">
		<svg width="1rem" height="1rem" viewBox="0 -960 960 960">
			<path d="M120-120v-320h80v184l504-504H520v-80h320v320h-80v-184L256-200h184v80H120Z" /></svg
		>
	</a>
</div>

`;
				}
			}

			text = text.replace(/@\[file\]/, sub);
			exist = text.search(/@\[file\]/) >= 0;
			i++;
		}
		return text;
	};

	const refresh = (text) => {
		content = process_content(text);
	};

	export const refresh2 = (data) => {
		post = { ...data };
		refresh(post.content);
	};

	refresh(post.content);
</script>

<hr />

{#if edit_mode}
	<div class="line">
		{#if $user.access.includes('post:edit_content')}
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

		{#if $user.access.includes('post:edit_files')}
			<Button
				size="small"
				on:click={() => {
					$module = {
						module: File,
						post,
						update
					};
				}}
			>
				<Icon icon="image" size="1.4" />
				Manage Files
			</Button>
		{/if}
	</div>
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
	.line {
		display: flex;
		gap: var(--sp1);
	}
</style>
