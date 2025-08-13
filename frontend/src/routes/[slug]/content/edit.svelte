<script>
	import { module, loading, notify, app } from '$lib/store.svelte.js';
	import { onMount } from 'svelte';

	import { IG } from '$lib/input';
	import { Button } from '$lib/button';
	import { Icon, Marked } from '$lib/macro';

	let textarea;
	let content = '';
	let error = $state({});

	const validate = () => {
		error = {};

		if (!textarea.value) {
			error.content = 'cannot be empty';
		} else if (textarea.value == module.value.post.content) {
			error.content = 'no change';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		loading.open('Saving Post . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/post/${module.value.post.key}`, {
			method: 'put',
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			},
			body: JSON.stringify({
				content: textarea.value
			})
		});
		resp = await resp.json();
		loading.close();

		if (resp.status == 200) {
			module.value.update(resp.post);
			module.value.refresh(resp.post);
			module.close();
			notify.open('Content Saved');
		} else {
			error = resp;
		}
	};

	onMount(() => {
		textarea.value = module.value.post.content;
		content = module.value.process_content(module.value.post.content);
	});
</script>

<form onsubmit={e.preventDefault} novalidate autocomplete="off">
	<strong class="ititle"> Edit Content </strong>

	<IG>
		<div class="block">
			<div class="marked">
				<Marked {content} />
			</div>
			<textarea
				placeholder="Content here"
				bind:this={textarea}
				onkeydown={(e) => {
					if (e.key === 'Tab') {
						e.preventDefault();
						const start = e.target.selectionStart;
						const end = e.target.selectionEnd;

						const text = textarea.value;
						textarea.value = `${text.substring(0, start)}\t${text.substring(end)}`;

						e.target.selectionStart = e.target.selectionEnd = start + 1;
					}
				}}
				onkeyup={() => {
					content = module.value.process_content(textarea.value);
				}}
			></textarea>
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

	<Button onclick={validate}>
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
		/* .block { */
		/* flex-direction: row-reverse; */
		/* } */
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
