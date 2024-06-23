<script>
	import { module, loading } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import IG from '$lib/input_group.svelte';
	import Button from '$lib/button/button.svelte';
	import Icon from '$lib/icon.svelte';
	import Dialogue from '$lib/dialogue.svelte';

	let form = {};
	let error = {};

	const validate = () => {
		error = {};

		if (!form.author_email) {
			error.author_email = 'cannot be empty';
		} else if (!/\S+@\S+\.\S+/.test(form.author_email)) {
			error.author_email = 'invalid email';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		$loading = 'Loading . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/post/${$module.post_key}`, {
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
			$module.update(resp.post);
			$module = {
				module: Dialogue,
				message: `A confirmation email has been sent to <b>${form.author_email}</b>`,
				buttons: [
					{
						name: 'OK',
						icon: 'check',
						fn: () => {
							$module = null;
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
	<strong class="ititle"> Edit Author </strong>
	{#if error.error}

		<div class="error">
			{error.error}
		</div>
	{/if}

	<IG
		name="Author Email"
		icon="email"
		error={error.author_email}
		placeholder="Email here"
		type="text"
		bind:value={form.author_email}
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
