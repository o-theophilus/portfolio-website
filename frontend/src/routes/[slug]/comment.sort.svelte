<script>
	import { portal, loading, user } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Button from '$lib/button/button.svelte';

	export let post_key;
	let error = {};

	let form = { ...$user.setting };
	let sort = {
		date: ['old', 'new'],
		vote: ['low', 'high']
	};

	let changed = false;
	const compare = () => {
		changed = false;
		if (
			form.sort_comment_by != $user.setting.sort_comment_by ||
			form.sort_comment_reverse != $user.setting.sort_comment_reverse
		) {
			changed = true;
		}
	};

	const submit = async () => {
		error = {};

		$loading = `Sorting comment . . .`;
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/setting`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify(form)
		});
		resp = await resp.json();

		if (resp.status == 200) {
			changed = false;
			$user = resp.user;
			submit_sort();
		} else {
			$loading = false;
			error = resp;
		}
	};

	const submit_sort = async () => {
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/comment/${post_key}`, {
			method: 'get',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			}
		});
		resp = await resp.json();
		$loading = false;

		if (resp.status == 200) {
			$portal = {
				for: 'comment',
				data: resp.comments
			};
		} else {
			error = resp;
		}
	};
</script>

<section>
	<div class="block">
		<div class="sort">
			sort by:

			<select
				bind:value={form.sort_comment_by}
				on:change={() => {
					compare();
				}}
			>
				{#each Object.entries(sort) as [name, op]}
					<option value={name}>{name}</option>
				{/each}
			</select>
			<select
				bind:value={form.sort_comment_reverse}
				on:change={() => {
					compare();
				}}
			>
				<option value={true}>{sort[form.sort_comment_by][1]}-{sort[form.sort_comment_by][0]}</option
				>
				<option value={false}
					>{sort[form.sort_comment_by][0]}-{sort[form.sort_comment_by][1]}</option
				>
			</select>
		</div>

		{#if changed}
			<Button class="tiny" on:click={submit}>Ok</Button>
		{/if}
	</div>

	{#if error.error}
		<span class="error">
			{error.error}
		</span>
	{/if}
</section>

<style>
	.block,
	.sort {
		display: flex;
		align-items: center;
	}
	.block {
		gap: var(--sp2);
	}

	select {
		background-color: transparent;
		border: none;
		color: var(--ft2);
		cursor: pointer;
	}
</style>
