<script>
	import { page } from '$app/stores';
	import {  loading, module } from '$lib/store.js';
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
						icon: 'check',
						fn: () => {
							$module = null;
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
		<div class="error">
			{error.error}
		</div>
	{/if}

	<IG
		name="Full name"
		icon="person"
		bind:value={form.name}
		error={error.name}
		type="text"
		placeholder="Name Here"
	/>
	<IG
		name="Email Address"
		icon="email"
		bind:value={form.email}
		error={error.email}
		type="text"
		placeholder="Email here"
	/>
	<IG
		name="Message"
		bind:value={form.message}
		error={error.message}
		type="textarea"
		placeholder="Message here"
	>
		<svelte:fragment slot="label">
			<Drop
				wide
				list={Object.keys(template)}
				on:change={(e) => {
					form.message = template[e.target.value];
					e.target.value = 'Select Template';
				}}
			>
				<div class="label">
					Message
					<Icon icon="keyboard_arrow_down" />
				</div>
			</Drop>
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
	.label {
		display: flex;
		align-items: center;
		gap: var(--sp1);

		font-size: 0.8rem;
		/* line-height: 200%; */
		margin-bottom: 4px;
	}

	.error {
		margin: var(--sp2) 0;
	}
</style>
