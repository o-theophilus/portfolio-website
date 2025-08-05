<script>
	import { module, loading, app } from '$lib/store.svelte.js';

	import { Button } from '$lib/button';
	import { IG } from '$lib/input';
	import { Icon } from '$lib/macro';

	import Email from './_email_3_email.svelte';

	let form = {
		...module.value.form
	};
	let error = {};

	const validate = () => {
		error = {};

		if (!form.code_1) {
			error.code_1 = 'cannot be empty';
		} else if (form.code_1.length != 6) {
			error.code_1 = 'invalid code';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		loading.open('loading . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/user/email/2`, {
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
			module.open(Email, { ...form, update: module.value.update });
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
	<br />

	<br />
	<div class="message">Code has been sent to: {app.user.email}.</div>

	<IG name="Code" error={error.code_1} bind:value={form.code_1} type="code"></IG>

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
