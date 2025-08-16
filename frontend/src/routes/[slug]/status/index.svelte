<script>
	import { module, loading, notify, app } from '$lib/store.svelte.js';

	import { Button } from '$lib/button';
	import { Icon } from '$lib/macro';
	import Delete from './delete.svelte';

	let _status = module.value.post.status;

	let error = $state({});

	const submit = async (status) => {
		if (!module.value.post.photo) {
			error.error = 'no title photo';
			return;
		}
		error = {};

		loading.open('Saving Post . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/post/${module.value.post.key}`, {
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
			module.value.update(resp.post);
			module.close();
			notify.open('Status Changed');
		} else {
			error = resp;
		}
	};
</script>

<div class="content">
	<div class="page_title">Change Status</div>

	{#if error.error}
		<div class="error">
			{error.error}
		</div>
	{/if}
	{#if error.status}
		<div class="error">
			{error.status}
		</div>
	{/if}

	<div>
		Status: <div class="status">{_status}</div>
	</div>

	<div>Change to:</div>
	<div class="line">
		{#if _status != 'active'}
			<Button
				onclick={() => {
					submit('active');
				}}
			>
				<Icon icon="check" />
				{'active'}
			</Button>
		{/if}

		{#if _status != 'draft'}
			<Button
				onclick={() => {
					submit('draft');
				}}
			>
				<Icon icon="design_services" />
				{'draft'}
			</Button>
		{/if}

		{#if _status != 'delete'}
			<Button onclick={() => module.open(Delete, { post: module.value.post })}>
				<Icon icon="delete" />
				Delete
			</Button>
		{/if}
	</div>
</div>

<style>
	.content {
		padding: var(--sp3);
	}

	.page_title {
		margin-bottom: var(--sp2);
	}

	.line {
		display: flex;
		gap: var(--sp1);
	}

	.error {
		margin: var(--sp2) 0;
	}

	.status {
		font-weight: 800;
	}
</style>
