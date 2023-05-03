<script>
	import { api_url, module, portal, loading } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Input from '$lib/input_group.svelte';
	import Button from '$lib/button.svelte';
	import Info from '$lib/__info__.svelte';
	import { onMount } from 'svelte';

	export let post;

	let form = {};
	let error = {};

	let textarea;
	onMount(() => {
		textarea.value = post.content;
	});

	const validate = () => {
		error = {};
		form.content = textarea.value;

		if (!form.content) {
			error.content = 'cannot be empty';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		$loading = 'Saving Post . . .';
		const resp = await fetch(`${api_url}/post/content/${post.key}`, {
			method: 'put',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify(form)
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
			} else if (data.status == 201) {
				error = data.message;
			} else {
				error.form = data.message;
			}
		}
	};
</script>

<form on:submit|preventDefault novalidate autocomplete="off">
	<strong class="big"> Edit Content </strong>

	{#if error.form}
		<span class="error">
			{error.form}
		</span>
	{/if}

	<Input name="content" error={error.content} let:id>
		<textarea
			placeholder="Content here"
			{id}
			bind:this={textarea}
			on:keydown={(e) => {
				if (e.key === 'Tab') {
					e.preventDefault();
					const start = e.target.selectionStart;
					const end = e.target.selectionEnd;

					const text = textarea.value;
					textarea.value = `${text.substring(0, start)}\t${text.substring(end)}`;

					e.target.selectionStart = e.target.selectionEnd = start + 1;
				}
			}}
		/>
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
