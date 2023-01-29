<script>
	import { goto } from '$app/navigation';
	import { api_url, module } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Input from '$lib/comp/input_group.svelte';
	import Button from '$lib/comp/button.svelte';
	import Info from '$lib/module/info.svelte';

	export let data;
	let { post_type } = data;

	let title;
	let error;

	const validate = () => {
		error = '';
		if (!title) {
			error = 'cannot be empty';
		}

		!error && submit();
	};

	const submit = async () => {
		const resp = await fetch(`${api_url}/${post_type}`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({ title })
		});

		if (resp.ok) {
			const data = await resp.json();
			if (data.status == 200) {
				$module = {
					module: Info,
					data: {
						title: 'Done',
						status: 'good',
						message: `${post_type} Created`,
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
		add {post_type}
	</strong>
	<form on:submit|preventDefault novalidate autocomplete="off">
		<Input name="title" {error} let:id>
			<input placeholder="Title here" type="text" {id} bind:value={title} />
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
		text-transform: capitalize;
	}
</style>
