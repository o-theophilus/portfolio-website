<script>
	import { module, notify, loading } from '$lib/store_old.js';
	import { token } from '$lib/cookie.js';

	import Button from '$lib/button_old/button.svelte';
	import IG from '$lib/input_group.svelte';
	import Icon from '$lib/icon.svelte';
	import Code from '$lib/input_code.svelte';

	let form = {
		...$module.form
	};
	let error = {};

	const validate = () => {
		error = {};

		if (!form.code_2) {
			error.code_2 = 'cannot be empty';
		} else if (form.code_2.length != 6) {
			error.code_2 = 'invalid code';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		$loading = 'loading . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/user/email/4`, {
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
			$module.update(resp.user);
			$notify.add('Email changed');
			$module = null;
		} else {
			error = resp;
		}
	};
</script>

<form on:submit|preventDefault novalidate autocomplete="off">
	<strong class="ititle"> Change Email </strong>

	{#if error.error}
		<div class="error">
			{error.error}
		</div>
	{/if}

	<div class="message">Code has been sent to: {form.email}.</div>

	<IG name="Code" error={error.code_2}>
		<Code bind:value={form.code_2} />
	</IG>

	<Button primary on:click={validate}>
		Submit
		<Icon icon="send" />
	</Button>
</form>

<style>
	form {
		padding: var(--sp3);
	}

	.error,
	.message {
		margin: var(--sp2) 0;
	}

	.message {
		background-color: color-mix(in srgb, var(--cl1), transparent 80%);
		color: var(--clb);
		padding: var(--sp1);
		width: 100%;
	}
</style>
