<script>
	import { module, app } from '$lib/store.svelte.js';

	import Button from '../button.svelte';
	import Edit from './edit.svelte';

	let { item, edit_mode, update } = $props();
	let src = $derived(item.photo || '/no_photo.png');
</script>

<div class="img">
	<img {src} alt={item.title} onerror={() => (src = '/file_error.png')} />
	<div class="line">
		{#if app.user.access.includes('post:edit_photo') && edit_mode}
			<Button
				onclick={() => {
					module.open(Edit, {
						key: item.key,
						name: item.title,
						photo: item.photo,
						type: 'post',
						slug: `/post/photo/${item.key}`,
						update
					});
				}}
			>
				Edit Photo
			</Button>
		{/if}
	</div>
</div>

<style>
	.img {
		position: relative;
	}

	img {
		display: block;

		width: 100%;
		border-radius: var(--sp1);

		background-color: var(--bg2);
	}
	.img .line {
		position: absolute;
		bottom: var(--sp1);
		left: var(--sp1);
	}
</style>
