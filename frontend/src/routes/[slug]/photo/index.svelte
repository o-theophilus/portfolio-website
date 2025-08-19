<script>
	import { module, app } from '$lib/store.svelte.js';

	import Button from '../button.svelte';
	import Edit from './edit.svelte';

	let { post, edit_mode, update } = $props();
	let src = $derived(post.photo || '/no_photo.png');
</script>

<div class="img">
	<img {src} alt={post.title} onerror={() => (src = '/file_error.png')} />
	<div class="line">
		{#if app.user.access.includes('post:edit_photo') && edit_mode}
			<Button
				onclick={() => {
					module.open(Edit, {
						key: post.key,
						name: post.title,
						photo: post.photo,
						type: 'post',
						slug: `/post/photo/${post.key}`,
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
