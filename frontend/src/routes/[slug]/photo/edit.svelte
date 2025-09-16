<script>
	import { loading, notify, module, app } from '$lib/store.svelte.js';

	import { Button } from '$lib/button';
	import { Icon } from '$lib/macro';
	import { Form } from '$lib/layout';

	let item = $state({ ...module.value });
	let has_photo = $state(item.photo ? true : false);
	let error = $state({});
	let input;
	let dragover = $state(false);
	let src = $derived(item.photo || '/select_photo.png');

	const validate = () => {
		error = {};
		let file = input.files[0];

		if (!file) {
			return;
		} else if (!['image/jpeg', 'image/png'].includes(file.type)) {
			error.error = 'invalid file';
		}

		Object.keys(error).length === 0 && submit(file);
		input.value = '';
	};

	const submit = async (file) => {
		let formData = new FormData();
		formData.append('file', file);

		loading.open('uploading . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}${item.slug}`, {
			method: 'put',
			headers: {
				Authorization: app.token
			},
			body: formData
		});
		resp = await resp.json();
		loading.close();
		input.value = '';

		if (resp.status == 200) {
			item.photo = resp[item.type].photo;
			module.value.update(resp[item.type]);
			has_photo = true;
			notify.open('Photo updated');
		} else {
			error = resp;
		}
	};

	const remove = async () => {
		error = {};

		loading.open('removing . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}${item.slug}`, {
			method: 'delete',
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			}
		});
		resp = await resp.json();
		loading.close();

		if (resp.status == 200) {
			item.photo = null;

			item.update(resp[item.type]);
			has_photo = false;
			notify.open('Photo removed');
		} else {
			error = resp;
		}
	};
</script>

<Form title="{item.type} Photo" error={error.error}>
	<img
		{src}
		alt={item.name}
		class:dragover
		class:no_photo={!has_photo}
		onerror={() => (src = '/file_error.png')}
		onclick={() => {
			if (!has_photo) {
				input.click();
			}
		}}
		ondragover={(e) => {
			e.preventDefault();
			dragover = true;
		}}
		ondragenter={() => {}}
		ondragleave={(e) => {
			e.preventDefault();
			dragover = false;
		}}
		ondrop={(e) => {
			dragover = false;
			if (!has_photo) {
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
		accept="image/jpeg, image/png"
		bind:this={input}
		onchange={(e) => {
			validate();
		}}
	/>

	<div class="line">
		<Button
			primary
			onclick={() => {
				input.click();
			}}
		>
			{#if item.photo}
				<Icon icon="square-pen" />
				Change
			{:else}
				<Icon icon="plus" />
				Add
			{/if}
		</Button>

		{#if has_photo}
			<Button
				--button-background-color-hover="red"
				onclick={() => {
					remove('delete');
				}}
			>
				<Icon icon="trash-2" />
				Delete
			</Button>
		{/if}
	</div>
</Form>

<style>
	img {
		width: 100%;
		border-radius: var(--sp1);
		outline: 2px solid transparent;
		transition:
			outline-color var(--trans),
			transform var(--trans);
	}
	img.no_photo:hover,
	.dragover.no_photo {
		outline-color: var(--cl1);
		cursor: pointer;
	}

	.line {
		margin-top: 16px;
	}
</style>
