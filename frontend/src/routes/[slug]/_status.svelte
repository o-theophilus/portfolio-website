<script>
	import { module, portal, loading } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Button from '$lib/button/button.svelte';
	import Dialogue from '$lib/dialogue.svelte';
	import Icon from '$lib/icon.svelte';
	import Delete from './_status.delete.svelte';

	let _status = $module.post.status;

	let error = {};

	const submit = async (status) => {
		error = {};

		$loading = 'Saving Post . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/post/${$module.post.key}`, {
			method: 'put',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({ status })
		});
		resp = await resp.json();
		$loading = false;

		if (resp.status == 200) {
			$portal = {
				for: 'post',
				data: resp.post
			};

			$module = {
				module: Dialogue,
				message: 'Status Changed',
				buttons: [
					{
						name: 'Ok',
						fn: () => {
							$module = '';
						}
					}
				]
			};
		} else {
			error = resp;
		}
	};
</script>

<div class="content">
	<strong class="ititle">Change Status</strong>
	<br /><br />
	<div>Status: <strong>{_status}</strong></div>
	<br />

	<div>Change to:</div>
	<div class="line">
		{#if _status != 'publish'}
			<Button
				on:click={() => {
					submit('publish');
				}}
			>
				<Icon icon="check" />
				{'publish'}
			</Button>
		{/if}

		{#if _status != 'draft'}
			<Button
				on:click={() => {
					submit('draft');
				}}
			>
				<Icon icon="design_services" />
				{'draft'}
			</Button>
		{/if}

		{#if _status != 'delete'}
			<Button
				on:click={() => {
					$module = {
						module: Delete,
						post: $module.post
					};
				}}
			>
				<Icon icon="delete" />
				Delete
			</Button>
		{/if}
	</div>

	{#if error.error}
		<span class="error">
			{error.error}
		</span>
	{/if}
	{#if error.status}
		<span class="error">
			{error.status}
		</span>
	{/if}
</div>

<style>
	.content {
		padding: var(--sp3);
	}

	.line {
		display: flex;
		gap: var(--sp1);
	}
</style>
