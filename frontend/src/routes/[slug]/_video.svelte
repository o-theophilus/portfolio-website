<script>
	import { module, portal, loading } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import IG from '$lib/input_group.svelte';
	import Button from '$lib/button/button.svelte';
	import Icon from '$lib/icon.svelte';
	import Dialogue from '$lib/dialogue.svelte';

	let post = $module.post;
	let video_count = $module.video_count;
	let videos = [...post.videos];
	let error = {};

	const validate = () => {
		error = {};

		if (videos.filter(Boolean).sort().join(', ') == post.videos.slice().sort().join(', ')) {
			error.videos = 'no change';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		error = {};

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
			$portal = {
				for: 'post',
				data: resp.post
			};

			$module = {
				module: Dialogue,
				message: `Videos Updated`,
				buttons: [
					{
						name: 'OK',
						icon: 'check',
						fn: () => {
							$module = null;
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
	<strong class="ititle"> Manage Video </strong>
	{#if error.error}
		<div class="error">
			{error.error}
		</div>
	{/if}

	<IG name="Video{video_count > 1 ? 's' : ''}" error={error.videos}>
		{#each Array(video_count) as _, i}
			<IG
				icon="Movie"
				error={error.title}
				placeholder="Video {i + 1} here"
				type="text"
				bind:value={videos[i]}
				no_pad
			/>
		{/each}
	</IG>

	<Button on:click={validate}>
		Submit
		<Icon icon="send" />
	</Button>
</form>

<style>
	form {
		padding: var(--sp3);
	}
	.error {
		margin: var(--sp2) 0;
	}
</style>
