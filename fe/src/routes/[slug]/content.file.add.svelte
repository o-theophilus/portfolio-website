<script>
	import { loading, notify, module } from '$lib/store_old.js';
	import { token } from '$lib/cookie.js';
	import { createEventDispatcher } from 'svelte';

	let emit = createEventDispatcher();

	let post = $module.post;
	let count = post.content.split('@[file]').length - 1;
	let active_photo = '';
	let input;
	let dragover = false;
	export let error = {};

	const on_input = () => {
		error = {};

		let files = [];
		for (let i = 0; i < input.files.length; i++) {
			let file = input.files[i];

			let err = '';
			if (!['image/jpeg', 'image/png', 'application/pdf'].includes(file.type)) {
				err = `${file.name} => invalid file`;
			} else if (files.length + post.files.length >= count) {
				err = `${file.name} => excess file`;
			}

			if (err) {
				error.error = error.error ? `${error.error}, ${err}` : err;
			} else {
				files.push(file);
			}
		}

		files.length > 0 && upload(files);
		input.value = '';
	};

	const upload = async (files) => {
		let formData = new FormData();
		for (let i in files) {
			formData.append('files', files[i]);
		}

		$loading = 'uploading . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/post/file/${post.key}`, {
			method: 'post',
			headers: {
				Authorization: $token
			},
			body: formData
		});
		resp = await resp.json();
		$loading = false;
		input.value = '';

		if (resp.status == 200) {
			post = resp.post;
			$module.update(post);
			emit('update', post.files);
			$notify.add('Photo added');

			if (resp.error) {
				error = resp;
			}
		} else {
			error = resp;
		}
	};

	export const add = () => {
		input.click();
	};
	export const reset = (data) => {
		post.files = data;
	};

	let dim = [1, 1];
	export const active = (data) => {
		active_photo = data;
		dim = [1, 1];

		if (!active_photo) {
			active_photo = '/select_file.png';
		} else if (active_photo.slice(-4) == '.jpg') {
			let match = active_photo.match(/_(\d+)x(\d+)\./);
			if (match) {
				dim = [parseInt(match[1]), parseInt(match[2])];
			}
		} else {
			active_photo = '/no_preview.png';
		}
	};

	active(post.files[0]);
</script>

<img
	src={active_photo}
	alt={post.title}
	class="main"
	class:dragover
	class:incomplete={post.files.length < count}
	style:--ar={dim[0] / dim[1]}
	on:click={() => {
		if (post.files.length < count) {
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
		if (post.files.length < count) {
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
	accept="image/jpeg, image/png, application/pdf"
	multiple
	bind:this={input}
	on:change={() => {
		on_input();
	}}
/>

<style>
	img {
		width: 100%;
		border-radius: var(--sp1);
		outline: 2px solid transparent;
		transition: outline-color var(--trans), transform var(--trans);

		aspect-ratio: var(--ar);
	}

	.incomplete:hover,
	.incomplete.dragover {
		outline-color: var(--cl1);
		cursor: pointer;
	}
</style>
