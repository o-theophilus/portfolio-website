<script>
	import { module, portal, loading, notification } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import IG from '$lib/input_group.svelte';
	import Button from '$lib/button/button.svelte';
	import Icon from '$lib/icon.svelte';
	import Dialogue from '$lib/dialogue.svelte';
	import Marked from '$lib/marked.svelte';

	let form = {
		path: $module.path
	};
	let comment = '';
	if ($module.comment) {
		comment = $module.comment;
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
		$loading = 'Adding Comment . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/comment/${$module.post_key}`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify(form)
		});
		resp = await resp.json();
		$loading = false;

		if (resp.status == 200) {
			console.log(resp.comments);
			$portal = {
				for: 'comment',
				data: resp.comments
			};

			$notification = {
				status: 200,
				message: 'Comment Added'
			};

			$module = null;
		} else {
			error = resp;
		}
	};
</script>

<form on:submit|preventDefault novalidate autocomplete="off">
	<strong class="ititle">
		{#if comment}
			Reply
		{:else}
			Add
		{/if}
		Comment
	</strong>
	{#if error.error}
		<br />
		<span class="error">
			{error.error}
		</span>
	{/if}

	{#if comment}
		<div class="comment">
			<Marked md={comment} />
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

	<Button on:click={validate}>
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

		background-color: var(--cl1_l);
		color: var(--ft1);
		font-size: small;
	}
</style>
