<script>
	import { page } from '$app/state';
	import { loading, module, app } from '$lib/store.svelte.js';

	import { template } from './footer.form.template.js';
	import { Button } from '$lib/button';
	import { EmailTemplate, Form } from '$lib/layout';
	import { Dialogue } from '$lib/info';
	import { IG, Dropdown } from '$lib/input';

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
			error.name = 'This field is required';
		} else if (form.name.length > 100) {
			error.name = 'This field cannot exceed 100 characters';
		}

		if (!form.email) {
			error.email = 'This field is required';
		} else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) {
			error.email = 'Invalid email address';
		} else if (form.email.length > 255) {
			error.email = 'This field cannot exceed 255 characters';
		}

		if (!form.message) {
			error.message = 'This field is required';
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
			<Dropdown
				--select-height="10"
				--select-padding-x="0"
				--select-font-size="0.8rem"
				--select-color="var(--ft2)"
				--select-color-hover="var(--ft1)"
				--select-background-color="transparent"
				--select-background-color-hover="transparent"
				--select-outline-color="transparent"
				label="Message"
				list={Object.keys(template)}
				icon2="chevron-down"
				onchange={(e) => {
					form.message = template[e];
				}}
			/>
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
