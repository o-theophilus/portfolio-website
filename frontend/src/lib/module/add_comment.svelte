<script>
	import { api_url, module, tick } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Input from '$lib/comp/input_group.svelte';
	import Button from '$lib/comp/button.svelte';
	import Info from '$lib/module/info.svelte';

	export let post;
	export let comment_key = '';
	console.log(comment_key);

	let form = {
		comment_key
	};
	let error = {};

	const validate = () => {
		error = {};

		if (!form.name) {
			error.name = 'cannot be empty';
		}
		if (!form.email) {
			error.email = 'cannot be empty';
		} else if (!/\S+@\S+\.\S+/.test(form.email)) {
			error.email = 'invalid email';
		}
		if (!form.comment) {
			error.comment = 'cannot be empty';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		const resp = await fetch(`${api_url}/${post.type}/comment/${post.slug}`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify(form)
		});

		if (resp.ok) {
			const data = await resp.json();

			if (data.status == 200) {
				tick(data.data.post);

				$module = {
					module: Info,
					title: 'Done',
					status: 'good',
					message: 'Comment Added',
					button: [
						{
							name: 'OK',
							href: ''
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
	<strong class="big"> Add Comment </strong>
	<form on:submit|preventDefault novalidate autocomplete="off">
		<Input name="name" error={error.name} let:id>
			<input placeholder="Name here" type="text" {id} bind:value={form.name} />
		</Input>
		<Input name="email" error={error.email} let:id>
			<input placeholder="Email here" type="text" {id} bind:value={form.email} />
		</Input>
		<Input name="comment" error={error.comment} let:id>
			<textarea placeholder="Comment here" {id} bind:value={form.comment} on:keypress />
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
