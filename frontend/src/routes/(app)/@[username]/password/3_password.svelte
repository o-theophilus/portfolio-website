<script>
	import { module, loading, notify, app } from '$lib/store.svelte.js';

	import { IG } from '$lib/input';
	import { Button } from '$lib/button';
	import { Form } from '$lib/layout';

	let form = $state({ ...module.value });
	let error = $state({});
	let show_password = $state(false);

	const validate = async () => {
		error = {};

		if (!form.password) {
			error.password = 'This field is required';
		} else if (
			!/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[^\s]+$/.test(form.password) ||
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

	<Button primary onclick={validate}>Change Password</Button>
	<Button
		--button-background-color="darkred"
		--button-background-color-hover="red"
		icon="x"
		onclick={() => {
			module.close();
		}}
	>
		Cancel
	</Button>
</Form>
