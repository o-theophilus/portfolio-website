<script>
	import { page } from '$app/state';

	import { module, loading, app } from '$lib/store.svelte.js';

	import { IG } from '$lib/input';
	import { Button, Link } from '$lib/button';
	import { Icon } from '$lib/macro';
	import Signup from './signup.svelte';
	import Forgot from './forgot_1.email.svelte';
	import EmailTemplate from './confirm.template.svelte';
	import Confirm from './confirm.svelte';

	let email_template;
	let show_password = false;

	let form = {
		email: module.value.email
	};
	let error = {};

	let return_url = page.url.pathname;
	if (module.value.return_url) {
		return_url = module.value.return_url;
	}

	const validate = () => {
		error = {};

		if (!form.email) {
			error.email = 'cannot be empty';
		}
		if (!form.password) {
			error.password = 'cannot be empty';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		form.email_template = email_template.innerHTML.replace(/&amp;/g, '&');

		loading.open('Loading . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/login`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			},
			body: JSON.stringify(form)
		});

		resp = await resp.json();
		if (resp.status != 200) {
			loading.close();
		}

		if (resp.status == 200) {
			app.token = resp.token;
			document.location = return_url;
		} else if (resp.error == 'not confirmed') {
			module.open(Confirm, { email: form.email });
		} else {
			error = resp;
		}
	};
</script>

<form on:submit|preventDefault novalidate autocomplete="off">
	<strong class="ititle"> Login </strong>
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

	<IG
		name="Password"
		icon="key"
		error={error.password}
		placeholder="Password here"
		type={show_password ? 'text' : 'password'}
		bind:value={form.password}
	></IG>

	<Button onclick={validate}>
		Submit
		<Icon icon="send" />
	</Button>

	<br />
	<div>
		<Link onclick={() => module.open(Signup, { email: form.email })}>Signup</Link>
		<span class="divider"> | </span>
		<Link onclick={() => module.open(Forgot, { email: form.email })}>Forgot Password</Link>
	</div>
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
