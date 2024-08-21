<script>
	import { flip } from 'svelte/animate';
	import { cubicInOut } from 'svelte/easing';
	import { loading, module, notification } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Button from '$lib/button/button.svelte';
	import BRound from '$lib/button/round.svelte';
	import Icon from '$lib/icon.svelte';

	let post = $module.post;
	let photo_count = post.content.split('{#photo}').length;
	let edit_mode = true;

	let input;
	let active_photo = post.photos[0] || '';
	let init_order = [...post.photos];
	let dragover = false;
	let error = {};

	const move_right = (dir = true) => {
		error = {};

		let i = post.photos.indexOf(active_photo);
		post.photos.splice(i, 1);
		i = dir ? i + 1 : i - 1;
		post.photos.splice(i, 0, active_photo);
		post = post;
	};

	const reorder_delete = async (method) => {
		error = {};

		$loading = `${method == 'delete' ? 'deleting' : 'saving'} . . .`;
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/post/photo/${post.key}`, {
			method: method,
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({
				photos: post.photos,
				active_photo
			})
		});
		resp = await resp.json();
		$loading = false;

		if (resp.status == 200) {
			init_order = [...resp.post.photos];
			post = resp.post;

			let msg = 'Order saved';
			if (method == 'delete') {
				msg = 'Photo deleted';
				active_photo = post.photos[0] || '';
			}
			$module.update(resp.post);

			$notification = {
				message: msg
			};
		} else {
			error = resp;
		}
	};

	const on_input = () => {
		error = {};

		let files = [];
		for (let i = 0; i < input.files.length; i++) {
			let file = input.files[i];
			let [media, type] = file.type.split('/');

			let err = '';
			if (media != 'image' || ['svg+xml', 'x-icon'].includes(type)) {
				err = `${file.name} => invalid file`;
			} else if (files.length + post.photos.length >= photo_count) {
				err = `${file.name} => excess file`;
			}

			if (err) {
				error.error = error.error ? `${error.error}, ${err}` : err;
			} else {
				files.push(file);
			}
		}

		files.length > 0 && upload_input(files);
	};

	const upload_input = async (files) => {
		let formData = new FormData();
		for (let i in files) {
			formData.append('files', files[i]);
		}

		$loading = 'uploading . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/post/photo/${post.key}`, {
			method: 'post',
			headers: {
				Authorization: $token
			},
			body: formData
		});
		resp = await resp.json();
		$loading = false;

		if (resp.status == 200) {
			init_order = [...resp.post.photos];
			active_photo = active_photo || post.photos[0];
			post = resp.post;
			$module.update(resp.post);
			$notification = {
				message: 'Photo added'
			};

			if (resp.error) {
				error.error = error.error ? `${error.error}, ${resp.error}` : resp.error;
			}
		} else {
			error = resp;
		}
	};

	$: if (!post.photos.includes(active_photo)) {
		active_photo = post.photos[0] || '';
	}
</script>

<div class="comp">
	<strong class="ititle"> Manage Photo </strong>
	<br />
	<br />
	<img
		src={active_photo || '/no_photo.png'}
		alt={post.title}
		class="main"
		class:dragover
		class:edit_mode={edit_mode && post.photos.length < photo_count}
		on:click={() => {
			if (edit_mode && post.photos.length < photo_count) {
				input.click();
			}
		}}
		on:dragover|preventDefault={() => {
			dragover = true;
		}}
		on:dragleave|preventDefault={() => {
			dragover = false;
		}}
		on:drop={(e) => {
			dragover = false;
			if (edit_mode && post.photos.length < photo_count) {
				e.preventDefault();
				input.files = e.dataTransfer.files;
				on_input();
			}
		}}
		role="presentation"
	/>
	<input
		style:display="none"
		type="file"
		accept="image/*"
		multiple
		bind:this={input}
		on:change={(e) => {
			on_input();
		}}
	/>

	{#if post.photos.length > 1}
		<div class="line">
			{#each post.photos as photo (photo)}
				<img
					animate:flip={{ delay: 0, duration: 250, easing: cubicInOut }}
					src={photo ? `${photo}/200` : '/no_photo.png'}
					alt={post.name}
					on:click={() => {
						error = {};
						active_photo = photo;
					}}
					class="thumbnail"
					class:active={active_photo == photo}
					role="presentation"
				/>
			{/each}
		</div>
	{/if}

	{#if edit_mode}
		<div class="line">
			<Button
				primary
				on:click={() => {
					input.click();
				}}
				disabled={post.photos.length >= photo_count}
			>
				<Icon icon="add" />
				Add ({photo_count - post.photos.length})
			</Button>

			<Button
				extra="hover_red"
				on:click={() => {
					reorder_delete('delete');
				}}
				disabled={post.photos.length == 0}
			>
				<Icon icon="delete" />
				Remove
			</Button>
		</div>
		<div class="line">
			<BRound
				icon="arrow_back"
				disabled={post.photos.length <= 1 || post.photos[0] == active_photo}
				on:click={() => {
					move_right(false);
				}}
			/>
			<Button
				size="small"
				disabled={JSON.stringify(init_order) == JSON.stringify(post.photos)}
				on:click={() => {
					reorder_delete('put');
				}}
			>
				<Icon icon="save" />
				Save
			</Button>
			<BRound
				icon="arrow_forward"
				disabled={post.photos.length <= 1 || post.photos[post.photos.length - 1] == active_photo}
				on:click={() => {
					move_right();
				}}
			/>
		</div>

		{#if error.error}
			<div class="error">
				{error.error}
			</div>
		{/if}
	{/if}
</div>

<style>
	.comp {
		padding: var(--sp3);
	}

	img {
		width: 100%;
		border-radius: var(--sp1);
		outline: 2px solid transparent;
		transition: outline-color var(--trans1), transform var(--trans1);
	}

	.line {
		display: flex;
		justify-content: center;
		align-items: center;
		gap: var(--sp1);
		flex-wrap: wrap;
		margin-top: var(--sp2);
	}
	.thumbnail {
		--size: 50px;
		width: var(--size);
		height: var(--size);
	}

	.thumbnail:hover,
	.edit_mode:hover,
	.edit_mode.dragover {
		outline-color: var(--cl1);
		cursor: pointer;
	}

	.active {
		outline-color: var(--cl1);
		transform: scale(1.1);
	}

	.error {
		margin: var(--sp2) 0;
	}
</style>
