<script>
	import { page } from '$app/state';

	import { app, loading, module } from '$lib/store.svelte.js';

	import { Button, Link } from '$lib/button';
	import { Checkbox, IG } from '$lib/input';
	import { Form } from '$lib/layout';
	import Confirm from './confirm.svelte';
	import EmailTemplate from './confirm.template.svelte';
	import Forgot from './forgot_1.email.svelte';
	import Signup from './signup.svelte';

	let email_template;

	let form = $state({
		email: module.value.email,
		remember: false
	});
	let error = $state({});

	let return_url = page.url.pathname;
	if (module.value.return_url) {
		return_url = module.value.return_url;
	}

	const validate = () => {
		error = {};

		if (!form.email) {
			error.email = 'This field is required';
		}
		if (!form.password) {
			error.password = 'This field is required';
		}
		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		form.email_template = email_template.innerHTML.replace(/&amp;/g, '&');

		loading.open('Loading . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/login`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			},
			body: JSON.stringify(form)
		});

		resp = await resp.json();
		if (resp.status != 200) {
			loading.close();
		}

		if (resp.status == 200) {
			app.token = resp.token;
			app.login = true;
			app.user = {};
			document.location = return_url;
		} else if (resp.error == 'not active') {
			module.open(Confirm, { email: form.email });
		} else {
			error = resp;
		}
	};
</script>

<Form title="Login" error={error.error}>
	<IG
		name="Email or Username"
		icon="mail"
		error={error.email}
		type="email"
		bind:value={form.email}
		placeholder="Email or Username here"
	/>

	<IG
		name="Password"
		icon="key-round"
		error={error.password}
		placeholder="Password here"
		type="password+"
		bind:value={form.password}
	></IG>

	<IG>
		{#snippet input()}
			<form onsubmit={(e) => e.preventDefault()} novalidate autocomplete="off">
				<Checkbox
					label="Remember me"
					value={form.remember}
					onclick={() => (form.remember = !form.remember)}
				></Checkbox>
			</form>
		{/snippet}
	</IG>

	<Button icon2="send-horizontal" onclick={validate}>Submit</Button>

	<br />
	<br />

	<div class="line">
		<Link onclick={() => module.open(Signup, { email: form.email })} --link-font-size="0.8rem">
			Signup
		</Link>
		<span class="divider"> | </span>
		<Link onclick={() => module.open(Forgot, { email: form.email })} --link-font-size="0.8rem">
			Forgot Password
		</Link>
	</div>
</Form>

<div bind:this={email_template} style="display: none;">
	<EmailTemplate />
</div>

<style>
	.line {
		gap: 16px;
	}
</style>
