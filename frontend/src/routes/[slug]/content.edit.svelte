<script>
	import { module, loading, notification } from '$lib/store.js';
	import { token } from '$lib/cookie.js';
	import { onMount } from 'svelte';

	import IG from '$lib/input_group.svelte';
	import Button from '$lib/button/button.svelte';
	import Icon from '$lib/icon.svelte';
	import Marked from '$lib/marked.svelte';

	let textarea;
	let content = '';
	let error = {};

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
			$module.update(resp.post);
			$module.refresh();
			$module = null;
			$notification = {
				message: 'Content Saved'
			};
		} else {
			error = resp;
		}
	};

	onMount(() => {
		textarea.value = $module.post.content;
		content = $module.process_content($module.post.content);
	});
</script>

<form on:submit|preventDefault novalidate autocomplete="off">
	<strong class="ititle"> Edit Content </strong>

	<IG>
		<div class="block">
			<div class="marked">
				<Marked {content} />
			</div>
			<textarea
				placeholder="Content here"
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
				on:keyup={() => {
					content = $module.process_content(textarea.value);
				}}
			/>
		</div>
	</IG>

	{#if error.error}
		<div class="error">
			{error.error}
		</div>
	{/if}

	{#if error.content}
		<div class="error">
			{error.content}
		</div>
	{/if}

	<Button on:click={validate}>
		Submit
		<Icon icon="send" />
	</Button>
</form>

<style>
	form {
		padding: var(--sp3);
	}

	.block {
		display: flex;
		flex-direction: column;
		gap: var(--sp2);

		height: calc(100vh - var(--sp4) * 5);
	}
	.marked,
	textarea {
		height: 100%;
	}

	.marked {
		overflow: auto;
		display: none;
	}

	@media screen and (min-width: 700px) {
		.block {
			flex-direction: unset;
		}
		.marked {
			display: block;
		}
		.marked,
		textarea {
			width: 100%;
		}
	}

	@media screen and (min-height: 600px) {
		.marked {
			display: block;
		}
	}

	textarea {
		display: block;

		resize: none;
		padding: var(--sp2);
		border-radius: var(--sp0);
		border: none;

		outline: 2px solid transparent;
		background-color: var(--bg2);
		color: var(--ft1);

		transition: outline-color var(--trans);
	}

	textarea:hover:not(.disabled) {
		outline-color: var(--ft1);
	}

	textarea:focus {
		outline-color: var(--ft1);
	}

	.error {
		margin: var(--sp2) 0;
	}
</style>
