<script>
	import { module, loading, notify, app } from '$lib/store.svelte.js';

	import { IG } from '$lib/input';
	import { Button } from '$lib/button';
	import { Icon } from '$lib/macro';
	import { Form } from '$lib/layout';

	let form = {
		actions: []
	};
	let error = $state({});

	const validate = () => {
		error = {};

		if (!form.note) {
			error.note = 'cannot be empty';
		}

		if (form.actions.length == 0) {
			error.actions = 'select action';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		error = {};

		loading.open(`Taking action${form.actions.length > 1 ? 's' : ''} . . .`);
		let resp = await fetch(
			`${import.meta.env.VITE_BACKEND}/admin/user/actions/${module.value.user.key}`,
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
			module.value.update(resp.user);
			module.close();
			notify.open('Done');
		} else {
			error = resp;
		}
	};
</script>

<Form title="Actions" error={error.error}>
	<div class="actions">
		{#if app.user.access.includes('user:reset_name')}
			<label>
				<input type="checkbox" bind:group={form.actions} value="reset_name" />
				Reset Name
			</label>
		{/if}
		{#if app.user.access.includes('user:reset_photo')}
			<label>
				<input type="checkbox" bind:group={form.actions} value="reset_photo" />
				Reset Photo
			</label>
		{/if}
		{#if error.actions}
			<span class="error">
				{error.actions}
			</span>
		{/if}
	</div>

	<IG
		name="Note"
		error={error.note}
		type="textarea"
		placeholder="Note here"
		bind:value={form.note}
	/>

	<Button onclick={validate}>
		Submit
		<Icon icon="send" />
	</Button>
</Form>

<style>
	.error {
		margin: var(--sp2) 0;
		font-size: 0.8rem;
	}

	.actions {
		margin: var(--sp2) 0;
	}

	label {
		display: flex;
		gap: var(--sp2);
	}
</style>
