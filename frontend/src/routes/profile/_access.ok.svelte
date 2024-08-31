<script>
	import { module, notify, loading } from '$lib/store.js';
	import { token } from '$lib/cookie.js';
	import { page } from '$app/stores';

	import Icon from '$lib/icon.svelte';
	import Button from '$lib/button/button.svelte';
	import ShowPassword from '../account/password_show.svelte';
	import IG from '$lib/input_group.svelte';
	import Access from './_access.svelte';

	let form = {
		access: $module.mods
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
		$loading = 'saving . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/admin/access/${$page.data.user.key}`, {
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
			$module = null;
			$notify.add('Access saved');
		} else {
			error = resp;
		}
	};
</script>

<form on:submit|preventDefault novalidate autocomplete="off">
	<strong class="ititle"> Accept Access </strong>
	{#if error.error}
		<div class="error">
			{error.error}
		</div>
	{/if}

	<IG
		name="Password"
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

	<div class="line">
		<Button on:click={validate}>
			Submit
			<Icon icon="send" />
		</Button>
		<Button
			on:click={() => {
				$module = {
					module: Access,
					mods: $module.mods
				};
			}}
		>
			Back
			<!-- <Icon icon="send" /> -->
		</Button>
	</div>
</form>

<style>
	form {
		padding: var(--sp3);
	}

	.error {
		margin: var(--sp2) 0;
	}

	.right {
		padding-right: var(--sp2);
	}

	.line {
		display: flex;
		align-items: center;
		gap: var(--sp1);
	}
</style>
