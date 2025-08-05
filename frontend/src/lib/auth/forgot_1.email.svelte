<script>
	import { module, app, loading } from '$lib/store.svelte.js';

	import { IG } from '$lib/input';
	import { Icon } from '$lib/macro';
	import { Button, Link } from '$lib/button';

	import Login from './login.svelte';
	import Code from './forgot_2.code.svelte';
	import EmailTemplate from './forgot.template.svelte';

	let form = {
		email: module.value.email
	};
	let error = {};
	let email_template;

	const validate = () => {
		error = {};

		if (!form.email) {
			error.email = 'cannot be empty';
		} else if (!/\S+@\S+\.\S+/.test(form.email)) {
			error.email = 'invalid email';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		loading.open('Requesting Code . . .');
		form.email_template = email_template.innerHTML.replace(/&amp;/g, '&');

		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/forgot/1`, {
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
			module.open(Code, form);
		} else {
			error = resp;
		}
	};
</script>

<form on:submit|preventDefault novalidate autocomplete="off">
	<strong class="ititle"> Forgot Password </strong>

	{#if error.error}
		<div class="error">
			{error.error}
		</div>
	{/if}

	<IG
		name="Email"
		icon="email"
		error={error.email}
		type="email"
		bind:value={form.email}
		placeholder="Email here"
	/>

	<Button primary onclick={validate}
		>Submit
		<Icon icon="send" />
	</Button>

	<br />

	<Link
		onclick={() => {
			module.open(Login, { email: form.email });
		}}
	>
		Login
	</Link>
</form>

<div bind:this={email_template} style="display: none;">
	<EmailTemplate />
</div>

<style>
	form {
		padding: var(--sp3);
	}

	.error {
		margin: var(--sp2) 0;
	}
</style>
