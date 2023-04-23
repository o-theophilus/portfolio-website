<script>
	import { api_url, module, portal, loading } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Input from '$lib/input_group.svelte';
	import Button from '$lib/button.svelte';
	import Info from '$lib/__info__.svelte';

	export let post;

	let videos = [...post.videos];
	let error = '';

	const submit = async () => {
		error = '';

		$loading = `Saving ${post.type} . . .`;
		const resp = await fetch(`${api_url}/post/videos/${post.key}`, {
			method: 'put',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({ videos })
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
					message: `Videos Updated`,
					button: [
						{
							name: 'OK',
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

<form on:submit|preventDefault novalidate autocomplete="off">
	<strong class="big"> Manage Video </strong>
	{#if error}
		<span class="error">
			{error}
		</span>
	{/if}
	<Input name="video{post.video_count > 1 ? 's' : ''}" let:id>
		{#each Array(post.video_count) as v, i}
			<input placeholder="video {i + 1} here " type="text" bind:value={videos[i]} />
		{/each}
	</Input>

	<Button
		on:click={() => {
			submit();
		}}
	>
		Submit
	</Button>
</form>

<style>
	form {
		padding: var(--gap3);
	}
</style>
