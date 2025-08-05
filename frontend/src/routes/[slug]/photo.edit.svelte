<script>
	import { loading, notify, module, app } from '$lib/store.svelte.js';

	import { Button } from '$lib/button';
	import { Icon } from '$lib/macro';

	let entity = { ...module.value.entity };

	let has_photo = entity.photo ? true : false;
	let error = {};
	let input;
	let dragover = false;

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
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/${entity.type}/photo/${entity.key}`, {
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
			entity.photo = resp[entity.type].photo;
			module.value.update(resp[entity.type]);
			has_photo = true;
			get_din();
			notify.open('Photo updated');
		} else {
			error = resp;
		}
	};

	const remove = async () => {
		error = {};

		loading.open('removing . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/${entity.type}/photo/${entity.key}`, {
			method: 'delete',
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			}
		});
		resp = await resp.json();
		loading.close();

		if (resp.status == 200) {
			entity.photo = null;
			module.value.update(resp[entity.type]);
			has_photo = false;
			notify.open('Photo removed');
		} else {
			error = resp;
		}
	};

	let dim = [1, 1];

	const get_din = () => {
		dim = [1, 1];
		let match = entity.photo?.match(/_(\d+)x(\d+)\./);
		if (match) {
			dim = [parseInt(match[1]), parseInt(match[2])];
		}
	};

	get_din();
</script>

<div class="comp">
	<strong class="ititle"> {entity.type} Photo </strong>
	<br />
	<br />
	<!-- onerror="this.src='/file_error.png';" -->
	<img
		src={entity.photo || '/select_photo.png'}
		alt={entity.name}
		class:dragover
		class:no_photo={!has_photo}
		style:--ar={dim[0] / dim[1]}
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

	{#if error.error}
		<div class="error">
			{@html error.error}
		</div>
	{/if}

	<div class="line">
		<Button
			primary
			onclick={() => {
				input.click();
			}}
		>
			{#if entity.photo}
				<Icon icon="edit" />
				Change
			{:else}
				<Icon icon="add" />
				Add
			{/if}
		</Button>

		{#if has_photo}
			<Button
				onclick={() => {
					remove('delete');
				}}
			>
				<Icon icon="delete" />
				Delete
			</Button>
		{/if}
	</div>
</div>

<style>
	.comp {
		padding: var(--sp3);
	}

	.ititle {
		text-transform: capitalize;
	}

	.error {
		margin: var(--sp2) 0;
	}

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
		display: flex;
		gap: var(--sp1);
	}
</style>
