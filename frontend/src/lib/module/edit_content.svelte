<script>
	import { api_url, module, tick } from '$lib/store.js';

	import Input from '$lib/comp/input_group.svelte';
	import Button from '$lib/comp/button.svelte';
	import Info from '$lib/module/info.svelte';

	export let data;
	let { post_type } = data;

	let { post } = data;

	// let form = {
	// 	format: 'md'
	// };
	// post.format = 'md';

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
		const resp = await fetch(`${api_url}/${post_type}/content/${post.slug}`, {
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
						title: "Done",
						status: 'good',
						message: "Content Saved",
						button: [
							{
								name: 'OK',
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
</script>

<section>
	<strong class="big">
		Edit {post_type} content
	</strong>
	<form on:submit|preventDefault novalidate autocomplete="off">
		<Input name="format" error={error.format} let:id>
			<!-- <label>
				<input type="radio" bind:group={post.format} value="html" />
				HTML
			</label> -->

			<label>
				<input type="radio" bind:group={post.format} value="markdown" />
				Markdown
			</label>

			<label>
				<input type="radio" bind:group={post.format} value="url" />
				URL
			</label>
			<!-- <label>
				<input type="radio" bind:group={post.format} value="document" />
				Document
			</label> -->
		</Input>
		<Input name="content" error={error.content} let:id>
			{#if post.format == 'markdown'}
				<textarea
					placeholder="Content here"
					{id}
					bind:value={post.content}
					on:keypress
				/>
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
</section>

<style>
	section {
		display: flex;
		flex-direction: column;
	}
	strong,
	form {
		padding: var(--gap3);
	}
	strong {
		border-bottom: 2px solid var(--mid_color);
	}

	textarea {
		width: calc(100vw - var(--gap5) * 2);
		min-height: 160px;
		height: calc(100vh - var(--gap5) * 8);
	}
</style>
