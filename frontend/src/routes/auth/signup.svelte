<script>
	import { module, loading } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Input from '$lib/input_group.svelte';
	import Button from '$lib/button/button.svelte';
	import Link from '$lib/button/link.svelte';
	import Icon from '$lib/icon.svelte';
	import Password from './password_checker.svelte';
	import Info from '$lib/info.svelte';
	import Login from './login.svelte';
	import EmailTemplate from './confirm.email_template.svelte';

	let email_template;

	let form = {
		email: $module.email
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
		} else if (!form.confirm_password) {
			error.confirm_password = 'cannot be empty';
		} else if (form.password != form.confirm_password) {
			error.confirm_password = 'does not match password';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		form.email_template = email_template.innerHTML.replace(/&amp;/g, '&');

		$loading = 'Loading . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/signup`, {
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
				module: Info,
				message: `A confirmation email has been sent to <b>${form.email}</b>`,
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
	<strong class="big"> Signup </strong>
	{#if error.error}
		<span class="error">
			{error.error}
		</span>
	{/if}
	<Input name="name" error={error.name} let:id>
		<input placeholder="name here" type="text" {id} bind:value={form.name} />
	</Input>
	<Input name="email" error={error.email} let:id>
		<input placeholder="email here" type="text" {id} bind:value={form.email} />
	</Input>
	<Input name="password" error={error.password} let:id>
		<input placeholder="password here" type="password" {id} bind:value={form.password} />
		<Password password={form.password} />
	</Input>
	<Input name="confirm password" error={error.confirm_password} let:id>
		<input
			placeholder="confirm password here"
			type="password"
			{id}
			bind:value={form.confirm_password}
		/>
	</Input>

	<Button on:click={validate}>
		Submit
		<Icon icon="send" />
	</Button>
	<Link
		on:click={() => {
			$module = {
				module: Login,
				email: form.email
			};
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
</style>
