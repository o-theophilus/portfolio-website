<script>
	import { module, portal, loading } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Button from '$lib/button.svelte';
	import Info from '$lib/info.svelte';

	export let post;

	let error = {};

	const submit = async (status) => {
		error = {};

		$loading = 'Saving Post . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/post/status/${post.key}`, {
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
			portal({
				for: 'post',
				data: resp.post
			});

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
	<div>Status: <strong>{post.status}</strong></div>
	<div>Change to:</div>
	{#if error.error}
		<span class="error">
			{error.error}
		</span>
	{/if}
	<div class="row">
		{#each ['draft', 'publish'] as status}
			{#if status != post.status}
				<Button
					on:click={() => {
						submit(status);
					}}
				>
					{status}
				</Button>
			{/if}
		{/each}
	</div>
</div>

<style>
	.content {
		padding: var(--gap3);
	}
</style>
