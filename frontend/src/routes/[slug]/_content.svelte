<script>
	import { module, portal, loading } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import IG from '$lib/input_group.svelte';
	import Button from '$lib/button/button.svelte';
	import Icon from '$lib/icon.svelte';
	import Dialogue from '$lib/dialogue.svelte';
	import { onMount } from 'svelte';

	let error = {};

	let textarea;

	onMount(() => {
		textarea.value = $module.post.content;
	});

	const validate = () => {
		error = {};

		if (!textarea.value) {
			error.content = 'cannot be empty';
		} else if (textarea.value == $module.post.content) {
			error.content = 'no change';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		$loading = 'Saving Post . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/post/${$module.post.key}`, {
			method: 'put',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({
				content: textarea.value
			})
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
	<strong class="ititle"> Edit Content </strong>

	{#if error.error}
		<span class="error">
			{error.error}
		</span>
	{/if}

	<IG name="content" error={error.content} let:id>
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

	textarea {
		display: block;

		max-width: 600px;
		width: calc(100vw - var(--sp4) * 2);
		min-height: 160px;
		height: calc(100vh - var(--sp4) * 9);
		resize: none;
		padding: var(--sp2);
		border-radius: var(--sp0);
		border: none;

		outline: 2px solid transparent;
		background-color: var(--ac4);
		color: var(--ac1);

		transition: outline-color var(--trans);
	}

	textarea:hover:not(.disabled) {
		outline-color: var(--ac1);
	}

	textarea:focus {
		outline-color: var(--ac1);
	}
</style>
