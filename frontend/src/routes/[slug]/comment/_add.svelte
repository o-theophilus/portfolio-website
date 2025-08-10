<script>
	import { module, loading, notify, app } from '$lib/store.svelte.js';

	import { IG } from '$lib/input';
	import { Button } from '$lib/button';
	import { Icon, Marked } from '$lib/macro';

	let form = {
		path: module.value.path
	};
	let comment = '';
	if (module.value.comment) {
		comment = module.value.comment;
	}
	let error = {};

	const validate = () => {
		error = {};

		if (!form.comment) {
			error.comment = 'cannot be empty';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		loading.open('Adding Comment . . .');
		let resp = await fetch(
			`${import.meta.env.VITE_BACKEND}/comment/${module.value.post_key}?${new URLSearchParams(
				module.value.search
			).toString()}`,
			{
				method: 'post',
				headers: {
					'Content-Type': 'application/json',
					Authorization: app.token
				},
				body: JSON.stringify(form)
			}
		);
		resp = await resp.json();
		loading.close();

		if (resp.status == 200) {
			module.value.update(resp.comments);
			module.close();
			notify.open('Comment Added');
		} else {
			error = resp;
		}
	};
</script>

<form onsubmit={(e) => e.preventDefault()} novalidate autocomplete="off">
	<strong class="ititle">
		{#if comment}
			Reply
		{:else}
			Add
		{/if}
		Comment
	</strong>
	{#if error.error}
		<div class="error">
			{error.error}
		</div>
	{/if}

	{#if comment}
		<div class="comment">
			<Marked content={comment} />
		</div>
	{/if}

	<IG
		name="Comment"
		error={error.comment}
		type="textarea"
		placeholder="Comment here"
		bind:value={form.comment}
		on:keypress
	/>

	<Button onclick={validate}>
		Submit
		<Icon icon="send" />
	</Button>
</form>

<style>
	form {
		padding: var(--sp3);
	}
	.comment {
		padding: 1px var(--sp2);
		border-radius: var(--sp0);

		background-color: color-mix(in srgb, var(--cl1), transparent 80%);
		color: var(--ft1);
		font-size: 0.8rem;
	}

	.error {
		margin: var(--sp2) 0;
	}
</style>
