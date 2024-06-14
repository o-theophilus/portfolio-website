<script>
	import { module, notification, loading } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Icon from '$lib/icon.svelte';
	import Button from '$lib/button/button.svelte';
	import ShowPassword from '../auth/password_show.svelte';
	import IG from '$lib/input_group.svelte';

	let form = {
		permissions: $module.permissions
	};
	let error = {};
	let show_password = false;

	const validate = async () => {
		error = {};

		if (!form.password) {
			error.password = 'This field is required';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		error = {};
		$loading = 'saving . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/admin/permission/${$module.key}`, {
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
			$module = '';
			$notification = {
				status: 200,
				message: 'Permissions saved'
			};
		} else {
			error = resp;
		}
	};
</script>

<form on:submit|preventDefault novalidate autocomplete="off">
	<strong class="ititle"> Accept Permissions </strong>
	{#if error.error}
		<br />
		<span class="error">
			{error.error}
		</span>
	{/if}

	<IG
		name="password"
		icon="key"
		error={error.password}
		bind:value={form.password}
		type={show_password ? 'text' : 'password'}
		placeholder="Password here"
	>
		<svelte:fragment slot="right">
			<div class="right">
				<ShowPassword bind:show_password />
			</div>
		</svelte:fragment>
	</IG>

	<Button on:click={validate}>
		Submit
		<Icon icon="send" />
	</Button>
</form>

<style>
	form {
		padding: var(--sp3);
	}

	.right {
		padding-right: var(--sp2);
	}
</style>
