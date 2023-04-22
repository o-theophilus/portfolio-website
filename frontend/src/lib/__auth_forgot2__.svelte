<script>
	import { api_url, _user, module } from '$lib/store.js';
	import { token as _token } from '$lib/cookie.js';

	import Input from '$lib/input_group.svelte';
	import Button from '$lib/button.svelte';
	import Password from '$lib/password_checker.svelte';
	import Login from './__auth_login__.svelte';
	import Info from './__info__.svelte';

	import EmailTemplate from './email_template.confirm.svelte';
	let email_template;

	export let token = '';
	let form = {};
	let error = {};

	const validate = () => {
		error = {};
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
		form.email_template = email_template.innerHTML;
		form.token = token;

		const resp = await fetch(`${api_url}/password_forgot2`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $_token
			},
			body: JSON.stringify(form)
		});

		if (resp.ok) {
			const data = await resp.json();

			if (data.status == 200) {
				$module = {
					module: Info,
					title: 'Done',
					status: 'good',
					message: `Password Changed`,
					button: [
						{
							name: 'OK',
							fn: () => {
								$module = '';
							}
						}
					]
				};
			} else if (data.status == 201) {
				error = data.message;
			} else {
				error.form = data.message;
			}
		}
	};
</script>

<form on:submit|preventDefault novalidate autocomplete="off">
	<strong class="big"> Change Password </strong>
	{#if error.form}
		<span class="error">
			{error.form}
		</span>
	{/if}

	<Input name="password" error={error.password} let:id>
		<input placeholder="password here" type="password" {id} bind:value={form.password} />
		<Password password={form.password} />
	</Input>
	<Input name="confirm pasword" error={error.confirm_password} let:id>
		<input
			placeholder="confirm pasword here"
			type="password"
			{id}
			bind:value={form.confirm_password}
		/>
	</Input>

	<Button
		on:click={() => {
			validate();
		}}
	>
		Submit
	</Button>
	<Button
		class="secondary"
		on:click={() => {
			$module = {
				module: Login
			};
		}}
	>
		Login
	</Button>
</form>

<div bind:this={email_template} style="display: none;">
	<EmailTemplate />
</div>

<style>
	form {
		padding: var(--gap3);
	}
</style>
