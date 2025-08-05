<script>
	import { loading, module, notify, app } from '$lib/store.svelte.js';

	import { IG } from '$lib/input';
	import { Button } from '$lib/button';
	import { Icon } from '$lib/macro';

	let report_key = module.value.report_key;
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

		loading.open(`Sending . . .`);
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/report/status/${report_key}`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			},
			body: JSON.stringify(form)
		});
		resp = await resp.json();
		loading.close();

		if (resp.status == 200) {
			module.close();
			notify.open('Resolved');
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
		onclick={() => {
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
