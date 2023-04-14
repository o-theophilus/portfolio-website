<script>
	import { api_url, module, tick } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Input from '$lib/comp/input_group.svelte';
	import Button from '$lib/comp/button.svelte';
	import Info from '$lib/module/info.svelte';

	export let post;

	let error = {};

	const validate = () => {
		error = {};

		if (!post.format) {
			error.format = 'cannot be empty';
		}
		if (!post.content) {
			error.content = 'cannot be empty';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		const resp = await fetch(`${api_url}/${post.type}/content/${post.slug}`, {
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
					message: 'Content Saved',
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
	<strong class="big"> Edit Content </strong>
	<Input name="format" error={error.format} let:id>
		<label>
			<input type="radio" bind:group={post.format} value="markdown" />
			Markdown
		</label>

		<label>
			<input type="radio" bind:group={post.format} value="url" />
			URL
		</label>
	</Input>
	<Input name="content" error={error.content} let:id>
		{#if post.format == 'markdown'}
			<textarea placeholder="Content here" {id} bind:value={post.content} on:keypress />
		{:else if post.format == 'url'}
			<input placeholder="Content here" type="text" {id} bind:value={post.content} />
		{/if}
	</Input>

	<Button
		on:click={() => {
			validate();
		}}
	>
		Submit
	</Button>
</form>

<style>
	form {
		padding: var(--gap3);
	}

	textarea {
		max-width: 600px;
		width: calc(100vw - var(--gap5) * 2);
		min-height: 160px;
		height: calc(100vh - var(--gap5) * 9);
	}
</style>
