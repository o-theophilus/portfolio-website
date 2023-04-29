<script>
	import { api_url, module, portal, loading } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Button from '$lib/button.svelte';
	import Info from '$lib/__info__.svelte';

	export let post;

	let error = '';

	const submit = async (status) => {
		error = '';

		$loading = `Saving ${post.type} . . .`;
		const resp = await fetch(`${api_url}/post/status/${post.key}`, {
			method: 'put',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({ status })
		});
		$loading = false;

		if (resp.ok) {
			const data = await resp.json();

			if (data.status == 200) {
				portal({
					for: 'post',
					data: data.data.post
				});

				$module = {
					module: Info,
					title: 'Done',
					status: 'good',
					message: 'Status Changed',
					button: [
						{
							name: 'Ok',
							fn: () => {
								$module = '';
							}
						}
					]
				};
			} else {
				error = data.message;
			}
		}
	};
</script>

<div class="content">
	<strong class="big">Change Status</strong>
	<br /><br />
	<div>Status: <strong>{post.status}</strong></div>
	<div>Change to:</div>
	{#if error}
		<span class="error">
			{error}
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
