<script>
	import { module, loading, app } from '$lib/store.svelte.js';

	import { Button } from '$lib/button';
	import { IG } from '$lib/input';
	import { Icon } from '$lib/macro';

	import Password from './_password_3_password.svelte';

	let form = {
		...module.value.form
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
		loading.open('loading . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/user/password/2`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			},
			body: JSON.stringify(form)
		});
		resp = await resp.json();
		loading.close();

		if (resp.status == 200) {
			module.open(Password, form);
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
	<div class="message">Code has been sent to: {app.user.email}.</div>

	<IG name="Code" error={error.code} bind:value={form.code} type="code"></IG>

	<Button primary onclick={validate}>
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
		background-color: color-mix(in srgb, var(--cl1), transparent 80%);
		color: var(--clb);
		padding: var(--sp1);
		width: 100%;
	}
</style>
