<script>
	import { module, loading } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Button from '$lib/button/button.svelte';
	import Icon from '$lib/icon.svelte';
	import EmailTemplate from './_email.template.svelte';

	import Code from './_email_2_code.svelte';

	let form = {};
	let error = {};
	let email_template;

	const submit = async () => {
		form.email_template = email_template.innerHTML.replace(/&amp;/g, '&');

		$loading = 'Requesting Code . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/user/email/1`, {
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
				module: Code,
				form,
				update: $module.update
			};
		} else {
			error = resp;
		}
	};
</script>

<div class="form">
	<strong class="ititle"> Change Email </strong>

	{#if error.error}
		<div class="error">
			{error.error}
		</div>
	{/if}
	<br />
	<br />

	<Button primary on:click={submit}>
		Request Code
		<Icon icon="send" />
	</Button>
</div>

<div bind:this={email_template} style="display: none;">
	<EmailTemplate />
</div>

<style>
	.form {
		padding: var(--sp3);
	}

	.error {
		margin: var(--sp2) 0;
	}
</style>
