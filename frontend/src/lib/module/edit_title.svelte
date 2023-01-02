<script>
	import { goto } from '$app/navigation';
	import { api_url, module, tick } from '$lib/store.js';

	import Input from '$lib/comp/input_group.svelte';
	import Button from '$lib/comp/button.svelte';
	import Info from '$lib/module/info.svelte';

	export let data;
	let { post_type } = data;

	let { post } = data;
	let error = '';

	const validate = () => {
		error = '';
		if (!post.title) {
			error = 'cannot be empty';
		}

		!error && submit();
	};

	const submit = async () => {
		const resp = await fetch(`${api_url}/${post_type}/title/${post.slug}`, {
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
						message: "Title Saved",
						button: [
							{
								name: 'OK',
								href: ''
							}
						]
					}
				};
				goto(`/${post_type}/${data.data.post.slug}`);
			} else {
				error = data.message;
			}
		}
	};
</script>

<section>
	<strong class="big">
		Edit {post_type} title
	</strong>
	<form on:submit|preventDefault novalidate autocomplete="off">
		<Input name="title" {error} let:id>
			<input placeholder="Title here" type="text" {id} bind:value={post.title} />
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

		width: 100%;
	}
	strong,
	form {
		padding: var(--gap3);
	}
	strong {
		border-bottom: 2px solid var(--mid_color);
	}
</style>
