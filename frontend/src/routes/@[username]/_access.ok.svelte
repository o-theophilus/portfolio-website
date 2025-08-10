<script>
	import { module, notify, loading, app } from '$lib/store.svelte.js';
	import { page } from '$app/state';

	import { Icon } from '$lib/macro';
	import { Button } from '$lib/button';
	import { IG } from '$lib/input';
	import { Form } from '$lib/layout';
	import Access from './_access.svelte';

	let form = {
		access: module.value.mods
	};
	let error = {};
	let show_password = false;

	const validate = async () => {
		error = {};

		if (!form.password) {
			error.password = 'cannot be empty';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		error = {};
		loading.open('saving . . .');
		let resp = await fetch(
			`${import.meta.env.VITE_BACKEND}/admin/user/access/${page.data.user.key}`,
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
			module.close();
			notify.open('Access saved');
		} else {
			error = resp;
		}
	};
</script>

<Form title="Accept Access" error={error.error}>
	<IG
		name="Password"
		icon="key"
		error={error.password}
		bind:value={form.password}
		type={show_password ? 'text' : 'password'}
		placeholder="Password here"
	></IG>

	<div class="line">
		<Button onclick={validate}>
			Submit
			<Icon icon="send" />
		</Button>
		<Button onclick={() => module.open(Access, { mods: module.value.mods })}>
			Back
			<!-- <Icon icon="send" /> -->
		</Button>
	</div>
</Form>

<style>
	.line {
		display: flex;
		align-items: center;
		gap: var(--sp1);
	}
</style>
