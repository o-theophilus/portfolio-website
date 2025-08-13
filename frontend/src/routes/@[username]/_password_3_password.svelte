<script>
	import { module, loading, notify, app } from '$lib/store.svelte.js';

	import { IG } from '$lib/input';
	import { Button } from '$lib/button';
	import { Form } from '$lib/Layout';
	import { Icon } from '$lib/macro';

	let form = {
		...module.value
	};

	let error = $state({});
	let show_password = false;

	const validate = async () => {
		error = {};

		if (!form.password) {
			error.password = 'cannot be empty';
		} else if (
			!/[a-z]/.test(form.password) ||
			!/[A-Z]/.test(form.password) ||
			!/[0-9]/.test(form.password) ||
			form.password.length < 8 ||
			form.password.length > 18
		) {
			error.password =
				'Password must include at least 1 lowercase letter, 1 uppercase letter, 1 number and must contain 8 - 18 characters';
		}

		if (!form.confirm_password) {
			error.confirm_password = 'cannot be empty';
		} else if (form.password && form.password != form.confirm_password) {
			error.confirm_password = 'Password and confirm password does not match';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		loading.open('loading . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/user/password/3`, {
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
			notify.open('Password changed');
			module.close();
		} else {
			error = resp;
		}
	};
</script>

<Form title="Change Password" error={error.error}>
	<IG
		name="Password"
		icon="key"
		error={error.password}
		bind:value={form.password}
		type="password++"
		placeholder="Password here"
	></IG>

	<IG
		name="Confirm Password"
		icon="key"
		error={error.confirm_password}
		bind:value={form.confirm_password}
		type="password"
		placeholder="Password here"
	/>

	<Button primary onclick={validate}>Change Password</Button>
	<Button
		--button-background-color="darkred"
		--button-background-color-hover="red"
		onclick={() => {
			module.close();
		}}
	>
		Cancel
		<Icon icon="close" />
	</Button>
</Form>
