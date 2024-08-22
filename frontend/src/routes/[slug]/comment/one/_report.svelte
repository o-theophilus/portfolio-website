<script>
	import { loading, module, notification } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import { template, tags } from './_report__template.js';
	import IG from '$lib/input_group.svelte';
	import Button from '$lib/button/button.svelte';
	import Tags from '$lib/tags.svelte';
	import Icon from '$lib/icon.svelte';
	import Link from '$lib/button/link.svelte';
	import Avatar from '$lib/avatar.svelte';
	import Drop from '$lib/dropdown.svelte';

	let reported = $module.reported;
	let entity = $module.entity;

	let form = {
		reported_key: reported.key,
		_entity_key: entity.key,
		_entity_type: entity.type,

		tags: [],
		report: ''
	};
	let error = {};

	const validate = () => {
		error = {};

		if (!form.report) {
			error.report = 'cannot be empty';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		$loading = 'Sending Report . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/report`, {
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
			$notification = {
				message: 'Report Submitted'
			};
		} else {
			error = resp;
		}
	};
</script>

<form on:submit|preventDefault novalidate autocomplete="off">
	<strong class="ititle"> Report </strong>

	<div class="highlight">
		<Avatar name={reported.name} photo={reported.photo} />
		<Link href="/profile?search={reported.key}" blank>
			{reported.name}
		</Link>
		<div />
		{entity.extra}
	</div>

	<hr />

	{#if error.error}
		<div class="error">
			{error.error}
		</div>
	{/if}

	<IG
		bind:value={form.report}
		error={error.report}
		type="textarea"
		placeholder="Reason for reporting"
	>
		<svelte:fragment slot="label">
			<Drop
				wide
				list={Object.keys(template)}
				on:change={(e) => {
					form.report = template[e.target.value];
					e.target.value = 'Select Template';
				}}
			/>

			<div class="gap" />
		</svelte:fragment>
	</IG>

	Select applicable tags

	<Tags
		style="1"
		{tags}
		active={form.tags}
		on:click={(e) => {
			if (form.tags.includes(e.detail)) {
				form.tags = form.tags.filter((i) => i != e.detail);
			} else {
				form.tags.push(e.detail);
			}
			form = form;
		}}
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

	.highlight {
		display: grid;
		grid-template-columns: 1fr 100%;
		gap: 0 var(--sp1);
		align-items: center;

		background-color: var(--bg2);
		padding: var(--sp2);
		border-radius: var(--sp0);
		margin: var(--sp2) 0;
	}

	.gap {
		height: var(--sp1);
	}

	.error {
		margin: var(--sp2) 0;
	}
</style>
