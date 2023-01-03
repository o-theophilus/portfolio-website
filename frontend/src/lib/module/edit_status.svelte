<script>
	import { goto } from '$app/navigation';
	import { api_url, module, tick } from '$lib/store.js';

	import Button from '$lib/comp/button.svelte';
	import Info from '$lib/module/info.svelte';

	export let data;
	let { post } = data;
	let { post_type } = data;

	let error = '';

	const submit = async () => {
		const resp = await fetch(`${api_url}/${post_type}/status/${post.slug}`, {
			method: 'put',
			headers: {
				'Content-Type': 'application/json'
				// Authorization: session.token
			},
			body: JSON.stringify(post)
		});

		if (resp.ok) {
			const data = await resp.json();

			if (data.status == 200) {
				tick(data.data.post);

				$module = {
					module: Info,
					data: {
						title: 'Done',
						status: 'good',
						message: 'Status Changed',
						button: [
							{
								name: 'Ok',
								href: ''
							}
						]
					}
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

<section>
	<strong class="big">Status</strong>
	<div class="content">
		<div>Status: {post.status}</div>
		<br />
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
</section>

<style>
	section {
		display: flex;
		flex-direction: column;

		width: 100%;
	}
	strong,
	.content {
		padding: var(--gap3);
	}
	strong {
		border-bottom: 2px solid var(--mid_color);
	}
</style>
