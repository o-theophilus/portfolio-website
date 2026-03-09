<script>
	import { Button } from '$lib/button';
	import { IG } from '$lib/input';
	import { Form } from '$lib/layout';
	import { app, loading, module, notify } from '$lib/store.svelte.js';
	import Access from './form.svelte';

	let form = $state({ access: module.value.access });
	let error = $state({});

	const validate = async () => {
		error = {};

		if (!form.password) {
			error.password = 'This field is required';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		error = {};

		loading.open('saving . . .');
		let resp = await fetch(
			`${import.meta.env.VITE_BACKEND}/users/${module.value.user.key}/access`,
			{
				method: 'put',
				headers: {
					'Content-Type': 'application/json',
					Authorization: app.token
				},
				body: JSON.stringify(form)
			}
		);
		resp = await resp.json();
		loading.close();

		if (resp.status == 200) {
			notify.open('Access saved');
			module.value.update(resp.user);
			module.close();
		} else {
			error = resp;
		}
	};
</script>

<Form title="Accept Access" error={error.error}>
	<IG
		name="Password"
		icon="key-round"
		error={error.password}
		bind:value={form.password}
		type="password+"
		placeholder="Password here"
	></IG>

	<div class="line">
		<Button
			icon="arrow-left"
			onclick={() =>
				module.open(Access, {
					user: module.value.user,
					update: module.value.update,
					access: module.value.access
				})}
		>
			Back
		</Button>
		<Button icon2="send-horizontal" onclick={validate}>Submit</Button>
	</div>
</Form>

<style>
	.line {
		display: flex;
		align-items: center;
		gap: 8px;
	}
</style>
