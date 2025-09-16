<script>
	import { module, loading, app } from '$lib/store.svelte.js';

	import { IG } from '$lib/input';
	import { Button } from '$lib/button';
	import { Form } from '$lib/layout';

	import { Dialogue } from '$lib/info';
	import Login from './login.svelte';

	let form = $state({ ...module.value });
	let error = $state({});
	let show_password = false;

	const validate_submit = async () => {
		error = {};

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
		loading.open('loading . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/forgot/3`, {
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
			module.open(Dialogue, {
				message: 'Password Successfully changed',
				buttons: [
					{
						name: 'Login',
						icon: 'login',
						fn: () => {
							module.open(Login, { email: form.email });
						}
					}
				]
			});
		} else {
			error = resp;
		}
	};
</script>

<Form title="Forgot Password" error={error.error}>
	<IG
		name="New Password"
		icon="key-round"
		error={error.password}
		bind:value={form.password}
		type="password++"
		placeholder="Password here"
	></IG>

	<IG
		name="Confirm New Password"
		icon="key-round"
		error={error.confirm_password}
		bind:value={form.confirm_password}
		type="password"
		placeholder="Password here"
	/>

	<Button icon2="send-horizontal" onclick={validate_submit}>Submit</Button>
</Form>
