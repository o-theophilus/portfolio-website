<script>
	import { api_url, _user, loading, module } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import { template } from './form_template.js';
	import Input from '$lib/comp/input_group.svelte';
	import Button from '$lib/comp/button.svelte';
	import Info from '$lib/module/info.svelte';

	import EmailTemplate from '$lib/email_template/email_template.svelte';
	let email_template;

	let form = {};
	if ($_user.status == 'verified') {
		form.name = $_user.name;
		form.email = $_user.email;
	}
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

		if (!form.message) {
			error.message = 'cannot be empty';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		form.email_template = email_template.innerHTML;

		$loading = 'Sending Email . . .';
		const resp = await fetch(`${api_url}/send_email`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify(form)
		});
		$loading = false;

		if (resp.ok) {
			const data = await resp.json();

			if (data.status == 401) {
				error.form = data.message;
			} else if (data.status == 201) {
				error = data.message;
			} else if (data.status == 200) {
				form = {};
				_form.reset();

				$module = {
					module: Info,
					title: 'Message Sent',
					status: 'good',
					message: `
					Thank you for contacting us,
					<br/>
					We will get back to you shortly
					`,
					button: [
						{
							name: 'OK',
							fn: () => {
								$module = '';
							}
						}
					]
				};
			} else {
				throw new Error('invalid request');
			}
		}
	};

	let msgStore = '';
	let _form;
</script>

<form on:submit|preventDefault={validate} novalidate autocomplete="off" bind:this={_form}>
	<Input name="full name" error={error.name} let:id svg="username">
		<input placeholder="Your Name" type="text" {id} bind:value={form.name} />
	</Input>

	<Input name="email address" error={error.email} let:id svg="emailAddress">
		<input placeholder="Your Email Address" type="text" {id} bind:value={form.email} />
	</Input>
	<Input name="message" error={error.message} let:id>
		<svelte:fragment slot="label">
			<select bind:value={form.message}>
				<option value={msgStore}>Message</option>
				{#each template as temp}
					<option value={temp.text}>{temp.name}</option>
				{/each}
			</select>
		</svelte:fragment>

		<textarea
			placeholder="Your Message"
			{id}
			bind:value={form.message}
			on:input={() => (msgStore = form.message)}
		/>
	</Input>
	{#if error.form}
		<div class="err">
			{error.form}
		</div>
	{/if}
	<Button class="wide">Send</Button>
</form>

<div bind:this={email_template} style="display: none;">
	<EmailTemplate>
		Name: {'{'}name{'}'}
		<br />
		Email: {'{'}email{'}'}
		<br /><br />
		{'{'}message{'}'}
	</EmailTemplate>
</div>

<style>
</style>
