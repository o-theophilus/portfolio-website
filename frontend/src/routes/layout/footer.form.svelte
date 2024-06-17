<script>
	import { page } from '$app/stores';
	import { user, loading, module } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import { template } from './footer.form.template.js';
	import Button from '$lib/button/button.svelte';
	import Icon from '$lib/icon.svelte';
	import Dialogue from '$lib/dialogue.svelte';
	import Drop from '$lib/dropdown.svelte';
	import IG from '$lib/input_group.svelte';

	import EmailTemplate from '$lib/email_template.svelte';
	let email_template;

	let form = {};
	let error = {};
	// if ($user.login) {
	// form.name = $user.name;
	// form.email = $user.email;
	// }

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
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/contact`, {
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

			$module = {
				module: Dialogue,
				title: 'Message Sent',
				message: `
					Thank you for contacting me,
					<br/>
					I will get back to you shortly
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
		}
	};
</script>

<form on:submit|preventDefault novalidate autocomplete="off">
	{#if error.error}
		<div class="err">
			{error.error}
		</div>
	{/if}

	<IG
		name="Full name"
		icon="person"
		bind:value={form.name}
		error={error.name}
		type="text"
		placeholder="Your name"
	/>
	<IG
		name="Email Address"
		icon="email"
		bind:value={form.email}
		error={error.email}
		type="text"
		placeholder="Your email address"
	/>
	<IG
		name="Message"
		bind:value={form.message}
		error={error.message}
		type="textarea"
		placeholder="Your message"
	>
		<svelte:fragment slot="label">
			<Drop
				wide
				list={Object.keys(template)}
				on:change={(e) => {
					form.message = template[e.target.value];
					e.target.value = 'Select Template';
				}}
			/>

			<div class="gap" />
		</svelte:fragment>
	</IG>

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
	.gap {
		height: var(--sp1);
	}
</style>
