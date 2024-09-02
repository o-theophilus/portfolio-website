<script>
	import { module, loading, notify, user } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import IG from '$lib/input_group.svelte';
	import Button from '$lib/button/button.svelte';
	import Icon from '$lib/icon.svelte';

	let form = {
		actions: []
	};
	let error = {};

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

		$loading = `Taking action${form.actions.length > 1 ? 's' : ''} . . .`;
		let resp = await fetch(
			`${import.meta.env.VITE_BACKEND}/admin/user/actions/${$module.user.key}`,
			{
				method: 'put',
				headers: {
					'Content-Type': 'application/json',
					Authorization: $token
				},
				body: JSON.stringify(form)
			}
		);
		resp = await resp.json();
		$loading = false;

		if (resp.status == 200) {
			$module.update(resp.user);
			$module = null;
			$notify.add('Done');
		} else {
			error = resp;
		}
	};
</script>

<form on:submit|preventDefault novalidate autocomplete="off">
	<strong class="ititle"> Actions </strong>
	{#if error.error}
		<div class="error">
			{error.error}
		</div>
	{/if}

	<div class="actions">
		{#if $user.access.includes('user:reset_name')}
			<label>
				<input type="checkbox" bind:group={form.actions} value="reset_name" />
				Reset Name
			</label>
		{/if}
		{#if $user.access.includes('user:reset_photo')}
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

	<Button on:click={validate}>
		Submit
		<Icon icon="send" />
	</Button>
</form>

<style>
	form {
		padding: var(--sp3);
	}
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
