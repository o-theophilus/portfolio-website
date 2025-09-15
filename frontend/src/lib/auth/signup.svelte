<script>
	import { module, loading, app } from '$lib/store.svelte.js';

	import { IG } from '$lib/input';
	import { Button, Link } from '$lib/button';
	import { Form } from '$lib/layout';
	import Login from './login.svelte';
	import EmailTemplate from './confirm.template.svelte';
	import Confirm from './confirm.svelte';

	let form = $state({ email: module.value.email });
	let email_template;
	let show_password = $state(false);
	let error = $state({});

	const validate = () => {
		error = {};

		form.name = form.name.trim().replace(/\s+/g, ' ');
		if (!form.name) {
			error.name = 'This field is required';
		} else if (form.name.length > 100) {
			error.name = 'This field cannot exceed 100 characters';
		}

		form.email = form.email.trim();
		if (!form.email) {
			error.email = 'This field is required';
		} else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) {
			error.email = 'Invalid email address';
		} else if (form.email.length > 255) {
			error.email = 'This field cannot exceed 255 characters';
		}

		if (!form.password) {
			error.password = 'This field is required';
		} else if (
			!/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]+$/.test(form.password) ||
			form.password.length < 8 ||
			form.password.length > 18
		) {
			error.password =
				'Password must include at least 1 lowercase letter, 1 uppercase letter, 1 number and must contain 8 - 18 characters';
		}

		if (!form.confirm_password) {
			error.confirm_password = 'This field is required';
		} else if (form.password && form.password != form.confirm_password) {
			error.confirm_password = 'Password and confirm password does not match';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		form.email_template = email_template.innerHTML.replace(/&amp;/g, '&');

		loading.open('Loading . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/signup`, {
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
			module.open(Confirm, { email: form.email });
		} else {
			error = resp;
		}
	};
</script>

<Form title="Signup" error={error.error}>
	<IG
		name="Name"
		icon="user"
		error={error.name}
		placeholder="Name here"
		type="text"
		bind:value={form.name}
	/>
	<IG
		name="Email"
		icon="mail"
		error={error.email}
		placeholder="Email here"
		type="text"
		bind:value={form.email}
	/>
	<IG
		name="Password"
		icon="key-round"
		bind:value={form.password}
		error={error.password}
		placeholder="Password here"
		type="password++"
		bind:show_password
	></IG>
	<IG
		name="Confirm Password"
		icon="key-round"
		bind:value={form.confirm_password}
		error={error.confirm_password}
		placeholder="Password here"
		type="password"
		bind:show_password
	/>

	<Button icon2="send-horizontal" onclick={validate}>Submit</Button>

	<br />
	<br />

	<Link onclick={() => module.open(Login, { email: form.email })} --link-font-size="0.8rem"
		>Login</Link
	>
</Form>

<div bind:this={email_template} style="display: none;">
	<EmailTemplate />
</div>
