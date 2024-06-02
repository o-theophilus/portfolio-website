<script>
	import { page } from '$app/stores';

	import { module, loading } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Input from '$lib/input_group.svelte';
	import Button from '$lib/button/button.svelte';
	import Link from '$lib/button/link.svelte';
	import Icon from '$lib/icon.svelte';
	import Info from '$lib/info.svelte';
	import EmailTemplate from './confirm.email_template.svelte';
	import Signup from './signup.svelte';
	import Forgot from './forgot.svelte';

	let email_template;

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
				module: Info,
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
	<strong class="big"> Login </strong>
	{#if error.error}
		<span class="error">
			{error.error}
		</span>
	{/if}
	<Input name="email" error={error.email} let:id>
		<input placeholder="email here" type="text" {id} bind:value={form.email} />
	</Input>
	<Input name="password" error={error.password} let:id>
		<input placeholder="password here" type="password" {id} bind:value={form.password} />
	</Input>

	<Button on:click={validate}>
		Submit
		<Icon icon="send" />
	</Button>
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
