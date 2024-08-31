<script>
	import { loading, module, notify } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import IG from '$lib/input_group.svelte';
	import Button from '$lib/button/button.svelte';
	import Icon from '$lib/icon.svelte';

	let report_key = $module.report_key;
	let form = {};
	let error = {};

	const validate = (status) => {
		error = {};

		if (!form.note) {
			error.note = 'cannot be empty';
		}

		Object.keys(error).length === 0 && submit(status);
	};

	const submit = async (status) => {
		form.status = status;

		$loading = `Sending . . .`;
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/report/status/${report_key}`, {
			method: 'post',
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
			$notify.add('Resolved');
		} else {
			error = resp;
		}
	};
</script>

<form on:submit|preventDefault novalidate autocomplete="off">
	<strong class="ititle">
		Resolve:
		<span class="caps">
			{report_key.slice(-10)}
		</span>
	</strong>

	{#if error.error}
		<div class="error">
			{error.error}
		</div>
	{/if}

	<IG name="Note" error={error.note} type="textarea" placeholder="Note" bind:value={form.note} />

	<Button
		on:click={() => {
			validate('resolved');
		}}
	>
		Resolve
		<Icon icon="send" />
	</Button>
</form>

<style>
	form {
		padding: var(--sp3);
	}

	.error {
		margin: var(--sp2) 0;
	}

	.caps {
		text-transform: uppercase;
	}
</style>
