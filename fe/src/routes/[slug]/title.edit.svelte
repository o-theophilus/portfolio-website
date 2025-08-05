<script>
	import { module, loading, notify } from '$lib/store_old.js';
	import { token } from '$lib/cookie.js';

	import IG from '$lib/input_group.svelte';
	import Button from '$lib/button_old/button.svelte';
	import Icon from '$lib/icon.svelte';

	let form = {
		title: $module.post.title
	};

	let error = {};

	const validate = () => {
		error = {};
		if (!form.title) {
			error.title = 'cannot be empty';
		} else if (form.title == $module.post.title) {
			error.title = 'no change';
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
			body: JSON.stringify(form)
		});
		resp = await resp.json();
		$loading = false;

		if (resp.status == 200) {
			window.history.replaceState(history.state, '', `/${resp.post.slug}`);
			$module.update(resp.post);
			$module = null;
			$notify.add('Title Saved');
		} else {
			error = resp;
		}
	};
</script>

<form on:submit|preventDefault novalidate autocomplete="off">
	<strong class="ititle"> Edit title </strong>
	{#if error.error}
		<div class="error">
			{error.error}
		</div>
	{/if}

	<IG
		name="Title"
		icon="edit"
		error={error.title}
		placeholder="Title here"
		type="text"
		bind:value={form.title}
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

	.error {
		margin: var(--sp2) 0;
	}
</style>
