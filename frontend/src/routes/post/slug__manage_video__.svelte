<script>
	import { api_url, module, tick } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Input from '$lib/input_group.svelte';
	import Button from '$lib/button.svelte';
	import Info from '$lib/__info__.svelte';

	export let post;

	let videos = [...post.videos];
	let error;

	const submit = async () => {
		const resp = await fetch(`${api_url}/${post.type}/videos/${post.slug}`, {
			method: 'put',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({ videos })
		});

		if (resp.ok) {
			const data = await resp.json();
			if (data.status == 200) {
				tick(data.data.post);

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

<section>
	<strong class="big"> Manage Video </strong>
	<form on:submit|preventDefault novalidate autocomplete="off">
		<Input name="video{post.video_count > 1 ? 's' : ''}" {error} let:id>
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
</section>

<style>
	section {
		display: flex;
		flex-direction: column;

		width: 100%;
	}
	strong,
	form {
		padding: var(--gap3);
	}
	strong {
		border-bottom: 2px solid var(--accent3);
	}
</style>
