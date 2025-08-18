<script>
	import { page } from '$app/state';
	import { loading, module, app } from '$lib/store.svelte.js';

	import { template } from './footer.form.template.js';
	import { Button } from '$lib/button';
	import { Icon } from '$lib/macro';
	import { EmailTemplate, Form } from '$lib/layout';
	import { Dialogue } from '$lib/info';
	import { IG } from '$lib/input';

	let email_template;
	let form = $state({});
	let error = $state({});

	$effect(() => {
		const x = page.url.pathname;
		error = {};
	});

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

		loading.open('Sending Email . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/contact`, {
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
			form = {};

			module.open(Dialogue, {
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
							module.close();
						}
					}
				]
			});
		} else {
			error = resp;
		}
	};
</script>

<Form error={error.error} --form-padding="0">
	<IG
		name="Full name"
		icon="user"
		bind:value={form.name}
		error={error.name}
		type="text"
		placeholder="Name Here"
	/>
	<IG
		name="Email Address"
		icon="mail"
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
		{#snippet label()}
			<button class="label">
				Message
				<Icon icon="chevron-down" />
				<select
					onchange={(e) => {
						form.message = e.target.value;
						e.target.value = 'Select Template';
					}}
				>
					{#each Object.entries(template) as [key, val]}
						<option value={val}>
							{key}
						</option>
					{/each}
				</select>
			</button>
		{/snippet}
	</IG>

	<Button icon2="send-horizontal" onclick={validate}>Send</Button>
</Form>

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
		position: relative;

		display: flex;
		align-items: center;
		gap: 8px;

		font-size: 0.8rem;
		background-color: unset;
		color: var(--ft2);
		border: none;
		padding: 0;
	}

	select {
		position: absolute;
		width: 74px;
		opacity: 0;
	}

	option {
		background-color: var(--bg1);
		color: var(--ft2);
		font-size: 1rem;
	}
</style>
