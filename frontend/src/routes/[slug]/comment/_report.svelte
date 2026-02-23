<script>
	import { app, loading, module, notify, page_state } from '$lib/store.svelte.js';

	import { Button, Tag } from '$lib/button';
	import { Dropdown, IG } from '$lib/input';
	import { Form } from '$lib/layout';
	import { tags, template } from './_report.template.js';
	import One from './one.svelte';

	let comment = { ...module.value.comment };

	let form = $state({
		entity_key: comment.key,
		entity_type: 'comment',
		comment: '',
		tags: []
	});
	let error = $state({});

	const validate = () => {
		error = {};

		if (!form.comment) {
			error.comment = 'This field is required';
		} else if (form.comment.length > 500) {
			error.comment = 'This field cannot exceed 500 characters';
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
			notify.open('Report Submitted');
			page_state.clear('report');
			module.close();
		} else {
			error = resp;
		}
	};
</script>

<Form title="Report" error={error.error}>
	<div class="comment">
		<One {comment}></One>
	</div>

	<IG
		bind:value={form.comment}
		error={error.comment}
		type="textarea"
		placeholder="Reason for reporting"
	>
		{#snippet label()}
			<Dropdown
				--select-height="10"
				--select-padding-x="0"
				--select-font-size="0.8rem"
				--select-background-color="transparent"
				--select-background-color-hover="transparent"
				--select-color="var(--ft2)"
				--select-color-hover="var(--ft1)"
				--select-outline-color="transparent"
				list={Object.keys(template)}
				label="Message"
				icon2="chevron-down"
				onchange={(e) => {
					form.comment = template[e];
				}}
			/>

			<span class="label">
				({500 - form.comment.length})
			</span>
		{/snippet}
	</IG>

	<div class="label">Select applicable tags</div>
	<div class="line">
		{#each tags as x}
			<Tag
				--tag-background-color={form.tags.includes(x) ? 'var(--cl1)' : 'unset'}
				--tag-color={form.tags.includes(x) ? 'white' : 'unset'}
				onclick={() => {
					if (form.tags.includes(x)) {
						form.tags = form.tags.filter((i) => i != x);
					} else {
						form.tags.push(x);
					}
				}}
			>
				{x}
			</Tag>
		{/each}
	</div>

	<Button icon2="send-horizontal" onclick={validate}>Submit</Button>
</Form>

<style>
	.comment {
		padding: 16px;

		background-color: var(--bg2);
		border-radius: 8px;
		outline: 1px solid var(--ol);
		outline-offset: -1px;
	}

	.label {
		font-size: 0.8rem;
	}
	.line {
		margin-top: 8px;
		margin-bottom: 16px;
		gap: 4px;
	}
</style>
