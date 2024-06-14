<script>
	import { module, notification, loading, portal } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import IG from '$lib/input_group.svelte';
	import Button from '$lib/button/button.svelte';
	import Icon from '$lib/icon.svelte';

	let form = {
		phone: $module.user.phone
	};

	let error = {};

	const validate = () => {
		error = {};
		if (!form.phone) {
			error.phone = 'cannot be empty';
		} else if (form.phone == $module.user.phone) {
			error.phone = 'no change';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		$loading = 'Saving Post . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/user/${$module.user.key}`, {
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
			$portal = {
				for: 'user',
				data: resp.user
			};

			$notification = {
				status: 200,
				message: 'Phone Number Changed'
			};

			$module = null;
		} else {
			error = resp;
		}
	};
</script>

<form on:submit|preventDefault novalidate autocomplete="off">
	<strong class="ititle"> Edit Phone Number </strong>
	{#if error.error}
		<span class="error">
			{error.error}
		</span>
	{/if}

	<IG
		name="Phone Number"
		icon="phone"
		error={error.phone}
		placeholder="Phone Number here"
		type="tel"
		bind:value={form.phone}
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
</style>
