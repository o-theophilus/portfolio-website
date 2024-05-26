<script>
	import { module, portal, loading } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Input from '$lib/input_group.svelte';
	import Button from '$lib/button.svelte';
	import Info from '$lib/info.svelte';
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
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/post/content/${post.key}`, {
			method: 'put',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify(form)
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
				message: 'Content Saved',
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
	<strong class="big"> Edit Content </strong>

	{#if error.error}
		<span class="error">
			{error.error}
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
