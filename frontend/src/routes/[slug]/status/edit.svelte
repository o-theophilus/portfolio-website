<script>
	import { module, loading, notify, app } from '$lib/store.svelte.js';

	import { Button } from '$lib/button';
	import { Form } from '$lib/layout';
	import Delete from './delete.svelte';
	import { slide } from 'svelte/transition';

	let post = {
		key: module.value.key,
		status: module.value.status,
		photo: module.value.photo
	};
	let _status = post.status;

	let error = $state({});

	const submit = async (status) => {
		if (!post.photo) {
			error.error = 'no title photo';
			return;
		}
		error = {};

		loading.open('Saving Post . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/post/${post.key}`, {
			method: 'put',
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			},
			body: JSON.stringify({ status })
		});
		resp = await resp.json();
		loading.close();

		if (resp.status == 200) {
			module.value.update(resp.item);
			module.close();
			notify.open('Status Changed');
		} else {
			error = resp;
		}
	};
</script>

<Form title="Change Status" error={error.error}>
	Status: <span class="status {_status}">{_status}</span>

	<br />
	<br />

	<div class="label">Change to:</div>

	{#if error.status}
		<div class="error" transition:slide>
			{error.status}
		</div>
	{/if}

	<div class="line">
		{#if _status != 'active'}
			<Button icon="check" onclick={() => submit('active')}>
				{'active'}
			</Button>
		{/if}

		{#if _status != 'draft'}
			<Button icon="square-pen" onclick={() => submit('draft')}>
				{'draft'}
			</Button>
		{/if}

		<Button
			--button-background-color-hover="red"
			icon="trash-2"
			onclick={() => module.open(Delete, { ...module.value })}
		>
			Delete
		</Button>
	</div>
</Form>

<style>
	.status {
		font-weight: 800;
	}
	.status.active {
		color: green;
	}
	.status.draft {
		color: red;
	}

	.label,
	.error {
		font-size: 0.8rem;
	}
	.error {
		color: red;
	}

	.line {
		margin-top: 8px;
	}
</style>
