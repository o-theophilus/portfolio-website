<script>
	import { module, notify, loading, app } from '$lib/store.svelte.js';
	import { page } from '$app/state';

	import { Button } from '$lib/button';
	import { IG } from '$lib/input';
	import { Form } from '$lib/layout';
	import Access from './form.svelte';

	let form = $state({ access: module.value.mods });
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
		icon="key-round"
		error={error.password}
		bind:value={form.password}
		type="password+"
		placeholder="Password here"
	></IG>

	<div class="line">
		<Button icon="arrow-left" onclick={() => module.open(Access, { mods: module.value.mods })}>
			Back
		</Button>
		<Button icon2="send-horizontal" onclick={validate}>Submit</Button>
	</div>
</Form>

<style>
	.line {
		display: flex;
		align-items: center;
		gap: var(--sp1);
	}
</style>
