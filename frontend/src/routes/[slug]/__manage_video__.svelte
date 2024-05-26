<script>
	import { module, portal, loading } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Input from '$lib/input_group.svelte';
	import Button from '$lib/button.svelte';
	import Info from '$lib/info.svelte';

	export let post;

	let videos = [...post.videos];
	let error = '';

	const submit = async () => {
		error = '';

		$loading = 'Saving Post . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/post/videos/${post.key}`, {
			method: 'put',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({ videos })
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
				message: `Videos Updated`,
				buttons: [
					{
						name: 'OK',
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

<form on:submit|preventDefault novalidate autocomplete="off">
	<strong class="big"> Manage Video </strong>
	{#if error}
		<span class="error">
			{error}
		</span>
	{/if}
	<Input name="video{post.video_count > 1 ? 's' : ''}">
		{#each Array(post.video_count) as _, i}
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
