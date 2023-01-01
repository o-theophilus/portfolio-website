<script>
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
		if (!post.description) {
			error = 'cannot be empty';
		}

		!error && submit();
	};

	const submit = async () => {
		const resp = await fetch(`${api_url}/${post_type}/description/${post.slug}`, {
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
						title: `${post_type} description edited`,
						status: 'good',
						message: `${post_type} description edited successfully`,
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
		{post_type} description
	</strong>
	<form on:submit|preventDefault novalidate autocomplete="off">
		<Input name="description" {error} let:id>
			<textarea placeholder="description here" {id} bind:value={post.description} />
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
