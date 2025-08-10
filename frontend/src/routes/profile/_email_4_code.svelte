<script>
	import { module, notify, loading, app } from '$lib/store.svelte.js';

	import { Button } from '$lib/button';
	import { IG } from '$lib/input';
	import { Icon } from '$lib/macro';
	import { Form } from '$lib/layout';

	let form = {
		...module.value.form
	};
	let error = {};

	const validate = () => {
		error = {};

		if (!form.code_2) {
			error.code_2 = 'cannot be empty';
		} else if (form.code_2.length != 6) {
			error.code_2 = 'invalid code';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		loading.open('loading . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/user/email/4`, {
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
			module.value.update(resp.user);
			notify.open('Email changed');
			module.close();
		} else {
			error = resp;
		}
	};
</script>

<Form title="Change Email" error={error.error}>
	<div class="message">Code has been sent to: {form.email}.</div>

	<IG name="Code" error={error.code_2} bind:value={form.code_2} type="code"></IG>

	<Button primary onclick={validate}>
		Submit
		<Icon icon="send" />
	</Button>
</Form>

<style>
	.message {
		margin: var(--sp2) 0;
	}

	.message {
		background-color: color-mix(in srgb, var(--cl1), transparent 80%);
		color: white;
		padding: var(--sp1);
		width: 100%;
	}
</style>
