<script>
	import { module, loading, app } from '$lib/store.svelte.js';

	import { Button } from '$lib/button';
	import { Icon } from '$lib/macro';
	import EmailTemplate from './_password.template.svelte';

	import Code from './_password_2_code.svelte';

	let form = {};
	let error = {};
	let email_template;

	const submit = async () => {
		form.email_template = email_template.innerHTML.replace(/&amp;/g, '&');

		loading.open('Requesting Code . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/user/password/1`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			},
			body: JSON.stringify(form)
		});
		resp = await resp.json();
		loading.close();

		if (resp.status == 200) {
			module.open(Code, form);
		} else {
			error = resp;
		}
	};
</script>

<div class="form">
	<strong class="ititle"> Change Password </strong>

	{#if error.error}
		<div class="error">
			{error.error}
		</div>
	{/if}
	<br />
	<br />

	<Button primary onclick={submit}>
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
