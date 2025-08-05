<script>
	import { module, loading, notify } from '$lib/store_old.js';
	import { token } from '$lib/cookie.js';

	import IG from '$lib/input_group.svelte';
	import Button from '$lib/button_old/button.svelte';
	import Icon from '$lib/icon.svelte';

	let user = { ...$module.user };
	let form = {};
	let error = {};

	const validate = () => {
		error = {};

		if (!form.note) {
			error.note = 'cannot be empty';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		error = {};

		$loading = `${user.status == 'blocked' ? 'Unblocking User' : 'Blocking User'} . . .`;
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/admin/user/block/${user.key}`, {
			method: 'put',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify(form)
		});
		resp = await resp.json();
		$loading = false;

		if (resp.status == 200) {
			$module.update(resp.user);
			$module = null;
			$notify.add(resp.user.status == 'blocked' ? 'User Blocked' : 'User Unblocked');
		} else {
			error = resp;
		}
	};
</script>

<form on:submit|preventDefault novalidate autocomplete="off">
	<strong class="ititle">
		{#if user.status == 'blocked'}
			Unblock
		{:else}
			Block
		{/if}
		User
	</strong>
	{#if error.error}
		<div class="error">
			{error.error}
		</div>
	{/if}

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
</style>
