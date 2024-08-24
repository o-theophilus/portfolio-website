<script>
	import { loading, notification, module } from '$lib/store.js';
	import { token } from '$lib/cookie.js';
	import { createEventDispatcher } from 'svelte';

	let emit = createEventDispatcher();

	let post = $module.post;
	let count = post.content.split('{#photo}').length;
	let active_photo = post.photos[0] || '/no_photo.png';
	let input;
	let dragover = false;
	let error = {};

	const on_input = () => {
		error = {};

		let files = [];
		for (let i = 0; i < input.files.length; i++) {
			let file = input.files[i];
			let [media, type] = file.type.split('/');

			let err = '';
			if (media != 'image' || ['svg+xml', 'x-icon'].includes(type)) {
				err = `${file.name} => invalid file`;
			} else if (files.length + post.photos.length >= count) {
				err = `${file.name} => excess file`;
			}

			if (err) {
				error.error = error.error ? `${error.error}, ${err}` : err;
			} else {
				files.push(file);
			}
		}

		files.length > 0 && upload(files);
	};

	const upload = async (files) => {
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
			post = resp.post;
			$module.update(post);
			emit('update', post.photos);

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

	export const add = () => {
		input.click();
	};
	export const active = (data) => {
		active_photo = data;
	};
	export const reset = (data) => {
		post.photos = data;
	};
</script>

<img
	src={active_photo}
	alt={post.title}
	class="main"
	class:dragover
	class:incomplete={post.photos.length < count}
	on:click={() => {
		if (post.photos.length < count) {
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
		if (post.photos.length < count) {
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
	on:change={() => {
		on_input();
	}}
/>

{#if error.error}
	<div class="error">
		{error.error}
	</div>
{/if}

<style>
	img {
		width: 100%;
		border-radius: var(--sp1);
		outline: 2px solid transparent;
		transition: outline-color var(--trans), transform var(--trans);
	}

	.incomplete:hover,
	.incomplete.dragover {
		outline-color: var(--cl1);
		cursor: pointer;
	}

	.error {
		margin: var(--sp2) 0;
	}
</style>
