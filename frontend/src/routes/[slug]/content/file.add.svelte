<script>
	import { loading, notify, module, app } from '$lib/store.svelte.js';

	let { ops } = $props();
	let input;
	let dragover = $state(false);

	const on_input = () => {
		ops.error = {};

		let files = [];
		for (let i = 0; i < input.files.length; i++) {
			let file = input.files[i];

			let err = '';
			if (!['image/jpeg', 'image/png'].includes(file.type)) {
				err = `${file.name} => invalid file`;
			} else if (files.length + ops.files.length >= ops.count) {
				err = `${file.name} => excess file`;
			}

			if (err) {
				ops.error.error = ops.error.error ? `${ops.error.error} <br/> ${err}` : err;
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

		loading.open('uploading . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/post/file/${ops.key}`, {
			method: 'post',
			headers: {
				Authorization: app.token
			},
			body: formData
		});
		resp = await resp.json();
		loading.close();
		input.value = '';

		if (resp.status == 200) {
			ops.files = resp.item.files;
			module.value.update(resp.item);
			notify.open('Photo added');

			if (resp.error) ops.error = resp;
		} else {
			ops.error = resp;
		}
	};

	export const add = () => {
		input.click();
	};

	let dim = $state([1, 1]);
</script>

<img
	src={ops.active}
	alt={ops.title}
	class="main"
	class:dragover
	class:incomplete={ops.files.length < ops.count}
	style:--ar={dim[0] / dim[1]}
	onclick={() => {
		if (ops.files.length < ops.count) {
			input.click();
		}
	}}
	ondragover={(e) => {
		e.preventDefault();
		dragover = true;
	}}
	ondragleave={(e) => {
		e.preventDefault();
		dragover = false;
	}}
	ondrop={(e) => {
		dragover = false;
		if (ops.files.length < ops.count) {
			e.preventDefault();
			input.files = e.dataTransfer.files;
			on_input();
		}
	}}
	onerror={(e) => (e.target.src = '/file_error.png')}
	role="presentation"
/>
<input
	style:display="none"
	type="file"
	accept="image/jpeg, image/png"
	multiple
	bind:this={input}
	onchange={on_input}
/>

<style>
	img {
		width: 100%;
		border-radius: var(--sp1);
		outline: 2px solid transparent;
		transition:
			outline-color var(--trans),
			transform var(--trans);

		aspect-ratio: var(--ar);
	}

	.incomplete:hover,
	.incomplete.dragover {
		outline-color: var(--cl1);
		cursor: pointer;
	}
</style>
