<script>
	import { module, app } from '$lib/store.svelte.js';

	import Button from '../button.svelte';
	import { Marked } from '$lib/macro';
	import Edit from './edit.svelte';
	import File from './file.svelte';
	import { PageNote } from '$lib/info';

	let { post, edit_mode, update } = $props();

	const process = (x) => {
		let temp = x.content;
		let exist = temp.search(/@\[file\]/) >= 0;
		let i = 0;

		while (exist) {
			let sub = `![${x.title}](/no_file.png)`;
			if (x.files[i]) {
				if (x.files[i].slice(-4) == '.jpg') {
					sub = `![${x.title}](${x.files[i]})`;
				} else if (x.files[i].slice(-4) == '.pdf') {
					let dim = [1, 1, 1];
					let match = x.files[i].match(/_(\d+)x(\d+)x(\d+)\./);
					if (!match) {
						match = x.files[i].match(/_(\d+\.\d+)x(\d+\.\d+)x(\d+)\./);
					}

					if (match) {
						dim = [match[1], match[2], match[3]];
					}

					sub = `
<div class="embed">
	<embed src="${x.files[i]}#toolbar=0" width="100%" style="aspect-ratio: ${dim[0]} / ${dim[1]};" type="application/pdf" />
	<a href="${x.files[i]}#toolbar=0" target="_blank">
		<svg width="1rem" height="1rem" viewBox="0 -960 960 960">
			<path d="M120-120v-320h80v184l504-504H520v-80h320v320h-80v-184L256-200h184v80H120Z" /></svg
		>
	</a>
</div>

`;
				}
			}

			temp = temp.replace(/@\[file\]/, sub);
			exist = temp.search(/@\[file\]/) >= 0;
			i++;
		}
		return temp;
	};
</script>

<hr />

{#if edit_mode}
	<div class="line">
		{#if app.user.access.includes('post:edit_content')}
			<Button onclick={() => module.open(Edit, { post, update, process })}>Edit Content</Button>
		{/if}

		{#if app.user.access.includes('post:edit_files') && post.content && post.content.includes('@[file]')}
			<Button icon="image" onclick={() => module.open(File, { post, update })}>Manage Files</Button>
		{/if}
	</div>
{/if}

{#if post.content}
	<br />
	<Marked content={process(post)} />
	<br />
{:else if edit_mode}
	<PageNote>No content</PageNote>
{/if}

<style>
	hr {
		margin: var(--sp2) 0;
	}
</style>
