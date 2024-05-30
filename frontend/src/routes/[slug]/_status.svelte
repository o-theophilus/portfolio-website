<script>
	import { module, portal, loading } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Button from '$lib/button.svelte';
	import Info from '$lib/info.svelte';
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
				module: Info,
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
	<strong class="big">Change Status</strong>
	<br /><br />
	<div>Status: <strong>{_status}</strong></div>
	<div>Change to:</div>
	<div class="line">
		{#each ['draft', 'publish'] as x}
			{#if _status != x}
				<Button
					on:click={() => {
						submit(x);
					}}
				>
					{x}
				</Button>
			{/if}
		{/each}
		{#if _status != 'delete'}
			<Button
				on:click={() => {
					$module = {
						module: Delete,
						post: $module.post
					};
				}}>Delete</Button
			>
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
</style>
