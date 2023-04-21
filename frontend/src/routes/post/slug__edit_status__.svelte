<script>
	import { api_url, module, tick } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Button from '$lib/button.svelte';
	import Info from '$lib/__info__.svelte';

	export let post;

	let error = '';

	const submit = async () => {
		const resp = await fetch(`${api_url}/${post.type}/status/${post.slug}`, {
			method: 'put',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify(post)
		});

		if (resp.ok) {
			const data = await resp.json();

			if (data.status == 200) {
				tick(data.data.post);

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
	let status = ['draft', 'publish'];
	status = status.filter(function (s) {
		return s != post.status;
	});
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
		{#each status as s}
			<Button
				on:click={() => {
					post.temp_status = s;
					submit();
				}}
			>
				{s}
			</Button>
		{/each}
	</div>
</div>

<style>
	.content {
		padding: var(--gap3);
	}
</style>
