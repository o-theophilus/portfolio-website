<script>
	import { module, user } from '$lib/store.js';

	import Button from '$lib/button/button.svelte';
	import Icon from '$lib/icon.svelte';
	import Edit from './photo.edit.svelte';

	export let post;
	export let edit_mode;
	export let update;
</script>

<div class="img">
	<img src={post.photo || '/no_photo.png'} alt={post.title} onerror="this.src='/file_error.png';" />
	<div class="line">
		{#if $user.access.includes('post:edit_photo') && edit_mode}
			<Button
				size="small"
				on:click={() => {
					$module = {
						module: Edit,
						entity: {
							key: post.key,
							name: post.title,
							photo: post.photo,
							type: 'post'
						},
						update
					};
				}}
			>
				<Icon icon="image" size="1.4" />
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
		margin: var(--sp2) 0;
		border-radius: var(--sp1);

		background-color: var(--bg2);
	}
	.img .line {
		position: absolute;
		bottom: var(--sp1);
		left: var(--sp1);
	}
</style>
