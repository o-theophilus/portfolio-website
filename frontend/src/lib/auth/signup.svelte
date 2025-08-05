<script>
	import { module, loading, app } from '$lib/store.svelte.js';

	import { IG } from '$lib/input';
	import { Button, Link } from '$lib/button';
	import { Icon } from '$lib/macro';
	import Login from './login.svelte';
	import EmailTemplate from './confirm.template.svelte';
	import Confirm from './confirm.svelte';

	let email_template;
	let show_password = false;

	let form = {
		email: module.value.email
	};
	let error = {};

	const validate = () => {
		error = {};

		if (!form.name) {
			error.name = 'cannot be empty';
		}
		if (!form.email) {
			error.email = 'cannot be empty';
		} else if (!/\S+@\S+\.\S+/.test(form.email)) {
			error.email = 'invalid email';
		}
		if (!form.password) {
			error.password = 'cannot be empty';
		} else if (
			!/[a-z]/.test(form.password) ||
			!/[A-Z]/.test(form.password) ||
			!/[0-9]/.test(form.password) ||
			form.password.length < 8 ||
			form.password.length > 18
		) {
			error.password =
				'must include at least 1 lowercase letter, 1 uppercase letter, 1 number and must contain 8 - 18 characters';
		}

		if (!form.confirm_password) {
			error.confirm_password = 'cannot be empty';
		} else if (form.password && form.password != form.confirm_password) {
			error.confirm_password = 'does not match password';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		form.email_template = email_template.innerHTML.replace(/&amp;/g, '&');

		loading.open('Loading . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/signup`, {
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
			module.open(Confirm, { email: form.email });
		} else {
			error = resp;
		}
	};
</script>

<form on:submit|preventDefault novalidate autocomplete="off">
	<strong class="ititle"> Signup </strong>
	{#if error.error}
		<div class="error">
			{error.error}
		</div>
	{/if}
	<IG
		name="Name"
		icon="person"
		error={error.name}
		placeholder="Name here"
		type="text"
		bind:value={form.name}
	/>
	<IG
		name="Email"
		icon="email"
		error={error.email}
		placeholder="Email here"
		type="text"
		bind:value={form.email}
	/>
	<IG
		name="Password"
		icon="key"
		error={error.password}
		placeholder="Password here"
		type={show_password ? 'text' : 'password'}
		bind:value={form.password}
	></IG>
	<IG
		name="Confirm Password"
		icon="key"
		error={error.confirm_password}
		placeholder="Password here"
		type={show_password ? 'text' : 'password'}
		bind:value={form.confirm_password}
	/>

	<Button onclick={validate}>
		Submit
		<Icon icon="send" />
	</Button>

	<br />

	<Link onclick={() => module.open(Login, { email: form.email })}>Login</Link>
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
