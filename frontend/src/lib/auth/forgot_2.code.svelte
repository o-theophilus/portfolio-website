<script>
	import { module, loading, app } from '$lib/store.svelte.js';

	import { IG } from '$lib/input';
	import { Icon } from '$lib/macro';
	import { Button } from '$lib/button';

	import Password from './forgot_3.password.svelte';

	let form = {
		...module.value.form
	};
	let error = {};

	const validate_submit = async () => {
		error = {};

		if (!form.code) {
			error.code = 'cannot be empty';
		} else if (form.code.length != 6) {
			error.code = 'invalid code';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		loading.open('loading . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/forgot/2`, {
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
			module.open(Password, form);
		} else {
			error = resp;
		}
	};
</script>

<form on:submit|preventDefault novalidate autocomplete="off">
	<strong class="ititle"> Forgot Password </strong>

	{#if error.error}
		<div class="error">
			{error.error}
		</div>
	{/if}

	<IG name="Code" error={error.code} bind:value={form.code} type="code"></IG>

	<Button primary onclick={validate_submit}
		>Submit
		<Icon icon="send" />
	</Button>
</form>

<style>
	form {
		padding: var(--sp3);
	}

	.error {
		margin: var(--sp2) 0;
	}
</style>
