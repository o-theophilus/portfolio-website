<script>
	import { loading, module, notify, app } from '$lib/store.svelte.js';

	import { Button, Link } from '$lib/button';
	import { Form } from '$lib/layout';
	import { IG, Dropdown } from '$lib/input';
	import { Icon, Avatar } from '$lib/macro';
	import { template, tags } from './one.report.template.js';

	let reported = module.value.reported;
	let entity = module.value.entity;

	let form = $state({
		reported_key: reported.key,
		_entity_key: entity.key,
		_entity_type: entity.type,

		tags: [],
		report: ''
	});
	let error = $state({});

	const validate = () => {
		error = {};

		if (!form.report) {
			error.report = 'cannot be empty';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		loading.open('Sending Report . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/report`, {
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
			notify.open('Report Submitted');
		} else {
			error = resp;
		}
	};
</script>

<Form title="Report" error={error.error}>
	<div class="highlight">
		<Avatar name={reported.name} photo={reported.photo} />
		<Link href="/profile?search={reported.key}" blank>
			{reported.name}
		</Link>
		<div></div>
		{entity.extra}
	</div>

	<hr />

	<IG
		bind:value={form.report}
		error={error.report}
		type="textarea"
		placeholder="Reason for reporting"
	>
		<svelte:fragment slot="label">
			<Dropdown
				wide
				list={Object.keys(template)}
				on:change={(e) => {
					form.report = template[e.target.value];
					e.target.value = 'Select Template';
				}}
			/>

			<div class="gap"></div>
		</svelte:fragment>
	</IG>

	Select applicable tags

	<!-- <Tags
		style="1"
		{tags}
		active={form.tags}
		onclick={(e) => {
			if (form.tags.includes(e.detail)) {
				form.tags = form.tags.filter((i) => i != e.detail);
			} else {
				form.tags.push(e.detail);
			}
			form = form;
		}}
	/> -->

	<!-- <div class="line wrap">
		{#each post.tags as x}
			<Tag
				onclick={() => {
					page_state.set({ tag: [x] });
				}}>{x}</Tag
			>
		{/each}
	</div> -->

	<Button onclick={validate}>
		Submit
		<Icon icon="send" />
	</Button>
</Form>

<style>
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
</style>
