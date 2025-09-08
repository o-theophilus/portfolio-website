<script>
	import { module, loading, notify, app } from '$lib/store.svelte.js';

	import { IG } from '$lib/input';
	import { Button } from '$lib/button';
	import { Form } from '$lib/layout';
	import { slide } from 'svelte/transition';

	let form = $state({ actions: [] });
	let error = $state({});

	const validate = () => {
		error = {};

		if (!form.note) {
			error.note = 'This field is required';
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
			`${import.meta.env.VITE_BACKEND}/admin/user/actions/${module.value.key}`,
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
		{#if app.user.access.includes('user:reset_username')}
			<label>
				<input type="checkbox" bind:group={form.actions} value="reset_username" />
				Reset Username
			</label>
		{/if}
		{#if app.user.access.includes('user:reset_photo')}
			<label>
				<input type="checkbox" bind:group={form.actions} value="reset_photo" />
				Reset Photo
			</label>
		{/if}
		{#if error.actions}
			<span class="error" transition:slide>
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

	<Button icon2="send-Horizontal" onclick={validate}>Submit</Button>
</Form>

<style>
	.error {
		margin: var(--sp2) 0;
		font-size: 0.8rem;
		color: red;
	}

	.actions {
		margin: var(--sp2) 0;
	}

	label {
		display: flex;
		gap: var(--sp2);
	}
</style>
