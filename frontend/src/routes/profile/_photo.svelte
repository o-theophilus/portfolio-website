<script>
	import { loading, notification, module } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Button from '$lib/button/button.svelte';
	import Icon from '$lib/icon.svelte';

	let user = { ...$module.user };
	let edit_mode = true;
	let error = {};
	let input;
	let dragover = false;
	const validate = () => {
		error = {};
		let file = input.files[0];

		let [media, type] = file.type.split('/');
		if (media != 'image' || ['svg+xml', 'x-icon'].includes(type)) {
			error.error = 'invalid file';
		}

		Object.keys(error).length === 0 && submit(file);
	};

	const submit = async (file) => {
		let formData = new FormData();
		formData.append('file', file);

		$loading = 'uploading . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/user/photo`, {
			method: 'put',
			headers: {
				Authorization: $token
			},
			body: formData
		});
		resp = await resp.json();
		$loading = false;

		if (resp.status == 200) {
			user = resp.user;
			$module.update(resp.user.photo);
			$notification = {
				message: 'Photo added'
			};

			error.error = resp.error;
		} else {
			error = resp;
		}
	};

	const remove = async () => {
		error = {};

		$loading = 'removing . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/user/photo`, {
			method: 'delete',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			}
		});
		resp = await resp.json();
		$loading = false;

		if (resp.status == 200) {
			user.photo = null;
			$module.update(null);
			$notification = {
				message: 'Photo removed'
			};
		} else {
			error = resp;
		}
	};

	let dim = [1 / 1];
	$: {
		dim = [1 / 1];
		let match = user.photo?.match(/_(\d+)x(\d+)\./);
		if (match) {
			dim = [parseInt(match[1]), parseInt(match[2])];
		}
	}
</script>

<div class="comp">
	<strong class="ititle"> User Photo </strong>
	<br />
	<br />
	<img
		src={user.photo || '/no_photo.png'}
		alt={user.name}
		class:dragover
		class:edit_mode
		style:--ar={dim[0] / dim[1]}
		on:click={() => {
			if (edit_mode) {
				input.click();
			}
		}}
		on:dragover|preventDefault={() => {
			dragover = true;
		}}
		on:dragenter
		on:dragleave|preventDefault={() => {
			dragover = false;
		}}
		on:drop={(e) => {
			dragover = false;
			if (edit_mode) {
				e.preventDefault();
				input.files = e.dataTransfer.files;
				validate();
			}
		}}
		role="presentation"
	/>
	<input
		style:display="none"
		type="file"
		accept="image/*"
		bind:this={input}
		on:change={(e) => {
			validate();
		}}
	/>

	{#if edit_mode}
		{#if error.error}
			<div class="error">
				{@html error.error}
			</div>
		{/if}

		{#if !user.photo}
			<Button
				primary
				on:click={() => {
					input.click();
				}}
			>
				<Icon icon="add" />
				Add
			</Button>
		{:else}
			<Button
				on:click={() => {
					remove('delete');
				}}
			>
				<Icon icon="delete" />
				Delete
			</Button>
		{/if}
	{/if}
</div>

<style>
	.comp {
		padding: var(--sp3);
	}

	.error {
		margin: var(--sp2) 0;
	}

	img {
		width: 100%;
		border-radius: var(--sp1);
		outline: 2px solid transparent;
		transition: outline-color var(--trans), transform var(--trans);
	}
	img.edit_mode:hover,
	.dragover.edit_mode {
		outline-color: var(--cl1);
		cursor: pointer;
	}
</style>
