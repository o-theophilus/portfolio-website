<script>
	import { page } from '$app/stores';
	import { user, loading, module } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import { template } from './footer.form.template.js';
	import Input from '$lib/input_group.svelte';
	import Button from '$lib/button/button.svelte';
	import Icon from '$lib/icon.svelte';
	import Info from '$lib/info.svelte';

	import EmailTemplate from '$lib/email_template.svelte';
	let email_template;

	let form = {};
	if ($user.status == 'verified') {
		form.name = $user.name;
		form.email = $user.email;
	}
	let error = {};

	const clear_error = () => {
		error = {};
	};

	$: clear_error($page);

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
		form.email_template = email_template.innerHTML.replace(/&amp;/g, '&');

		$loading = 'Sending Email . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/send_email`, {
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
			form = {};
			_form.reset();

			$module = {
				module: Info,
				title: 'Message Sent',
				message: `
					Thank you for contacting us,
					<br/>
					We will get back to you shortly
					`,
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
			// throw new Error(data.message);
		}
	};

	let msgStore = '';
	let _form;
</script>

<form on:submit|preventDefault novalidate autocomplete="off" bind:this={_form}>
	{#if error.error}
		<div class="err">
			{error.error}
		</div>
	{/if}

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
	<Button size="wide" on:click={validate}>
		Send
		<Icon icon="send" />
	</Button>
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
