<script>
	import { module, app } from '$lib/store.svelte.js';

	import Button from '../button.svelte';
	import { Marked } from '$lib/macro';
	import Edit from './edit.svelte';
	import File from './file.svelte';
	import { PageNote } from '$lib/info';

	let { item, edit_mode, update } = $props();

	const process = (x) => {
		let temp = x.content;
		let exist = temp.search(/@\[file\]/) >= 0;
		let i = 0;

		while (exist) {
			let sub = `![${x.title}](/no_file.png)`;
			if (x.files[i]) {
				if (x.files[i].slice(-4) == '.jpg') {
					sub = `![${x.title}](${x.files[i]})`;
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
			<Button onclick={() => module.open(Edit, { item, update, process })}>Edit Content</Button>
		{/if}

		{#if app.user.access.includes('post:edit_files') && item.content && item.content.includes('@[file]')}
			<Button icon="image" onclick={() => module.open(File, { item, update })}>Manage Files</Button>
		{/if}
	</div>
{/if}

{#if item.content}
	<br />
	<Marked content={process(item)} />
	<br />
{:else if edit_mode}
	<PageNote>No content</PageNote>
{/if}

<style>
	hr {
		margin: var(--sp2) 0;
	}
</style>
