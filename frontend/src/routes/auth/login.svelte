<script>
	import { page } from '$app/stores';

	import { module, loading } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import IG from '$lib/input_group.svelte';
	import Button from '$lib/button/button.svelte';
	import Link from '$lib/button/link.svelte';
	import Icon from '$lib/icon.svelte';
	import Dialogue from '$lib/dialogue.svelte';
	import EmailTemplate from './confirm.email_template.svelte';
	import Signup from './signup.svelte';
	import Forgot from './forgot.svelte';
	import PasswordShow from './password_show.svelte';

	let email_template;
	let show_password = false;

	let form = {
		email: $module.email
	};
	let error = {};

	let return_url = $page.url.pathname;
	if ($module.return_url) {
		return_url = $module.return_url;
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

		$loading = 'Loading . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/login`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify(form)
		});

		resp = await resp.json();
		console.log(resp);
		if (resp.status != 200) {
			$loading = false;
		}

		if (resp.status == 200) {
			$token = resp.token;
			document.location = return_url;
		} else if (resp.error == 'not confirmed') {
			$module = {
				module: Dialogue,
				title: 'Email has not been confirmed',
				status: 201,
				message: `A confirmation email has been sent to: <b>${form.email}</b>`,
				buttons: [
					{
						name: 'OK',
						fn: () => {
							$module = '';
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
	<strong class="ititle"> Login </strong>
	{#if error.error}
		<span class="error">
			{error.error}
		</span>
	{/if}
	<IG
		name="email"
		icon="email"
		error={error.email}
		placeholder="email here"
		type="text"
		bind:value={form.email}
	/>
	<IG
		name="password"
		icon="key"
		error={error.password}
		placeholder="password here"
		type={show_password ? 'text' : 'password'}
		bind:value={form.password}
	>
		<svelte:fragment slot="right">
			<PasswordShow bind:show_password />
		</svelte:fragment>
	</IG>

	<Button on:click={validate}>
		Submit
		<Icon icon="send" />
	</Button>

	<br />
	<div>
		<Link
			on:click={() => {
				$module = {
					module: Signup,
					email: form.email
				};
			}}
		>
			Signup
		</Link>
		<span class="divider"> | </span>
		<Link
			on:click={() => {
				$module = {
					module: Forgot,
					email: form.email
				};
			}}
		>
			Forgot Password
		</Link>
	</div>
</form>

<div bind:this={email_template} style="display: none;">
	<EmailTemplate />
</div>

<style>
	form {
		padding: var(--sp3);
	}
</style>
