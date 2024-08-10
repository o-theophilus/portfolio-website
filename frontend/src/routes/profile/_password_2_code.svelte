<script>
	import { module, loading, user } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Button from '$lib/button/button.svelte';
	import IG from '$lib/input_group.svelte';
	import Icon from '$lib/icon.svelte';
	import Code from '$lib/input_code.svelte';

	import Password from './_password_3_password.svelte';

	let form = {
		...$module.form
	};
	let error = {};

	const validate = () => {
		error = {};

		if (!form.code) {
			error.code = 'cannot be empty';
		} else if (form.code.length != 6) {
			error.code = 'invalid code';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		$loading = 'loading . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/user/password/2`, {
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
			$module = {
				module: Password,
				form
			};
		} else {
			error = resp;
		}
	};
</script>

<form on:submit|preventDefault novalidate autocomplete="off">
	<strong class="ititle"> Change Password </strong>

	{#if error.error}
		<div class="error">
			{error.error}
		</div>
	{/if}
	<br />

	<br />
	<div class="message">Code has been sent to: {$user.email}.</div>

	<IG name="Code" error={error.code}>
		<Code bind:value={form.code} />
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

	.error {
		margin: var(--sp2) 0;
	}

	.message {
		background-color: var(--cl1_l);
		color: var(--clb);
		padding: var(--sp1);
		width: 100%;
	}
</style>
